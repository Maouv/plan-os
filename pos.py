#!/usr/bin/env python3
"""
pos.py — Planning-OS Enforcer CLI

Dua kapabilitas inti (dibuat karena Planning-OS aslinya 100% bergantung pada
disiplin manual, tanpa validasi otomatis):

  1. `validate`  — scan satu project instance (ENTITY_FOLDERS + master
                    plan/project file di root), laporkan pelanggaran
                    Mandatory Rules (05 § 5.2): orphan file, index tidak
                    sinkron, metadata hilang, file > 400 baris, status tidak
                    valid, ID duplikat, cross-reference yang nyasar, 14
                    heading Mandatory Review Section hilang (03 §3.2),
                    entitas stale (--stale-days). `--full-instance` juga
                    mewajibkan seluruh scaffold 04 §4.2 lengkap.
  2. `new-id`    — generate ID berikutnya untuk tipe entitas tertentu (PROJ/
                    FEAT/TASK/BUG/ENH/REF/MIG/BKLG) dengan scan seluruh
                    project, supaya tidak ada dua entitas kebetulan dapat ID
                    sama.
  3. `depgraph`  — bangun graph dari field depends_on di semua entitas
                    (termasuk master plan/project file di root), deteksi
                    circular dependency (yang bikin SOP-00 poin 5 mustahil
                    dijalankan), dan cetak urutan pemrosesan yang valid
                    (topological sort) sesuai amanat SOP-00 poin 4. Graph
                    kosong dianggap KEGAGALAN kecuali `--allow-empty`.

Didesain zero-dependency (stdlib only) supaya bisa langsung jalan di VPS/
Termux tanpa install apa-apa.

Catatan cakupan yang jujur (lihat issue/plan-os-tooling-and-spec-friction.md
#3): 14 heading Mandatory Review Section ditegakkan sebagai hard error. 27
lifecycle stage heading (03 §3.1) BELUM ditegakkan sebagai hard error karena
template saat ini tidak mendefinisikan heading eksplisit untuk semua 27 tahap
per tipe entitas secara seragam — validator mencetak ini sebagai catatan
cakupan, bukan pura-pura sudah lengkap.

USAGE
-----
    python3 pos.py validate <path-ke-project>
    python3 pos.py validate <path-ke-project> --stale-days 14
    python3 pos.py validate <path-ke-project> --full-instance
    python3 pos.py validate <path-ke-project> --json   (output terstruktur untuk
        dikonsumsi tool/agent lain, mis. Hermes — bukan scrape teks manusia)
    python3 pos.py new-id <path-ke-project> <TYPE>
    python3 pos.py new-id <path-ke-project> <TYPE> --claim   (langsung catat
        ID ini sebagai "sudah dipakai" di .pos-id-ledger.json, mencegah race
        antar sesi AI yang jalan paralel)
    python3 pos.py depgraph <path-ke-project>
    python3 pos.py depgraph <path-ke-project> --allow-empty
    python3 pos.py depgraph <path-ke-project> --json   (sertakan failure_type:
        "path_not_found" | "empty_graph" | "cycle" | "dangling_ref" | null)

TYPE yang dikenal: PROJ, FEAT, TASK, BUG, ENH, REF, MIG, BKLG
(bisa ditambah sendiri di ID_PREFIXES di bawah kalau Planning-OS di-extend)

Exit code: 0 kalau validate/depgraph bersih, 1 kalau ada temuan pelanggaran,
circular dependency, dangling depends_on reference, atau graph kosong tanpa
--allow-empty (untuk dipakai di CI / pre-commit hook / SOP-04 closing check).
`--json` tidak mengubah exit code, hanya format output — exit code tetap jadi
sinyal utama untuk gate/CI, `--json` untuk konsumsi terprogram yang butuh
detail per-temuan.
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
# NB (issue plan-os-tooling-and-spec-friction.md #6): "discovery" ada di
# TEMPLATE-project.md sejak awal tapi hilang dari daftar ini — project-level
# validation jadi langsung false-positive begitu ditambahkan. Disatukan di sini.
VALID_STATUSES = {
    "idea", "discovery", "backlog", "ready", "planning", "in-progress", "review",
    "reported", "investigating", "done", "archived",
}
ID_PREFIXES = {
    "PROJ": "project",  # issue #5: ada di TEMPLATE-project.md tapi tidak di allocator
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

# issue #4: canonical filename Decision Log = 09-decision-log.md (selaras urutan
# scaffold di 04 §4.2). Semua referensi lain (`08-decision-log.md`) di docs/
# template sudah disamakan ke ini.
DECISION_LOG_NAME = "09-decision-log.md"

# issue #3 (bagian review): 14 sub-bagian wajib dari 03 §3.2 / TEMPLATE-review-
# checklist.md. Heading harus ADA (boleh isi "Not Applicable — <alasan>" untuk
# pekerjaan kecil, tapi heading sendiri tidak boleh hilang).
MANDATORY_REVIEW_HEADINGS = [
    "Potential Bugs", "Known Risks", "Edge Cases", "Failure Cases",
    "Negative Test Cases", "Regression Risk", "Rollback Plan",
    "Validation Checklist", "Review Checklist", "Acceptance Checklist",
    "User Testing Result", "Post Implementation Review", "Lessons Learned",
    "Future Improvement",
]

METADATA_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
ID_LINE_RE = re.compile(r"^id:\s*([A-Z]+-\d+)\s*$", re.MULTILINE)
STATUS_LINE_RE = re.compile(r"^status:\s*([a-zA-Z-]+)", re.MULTILINE)
SUMMARY_BLOCK_RE = re.compile(r"\*\*Summary Block:\*\*")
LINK_RE = re.compile(r"\]\(([^)]+\.md)\)")

# Scaffold wajib per 04 §4.2 untuk "full project instance". Dipakai oleh
# --full-instance (issue #1 & #8: sebelumnya scaffold parsial bisa lolos
# validate 100% karena tidak ada yang mengecek kelengkapan struktur ini sama
# sekali).
REQUIRED_SCAFFOLD = [
    "00-INDEX.md",
    "00-backlog",
    "01-discovery",
    "02-requirement",
    "03-planning",
    "04-design-architecture",
    "05-features",
    "06-tasks",
    "07-bugs-and-fixes",
    "08-refactor-and-enhancement",
    DECISION_LOG_NAME,
    "10-review-and-retro",
    "99-archive",
]


@dataclass
class Finding:
    severity: str  # "error" | "warn"
    file: str
    message: str


@dataclass
class ValidationReport:
    findings: list = field(default_factory=list)
    scope: dict = field(default_factory=dict)  # discovered / checked / skipped counts

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


def root_project_files(root: Path) -> list[Path]:
    """Master plan / project-level file langsung di root project (04 §4.2:
    dibuat dari TEMPLATE-project.md, id: PROJ-xxxx).

    issue #1 (High): sebelumnya file ini SAMA SEKALI tidak diperiksa karena
    entity_detail_files() cuma melihat ke 4 ENTITY_FOLDERS. Master plan Graps
    ~1.179 baris lolos validate tanpa diperiksa metadata/Summary
    Block/lifecycle/review-nya sama sekali. Root project file dikenali dari
    metadata `type: project` (bukan sekadar "file .md apapun di root", supaya
    00-backlog/ dan file catatan lepas lain tidak ikut dianggap entitas wajib).
    """
    out = []
    for p in sorted(root.glob("*.md")):
        if p.name == "00-INDEX.md":
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        meta = parse_metadata(text)
        if meta and meta.get("type") == "project":
            out.append(p)
    return out


def checked_entity_files(root: Path) -> list[Path]:
    """Union semua file yang WAJIB melalui pemeriksaan entitas penuh:
    ENTITY_FOLDERS + master plan/project file di root (issue #1)."""
    return root_project_files(root) + entity_detail_files(root)


def relpath(root: Path, p: Path) -> str:
    try:
        return str(p.relative_to(root))
    except ValueError:
        return str(p)


def validate_project(root: Path, stale_days: int | None = None, full_instance: bool = False) -> ValidationReport:
    report = ValidationReport()
    today = date.today()

    if not root.exists():
        report.error(str(root), "Path project tidak ditemukan.")
        return report

    root_index = root / "00-INDEX.md"
    if not root_index.exists():
        report.error(relpath(root, root_index), "Project tidak punya 00-INDEX.md root (wajib, lihat 04 §4.2).")

    # --- Rule (opt-in): scaffold wajib 04 §4.2 harus lengkap untuk full instance ---
    # issue #1 acceptance criteria: "Full-instance mode gagal bila scaffold wajib
    # tidak lengkap." Opt-in (bukan default) karena project kecil yang sengaja
    # belum memakai semua folder (mis. belum ada bug sama sekali) bukan berarti
    # rusak — hanya belum "full instance".
    if full_instance:
        for entry in REQUIRED_SCAFFOLD:
            if not (root / entry).exists():
                report.error(entry, "Scaffold wajib (04 §4.2) tidak ditemukan — full-instance tidak lengkap.")

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

    # issue #1: dulu hanya entity_detail_files() (4 folder) yang diperiksa
    # penuh — master plan/project file di root lolos tanpa dicek sama sekali.
    entities = checked_entity_files(root)
    all_files = all_md_files(root)
    skipped = [f for f in all_files if f not in entities and f.name != "00-INDEX.md"]
    report.scope = {
        "discovered": len(all_files),
        "checked": len(entities),
        "skipped": len(skipped),
    }

    # issue #12 pra-scan: hitung berapa file yang mendeklarasikan tiap id agar
    # orphan-check di bawah tahu kapan fallback "id muncul di index" AMBIGU
    # (duplicate id) dan harus dimatikan untuk file-file yang berbagi id itu.
    id_counts: dict[str, int] = {}
    for f in entities:
        m = parse_metadata(f.read_text(encoding="utf-8", errors="replace"))
        fid = (m or {}).get("id", "")
        if fid:
            id_counts[fid] = id_counts.get(fid, 0) + 1

    for f in entities:
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

        # --- Rule: 14 sub-bagian Mandatory Review Section wajib ada (03 §3.2) ---
        # issue #3 (bagian review): sebelumnya hanya string "Summary Block" yang
        # dicek; hampir seluruh 14 heading review bisa hilang tanpa terdeteksi.
        # Heading dicek sebagai "### <nama>"; isi boleh "Not Applicable — alasan"
        # (03 §3.2 aturan keras), yang penting heading tidak dihapus.
        missing_review = [
            h for h in MANDATORY_REVIEW_HEADINGS
            if not re.search(rf"^###\s+{re.escape(h)}\s*$", text, re.MULTILINE)
        ]
        if missing_review:
            report.error(
                rel,
                f"Mandatory Review Section tidak lengkap — {len(missing_review)}/14 heading hilang: "
                f"{', '.join(missing_review)} (wajib, 03 §3.2).",
            )

        # --- Rule: file terlalu besar ---
        n_lines = text.count("\n") + 1
        if n_lines > MAX_LINES:
            report.warn(
                rel,
                f"File {n_lines} baris, melebihi target {MAX_LINES} baris (01 ADR-001 rule 5) — pertimbangkan dipecah.",
            )

        # --- Rule: file wajib terdaftar di 00-INDEX.md folder induknya ---
        # issue #12 fix: dulu fallback-nya "id file ini muncul di suatu tempat
        # di idx_text" — substring global, bukan baris registrasi spesifik
        # untuk file ini. Kalau dua file berbagi id yang sama (duplicate id)
        # dan cuma satu yang benar-benar terdaftar, file yang TIDAK terdaftar
        # tetap lolos karena id-nya ikut "ketemu" lewat baris registrasi file
        # lain. Fix: fallback id-based HANYA dipakai kalau id itu unik
        # (id_counts == 1) di antara entities yang diperiksa — begitu id
        # duplikat, fallback dimatikan dan registrasi wajib dibuktikan lewat
        # nama file itu sendiri, bukan id yang bisa dipakai bersama.
        parent_index = f.parent / "00-INDEX.md"
        if parent_index.exists():
            idx_text = parent_index.read_text(encoding="utf-8", errors="replace")
            fid = (meta or {}).get("id", "")
            registered = f.name in idx_text
            if not registered and fid and id_counts.get(fid, 0) == 1:
                registered = fid in idx_text
            if not registered:
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

    # --- Catatan cakupan: 27 lifecycle stage heading (03 §3.1) ---
    # issue #3 (bagian lifecycle): TEMPLATE-project.md/feature/task/bugfix TIDAK
    # mendefinisikan heading untuk seluruh 27 tahap secara literal dan seragam
    # (mis. task template tidak punya heading Testing/QA/Deployment/Monitoring
    # sendiri). Memaksa 27-heading check yang seragam di semua tipe entitas akan
    # men-false-positive setiap task/bugfix kecil yang sah sesuai desain template
    # saat ini. Fix yang jujur untuk ini adalah redesign template per-tipe
    # (menambahkan heading eksplisit yang applicable per tipe), bukan menambal di
    # validator. Bagian yang SUDAH bisa ditegakkan otomatis (14 heading Mandatory
    # Review Section, yang meng-cover cluster 3/4/5/6) sudah dicek di atas.
    report.warn(
        str(root),
        "Cakupan diketahui: 27 lifecycle stage heading (03 §3.1) belum ditegakkan penuh — "
        "template saat ini tidak mendefinisikan heading eksplisit untuk semua 27 tahap per "
        "tipe entitas. Lihat issue plan-os-tooling-and-spec-friction.md #3 untuk rencana "
        "redesign template yang diperlukan sebelum ini bisa jadi hard error.",
    )

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
    scope = report.scope
    if scope:
        print(
            f"Scope: {scope['discovered']} file .md ditemukan, "
            f"{scope['checked']} diperiksa penuh (entity + master plan), "
            f"{scope['skipped']} dilewati (index/backlog/catatan pendukung)."
        )

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


def print_report_json(report: ValidationReport, root: Path) -> int:
    """Versi machine-readable dari print_report(), untuk `validate --json` —
    dipakai supaya tool/agent lain (mis. Hermes) bisa parse hasil per finding
    tanpa scrape teks manusia. Exit code sama persis dengan mode teks."""
    errors = [f for f in report.findings if f.severity == "error"]
    warns = [f for f in report.findings if f.severity == "warn"]
    payload = {
        "root": str(root),
        "scope": report.scope,
        "findings": [
            {"severity": f.severity, "file": f.file, "message": f.message}
            for f in report.findings
        ],
        "error_count": len(errors),
        "warn_count": len(warns),
        "ok": len(errors) == 0,
    }
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
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

    # issue #11 fix: sebelumnya --claim langsung lanjut ke save_ledger(), yang
    # menulis .pos-id-ledger.json ke folder yang belum ada -> unhandled
    # FileNotFoundError sampai ke shell. new-id TANPA --claim tetap boleh
    # jalan di path yang belum ada (cuma menghitung, tidak menulis apa-apa),
    # sama seperti validate_project()/run_depgraph() yang sudah guard
    # root.exists() lebih dulu.
    if claim and not root.exists():
        raise SystemExit(
            f"❌ Path project tidak ditemukan: {root} — tidak bisa --claim ID di sini "
            f"karena ledger (.pos-id-ledger.json) butuh folder project yang sudah ada. "
            f"Scaffold dulu foldernya (lihat 05 SOP §New project), baru claim ID."
        )

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
    for f in checked_entity_files(root):
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


def run_depgraph(root: Path, allow_empty: bool = False, json_output: bool = False) -> int:
    """`json_output=True` mengembalikan payload machine-readable (root,
    entity_count, unknown_refs, cycles, order, failure_type, ok) alih-alih
    teks manusia — dipakai oleh `depgraph --json`. Pesan teks tetap identik
    dengan mode default; dikumpulkan lewat emit() lalu di-flush di akhir
    supaya kedua mode selalu konsisten dari satu sumber logika yang sama."""
    lines: list[str] = []

    def emit(msg: str = ""):
        lines.append(msg)

    def finish(exit_code: int, payload: dict) -> int:
        if json_output:
            print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        else:
            for line in lines:
                print(line)
        return exit_code

    if not root.exists():
        emit(f"❌ Path project tidak ditemukan: {root}")
        return finish(1, {
            "root": str(root), "path_exists": False, "entity_count": 0,
            "unknown_refs": [], "cycles": [], "order": [],
            "ok": False, "failure_type": "path_not_found",
        })

    graph, labels = build_dep_graph(root)

    if not graph:
        # issue #2 (High): sebelumnya exit code 0 di sini, sehingga "kosong"
        # bisa disalahartikan sebagai "graph tervalidasi dan bersih" — ini
        # benar-benar terjadi saat audit awal Graps. Sekarang eksplisit
        # dianggap BUKAN sukses kecuali dipanggil dengan --allow-empty (mis.
        # untuk project yang memang baru dimulai dan belum punya entitas).
        emit(f"entities=0; graph not validated — tidak ada entitas dengan metadata id di {root}.")
        if allow_empty:
            emit("(--allow-empty aktif: dianggap bukan pelanggaran.)")
            return finish(0, {
                "root": str(root), "path_exists": True, "entity_count": 0,
                "unknown_refs": [], "cycles": [], "order": [], "allow_empty": True,
                "ok": True, "failure_type": None,
            })
        emit(
            "Jika project sudah punya feature/task yang direncanakan, ini kemungkinan "
            "besar bug (file belum di-scan atau metadata hilang). Jika project memang "
            "baru dan belum ada entitas, jalankan ulang dengan --allow-empty."
        )
        return finish(1, {
            "root": str(root), "path_exists": True, "entity_count": 0,
            "unknown_refs": [], "cycles": [], "order": [], "allow_empty": False,
            "ok": False, "failure_type": "empty_graph",
        })

    # cek depends_on yang menunjuk ke ID yang tidak ada file-nya sama sekali
    unknown_refs = []
    for n, deps in graph.items():
        for d in deps:
            if d not in graph:
                unknown_refs.append((n, d))

    cycles = find_cycles(graph)

    if unknown_refs:
        # issue #12 follow-up (severity: dangling depends_on): sebelumnya ini
        # cuma dicetak dengan ⚠️ dan TETAP exit 0 — inkonsisten dengan
        # `validate`, yang menganggap broken markdown link (04 §4.6) sebagai
        # ERROR keras (exit 1). Dependency yang menunjuk ke ID yang filenya
        # tidak ada adalah kelas masalah yang sama (referensi nyasar ke
        # sesuatu yang tidak ada) — kalau satu jadi hard failure yang lain
        # juga harus, supaya "depgraph bersih" tidak jadi false confidence
        # yang sama seperti masalah original di issue #1/#2. Sekarang
        # diperlakukan sebagai ERROR dan membuat depgraph exit 1.
        emit(f"❌ {len(unknown_refs)} depends_on menunjuk ke ID yang tidak ditemukan file-nya "
             f"(diperlakukan sebagai error — konsisten dengan broken-link check di `validate`):")
        emit()
        for n, d in unknown_refs:
            emit(f"  {n} depends_on '{d}' — tidak ada file dengan id ini ({labels.get(n)})")
        emit()
        emit("Perbaiki depends_on yang nyasar ini sebelum urutan pemrosesan di bawah bisa dipercaya penuh.")
        emit()

    if cycles:
        emit(f"❌ CIRCULAR DEPENDENCY ditemukan ({len(cycles)}) — SOP-00 poin 4/5 tidak bisa dijalankan sampai ini diperbaiki:")
        emit()
        for c in cycles:
            emit(f"  {' → '.join(c)}")
        emit()
        emit("Perbaiki depends_on di file-file yang terlibat sebelum melanjutkan urutan pemrosesan.")
        return finish(1, {
            "root": str(root), "path_exists": True, "entity_count": len(graph),
            "unknown_refs": [{"from": n, "to": d} for n, d in unknown_refs],
            "cycles": cycles, "order": [],
            "ok": False, "failure_type": "cycle",
        })

    order = topological_order(graph)
    if unknown_refs:
        emit(f"⚠️  Urutan pemrosesan di bawah ({len(order)} entitas) dihitung tanpa memperhitungkan "
             f"depends_on yang nyasar di atas — jangan dipercaya sampai referensi itu diperbaiki:")
    else:
        emit(f"✅ Tidak ada circular dependency. Urutan pemrosesan yang disarankan ({len(order)} entitas, "
             f"dependency lebih dulu):")
    emit()
    for i, fid in enumerate(order, 1):
        emit(f"  {i}. {fid} — {labels.get(fid, '')}")

    ok = not unknown_refs
    return finish(1 if unknown_refs else 0, {
        "root": str(root), "path_exists": True, "entity_count": len(graph),
        "unknown_refs": [{"from": n, "to": d} for n, d in unknown_refs],
        "cycles": [], "order": order,
        "ok": ok, "failure_type": None if ok else "dangling_ref",
    })


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
    p_validate.add_argument("--full-instance", action="store_true",
                             help="Wajibkan seluruh scaffold 04 §4.2 lengkap (00-backlog/, 01-discovery/, "
                                  "... 09-decision-log.md, dst) — gagal jika ada yang hilang")
    p_validate.add_argument("--json", action="store_true",
                             help="Output JSON terstruktur (scope, findings[], error_count, warn_count, ok) "
                                  "alih-alih teks manusia — untuk dikonsumsi tool/agent lain (mis. Hermes)")

    p_newid = sub.add_parser("new-id", help="Generate ID berikutnya untuk tipe entitas")
    p_newid.add_argument("project_path", type=Path)
    p_newid.add_argument("type", help="PROJ | FEAT | TASK | BUG | ENH | REF | MIG | BKLG")
    p_newid.add_argument("--claim", action="store_true",
                          help="Catat ID ini di ledger supaya tidak dipakai ulang (cegah race antar sesi)")

    p_depgraph = sub.add_parser("depgraph", help="Cek dependency graph: circular dependency + urutan pemrosesan")
    p_depgraph.add_argument("project_path", type=Path)
    p_depgraph.add_argument("--allow-empty", action="store_true",
                             help="Jangan anggap graph kosong (0 entitas) sebagai kegagalan — untuk project baru")
    p_depgraph.add_argument("--json", action="store_true",
                             help="Output JSON terstruktur (entity_count, unknown_refs[], cycles[], order[], "
                                  "failure_type, ok) alih-alih teks manusia — untuk dikonsumsi tool/agent lain")

    args = parser.parse_args()

    if args.cmd == "validate":
        report = validate_project(args.project_path, stale_days=args.stale_days, full_instance=args.full_instance)
        if args.json:
            sys.exit(print_report_json(report, args.project_path))
        sys.exit(print_report(report, args.project_path))

    elif args.cmd == "new-id":
        result = new_id(args.project_path, args.type, args.claim)
        print(result)
        sys.exit(0)

    elif args.cmd == "depgraph":
        sys.exit(run_depgraph(args.project_path, allow_empty=args.allow_empty, json_output=args.json))


if __name__ == "__main__":
    main()


