---
id: PROJ-0001
type: project
status: in-progress
owner: Maou
created: 2026-06-20
updated: 2026-07-14
depends_on: []
related: [FEAT-0006, TASK-0061, BUG-0012]
---

# graps — Code Dependency Visualization & Analysis Tool

> **Summary Block:** Tool untuk memvisualisasikan dan menganalisis dependency graph dari codebase (Python backend + web frontend). Target user: developer yang butuh memahami struktur import, function call, dan circular dependency di project besar. Definition of Done level project: renderer DOM tree-view stabil menggantikan Canvas/force-graph, backend Python bebas mypy error, dan CLI bisa dipakai end-to-end tanpa crash.

## 1. Discovery
### 1.1 Idea
Codebase besar sering sulit dipahami strukturnya hanya dari baca kode manual. graps mem-parse AST Python, membangun graph dependency, dan menyajikannya secara visual agar developer bisa cepat identifikasi circular dependency, coupling tinggi, dan risk area.

### 1.2 Research
Force-graph/Canvas renderer (versi awal) sulit di-debug dan tidak accessible (tidak ada DOM element yang bisa di-inspect). Riset internal (lihat DEC-0002 di decision log) memutuskan pindah ke DOM tree-view + SVG edge overlay.

### 1.3 Analysis
_(SWOT ringkas)_
- Strength: parsing AST sudah solid, cache layer ada.
- Weakness: renderer lama sulit di-maintain.
- Opportunity: DOM-based renderer buka jalan untuk fitur filter/search native browser.
- Threat: migrasi renderer berisiko regresi pada edge rendering (imports, function calls, circular deps).

## 2. Requirement
### 2.1 Functional Requirements
- FR-001: Setiap file node dirender sebagai rectangle card (bukan list row).
- FR-002: Edge (import, function call, circular dependency) digambar sebagai SVG overlay yang mengikuti posisi card.
- FR-003: CLI dan backend bebas error mypy sebelum rilis.

### 2.2 Non-Functional Requirements
- NFR-001: Rendering tetap responsif untuk graph dengan >200 file node.

### 2.3 Constraints & Assumptions
- Constraint: tidak boleh regresi fitur risk-flag yang sudah ada di Canvas renderer lama.
- Assumption: mayoritas project yang dianalisis berukuran menengah (<500 file).

## 3. Planning
### 3.1 Work Breakdown Structure (WBS)
```
1. Phase 5 — Backend hardening (mypy fixes, resolver, graph_builder)
2. Phase 6 — DOM tree-view renderer
   6.1 File-card component
   6.2 SVG edge overlay (imports, calls, circular deps)
   6.3 Layout & positioning
3. Phase 7 — Filter/search di atas DOM renderer
```

### 3.2 Timeline
| Phase | Mulai | Selesai | Milestone |
|---|---|---|---|
| Phase 5 | 2026-07-01 | 2026-07-08 | 0 mypy error |
| Phase 6 | 2026-07-09 | in-progress | Edge rendering stabil |

### 3.3 RACI
| Deliverable | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| DOM renderer | Maou | Maou | — | — |

## 4. Design & Architecture
### 4.1 Design
File node = card dengan header (nama file) + body (ringkas metrik: jumlah import, jumlah fungsi).

### 4.2 Architecture
Frontend: tree-view DOM untuk node, layer SVG terpisah di-absolute-position di atasnya untuk edge. Backend: AST parser → graph builder → JSON graph → di-render frontend.

## 5. Features
> Daftar Feature ada di `05-features/00-INDEX.md` pada instance project sungguhan. Contoh 1 feature: `EXAMPLE-feature-dom-tree-renderer.md`.

## 6. Risks & Dependencies
| Risk/Dependency | Tipe | Mitigasi | Owner |
|---|---|---|---|
| Circular dependency edge salah gambar | Risk | Test khusus graph dengan circular import | Maou |
| Card overlap saat file banyak | Risk | Layout algorithm dengan collision detection | Maou |

---

## 7. Mandatory Review Section
_(lihat `EXAMPLE-bug-file-node-not-rectangle.md` untuk contoh Mandatory Review Section terisi penuh pada level task/bug)_

## 8. Decision Log
> Ringkasan; detail penuh di `EXAMPLE-decision-log.md`.
- DEC-0001: Pilih hybrid index/detail folder structure untuk Planning-OS itu sendiri.
- DEC-0002: Ganti renderer Canvas/force-graph → DOM tree-view + SVG overlay.

## 9. Closing
### 9.1 Post Implementation Review
_(diisi setelah Phase 6 selesai)_

### 9.2 Lessons Learned
_(diisi setelah Phase 6 selesai)_

### 9.3 Status Akhir
in-progress — Phase 6 sedang berjalan, fokus saat ini di edge rendering dan file-card sebagai rectangle.
