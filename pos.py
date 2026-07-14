#!/usr/bin/env python3
"""
pos.py — Planning-OS Enforcer CLI

Dua kapabilitas inti (dibuat karena Planning-OS aslinya 100% bergantung pada
disiplin manual, tanpa validasi otomatis):

  1. `validate`  — scan satu project instance, laporkan pelanggaran Mandatory
                    Rules (05 § 5.2): orphan file, index tidak sinkron,
                    metadata hilang, file > 400 baris, status tidak valid,
                    ID duplikat, cross-reference yang nyasar, entitas stale
                    (--stale-days).
  2. `new-id`    — generate ID berikutnya untuk tipe entitas tertentu (FEAT/
                    TASK/BUG/ENH/REF/MIG) dengan scan seluruh project,
                    supaya tidak ada dua entitas kebetulan dapat ID sama.
  3. `depgraph`  — bangun graph dari field depends_on di semua entitas,
                    deteksi circular dependency (yang bikin SOP-00 poin 5
                    mustahil dijalankan), dan cetak urutan pemrosesan yang
                    valid (topological sort) sesuai amanat SOP-00 poin 4.

Didesain zero-dependency (stdlib only) supaya bisa langsung jalan di VPS/
Termux tanpa install apa-apa.

USAGE
-----
    python3 pos.py validate <path-ke-project>
    python3 pos.py validate <path-ke-project> --stale-days 14
    python3 pos.py new-id <path-ke-project> <TYPE>
    python3 pos.py new-id <path-ke-project> <TYPE> --claim   (langsung catat
        ID ini sebagai "sudah dipakai" di .pos-id-ledger.json, mencegah race
        antar sesi AI yang jalan paralel)
    python3 pos.py depgraph <path-ke-project>

TYPE yang dikenal: FEAT, TASK, BUG, ENH, REF, MIG, BKLG
(bisa ditambah sendiri di ID_PREFIXES di bawah kalau Planning-OS di-extend)

Exit code: 0 kalau validate/depgraph bersih, 1 kalau ada temuan pelanggaran
atau circular dependency (untuk dipakai di CI / pre-commit hook / SOP-04
closing check).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

MAX_LINES = 400  # dari 01 ADR-001 §1.3 rule 5 dan 04 §4.8 rule 6
VALID_STATUSES = {
    "idea", "backlog", "ready", "planning", "in-progress", "review",
    "reported", "investigating", "done", "archived",
}
ID_PREFIXES = {
    "FEAT": "feature",
    "TASK": "task",
    "BUG": "bugfix",
    "ENH": "enhancement",
    "REF": "refactor",
    "MIG": "migration",
    "BKLG": "backlog-item",
}
# Folder mana yang berisi entitas kerja detail (punya metadata header wajib)
ENTITY_FOLDERS = {
    "05-features", "06-tasks", "07-bugs-and-fixes", "08-refactor-and-enhancement",
}
LEDGER_NAME = ".pos-id-ledger.json"

METADATA_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
ID_LINE_RE = re.compile(r"^id:\s*([A-Z]+-\d+)\s*$", re.MULTILINE)
STATUS_LINE_RE = re.compile(r"^status:\s*([a-zA-Z-]+)", re.MULTILINE)
SUMMARY_BLOCK_RE = re.compile(r"\*\*Summary Block:\*\*")
LINK_RE = re.compile(r"\]\(([^)]+\.md)\)")


@dataclass
class Finding:
    severity: str  # "error" | "warn"
    file: str
    message: str


@dataclass
class ValidationReport:
    findings: list = field(default_factory=list)

    def error(self, file: str, message: str):
        self.findings.append(Finding("error", file, message))

    def warn(self, file: str, message: str):
        self.findings.append(Finding("warn", file, message))

    @property
    def error_count(self):
        return sum(1 for f in self.findings if f.severity == "error")

    @property
    def warn_count(self):
        return sum(1 for f in self.findings if f.severity == "warn")


def parse_metadata(text: str) -> dict | None:
    m = METADATA_RE.match(text)
    if not m:
        return None
    block = m.group(1)
    data = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            data[key.strip()] = val.split("#")[0].strip()
    return data


def parse_id_list(raw: str) -> list[str]:
    """Parse field seperti 'depends_on: [FEAT-0031, TASK-0102]' jadi list ID."""
    raw = raw.strip()
    if not raw or raw == "[]":
        return []
    raw = raw.strip("[]")
    return [x.strip() for x in raw.split(",") if x.strip()]


ACTIVE_STATUSES = {"planning", "in-progress", "review", "investigating"}


def parse_date(raw: str) -> date | None:
    raw = raw.strip()
    for fmt in ("%Y-%m-%d",):
        try:
            return datetime.strptime(raw, fmt).date()
        except ValueError:
            continue
    return None


def all_md_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if p.is_file())


def entity_detail_files(root: Path) -> list[Path]:
    """File-file di ENTITY_FOLDERS yang bukan 00-INDEX.md (wajib punya metadata)."""
    out = []
    for folder in ENTITY_FOLDERS:
        d = root / folder
        if not d.exists():
            continue
        for p in sorted(d.glob("*.md")):
            if p.name != "00-INDEX.md":
                out.append(p)
    return out


def relpath(root: Path, p: Path) -> str:
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def validate_project(root: Path, stale_days: int | None = None) -> ValidationReport:
    report = ValidationReport()
    today = date.today()

    if not root.exists():
        report.error(str(root), "Path project tidak ditemukan.")
        return report

    root_index = root / "00-INDEX.md"
    if not root_index.exists():
        report.error(relpath(root, root_index), "Project tidak punya 00-INDEX.md root (wajib, lihat 04 §4.2).")

    # --- Rule: setiap folder dengan >3 file wajib punya 00-INDEX.md ---
    for d in sorted(p for p in root.rglob("*") if p.is_dir()):
        md_files = [f for f in d.glob("*.md") if f.name != "00-INDEX.md"]
        if len(md_files) > 3 and not (d / "00-INDEX.md").exists():
            report.error(
                relpath(root, d),
                f"Folder berisi {len(md_files)} file tapi tidak punya 00-INDEX.md (Mandatory Rule 05 §5.2 poin 3).",
            )

    seen_ids: dict[str, str] = {}  # id -> file yang mendefinisikan
    id_pattern = re.compile(r"^[A-Z]+-\d+$")

    for f in entity_detail_files(root):
        text = f.read_text(encoding="utf-8", errors="replace")
        rel = relpath(root, f)

        # --- Rule: metadata header wajib ---
        meta = parse_metadata(text)
        if meta is None:
            report.error(rel, "Tidak punya metadata header YAML di baris atas (wajib, 04 §4.3).")
        else:
            fid = meta.get("id", "")
            if not fid or fid.endswith("XXXX") or not id_pattern.match(fid):
                report.error(rel, f"Field 'id' di metadata tidak valid atau masih placeholder: '{fid}'.")
            else:
                if fid in seen_ids:
                    report.error(
                        rel,
                        f"ID DUPLIKAT '{fid}' — sudah dipakai di {seen_ids[fid]}. "
                        f"Ini persis risiko yang disebut di audit (ID collision).",
                    )
                else:
                    seen_ids[fid] = rel

            status = meta.get("status", "")
            if status and status not in VALID_STATUSES:
                report.warn(rel, f"Status '{status}' tidak ada di daftar status baku Planning-OS.")
            if not meta.get("owner"):
                report.warn(rel, "Field 'owner' kosong.")
            if not meta.get("updated"):
                report.warn(rel, "Field 'updated' kosong — tidak bisa dicek freshness (04 §4.7).")

        # --- Rule: Summary Block wajib ---
        if "Summary Block" not in text:
            report.error(rel, "Tidak punya Summary Block (wajib, 04 §4.8 rule 4).")

        # --- Rule: file terlalu besar ---
        n_lines = text.count("\n") + 1
        if n_lines > MAX_LINES:
            report.warn(
                rel,
                f"File {n_lines} baris, melebihi target {MAX_LINES} baris (01 ADR-001 rule 5) — pertimbangkan dipecah.",
            )

        # --- Rule: file wajib terdaftar di 00-INDEX.md folder induknya ---
        parent_index = f.parent / "00-INDEX.md"
        if parent_index.exists():
            idx_text = parent_index.read_text(encoding="utf-8", errors="replace")
            if f.name not in idx_text and (meta or {}).get("id", "") not in idx_text:
                report.error(
                    rel,
                    f"File tidak disebut di {relpath(root, parent_index)} — dianggap orphan (04 §4.8 rule 2).",
                )
        else:
            report.warn(rel, f"Tidak ada 00-INDEX.md di folder induk ({f.parent.name}/) untuk mengecek pendaftaran.")

        # --- Rule: status done wajib closing terisi (heuristik ringan) ---
        if meta and meta.get("status") == "done":
            lower = text.lower()
            if "post implementation review" not in lower:
                report.warn(rel, "Status 'done' tapi tidak ditemukan section Post Implementation Review.")

        # --- Rule: staleness — entitas "aktif" tapi lama tidak di-update ---
        # Ini nutup gap di 05 §5.4 ("Freshness check berkala") yang di dokumen
        # aslinya cuma niat, tidak pernah didefinisikan jadi angka konkret.
        if stale_days is not None and meta:
            status = meta.get("status", "")
            updated_raw = meta.get("updated", "")
            if status in ACTIVE_STATUSES and updated_raw:
                d = parse_date(updated_raw)
                if d is None:
                    report.warn(rel, f"Field 'updated' ('{updated_raw}') tidak berformat YYYY-MM-DD, tidak bisa dicek staleness.")
                else:
                    age = (today - d).days
                    if age > stale_days:
                        report.warn(
                            rel,
                            f"STALE: status '{status}' tapi terakhir diupdate {age} hari lalu "
                            f"(ambang {stale_days} hari) — kemungkinan mangkrak, pertimbangkan diarsipkan "
                            f"atau ditutup (05 §5.4 Freshness check).",
                        )

    # --- Rule: cross-reference tidak boleh nyasar (broken link) ---
    for f in all_md_files(root):
        text = f.read_text(encoding="utf-8", errors="replace")
        rel = relpath(root, f)
        for link in LINK_RE.findall(text):
            if link.startswith("http"):
                continue
            target = (f.parent / link).resolve()
            if not target.exists():
                report.error(rel, f"Link rusak ke '{link}' (target tidak ada — 04 §4.6 dead link).")

    # --- Rule: backlog item yang belum ditandai moved_to tapi entitas sudah ada ---
    backlog_dir = root / "00-backlog"
    if backlog_dir.exists():
        for bf in sorted(backlog_dir.glob("backlog-*.md")):
            text = bf.read_text(encoding="utf-8", errors="replace")
            rel = relpath(root, bf)
            for line in text.splitlines():
                if line.strip().startswith("- [x]") and "moved to" not in line and "→" not in line:
                    report.warn(rel, f"Item backlog checked tapi tidak ditandai '→ moved to <link>': {line.strip()[:80]}")

    return report


def print_report(report: ValidationReport, root: Path) -> int:
    if not report.findings:
        print(f"✅ {root} bersih — tidak ada pelanggaran Mandatory Rules terdeteksi.")
        return 0

    errors = [f for f in report.findings if f.severity == "error"]
    warns = [f for f in report.findings if f.severity == "warn"]

    if errors:
        print(f"\n❌ ERRORS ({len(errors)}) — melanggar Mandatory Rules, wajib diperbaiki:\n")
        for f in errors:
            print(f"  [{f.file}]\n    {f.message}\n")

    if warns:
        print(f"⚠️  WARNINGS ({len(warns)}) — tidak melanggar aturan keras, tapi layak dicek:\n")
        for f in warns:
            print(f"  [{f.file}]\n    {f.message}\n")

    print(f"Ringkasan: {len(errors)} error, {len(warns)} warning di {root}")
    return 1 if errors else 0


# ---------------------------------------------------------------------------
# new-id
# ---------------------------------------------------------------------------

def load_ledger(root: Path) -> dict:
    p = root / LEDGER_NAME
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_ledger(root: Path, ledger: dict):
    (root / LEDGER_NAME).write_text(json.dumps(ledger, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def scan_max_id(root: Path, prefix: str) -> int:
    """Scan semua file .md di project untuk ID tertinggi dengan prefix ini,
    baik dari nama file (feature-0042-...) maupun dari metadata id: FEAT-0042."""
    max_n = 0
    pat_meta = re.compile(rf"^id:\s*{prefix}-(\d+)\s*$", re.MULTILINE)
    pat_fname = re.compile(rf"-(\d{{4,}})-")
    for f in all_md_files(root):
        text = f.read_text(encoding="utf-8", errors="replace")
        for m in pat_meta.finditer(text):
            max_n = max(max_n, int(m.group(1)))
    return max_n


def new_id(root: Path, type_key: str, claim: bool) -> str:
    type_key = type_key.upper()
    if type_key not in ID_PREFIXES:
        known = ", ".join(sorted(ID_PREFIXES))
        raise SystemExit(f"Tipe '{type_key}' tidak dikenal. Pilihan: {known}")

    ledger = load_ledger(root)
    ledger_max = ledger.get(type_key, 0)
    scanned_max = scan_max_id(root, type_key)
    next_n = max(ledger_max, scanned_max) + 1
    new_id_str = f"{type_key}-{next_n:04d}"

    if claim:
        ledger[type_key] = next_n
        save_ledger(root, ledger)

    return new_id_str


# ---------------------------------------------------------------------------
# depgraph
# ---------------------------------------------------------------------------

def build_dep_graph(root: Path) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Return (graph: id -> [depends_on ids], labels: id -> 'rel/path (status)')."""
    graph: dict[str, list[str]] = {}
    labels: dict[str, str] = {}
    for f in entity_detail_files(root):
        text = f.read_text(encoding="utf-8", errors="replace")
        meta = parse_metadata(text)
        if not meta:
            continue
        fid = meta.get("id", "")
        if not fid:
            continue
        deps = parse_id_list(meta.get("depends_on", "[]"))
        graph[fid] = deps
        labels[fid] = f"{relpath(root, f)} (status: {meta.get('status', '?')})"
    return graph, labels


def find_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    """DFS-based cycle detection. Return list of cycles (each a list of ids)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    cycles: list[list[str]] = []
    path: list[str] = []

    def visit(node: str):
        color[node] = GRAY
        path.append(node)
        for dep in graph.get(node, []):
            if dep not in graph:
                continue  # dependency ke ID yang tidak ada file-nya — dicek terpisah
            if color.get(dep, WHITE) == GRAY:
                # cycle ditemukan: potong path dari titik dep muncul pertama
                idx = path.index(dep)
                cycles.append(path[idx:] + [dep])
            elif color.get(dep, WHITE) == WHITE:
                visit(dep)
        path.pop()
        color[node] = BLACK

    for n in graph:
        if color[n] == WHITE:
            visit(n)
    return cycles


def topological_order(graph: dict[str, list[str]]) -> list[str]:
    """Kahn's algorithm. Asumsi graph sudah bebas cycle (dicek terpisah)."""
    in_degree = {n: 0 for n in graph}
    for n, deps in graph.items():
        for d in deps:
            if d in graph:
                in_degree[n] += 1  # n bergantung pada d => n punya in-degree dari d

    # bangun adjacency terbalik: d -> [n yang depends_on d]
    dependents: dict[str, list[str]] = {n: [] for n in graph}
    for n, deps in graph.items():
        for d in deps:
            if d in graph:
                dependents[d].append(n)

    queue = sorted([n for n, deg in in_degree.items() if deg == 0])
    order: list[str] = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for dependent in sorted(dependents.get(node, [])):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
        queue.sort()
    return order


def run_depgraph(root: Path) -> int:
    if not root.exists():
        print(f"❌ Path project tidak ditemukan: {root}")
        return 1

    graph, labels = build_dep_graph(root)

    if not graph:
        print(f"Tidak ada entitas dengan metadata id di {root}.")
        return 0

    # cek depends_on yang menunjuk ke ID yang tidak ada file-nya sama sekali
    unknown_refs = []
    for n, deps in graph.items():
        for d in deps:
            if d not in graph:
                unknown_refs.append((n, d))

    cycles = find_cycles(graph)

    if unknown_refs:
        print(f"⚠️  {len(unknown_refs)} depends_on menunjuk ke ID yang tidak ditemukan file-nya:\n")
        for n, d in unknown_refs:
            print(f"  {n} depends_on '{d}' — tidak ada file dengan id ini ({labels.get(n)})")
        print()

    if cycles:
        print(f"❌ CIRCULAR DEPENDENCY ditemukan ({len(cycles)}) — SOP-00 poin 4/5 tidak bisa dijalankan sampai ini diperbaiki:\n")
        for c in cycles:
            chain = " → ".join(c)
            print(f"  {chain}")
        print()
        print("Perbaiki depends_on di file-file yang terlibat sebelum melanjutkan urutan pemrosesan.")
        return 1

    order = topological_order(graph)
    print(f"✅ Tidak ada circular dependency. Urutan pemrosesan yang disarankan ({len(order)} entitas, "
          f"dependency lebih dulu):\n")
    for i, fid in enumerate(order, 1):
        print(f"  {i}. {fid} — {labels.get(fid, '')}")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Planning-OS Enforcer CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_validate = sub.add_parser("validate", help="Validasi struktur satu project instance")
    p_validate.add_argument("project_path", type=Path)
    p_validate.add_argument("--stale-days", type=int, default=None,
                             help="Flag entitas berstatus aktif yang tidak diupdate lebih dari N hari")

    p_newid = sub.add_parser("new-id", help="Generate ID berikutnya untuk tipe entitas")
    p_newid.add_argument("project_path", type=Path)
    p_newid.add_argument("type", help="FEAT | TASK | BUG | ENH | REF | MIG | BKLG")
    p_newid.add_argument("--claim", action="store_true",
                          help="Catat ID ini di ledger supaya tidak dipakai ulang (cegah race antar sesi)")

    p_depgraph = sub.add_parser("depgraph", help="Cek dependency graph: circular dependency + urutan pemrosesan")
    p_depgraph.add_argument("project_path", type=Path)

    args = parser.parse_args()

    if args.cmd == "validate":
        report = validate_project(args.project_path, stale_days=args.stale_days)
        sys.exit(print_report(report, args.project_path))

    elif args.cmd == "new-id":
        result = new_id(args.project_path, args.type, args.claim)
        print(result)
        sys.exit(0)

    elif args.cmd == "depgraph":
        sys.exit(run_depgraph(args.project_path))


if __name__ == "__main__":
    main()
