# 03 — Implementation Lifecycle & Mandatory Review System

> **Summary Block:** Setiap entitas kerja (Project/Feature/Task/Bug Fix/Enhancement/Refactor) **wajib** melalui 27 tahap lifecycle di bawah — tidak boleh loncat dari "Implementation" langsung ke "selesai". Bagian kedua mendefinisikan Mandatory Review Section yang wajib ada di setiap dokumen kerja, tanpa terkecuali.

---

## 3.1 Implementation Lifecycle (Wajib, 27 Tahap)

Tahap dikelompokkan menjadi 6 klaster agar mudah dipetakan ke framework di `02`.

### Klaster 1 — Discovery
1. **Idea** — pencatatan gagasan awal, belum tervalidasi.
2. **Research** — pengumpulan data pendukung (user, teknis, kompetitor).
3. **Analysis** — mengolah riset jadi insight (pakai SWOT/PESTLE/JTBD sesuai konteks).
4. **Requirement** — merumuskan Functional & Non-Functional Requirement + Acceptance Criteria.

### Klaster 2 — Planning & Design
5. **Planning** — WBS, timeline, resource, dependency, RACI.
6. **Design** — solusi pada level user/produk (UX flow, API contract level konsep).
7. **Architecture** — solusi pada level sistem/teknis (komponen, data model, integrasi).

### Klaster 3 — Build
8. **Implementation** — proses coding/eksekusi teknis sesungguhnya.
9. **Self Review** — pelaksana memeriksa hasil kerjanya sendiri terhadap Acceptance Criteria.
10. **AI Review** — pemeriksaan otomatis/AI-assisted terhadap kode/dokumen (pattern, konsistensi, potensi bug).
11. **Code Review** — pemeriksaan oleh manusia lain (peer review).

### Klaster 4 — Verification (lihat juga § 3.2 Mandatory Review Section)
12. **Testing** — eksekusi test (unit/integration/e2e sesuai konteks).
13. **QA** — quality assurance menyeluruh terhadap requirement.
14. **Potential Bug Review** — telaah eksplisit kemungkinan bug yang belum kelihatan.
15. **Edge Case Review** — telaah skenario ekstrem/jarang.
16. **Negative Scenario Review** — telaah skenario input/kondisi salah.
17. **Security Review** — telaah celah keamanan.
18. **Performance Review** — telaah dampak performa/skalabilitas.
19. **Compatibility Review** — telaah kompatibilitas lintas environment/versi/platform.

### Klaster 5 — Validation dengan User
20. **User Testing** — pengujian oleh user/stakeholder nyata.
21. **User Feedback** — pengumpulan tanggapan.
22. **Revision** — perbaikan berdasarkan hasil klaster 4 & 5.

### Klaster 6 — Release & Closing
23. **Deployment** — perilisan ke environment target.
24. **Monitoring** — pengawasan pasca-rilis.
25. **Post Implementation Review (PIR)** — evaluasi formal apakah hasil sesuai tujuan awal.
26. **Lessons Learned** — insight terdokumentasi untuk dipakai ulang.
27. **Continuous Improvement / Archive** — tindak lanjut perbaikan berkelanjutan, atau pengarsipan jika entitas kerja sudah tidak aktif.

> **Aturan:** Tahap boleh disederhanakan (digabung dalam satu baris "Not Applicable — [alasan singkat]") untuk pekerjaan kecil, tapi **heading tahap tidak boleh dihapus**. Ini mencegah orang diam-diam melewati tahap penting hanya karena terburu-buru.

---

## 3.2 Mandatory Review Section (Wajib di SETIAP Feature/Task/Bug Fix/Refactor/Enhancement)

Tidak opsional. Ini bagian tetap dari `templates/` — lihat template terkait untuk formatnya siap pakai.

1. **Potential Bugs** — daftar dugaan bug yang mungkin muncul, meski belum terbukti.
2. **Known Risks** — risiko yang sudah diketahui sejak awal.
3. **Edge Cases** — daftar kondisi ekstrem yang harus ditangani.
4. **Failure Cases** — cara sistem gagal, dan apakah gagalnya "aman" (graceful) atau tidak.
5. **Negative Test Cases** — skenario uji dengan input/kondisi salah.
6. **Regression Risk** — bagian sistem lama yang berisiko rusak.
7. **Rollback Plan** — langkah konkret membatalkan perubahan bila gagal di production.
8. **Validation Checklist** — daftar cek "apakah kita membangun hal yang benar".
9. **Review Checklist** — daftar cek proses review sudah dilakukan (self/AI/code/security/dll).
10. **Acceptance Checklist** — daftar cek terhadap Acceptance Criteria awal.
11. **User Testing Result** — ringkasan hasil pengujian user (atau "Not Applicable" + alasan bila memang tak melibatkan user langsung).
12. **Post Implementation Review** — evaluasi setelah rilis: apakah tujuan tercapai, metrik bergerak sesuai harapan.
13. **Lessons Learned** — insight baru dari pengerjaan ini.
14. **Future Improvement** — hal yang sengaja ditunda/dicatat untuk iterasi berikutnya.

> **Aturan keras:** dokumen kerja yang tidak memiliki 14 sub-bagian ini dianggap **belum lengkap**, terlepas dari seberapa bagus kode/hasilnya. Untuk pekerjaan sangat kecil, tiap poin boleh diisi 1 baris "Tidak relevan — [alasan]", tapi heading-nya wajib tetap ada (prinsip sama dengan § 3.1).

---

## 3.3 Pemetaan Lifecycle → Framework (referensi cepat)

| Tahap Lifecycle | Framework yang Relevan |
|---|---|
| Research/Analysis | SWOT, PESTLE, JTBD |
| Requirement | MoSCoW |
| Planning | WBS, RACI, CPM |
| Design | Design Thinking, Double Diamond, User Story Mapping |
| Prioritas antar Feature (Backlog) | RICE, ICE |
| Implementation/eksekusi harian | Scrum atau Kanban (pilih salah satu per tim, jangan campur) |
| Continuous Improvement | PDCA, Six Sigma/DMAIC (untuk masalah kualitas berulang skala besar) |
| Strategy tahunan | Balanced Scorecard, OKR |

---

## 3.4 Definition of Ready vs Definition of Done (baku sistem ini)

**Definition of Ready** (sebelum Task boleh masuk Implementation):
- Requirement & Acceptance Criteria sudah ditulis.
- Dependency sudah teridentifikasi.
- Owner/PIC sudah ditetapkan.

**Definition of Done** (sebelum Task boleh ditutup):
- Seluruh 14 poin Mandatory Review Section (§ 3.2) terisi.
- Seluruh tahap klaster 3 & 4 di § 3.1 sudah dilalui (atau ditandai Not Applicable dengan alasan).
- Decision Log diperbarui jika ada keputusan penting selama pengerjaan.
