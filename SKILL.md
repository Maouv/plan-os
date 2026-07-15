---
name: plan-os
description: Use this skill whenever the user is working inside a Plan-OS project — creating or updating a project/feature/task/bugfix file, capturing backlog items, running `pos.py validate`/`new-id`/`depgraph`, closing out work, or asking about Plan-OS structure, lifecycle, or Mandatory Rules. Trigger on mentions of "Plan-OS", "planning-os", `pos.py`, project scaffolds under `projects/<slug>/`, Decision Log, Mandatory Review Section, or requests to add a feature/task/bug/refactor/enhancement to an existing project. Always run `pos.py validate` (and `depgraph` if `depends_on` was touched) after creating or editing any entity file — never hand-wave completion without it.
---

# Plan-OS

Plan-OS is a spec-driven planning system: every unit of work (project, feature,
task, bug fix, enhancement, refactor) is a single Markdown file with a strict
metadata header, a Summary Block, and a Mandatory Review Section. `pos.py` is
the zero-dependency enforcer CLI that catches violations of these rules
automatically instead of relying on manual discipline.

**Golden rule:** never tell the user something is "done" or "validated" for a
Plan-OS entity without actually running `pos.py validate` (and reading the
output) first. The whole point of this skill is to stop false confidence.

## 1. Know the source of truth

The kernel docs are the spec; do not improvise structure from memory. Read the
relevant one before doing anything non-trivial:

| Doc | Covers |
|---|---|
| `00-INDEX.md` | Entry point, quick-start routing |
| `01-RESEARCH-AND-ARCHITECTURE-DECISION.md` | Why the system is designed this way (ADR-001: file size limits, etc.) |
| `02-VOCABULARY-AND-FRAMEWORKS.md` | SWOT/PESTLE/JTBD/RICE/WBS/RACI — which framework applies at which stage |
| `03-LIFECYCLE-AND-REVIEW-SYSTEM.md` | The 27-stage lifecycle + the 14-section Mandatory Review Section (verbatim heading names) |
| `04-KNOWLEDGE-ARCHITECTURE-AND-CONTEXT-ENGINEERING.md` | Folder/file layout, naming, metadata schema, cross-referencing rules |
| `05-SOP-GOVERNANCE-MAINTENANCE.md` | Step-by-step SOPs (new project, add feature, handle bug, close entity) + the non-negotiable Mandatory Rules |
| `06-SELF-AUDIT.md` | Revision history of the kernel itself |
| `templates/*.md` | Copy-paste starting point for every entity type |
| `_examples/*.md` | Fully filled-out reference examples |

If a doc and `pos.py`'s actual behavior disagree, treat that as a bug to flag
(see §6), not something to silently work around.

## 2. Project scaffold (04 §4.2)

```
projects/<project-slug>/
├── 00-INDEX.md                 ← index & status (SSoT for project status)
├── 00-backlog/                 ← capture layer, split by intent
│   ├── 00-INDEX.md
│   ├── backlog-features.md
│   ├── backlog-refactor-enhancement.md
│   └── backlog-bugs.md
├── 01-discovery/
├── 02-requirement/
├── 03-planning/
├── 04-design-architecture/
├── 05-features/                ← 00-INDEX.md + feature-<id>-<slug>.md
├── 06-tasks/                   ← 00-INDEX.md + task-<id>-<slug>.md
├── 07-bugs-and-fixes/          ← 00-INDEX.md + bug-<id>-<slug>.md
├── 08-refactor-and-enhancement/← 00-INDEX.md + <ref|enh>-<id>-<slug>.md
├── 09-decision-log.md          ← canonical filename, single SSoT for decisions
├── 10-review-and-retro/
└── 99-archive/                 ← archived (never deleted) entities
```

There is also usually a **master plan / project file** directly at the project
root (built from `templates/TEMPLATE-project.md`, metadata `type: project`,
`id: PROJ-XXXX`) — this is a real entity and must be validated like any other,
not treated as free-form prose.

Rule of thumb: any folder with more than 3 files needs its own `00-INDEX.md`.

## 3. Metadata header (04 §4.3) — required on every entity file

```yaml
---
id: FEAT-0042
type: feature        # project | feature | task | bugfix | enhancement | refactor | migration | backlog-item
status: in-progress   # idea | discovery | backlog | ready | planning | in-progress | review | reported | investigating | done | archived
owner: <name>
created: 2026-07-14
updated: 2026-07-14
depends_on: [FEAT-0031]
related: [TASK-0102, TASK-0103]
---
```

Every entity also needs a `> **Summary Block:**` line right under the H1 title.

## 4. ID prefixes (allocate with `pos.py new-id`, never hand-roll)

| Prefix | Type |
|---|---|
| `PROJ` | project |
| `FEAT` | feature |
| `TASK` | task |
| `BUG` | bugfix |
| `ENH` | enhancement |
| `REF` | refactor |
| `MIG` | migration |
| `BKLG` | backlog-item |

## 5. The 14 Mandatory Review Section headings (03 §3.2)

Every feature/task/bugfix/enhancement/refactor — and the project master plan —
must contain these headings verbatim (copy from
`templates/TEMPLATE-review-checklist.md`). Content can be condensed to
`Not Applicable — <short reason>` for small work, but **the heading itself
must never be deleted**:

```
Potential Bugs, Known Risks, Edge Cases, Failure Cases, Negative Test Cases,
Regression Risk, Rollback Plan, Validation Checklist, Review Checklist,
Acceptance Checklist, User Testing Result, Post Implementation Review,
Lessons Learned, Future Improvement
```

`pos.py validate` enforces all 14 as hard errors if any are missing.

## 6. Using `pos.py` — do this after every entity change

```bash
# Validate one project instance
python3 pos.py validate projects/<slug>
python3 pos.py validate projects/<slug> --stale-days 14        # flag stale active entities
python3 pos.py validate projects/<slug> --full-instance         # also require full 04 §4.2 scaffold

# Allocate the next ID for a type (PROJ/FEAT/TASK/BUG/ENH/REF/MIG/BKLG)
python3 pos.py new-id projects/<slug> FEAT
python3 pos.py new-id projects/<slug> FEAT --claim              # reserve it in .pos-id-ledger.json

# Dependency graph: circular-dependency check + safe processing order
python3 pos.py depgraph projects/<slug>
python3 pos.py depgraph projects/<slug> --allow-empty           # OK for a brand-new project with 0 entities
```

Exit code is `1` if there's anything to fix — treat non-zero as "not done yet,"
not as noise. `validate` always prints a scope line first
(`N discovered / M checked / K skipped`) — read it. If "checked" looks
suspiciously low relative to how many entity files you expect, something is
being skipped and needs investigating before you trust a clean report.

`depgraph` on a project with zero entities now fails by default (not a silent
`exit 0`) — pass `--allow-empty` only when the project genuinely hasn't
started yet.

## 7. Standard workflows (05 SOPs)

- **New project**: scaffold per §2, `status: idea` in root `00-INDEX.md`, run
  Discovery cluster before writing final requirements.
- **New feature**: copy `TEMPLATE-feature.md` → `05-features/feature-<id>-<slug>.md`,
  fill metadata + Summary Block, register one line in `05-features/00-INDEX.md`,
  `new-id FEAT --claim` for the ID, run the full lifecycle including all 14
  Mandatory Review Section items.
- **New bug**: copy `TEMPLATE-bugfix-enhancement-refactor.md` →
  `07-bugs-and-fixes/bug-<id>-<slug>.md`. Root Cause Analysis is mandatory
  *before* proposing a fix. Regression Risk and Rollback Plan must be filled
  before deployment.
- **Bulk requests** ("add 10 features"): split by intent first (feature vs
  refactor/enhancement vs bug) into the matching `00-backlog/backlog-*.md`
  file — bulk capture is fine here. Processing from backlog into a full
  entity (Requirement → Implementation → Mandatory Review) must happen
  **one at a time, in dependency order** — never bulk-process. If intent is
  ambiguous or requests contradict each other, stop and ask the user before
  filing anything.
- **Closing an entity**: all 14 Mandatory Review Section items filled →
  Post Implementation Review + Lessons Learned written → `status: done` →
  after the retention window, move the file to `99-archive/` and set
  `status: archived` (never delete it).
- **Changing the Plan-OS kernel itself** (`00`–`06` at repo root): this goes
  through Governance (§5.3 of `05-SOP-GOVERNANCE-MAINTENANCE.md`), not a
  direct one-off edit.

## 8. Non-negotiable Mandatory Rules (05 §5.2) — quick checklist

- No entity reaches `status: done` without all 14 Mandatory Review Section items filled.
- No fact is defined in more than one file — cross-reference with links + IDs, never copy-paste content.
- Any folder with >3 files needs its own `00-INDEX.md`.
- Every detail file has a metadata header + Summary Block.
- Real decisions go in the Decision Log (`09-decision-log.md`), not just in chat.
- Nothing is ever deleted — only archived to `99-archive/`.
- Kernel docs are governance-only, not freely editable.
- Backlog stays split by intent (feature / refactor-enhancement / bug), never mixed in one list.
- Ambiguous or contradictory bulk requests get a clarifying question, not a guess.

## 9. Known gaps — be honest about them, don't paper over

`pos.py` in this repo has been patched for the issues logged in
`issue/plan-os-tooling-and-spec-friction.md`, but one thing remains
**intentionally unenforced**: the 27 lifecycle-stage headings from
`03-LIFECYCLE-AND-REVIEW-SYSTEM.md` §3.1 are not checked as hard errors,
because the current templates (project/feature/task/bugfix) don't define
matching headings uniformly per entity type — enforcing it literally would
false-positive on legitimate small tasks/bugfixes. `validate` prints this as
an explicit coverage warning rather than pretending it's covered. If you're
asked to "fully enforce the lifecycle," the honest answer is that the
templates need a redesign first — don't just silence the warning in the
validator.

If you find another mismatch between what a doc claims and what `pos.py`
actually checks, say so plainly rather than assuming the doc or the code is
automatically right.

