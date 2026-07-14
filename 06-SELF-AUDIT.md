# 06 — Self-Audit & Revision History

> **Summary Block:** Audit internal terhadap desain Planning-OS sebelum dianggap final: pencarian missing section, redundansi, context pollution, penamaan lemah, dan modularitas lemah — beserta perbaikan yang diterapkan. Juga tempat mencatat Change Proposal (lihat `05` § 5.3).

---

## 6.1 Temuan Audit & Perbaikan yang Diterapkan

| # | Temuan | Kategori | Perbaikan |
|---|---|---|---|
| 1 | `templates/00-INDEX.md` disebut di `04` tapi belum ada isinya secara eksplisit | Missing section | Dibuat sebagai file terpisah di `templates/00-INDEX.md`, berisi peta 6 template + kapan dipakai. |
| 2 | Tidak ada jalur ringan untuk task sangat kecil (mis. ubah 1 baris config) — risiko orang menghindari sistem karena dirasa berat | Weak scalability / adoption risk | Ditambahkan **Lightweight Mode** di `templates/00-INDEX.md` § Lightweight Mode: untuk task <1 jam, seluruh Mandatory Review Section boleh diringkas jadi 1 baris per poin, tapi heading tetap wajib ada (konsisten dengan aturan di `03`). |
| 3 | Semua folder bernama `00-INDEX.md` — berisiko membingungkan manusia yang membuka banyak tab sekaligus | Bad naming (minor) | Diterima secara sadar (accepted tradeoff): konsistensi nama untuk AI lebih penting daripada keunikan nama untuk tab browser; mitigasi via title di dalam Summary Block, bukan via nama file. |
| 4 | RACI disebut sebagai istilah & framework tapi tidak ada contoh tabel konkret | Missing example | Contoh tabel RACI ditambahkan di `templates/TEMPLATE-project.md` § Planning. |
| 5 | Tidak ada definisi eksplisit soal siapa yang boleh memindahkan file ke `99-archive/` | Governance gap | Ditambahkan ke `05` SOP-04: pemindahan ke archive adalah bagian dari SOP Closing, dieksekusi oleh Owner entitas kerja tsb, bukan sembarang orang. |
| 6 | Belum ada mekanisme eksplisit untuk AI agent yang beroperasi otonom (bukan sekadar dibaca manusia) mengetahui "apakah boleh mengeksekusi/menulis" | Missing AI operating rule | Ditambahkan § 6.2 di file ini: AI Operating Rules, sebagai lapisan tambahan di atas Context Engineering (`04`). |
| 7 | Redundansi berpotensi: istilah "Review" muncul di `02` (vocabulary) dan `03` (mandatory review) | Redundancy check | Bukan redundansi nyata — `02` mendefinisikan istilah, `03` mendefinisikan proses wajib memakai istilah itu. Dipertahankan, ditandai jelas via cross-reference agar tidak disalin ulang. |
| 8 | Tidak ada batas eksplisit kapan sebuah Project dianggap terlalu besar dan harus dipecah jadi beberapa Project | Missing scaling trigger | Ditambahkan aturan di `05` § 5.5: jika `05-features/00-INDEX.md` sebuah project melebihi ~30 feature aktif, evaluasi pemecahan menjadi sub-project/domain terpisah. |
| 9 | Tidak ada aturan eksplisit soal bulk request dari user (mis. "tambah 10 fitur sekaligus") — berisiko AI memproses banyak entitas kerja serentak tanpa Requirement/Mandatory Review yang benar-benar spesifik per item, dan berisiko backlog feature/refactor/bug tercampur jadi satu daftar | Missing AI operating rule + weak modularization di backlog | Ditambahkan `04` § 4.2a (backlog dipisah 3 file per intent: feature/refactor-enhancement/bug), `TEMPLATE-backlog.md` baru, SOP-00 di `05`, dan Mandatory Rules poin 8–9 di `05` § 5.2: capture boleh bulk, pemrosesan wajib satu-satu berurutan dependency, dan AI wajib berhenti minta klarifikasi jika permintaan user dalam satu batch ambigu/kontradiktif. |

## 6.2 AI Operating Rules (tambahan hasil audit)

1. AI/agent yang membaca sistem ini untuk **tujuan informasi** (menjawab pertanyaan) boleh membaca index + file relevan secara bebas.
2. AI/agent yang **menulis/mengubah** file di sistem ini wajib: (a) memperbarui metadata `updated`, (b) mendaftarkan file baru ke index folder induk, (c) tidak pernah menghapus histori — hanya mengubah `status`.
3. AI/agent tidak boleh mengubah file kernel (`00`–`06` di root) tanpa proses Governance (`05` § 5.3) — ini berlaku sama baik pengubahnya manusia maupun AI.
4. Jika AI menemukan duplikasi informasi antar file, itu dilaporkan sebagai temuan (mirip baris di § 6.1), bukan diam-diam diperbaiki sepihak untuk topik yang berdampak besar.

## 6.3 Kriteria "Selesai" untuk Desain Sistem Ini Sendiri

- [x] Research summary ada dan actionable (`01`).
- [x] Architecture Decision Record dengan tradeoff eksplisit dan keputusan final (`01`).
- [x] Vocabulary lengkap & terkelompok, tidak dicampur jadi 1 daftar datar (`02`).
- [x] Framework library berdiri sendiri per entri (`02`).
- [x] Lifecycle 27 tahap, tidak ada shortcut implisit (`03`).
- [x] Mandatory Review Section wajib, tidak opsional (`03`).
- [x] Struktur folder nyata untuk kernel & instance (`04`).
- [x] Metadata, naming convention, cross-reference, versioning (`04`).
- [x] Context engineering strategy eksplisit & actionable (`04`).
- [x] SOP operasional harian (`05`).
- [x] Mandatory rules tegas (`05`).
- [x] Governance untuk mengubah sistem itu sendiri (`05`).
- [x] Maintenance & scalability strategy (`05`).
- [x] Future expansion strategy (`05`).
- [x] Self-audit dengan temuan nyata + perbaikan (file ini).

## 6.4 Revision History

| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0.0 | 2026-07-14 | Rilis awal Planning-OS: kernel 00–06 + templates. |
| 1.1.0 | 2026-07-14 | Backlog dipisah per intent (`00-backlog/` di `04` § 4.2a, folder instance direnumber: `08-refactor-and-enhancement/` baru, `decision-log`→09, `review-and-retro`→10), `TEMPLATE-backlog.md` baru, SOP-00 (Bulk Capture) di `05`, Mandatory Rules poin 8–9 (pemrosesan satu-satu berurutan dependency + wajib klarifikasi untuk permintaan ambigu/kontradiktif). Lihat temuan #9 di § 6.1. |

## 6.5 Change Proposal Log (diisi ke depan)

_Belum ada proposal. Format entri baru:_

```
### CP-001: <judul singkat>
- Diusulkan oleh: <nama>
- Tanggal: <tanggal>
- Masalah yang dipecahkan: ...
- Perubahan diusulkan: ...
- Dampak breaking: ya/tidak
- Keputusan Architecture Council: pending/approved/rejected
```
