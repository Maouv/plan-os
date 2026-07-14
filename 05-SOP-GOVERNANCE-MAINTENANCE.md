# 05 — SOP, Governance, Maintenance & Scalability Strategy

> **Summary Block:** Prosedur operasional standar untuk memakai Planning-OS sehari-hari, aturan wajib yang tidak bisa dilanggar, mekanisme governance untuk mengubah sistem ini sendiri, serta strategi pemeliharaan dan perluasan jangka panjang.

---

## 5.1 SOP — Standard Operating Procedure

### SOP-00: Bulk Capture ke Backlog (Wajib Dipisah per Intent)
1. Saat user memberi banyak permintaan sekaligus (mis. "aku mau nambah 10 fitur"), AI **wajib** memilah tiap item berdasarkan intent-nya lebih dulu: Feature / Refactor-Enhancement / Bug. Jangan asumsikan semua item berintent sama hanya karena diucapkan dalam satu pesan.
2. Tiap item dicatat sebagai 1 baris di file backlog yang sesuai intent-nya (`00-backlog/backlog-features.md`, `backlog-refactor-enhancement.md`, atau `backlog-bugs.md` — lihat `04` § 4.2a). Bulk di tahap ini diperbolehkan, karena belum masuk lifecycle dan belum ada Mandatory Review Section yang perlu diisi serius.
3. Jika dalam satu batch permintaan user ada item yang ambigu intent-nya, saling kontradiksi (mis. "ganti total arsitektur X" sekaligus "jangan ubah struktur X sama sekali"), atau item yang requirement-nya belum jelas — AI **wajib berhenti dan konfirmasi ke user** sebelum mencatatnya ke backlog manapun. Jangan menebak intent demi kecepatan.
4. Setelah semua item tercatat di backlog, AI mengusulkan urutan pemrosesan berdasarkan dependency (bukan sekadar urutan disebut user) — lihat SOP-01/02/03 di bawah untuk tiap intent.
5. Pemrosesan dari backlog menuju entitas kerja penuh (Requirement → Planning → Implementation → Mandatory Review) **wajib satu-satu, mengikuti urutan dependency**, bukan bulk. Lihat § 5.2 Mandatory Rules poin 8.

### SOP-01: Memulai Project Baru
1. Buat folder `projects/<project-slug>/` mengikuti struktur di `04` § 4.2.
2. Isi `00-INDEX.md` project dengan status awal `idea`.
3. Jalankan Klaster 1 (Discovery) dari lifecycle `03` § 3.1 sebelum menulis satu baris pun requirement final.
4. Requirement disetujui → lanjut ke Planning.

### SOP-02: Menambah Feature ke Project Berjalan
1. Salin `templates/TEMPLATE-feature.md` ke `05-features/feature-<id>-<slug>.md`.
2. Isi metadata (`04` § 4.3) dan Summary Block.
3. Daftarkan 1 baris di `05-features/00-INDEX.md`.
4. Jalankan lifecycle penuh (`03`), termasuk 14 poin Mandatory Review Section — tidak boleh dilewati.

### SOP-03: Menangani Bug
1. Salin `templates/TEMPLATE-bugfix-enhancement-refactor.md` ke `07-bugs-and-fixes/bug-<id>-<slug>.md`.
2. Isi Root Cause Analysis sebelum menulis fix (wajib, bukan opsional).
3. Wajib isi Regression Risk dan Rollback Plan sebelum deployment.

### SOP-04: Menutup (Closing) Entitas Kerja
1. Pastikan seluruh Mandatory Review Section (`03` § 3.2) terisi.
2. Isi Post Implementation Review + Lessons Learned.
3. Update `status: done` di metadata.
4. Setelah periode retensi aktif berakhir (ditentukan tim, default 1 rilis siklus), pindahkan file ke `99-archive/` — **jangan dihapus**, ubah status jadi `archived`.

### SOP-05: Mengubah Kernel Planning-OS Itu Sendiri
Lihat § 5.3 Governance — tidak boleh diedit bebas seperti file project biasa.

---

## 5.2 Mandatory Rules (tidak bisa dinegosiasikan)

1. Tidak ada entitas kerja berstatus `done` tanpa 14 poin Mandatory Review Section terisi (`03` § 3.2).
2. Tidak ada informasi yang didefinisikan di lebih dari satu file (SSoT, `01` ADR-001 & `04` § 4.6).
3. Setiap folder berisi >3 file wajib punya `00-INDEX.md`.
4. Setiap file detail wajib punya metadata header + Summary Block.
5. Keputusan penting wajib masuk Decision Log — bukan hanya di chat/pesan personal.
6. File tidak pernah dihapus untuk entitas yang pernah aktif — hanya diarsipkan (`99-archive/`), demi audit trail.
7. Kernel (`00`–`06` root) hanya boleh diubah lewat proses Governance (§ 5.3), tidak lewat edit langsung oleh 1 orang.
8. Backlog wajib dipisah per intent — Feature / Refactor-Enhancement / Bug tidak boleh dicampur dalam satu file atau satu daftar (`04` § 4.2a). Capture boleh bulk, tapi pemrosesan (Requirement → Implementation → Mandatory Review) wajib satu entitas kerja per waktu, berurutan sesuai dependency — bukan diproses serentak hanya karena diminta bulk oleh user.
9. Jika permintaan user dalam satu batch mengandung intent yang ambigu, saling kontradiksi, atau requirement yang belum jelas, AI wajib berhenti dan minta klarifikasi (`05` SOP-00 poin 3) sebelum mencatat/memproses — AI tidak boleh menebak demi terlihat responsif, terutama karena keinginan user bisa berubah-ubah atau tidak konsisten antar pesan.

---

## 5.3 Governance

### Peran
- **Architecture Council** (bisa 1 orang di tim kecil): pemegang otoritas akhir perubahan kernel Planning-OS.
- **Contributor**: siapa pun yang memakai sistem ini untuk project sehari-hari, boleh mengusulkan perubahan kernel tapi tidak mengeksekusi langsung.

### Proses Perubahan Kernel
1. Usulan perubahan ditulis sebagai entri baru di `06-SELF-AUDIT.md` § Change Proposal.
2. Architecture Council review: apakah perubahan menambah context pollution, duplikasi, atau melanggar prinsip inti (`00` § 0.5)?
3. Jika disetujui: versi kernel naik (semantic versioning di `00-INDEX.md`), perubahan dicatat di histori revisi (`06`).
4. Perubahan **breaking** (mengubah struktur folder wajib) butuh masa transisi — kedua struktur lama & baru didukung sementara, didokumentasikan eksplisit.

### Kapan Wajib Review Kernel
- Setiap 6–12 bulan (jadwal tetap), atau
- Saat ditemukan pola pelanggaran berulang terhadap Mandatory Rules (sinyal bahwa sistem terlalu berat/tidak sesuai kebutuhan nyata).

---

## 5.4 Maintenance Strategy

- **Freshness check berkala**: index di tiap level (`04` § 4.4) diperiksa agar tidak menunjuk ke file yang sudah diarsipkan tanpa update status.
- **Dead link audit**: cross-reference (`04` § 4.6) diperiksa agar tidak ada link rusak ke file yang sudah dipindah.
- **Duplication audit**: pemeriksaan berkala apakah ada informasi yang mulai terduplikasi antar file akibat orang terburu-buru menyalin alih-alih menautkan.
- Semua temuan maintenance dicatat sebagai Task di `06-tasks/` project internal "Planning-OS Maintenance" (Planning-OS memelihara dirinya sendiri memakai pola yang sama).

## 5.5 Scalability Strategy

- **Horizontal**: menambah project baru = menambah folder baru mengikuti scaffold (`04` § 4.2) — tidak menyentuh kernel sama sekali.
- **Vertical**: jika satu project menjadi sangat besar (ratusan feature), `05-features/00-INDEX.md` boleh dipecah lagi menjadi sub-index per domain (mis. `05-features/checkout/00-INDEX.md`), mengikuti pola hybrid yang sama secara rekursif.
- **Multi-tim**: setiap tim boleh punya `projects/<team>/` sebagai namespace, tapi tetap tunduk pada kernel yang sama — mencegah tiap tim menciptakan "dialek" planning sendiri.

## 5.6 Future Expansion Strategy

- Sistem ini didesain agar bisa menambah jenis entitas kerja baru (mis. "Experiment" untuk A/B test, "Migration" untuk perpindahan sistem) dengan pola yang sama: tambah 1 template baru di `templates/`, tambah 1 folder scaffold baru di `04`, daftarkan di index — tanpa mengubah prinsip inti.
- Integrasi ke tools eksekusi nyata (Jira/Linear/Notion) diperlakukan sebagai **lapisan sinkronisasi**, bukan pengganti SSoT: file Markdown di sistem ini tetap sumber kebenaran; tool eksternal adalah cermin/pelaksana, bukan alternatif dokumentasi.
