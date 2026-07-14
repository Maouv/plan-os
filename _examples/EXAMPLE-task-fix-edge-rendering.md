---
id: TASK-0061
type: task
status: in-progress
owner: Maou
created: 2026-07-13
updated: 2026-07-14
depends_on: [FEAT-0006]
related: [BUG-0012]
---

# Fix edge rendering (imports, function calls, circular dependencies)

> **Summary Block:** Pastikan SVG edge overlay tergambar benar untuk ketiga jenis edge di DOM tree-view renderer, dan posisinya tetap sinkron saat card di-expand/collapse/scroll.

## Definition of Ready
- [x] Requirement jelas (lihat FEAT-0006 § 1)
- [x] Dependency teridentifikasi (renderer file-card harus render lebih dulu)
- [x] Owner ditetapkan

## Deskripsi Kerja
Implementasi ulang logic penggambaran edge: baca posisi tiap file-card lewat `getBoundingClientRect()`, gambar garis SVG sesuai jenis edge (solid untuk import, dashed untuk call, warna khusus untuk circular dependency), dan re-render ulang saat ada perubahan layout (expand/collapse/scroll/resize).

## Checklist Eksekusi
- [x] Render file node sebagai rectangle card (bukan list row).
- [x] Edge import (garis solid).
- [x] Edge function call (garis dashed).
- [ ] Edge circular dependency (highlight warna khusus).
- [ ] Re-calculate posisi edge saat scroll/resize.

## Mandatory Review Section
_(Lightweight Mode — task turunan langsung dari feature, review penuh ada di FEAT-0006)_
- Risiko utama: edge circular dependency belum ter-highlight beda, berpotensi membingungkan user membedakan dengan edge biasa.

## Definition of Done
- [ ] Seluruh checklist eksekusi selesai
- [ ] Mandatory Review Section terisi
- [ ] Metadata `status: done` diperbarui
