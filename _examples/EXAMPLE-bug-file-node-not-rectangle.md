---
id: BUG-0012
type: bugfix
status: in-progress
owner: Maou
created: 2026-07-14
updated: 2026-07-14
depends_on: []
related: [FEAT-0006, TASK-0061]
---

# File nodes render as plain list rows instead of rectangle cards

> **Summary Block:** Setelah migrasi ke DOM tree-view, file node sempat tampil sebagai baris list polos, bukan rectangle card sesuai FR-001 di FEAT-0006. Berdampak ke seluruh user yang membuka UI graps karena visual hierarchy jadi tidak jelas.

## 1. Deskripsi Masalah / Tujuan Perubahan
File-card component tidak menerapkan style card (border, padding, header/body) — hasil render terlihat seperti `<li>` polos tanpa struktur visual, sehingga sulit membedakan antar file dan edge overlay jadi salah posisi karena bounding box row lebih tipis dari yang diasumsikan SVG layer.

## 2. Root Cause Analysis
Komponen file-card memakai class CSS lama peninggalan list-row renderer sebelumnya (belum di-refactor penuh saat migrasi Phase 6 dimulai). Karena bounding box row lebih tipis dari card yang diharapkan, kalkulasi posisi edge SVG (yang bergantung pada `getBoundingClientRect()` dari card) ikut salah.

## 3. Proposed Fix / Change
Refactor file-card component agar memakai struktur card penuh (wrapper dengan border + header + body), lalu re-run kalkulasi posisi edge setelah style baru diterapkan agar SVG overlay ikut align ulang.

## 4. Scope & Impact
- Komponen terdampak: file-card component, SVG edge overlay (karena bergantung pada dimensi card).
- Blast Radius: seluruh tampilan graph di UI graps — semua user terdampak sampai fix di-deploy.

## 5. Mandatory Review Section
### Potential Bugs
- Edge overlay bisa telat re-align jika kalkulasi posisi dijalankan sebelum CSS baru selesai di-apply browser.

### Known Risks
- Perubahan dimensi card mengubah total tinggi tree, berpotensi geser scroll position user.

### Edge Cases
- File dengan nama sangat panjang bisa membuat card melebar tidak proporsional.

### Failure Cases
- Jika card belum ter-mount saat edge dihitung, posisi edge jadi (0,0).

### Negative Test Cases
- Tree kosong tidak boleh menyebabkan error saat kalkulasi posisi.

### Regression Risk
- Perlu re-test fitur risk-flag lama yang bergantung pada layout list-row.

### Rollback Plan
- Revert ke class CSS list-row lama sambil menonaktifkan sementara SVG edge overlay via feature flag.

### Validation Checklist
- [ ] Card tampil dengan border dan header di semua browser yang didukung.
- [ ] Edge overlay align dengan card setelah fix.

### Review Checklist
- [ ] Self Review
- [ ] AI Review
- [ ] Code Review
- [ ] Security Review
- [ ] Performance Review
- [ ] Compatibility Review

### Acceptance Checklist
- [ ] FR-001 di FEAT-0006 terpenuhi (card, bukan list row).

### User Testing Result
_(belum dilakukan)_

### Post Implementation Review
_(diisi setelah fix di-deploy)_

### Lessons Learned
_(diisi setelah fix di-deploy)_

### Future Improvement
_(diisi setelah fix di-deploy)_

## 6. Closing
### Post Implementation Review
_(belum diisi — masih in-progress)_

### Lessons Learned
_(belum diisi)_

### Future Improvement
_(belum diisi)_
