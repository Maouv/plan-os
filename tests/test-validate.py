"""Tests untuk `pos.py validate` (validate_project / print_report)."""
from __future__ import annotations

from conftest import entity_text

import pos


def _errors(report):
    return [f for f in report.findings if f.severity == "error"]


def _warns(report):
    return [f for f in report.findings if f.severity == "warn"]


def test_clean_project_has_zero_errors(project):
    report = pos.validate_project(project)
    assert _errors(report) == []


def test_scope_reports_discovered_checked_skipped(project):
    # Regression: issue #1 acceptance criteria — validate wajib melaporkan
    # jumlah file discovered/checked/skipped, bukan diam-diam.
    report = pos.validate_project(project)
    assert report.scope["discovered"] >= 1
    assert report.scope["checked"] == 1  # cuma FEAT-0001
    assert "skipped" in report.scope


def test_root_project_master_plan_is_checked(project):
    # Regression: issue #1 — master plan (type: project) di root project
    # dulu SAMA SEKALI tidak diperiksa oleh entity_detail_files(). Sekarang
    # root_project_files() harus menangkapnya lewat metadata type: project.
    master = project / "master-plan.md"
    master.write_text(entity_text(entity_id="PROJ-0001", entity_type="project"), encoding="utf-8")
    report = pos.validate_project(project)
    assert report.scope["checked"] == 2  # FEAT-0001 + master plan
    # Master plan tidak terdaftar di manapun -> harus kena orphan-ish warning,
    # bukan lolos diam-diam seperti sebelum fix.
    assert any("master-plan.md" in f.file for f in report.findings)


def test_missing_metadata_header_is_error(project):
    f = project / "05-features" / "feature-0002-broken.md"
    f.write_text("# Tidak ada metadata\n\nIsi bebas.\n", encoding="utf-8")
    report = pos.validate_project(project)
    assert any("metadata header" in e.message for e in _errors(report))


def test_missing_summary_block_is_error(project):
    f = project / "05-features" / "feature-0002-nosum.md"
    f.write_text(entity_text(entity_id="FEAT-0002", include_summary=False), encoding="utf-8")
    report = pos.validate_project(project)
    assert any("Summary Block" in e.message for e in _errors(report) if e.file.endswith("nosum.md"))


def test_missing_review_headings_are_reported_individually(project):
    # Regression: issue #3 — dulu cuma string "Summary Block" yang dicek;
    # heading review section bisa hilang tanpa terdeteksi sama sekali.
    f = project / "05-features" / "feature-0002-partial-review.md"
    f.write_text(
        entity_text(entity_id="FEAT-0002", omit_review_headings=["Rollback Plan", "Regression Risk"]),
        encoding="utf-8",
    )
    report = pos.validate_project(project)
    matches = [e for e in _errors(report) if "partial-review.md" in e.file]
    assert matches
    assert "Rollback Plan" in matches[0].message
    assert "Regression Risk" in matches[0].message


def test_duplicate_id_is_error(project):
    f = project / "05-features" / "feature-0099-dup.md"
    f.write_text(entity_text(entity_id="FEAT-0001"), encoding="utf-8")  # sama dengan fixture
    report = pos.validate_project(project)
    assert any("DUPLIKAT" in e.message for e in _errors(report))


def test_orphan_file_not_registered_in_index_is_error(project):
    f = project / "05-features" / "feature-0002-orphan.md"
    f.write_text(entity_text(entity_id="FEAT-0002"), encoding="utf-8")
    # sengaja TIDAK didaftarkan di 05-features/00-INDEX.md
    report = pos.validate_project(project)
    assert any("orphan" in e.message for e in _errors(report) if "orphan.md" in e.file)


def test_duplicate_id_does_not_hide_unregistered_orphan(project):
    # Regression: issue #12 — dulu file kedua dengan id duplikat & TIDAK
    # terdaftar bisa lolos orphan-check karena id-nya "ketemu" sebagai
    # substring di baris registrasi file LAIN yang berbagi id sama. Sekarang
    # registrasi harus dibuktikan lewat nama file spesifik saat id duplikat.
    dup = project / "05-features" / "feature-0001-duplicate-unregistered.md"
    dup.write_text(entity_text(entity_id="FEAT-0001"), encoding="utf-8")
    # 00-INDEX.md hanya menyebut file asli (feature-0001-demo.md), bukan
    # dup.name -- tapi id FEAT-0001 tetap muncul di index lewat baris asli.
    report = pos.validate_project(project)
    orphan_hits = [e for e in _errors(report) if "duplicate-unregistered.md" in e.file and "orphan" in e.message]
    assert orphan_hits, "file duplikat-ID yang tidak terdaftar harus tetap kena orphan error"


def test_broken_relative_link_is_error(project):
    f = project / "05-features" / "feature-0002-link.md"
    f.write_text(
        entity_text(entity_id="FEAT-0002", body="Lihat [broken](../06-tasks/task-9999-ghost.md)."),
        encoding="utf-8",
    )
    (project / "05-features" / "00-INDEX.md").write_text(
        (project / "05-features" / "00-INDEX.md").read_text(encoding="utf-8") + "- feature-0002-link.md\n",
        encoding="utf-8",
    )
    report = pos.validate_project(project)
    assert any("Link rusak" in e.message for e in _errors(report))


def test_file_over_400_lines_warns(project):
    f = project / "05-features" / "feature-0002-huge.md"
    f.write_text(entity_text(entity_id="FEAT-0002", extra_lines=450), encoding="utf-8")
    (project / "05-features" / "00-INDEX.md").write_text(
        (project / "05-features" / "00-INDEX.md").read_text(encoding="utf-8") + "- feature-0002-huge.md\n",
        encoding="utf-8",
    )
    report = pos.validate_project(project)
    assert any("melebihi target" in w.message for w in _warns(report) if "huge.md" in w.file)


def test_folder_with_more_than_3_files_requires_index(project):
    tasks_dir = project / "06-tasks"
    tasks_dir.mkdir()
    for i in range(4):
        (tasks_dir / f"task-000{i}-x.md").write_text(entity_text(entity_id=f"TASK-000{i}"), encoding="utf-8")
    # sengaja TIDAK membuat 06-tasks/00-INDEX.md
    report = pos.validate_project(project)
    assert any("tidak punya 00-INDEX.md" in e.message for e in _errors(report))


def test_full_instance_flag_requires_complete_scaffold(project):
    report_default = pos.validate_project(project, full_instance=False)
    report_full = pos.validate_project(project, full_instance=True)
    assert _errors(report_default) == []  # tanpa flag, scaffold parsial OK
    assert any("Scaffold wajib" in e.message for e in _errors(report_full))


def test_invalid_status_warns(project):
    f = project / "05-features" / "feature-0002-badstatus.md"
    f.write_text(entity_text(entity_id="FEAT-0002", status="halfway-there"), encoding="utf-8")
    (project / "05-features" / "00-INDEX.md").write_text(
        (project / "05-features" / "00-INDEX.md").read_text(encoding="utf-8") + "- feature-0002-badstatus.md\n",
        encoding="utf-8",
    )
    report = pos.validate_project(project)
    assert any("tidak ada di daftar status baku" in w.message for w in _warns(report))


def test_discovery_status_is_accepted():
    # Regression: issue #6 — VALID_STATUSES dulu tidak memuat "discovery"
    # walau dipakai di TEMPLATE-project.md.
    assert "discovery" in pos.VALID_STATUSES


def test_stale_active_entity_warns(project, monkeypatch):
    f = project / "05-features" / "feature-0002-stale.md"
    f.write_text(
        entity_text(entity_id="FEAT-0002", status="in-progress", updated="2020-01-01"),
        encoding="utf-8",
    )
    (project / "05-features" / "00-INDEX.md").write_text(
        (project / "05-features" / "00-INDEX.md").read_text(encoding="utf-8") + "- feature-0002-stale.md\n",
        encoding="utf-8",
    )
    report = pos.validate_project(project, stale_days=14)
    assert any("STALE" in w.message for w in _warns(report))


def test_done_status_without_pir_warns(project):
    f = project / "05-features" / "feature-0002-done.md"
    f.write_text(entity_text(entity_id="FEAT-0002", status="done", omit_review_headings=[]), encoding="utf-8")
    (project / "05-features" / "00-INDEX.md").write_text(
        (project / "05-features" / "00-INDEX.md").read_text(encoding="utf-8") + "- feature-0002-done.md\n",
        encoding="utf-8",
    )
    report = pos.validate_project(project)
    # entity_text() sertakan heading "Post Implementation Review" tapi tanpa
    # isi substantif -- tapi karena stringnya ada, warning ini seharusnya
    # TIDAK muncul (heuristik cuma cek keberadaan string).
    assert not any("Post Implementation Review" in w.message for w in _warns(report) if "done.md" in w.file)


def test_backlog_checked_without_moved_to_warns(project):
    backlog_dir = project / "00-backlog"
    backlog_dir.mkdir()
    (backlog_dir / "backlog-features.md").write_text(
        "# Backlog\n\n- [x] TEMP-99 — sudah dikerjakan tapi lupa ditandai pindah\n",
        encoding="utf-8",
    )
    report = pos.validate_project(project)
    assert any("moved to" in w.message for w in _warns(report))


def test_nonexistent_project_path_is_error(tmp_path):
    ghost = tmp_path / "not-here"
    report = pos.validate_project(ghost)
    assert _errors(report)

