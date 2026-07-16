"""Tests untuk fitur baru ENH-0001: `pos.py --version` + pyproject.toml sebagai SSoT."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pos

POS_PY = Path(pos.__file__).resolve()
REPO_ROOT = POS_PY.parent


def test_get_version_reads_pyproject_toml_next_to_pos_py():
    version = pos.get_version()
    pyproject_text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert f'version = "{version}"' in pyproject_text


def test_get_version_falls_back_when_pyproject_missing(tmp_path, monkeypatch):
    # Simulasikan pos.py berdiri sendiri tanpa pyproject.toml di sekitarnya
    # (mis. skenario copy-paste manual) -> tidak boleh crash, harus fallback.
    fake_pos = tmp_path / "isolated" / "pos.py"
    fake_pos.parent.mkdir()
    fake_pos.write_text(POS_PY.read_text(encoding="utf-8"), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(fake_pos), "--version"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert pos._VERSION_FALLBACK in result.stdout


def test_cli_version_flag_matches_get_version():
    result = subprocess.run(
        [sys.executable, str(POS_PY), "--version"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert pos.get_version() in result.stdout


def test_version_lookup_also_checks_parent_dir_for_future_tools_layout(tmp_path):
    # Regression-guard yang disengaja untuk TEMP-05 (root repo reorg): kalau
    # nanti pos.py pindah ke tools/pos.py, get_version() harus tetap ketemu
    # pyproject.toml di root repo (satu level di atas tools/).
    fake_root = tmp_path / "future-layout"
    tools_dir = fake_root / "tools"
    tools_dir.mkdir(parents=True)
    (fake_root / "pyproject.toml").write_text('version = "9.9.9"\n', encoding="utf-8")
    fake_pos = tools_dir / "pos.py"
    fake_pos.write_text(POS_PY.read_text(encoding="utf-8"), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(fake_pos), "--version"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "9.9.9" in result.stdout

