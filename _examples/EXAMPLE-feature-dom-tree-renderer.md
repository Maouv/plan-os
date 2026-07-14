---
id: FEAT-0006
type: feature
status: in-progress
owner: Maou
created: 2026-07-09
updated: 2026-07-14
depends_on: []
related: [PROJ-0001, TASK-0061, BUG-0012]
---

# DOM Tree-View Renderer (Phase 6)

> **Summary Block:** Mengganti Canvas/force-graph renderer graps dengan DOM tree-view: file node sebagai rectangle card, edge (import/call/circular) sebagai SVG overlay. Dipakai oleh developer yang membuka UI graps untuk eksplorasi dependency graph.

## 1. Requirement & Acceptance Criteria
### Functional Requirements
- FR-001: File node dirender sebagai rectangle card, bukan plain list row.
- FR-002: Edge import digambar sebagai garis solid.
- FR-003: Edge function call digambar sebagai garis putus-putus.
- FR-004: Circular dependency di-highlight warna berbeda.

### Acceptance Criteria
- [ ] Semua file node tampil sebagai card dengan border dan header.
- [ ] Edge tetap mengikuti posisi card saat tree di-expand/collapse.
- [ ] Circular dependency edge terlihat jelas beda dari edge biasa.

## 2. Design
Card tersusun mengikuti struktur folder (tree), bukan free-form layout seperti force-graph lama. SVG overlay ditempatkan di layer terpisah dengan posisi dihitung ulang tiap kali tree berubah (expand/collapse/scroll).

## 3. Architecture / Technical Notes
Komponen terdampak: `renderer/` (frontend), tidak menyentuh `ast_parser.py`/`graph_builder.py` di backend karena struktur JSON graph tidak berubah. Posisi card dihitung lewat `getBoundingClientRect()` lalu edge di-redraw memakai koordinat tersebut.

## 4. Prioritization
- Impact: Tinggi — renderer lama sudah deprecated.
- Effort: Medium.
- RICE/ICE Score (opsional): —

## 5. Implementation Notes
Edge overlay harus recalculate posisi setiap resize/scroll event, bukan hanya sekali saat render awal — ini akar masalah di `BUG-0012` (lihat contoh bugfix).

## 6. Mandatory Review Section
### Potential Bugs
- Edge tidak ikut update posisi saat card di-collapse.

### Known Risks
- Circular dependency dengan banyak node bisa membuat edge saling tumpang tindih secara visual.

### Edge Cases
- File tanpa import/call sama sekali (node terisolasi).
- Circular dependency melibatkan >2 file (A→B→C→A).

### Failure Cases
- SVG overlay gagal render jika container belum selesai mount (race condition).

### Negative Test Cases
- Graph kosong (0 file) tidak boleh crash renderer.

### Regression Risk
- Fitur risk-flag dari Canvas renderer lama harus tetap tampil setelah migrasi.

### Rollback Plan
- Toggle feature flag untuk kembali ke Canvas renderer lama jika DOM renderer bermasalah di production.

### Validation Checklist
- [ ] Test dengan graph >200 file node.
- [ ] Test dengan circular dependency.

### Review Checklist
- [ ] Self Review
- [ ] AI Review
- [ ] Code Review
- [ ] Security Review
- [ ] Performance Review
- [ ] Compatibility Review

### Acceptance Checklist
- [ ] Semua Acceptance Criteria di § 1 terpenuhi.

### User Testing Result
_(diisi setelah testing manual oleh Maou)_

### Post Implementation Review
_(diisi setelah feature selesai)_

### Lessons Learned
_(diisi setelah feature selesai)_

### Future Improvement
_(diisi setelah feature selesai)_

## 7. Closing
### Post Implementation Review
_(belum diisi — feature masih in-progress)_

### Lessons Learned
_(belum diisi)_

### Future Improvement
_(belum diisi)_
