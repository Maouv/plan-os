---
id: BUG-0012
type: bugfix
status: in-progress
owner: Maou
created: 2026-07-14
updated: 2026-07-14
depends_on: []
related: [FEAT-0006, TASK-0061]
lifecycle_ref: 03-LIFECYCLE-AND-REVIEW-SYSTEM.md § 3.1
---

# Lifecycle Log — BUG-0012: File nodes render as plain list rows instead of rectangle cards

> **Summary Block:** Contoh log eksplisit ke-27 tahap Implementation Lifecycle (lihat `03-LIFECYCLE-AND-REVIEW-SYSTEM.md` § 3.1) untuk satu entitas kerja yang sama seperti `EXAMPLE-bug-file-node-not-rectangle.md`. File ini BUKAN pengganti dokumen bugfix utama — ini contoh format log tahap-per-tahap untuk kasus butuh audit trail lifecycle secara eksplisit (misal: compliance, post-mortem besar). Untuk kerja harian, cukup pakai `TEMPLATE-bugfix-enhancement-refactor.md` + tandai "Not Applicable" di tahap yang tidak relevan, sesuai § 3.1 aturan.

---

## Klaster 1 — Discovery

**1. Idea**
Ditemukan saat testing manual Phase 6: file node tampil seperti baris list polos, bukan card.

**2. Research**
Cek commit history renderer — file-card component masih memakai class CSS peninggalan list-row renderer versi lama, belum sempat di-refactor saat migrasi dimulai.

**3. Analysis**
Root cause bukan di logic render, tapi di CSS class yang salah diwariskan. Dampak menjalar ke SVG edge overlay karena bounding box row lebih tipis dari card yang diharapkan.

**4. Requirement**
FR-001 di `FEAT-0006` harus terpenuhi: file node = rectangle card dengan border + header + body.

## Klaster 2 — Planning & Design

**5. Planning**
Scope kecil, 1 file component + re-align kalkulasi posisi edge. Tidak perlu WBS terpisah, cukup masuk sebagai 1 task di bawah `TASK-0061`.

**6. Design**
Card: wrapper dengan border, header berisi nama file, body berisi ringkas metrik (jumlah import/fungsi).

**7. Architecture**
Tidak ada perubahan API/data model — murni perubahan presentational component di frontend. Kalkulasi posisi edge tetap pakai `getBoundingClientRect()`, hanya dijalankan ulang setelah style card baru diterapkan.

## Klaster 3 — Build

**8. Implementation**
Refactor file-card component: ganti class CSS list-row → class CSS card penuh. Tambahkan re-calculate posisi edge setelah render card selesai.

**9. Self Review**
Dicek manual: card tampil dengan border, edge overlay align — untuk kasus dependency import dan function call. Circular dependency highlight belum dicek (lihat § Klaster 4).

**10. AI Review**
Diagnosa pola: perubahan dimensi elemen yang jadi anchor SVG overlay berisiko tinggi menimbulkan race condition kalau kalkulasi posisi dijalankan sebelum browser selesai apply CSS — dicatat sebagai Known Risk.

**11. Code Review**
_(Not Applicable — single-owner project, tidak ada reviewer kedua saat ini)_

## Klaster 4 — Verification

**12. Testing**
Manual test: render graph kecil (5 file) dan graph besar (>200 file), cek card tampil benar di keduanya.

**13. QA**
Cross-check terhadap FR-001 s.d. FR-004 di `FEAT-0006` — FR-001 s.d. FR-003 lolos, FR-004 (circular dependency highlight) masih pending, dicatat sebagai open item di `TASK-0061`.

**14. Potential Bug Review**
Edge overlay berpotensi telat re-align jika card belum selesai mount — lihat Mandatory Review Section di `EXAMPLE-bug-file-node-not-rectangle.md`.

**15. Edge Case Review**
File dengan nama sangat panjang membuat card melebar tidak proporsional — belum ada fix, dicatat sebagai Future Improvement.

**16. Negative Scenario Review**
Tree kosong (0 file) diuji, tidak menyebabkan error saat kalkulasi posisi edge.

**17. Security Review**
_(Not Applicable — perubahan murni presentational, tidak menyentuh data/auth/network)_

**18. Performance Review**
Re-calculate posisi edge saat resize/scroll berpotensi jadi bottleneck kalau graph besar — belum di-profile, dicatat sebagai risiko terbuka.

**19. Compatibility Review**
Diuji di 1 browser (Chrome) saja sejauh ini — Firefox/Safari belum, dicatat sebagai Validation Checklist item yang belum tercentang.

## Klaster 5 — Validation dengan User

**20. User Testing**
_(Belum dilakukan — owner project adalah user tunggal saat ini, self-testing dianggap representative untuk tahap ini)_

**21. User Feedback**
_(Belum dilakukan, menyusul setelah FR-004 selesai)_

**22. Revision**
Belum ada revisi berdasarkan feedback eksternal karena tahap 20–21 belum berjalan.

## Klaster 6 — Release & Closing

**23. Deployment**
_(Belum deploy — masih di local development, menunggu FR-004 selesai sebelum dianggap 1 batch rilis)_

**24. Monitoring**
_(Not Applicable saat ini — belum ada environment production untuk graps)_

**25. Post Implementation Review (PIR)**
_(Belum diisi — bug ini masih berstatus in-progress)_

**26. Lessons Learned**
Sementara: migrasi renderer sebaiknya audit semua class CSS lama di awal Phase 6, bukan ditemukan belakangan lewat bug seperti ini.

**27. Continuous Improvement / Archive**
Status: **in-progress**, belum diarsipkan. Akan di-review ulang setelah `TASK-0061` checklist edge circular dependency selesai.

---

> Tahap yang ditandai *Not Applicable* tetap mempertahankan heading-nya sesuai aturan § 3.1 — bukan dihapus, supaya jelas bahwa tahap tersebut memang dipertimbangkan dan sengaja dilewati, bukan lupa dikerjakan.
