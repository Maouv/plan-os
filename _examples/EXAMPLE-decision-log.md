# Decision Log — graps

> **Summary Block:** SSoT seluruh keputusan penting project graps. Entri baru ditambah di atas (paling baru paling atas).

---

### DEC-0002: Ganti renderer Canvas/force-graph ke DOM tree-view + SVG overlay
- **Tanggal:** 2026-07-08
- **Diputuskan oleh:** Maou
- **Konteks/Masalah:** Canvas/force-graph renderer sulit di-debug, tidak accessible, dan posisi node susah dikontrol untuk struktur folder yang hierarkis.
- **Opsi yang dipertimbangkan:** (1) Tetap di Canvas dengan perbaikan incremental, (2) Pindah ke DOM tree-view + SVG edge overlay, (3) Pindah ke library graph pihak ketiga.
- **Keputusan:** Pindah ke DOM tree-view + SVG edge overlay (opsi 2).
- **Alasan:** DOM lebih mudah di-debug lewat browser devtools, native accessible, dan struktur tree cocok dengan sifat hierarkis file/folder dibanding force-graph yang free-form.
- **Dampak/Konsekuensi:** Seluruh renderer lama (Canvas/force-graph) di-deprecate; perlu migrasi ulang logic edge rendering (lihat FEAT-0006, BUG-0012).
- **Terkait:** FEAT-0006, TASK-0061, BUG-0012

---

### DEC-0001: Selesaikan mypy error di backend sebelum lanjut ke Phase 6
- **Tanggal:** 2026-07-01
- **Diputuskan oleh:** Maou
- **Konteks/Masalah:** 46 mypy error tersebar di 8 file backend berpotensi menyembunyikan bug tipe data saat frontend baru mulai konsumsi API graph.
- **Opsi yang dipertimbangkan:** (1) Perbaiki mypy error dulu sebelum Phase 6, (2) Jalankan paralel dengan Phase 6.
- **Keputusan:** Perbaiki dulu (opsi 1), sequential bukan paralel.
- **Alasan:** Renderer baru bergantung pada bentuk data graph yang konsisten; lebih murah memperbaiki tipe data di backend sebelum frontend mulai bergantung padanya.
- **Dampak/Konsekuensi:** Phase 6 mulai 1 minggu lebih lambat, tapi backend jadi lebih stabil sebagai fondasi.
- **Terkait:** PROJ-0001

---
