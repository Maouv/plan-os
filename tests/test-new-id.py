"""Tests untuk `pos.py new-id` (allocator ID + ledger)."""
from __future__ import annotations

import json

import pytest

import pos


def test_new_id_skips_past_existing_feat_in_fixture(project):
    # project fixture sudah punya FEAT-0001 -> next harus 0002, bukan 0001.
    assert pos.new_id(project, "FEAT", claim=False) == "FEAT-0002"


def test_new_id_first_allocation_for_untouched_type_is_0001(project):
    # TASK belum pernah dipakai di fixture manapun -> mulai dari 0001.
    assert pos.new_id(project, "TASK", claim=False) == "TASK-0001"


def test_new_id_unknown_type_raises_systemexit(project):
    with pytest.raises(SystemExit):
        pos.new_id(project, "NOPE", claim=False)


def test_new_id_proj_prefix_is_supported(project):
    # Regression: issue #5 — PROJ dipakai di TEMPLATE-project.md tapi dulu
    # tidak ada di ID_PREFIXES allocator.
    assert pos.new_id(project, "PROJ", claim=False) == "PROJ-0001"


def test_new_id_without_claim_does_not_crash_on_nonexistent_path(tmp_path):
    ghost = tmp_path / "does-not-exist-yet"
    assert not ghost.exists()
    # new-id TANPA --claim harus tetap jalan (cuma menghitung, tidak menulis).
    result = pos.new_id(ghost, "FEAT", claim=False)
    assert result == "FEAT-0001"
    assert not ghost.exists()


def test_new_id_with_claim_fails_cleanly_on_nonexistent_path(tmp_path):
    # Regression test untuk issue #11 (High): dulu ini crash dengan
    # unhandled FileNotFoundError traceback. Sekarang wajib SystemExit
    # bersih, dan folder tidak boleh ter-create sebagai side effect.
    ghost = tmp_path / "does-not-exist-yet"
    with pytest.raises(SystemExit):
        pos.new_id(ghost, "FEAT", claim=True)
    assert not ghost.exists()


def test_new_id_claim_writes_ledger_and_increments(project):
    first = pos.new_id(project, "TASK", claim=True)
    assert first == "TASK-0001"
    ledger_path = project / pos.LEDGER_NAME
    assert ledger_path.exists()
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert ledger["TASK"] == 1

    second = pos.new_id(project, "TASK", claim=True)
    assert second == "TASK-0002"


def test_new_id_claim_respects_scanned_max_over_stale_ledger(project):
    # Kalau ledger ketinggalan (mis. manual edit file dengan id lebih tinggi
    # tanpa lewat --claim), allocator wajib pakai max(ledger, scanned) + 1 —
    # bukan cuma ledger — supaya tidak collision dengan id yang sudah ada.
    (project / pos.LEDGER_NAME).write_text(json.dumps({"FEAT": 1}), encoding="utf-8")
    # Tulis file dengan id FEAT-0005 langsung (tanpa lewat allocator).
    from conftest import entity_text
    (project / "05-features" / "feature-0005-manual.md").write_text(
        entity_text(entity_id="FEAT-0005"), encoding="utf-8"
    )
    assert pos.new_id(project, "FEAT", claim=False) == "FEAT-0006"

