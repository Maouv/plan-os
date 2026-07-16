"""Shared fixtures untuk test suite pos.py (ENH-0001).

Kenapa builder, bukan file fixture statis di disk: setiap test butuh variasi
kecil (satu heading hilang, satu file >400 baris, dsb) dari entitas yang
"kalau tidak" valid — builder parametrik jauh lebih murah dipelihara
daripada puluhan file .md statis yang nyaris identik.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

ALL_REVIEW_HEADINGS = [
    "Potential Bugs", "Known Risks", "Edge Cases", "Failure Cases",
    "Negative Test Cases", "Regression Risk", "Rollback Plan",
    "Validation Checklist", "Review Checklist", "Acceptance Checklist",
    "User Testing Result", "Post Implementation Review", "Lessons Learned",
    "Future Improvement",
]


def review_block(omit: list[str] | None = None) -> str:
    """14 heading Mandatory Review Section (03 §3.2), minus `omit` bila diisi."""
    omit = omit or []
    lines = ["## Mandatory Review Section"]
    for h in ALL_REVIEW_HEADINGS:
        if h in omit:
            continue
        lines.append(f"### {h}\n- Not Applicable — test fixture.")
    return "\n".join(lines)


def entity_text(
    entity_id: str = "FEAT-0001",
    entity_type: str = "feature",
    status: str = "in-progress",
    owner: str = "tester",
    created: str = "2026-07-01",
    updated: str = "2026-07-01",
    depends_on: str = "[]",
    include_summary: bool = True,
    omit_review_headings: list[str] | None = None,
    extra_lines: int = 0,
    body: str = "",
) -> str:
    summary = "> **Summary Block:** Entity fixture untuk test.\n" if include_summary else ""
    padding = "\n".join(f"Padding line {i}." for i in range(extra_lines))
    return (
        f"---\n"
        f"id: {entity_id}\n"
        f"type: {entity_type}\n"
        f"status: {status}\n"
        f"owner: {owner}\n"
        f"created: {created}\n"
        f"updated: {updated}\n"
        f"depends_on: {depends_on}\n"
        f"related: []\n"
        f"---\n\n"
        f"# {entity_id} Fixture\n\n"
        f"{summary}\n"
        f"{body}\n"
        f"{padding}\n\n"
        f"{review_block(omit_review_headings)}\n"
    )


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """Project scaffold minimal-tapi-valid: root index + satu folder entitas
    (05-features/) berisi satu feature yang lolos validate 100% bersih.
    Test individual menambah/merusak file di atas fondasi ini."""
    root = tmp_path / "demo-project"
    root.mkdir()
    (root / "00-INDEX.md").write_text("# Demo Project\n\nStatus: in-progress\n", encoding="utf-8")

    feat_dir = root / "05-features"
    feat_dir.mkdir()
    (feat_dir / "feature-0001-demo.md").write_text(entity_text(), encoding="utf-8")
    (feat_dir / "00-INDEX.md").write_text(
        "# Features Index\n\n- FEAT-0001 — feature-0001-demo.md — in-progress\n",
        encoding="utf-8",
    )
    return root

