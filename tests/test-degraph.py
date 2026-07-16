"""Tests untuk `pos.py depgraph` (build_dep_graph / find_cycles / run_depgraph)."""
from __future__ import annotations

from conftest import entity_text

import pos


def test_empty_graph_without_allow_empty_fails(tmp_path):
    # Regression: issue #2 (High) — dulu graph kosong exit 0, disalahartikan
    # sebagai "graph tervalidasi dan bersih".
    root = tmp_path / "empty-project"
    root.mkdir()
    (root / "00-INDEX.md").write_text("# Empty\n", encoding="utf-8")
    exit_code = pos.run_depgraph(root, allow_empty=False)
    assert exit_code == 1


def test_empty_graph_with_allow_empty_succeeds(tmp_path):
    root = tmp_path / "empty-project"
    root.mkdir()
    (root / "00-INDEX.md").write_text("# Empty\n", encoding="utf-8")
    exit_code = pos.run_depgraph(root, allow_empty=True)
    assert exit_code == 0


def test_path_not_found_fails_with_failure_type(tmp_path):
    ghost = tmp_path / "not-here"
    graph, labels = pos.build_dep_graph(ghost)
    assert graph == {}


def test_circular_dependency_detected(project):
    a = project / "05-features" / "feature-0002-a.md"
    b = project / "05-features" / "feature-0003-b.md"
    a.write_text(entity_text(entity_id="FEAT-0002", depends_on="[FEAT-0003]"), encoding="utf-8")
    b.write_text(entity_text(entity_id="FEAT-0003", depends_on="[FEAT-0002]"), encoding="utf-8")
    graph, labels = pos.build_dep_graph(project)
    cycles = pos.find_cycles(graph)
    assert cycles, "circular dependency A<->B harus terdeteksi"


def test_no_cycle_gives_valid_topological_order(project):
    a = project / "05-features" / "feature-0002-a.md"
    b = project / "05-features" / "feature-0003-b.md"
    # b depends_on a -> urutan harus a sebelum b
    a.write_text(entity_text(entity_id="FEAT-0002"), encoding="utf-8")
    b.write_text(entity_text(entity_id="FEAT-0003", depends_on="[FEAT-0002]"), encoding="utf-8")
    graph, _ = pos.build_dep_graph(project)
    assert pos.find_cycles(graph) == []
    order = pos.topological_order(graph)
    assert order.index("FEAT-0002") < order.index("FEAT-0003")


def test_dangling_depends_on_is_treated_as_error(project):
    a = project / "05-features" / "feature-0002-a.md"
    a.write_text(entity_text(entity_id="FEAT-0002", depends_on="[FEAT-9999]"), encoding="utf-8")
    exit_code = pos.run_depgraph(project, allow_empty=False)
    # FEAT-9999 tidak punya file -> dangling ref -> exit 1 (konsisten dengan
    # broken-link check di validate, bukan exit 0 dengan warning lemah).
    assert exit_code == 1


def test_json_output_ok_true_for_clean_graph(project, capsys):
    b = project / "05-features" / "feature-0002-b.md"
    b.write_text(entity_text(entity_id="FEAT-0002", depends_on="[FEAT-0001]"), encoding="utf-8")
    exit_code = pos.run_depgraph(project, allow_empty=False, json_output=True)
    assert exit_code == 0
    out = capsys.readouterr().out
    import json
    payload = json.loads(out)
    assert payload["ok"] is True
    assert payload["failure_type"] is None


def test_json_output_failure_type_for_cycle(project, capsys):
    a = project / "05-features" / "feature-0002-a.md"
    b = project / "05-features" / "feature-0003-b.md"
    a.write_text(entity_text(entity_id="FEAT-0002", depends_on="[FEAT-0003]"), encoding="utf-8")
    b.write_text(entity_text(entity_id="FEAT-0003", depends_on="[FEAT-0002]"), encoding="utf-8")
    exit_code = pos.run_depgraph(project, allow_empty=False, json_output=True)
    assert exit_code == 1
    out = capsys.readouterr().out
    import json
    payload = json.loads(out)
    assert payload["failure_type"] == "cycle"

