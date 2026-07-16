---
id: ENH-0001
type: enhancement
status: done
owner: Maou
created: 2026-07-16
updated: 2026-07-16
depends_on: []
related: []
---

# `pos.py` Packaging + Test Suite

> **Summary Block:** `pos.py` sudah dipatch untuk 12 temuan terdokumentasi
> (`issue/new-id-claim-orhpan-file.md`), tapi seluruh perbaikan itu
> diverifikasi manual, bukan lewat automated test — regresi baru di masa
> depan tidak akan tertangkap otomatis. Item ini menambahkan `pyproject.toml`
> (SSoT versi paket, `pos --version`) dan `tests/` (pytest) sebagai jaring
> pengaman sebelum TEMP-05 (root repo reorg) menyentuh `pos.py`.

## 1. Deskripsi Masalah / Tujuan Perubahan
`pos.py` adalah enforcer inti Plan-OS, tapi tidak punya test otomatis sama
sekali. 12 bug di `issue/new-id-claim-orhpan-file.md` (termasuk 2 High
severity: validator melewatkan master plan root, `depgraph` kosong dianggap
sukses) sudah diperbaiki di source, tapi status "sudah fix" itu hanya
berdasar catatan tertulis di komentar kode dan re-testing manual satu kali
per temuan — tidak ada yang mencegah regresi diam-diam saat `pos.py`
di-refactor (mis. saat TEMP-05 memindahkannya ke `tools/pos.py`).

Tujuan: (a) `pyproject.toml` supaya ada `pos --version` sebagai sumber
kebenaran versi paket, bukan teks bebas; (b) suite pytest yang meng-cover
`validate`, `new-id`, `depgraph`, dan secara eksplisit meregresi-test
temuan-temuan yang paling berisiko diam-diam rusak lagi.

## 2. Root Cause Analysis
_(Not Applicable — ini enhancement, bukan bugfix. "Akar masalah" di sini
adalah gap proses: perbaikan bug sebelumnya tidak disertai automated test,
bukan bug baru yang perlu di-diagnosis.)_

## 3. Proposed Fix / Change
1. `pyproject.toml` di root repo: metadata paket (`name`, `version`,
   `requires-python`), entry point `pos = "pos:main"`, konfigurasi
   `[tool.pytest.ini_options]`.
2. `pos.py`: tambah `get_version()` yang membaca `version = "..."` dari
   `pyproject.toml` lewat regex (bukan `tomllib`, supaya tidak menaikkan
   syarat minimum Python secara diam-diam), dicari di folder `pos.py` sendiri
   dan satu level di atasnya (antisipasi TEMP-05 memindah `pos.py` ke
   `tools/`). Tambah flag `--version` di parser top-level.
3. `tests/` (pytest): `conftest.py` (fixture builder entitas + project
   scaffold minimal-valid), `test_validate.py`, `test_new_id.py`,
   `test_depgraph.py`, `test_packaging.py` — total 39 test case, termasuk
   regression test eksplisit untuk temuan #1, #2, #3, #5, #6, #11, #12 dari
   `issue/new-id-claim-orhpan-file.md`.

**Di luar scope item ini (sengaja tidak dikerjakan sekarang):**
- Temuan #8 (atomic scaffold generator `init-project`/`add-feature`), #9
  (`--count` bulk claim), #10 (metadata parser YAML terbatas) — ketiganya
  masih *suggested fix* yang belum diimplementasikan di `pos.py` sama
  sekali (dicek langsung di source, bukan diasumsikan dari komentar). Test
  suite ini tidak bisa meregresi-test sesuatu yang belum ada; ini dicatat di
  Future Improvement, bukan diam-diam dianggap selesai.
- Sinkronisasi `Versi: 1.1.0` di `00-INDEX.md` root (kernel) dengan versi
  paket di `pyproject.toml` — lihat Known Risks poin 1.

## 4. Scope & Impact
- **Komponen terdampak:** `pos.py` (root), file baru `pyproject.toml` dan
  `tests/**` (root, di luar `projects/`). Tidak menyentuh `00`–`06` kernel
  docs.
- **Blast Radius:** kecil — file baru + satu fungsi baru (`get_version`) dan
  satu flag CLI baru (`--version`) di `pos.py`. Tidak mengubah perilaku
  `validate`/`new-id`/`depgraph` yang sudah ada; seluruh 39 test memverifikasi
  perilaku existing tidak berubah, bukan menambah behavior baru pada command
  itu.

## 5. Lifecycle Stage Tracking
### Klaster 1 — Discovery: Done (baca `issue/new-id-claim-orhpan-file.md`, `pos.py` source, backlog TEMP-06)
### Klaster 2 — Planning & Design: Done (lihat § 3 Proposed Fix/Change)
### Klaster 3 — Build: Done
- Implementation: Done (`pyproject.toml`, `get_version()`, `--version` flag, `tests/` 39 case)
- Self Review: Done (lihat § 6 Mandatory Review Section)
- AI Review: Done (ditulis & direview oleh Claude dalam sesi yang sama)
- Code Review: Not Applicable — solo developer, tidak ada peer reviewer manusia lain saat ini.
### Klaster 4 — Verification: Done
- Testing: Done — `python3 -m pytest tests/` → 39 passed.
- QA: Done — dicocokkan manual terhadap Acceptance Criteria § 6.
- Potential Bug Review, Edge Case Review, Negative Scenario Review, Security
  Review, Performance Review, Compatibility Review: lihat § 6 Mandatory
  Review Section (masing-masing sudah diisi jujur, bukan template kosong).
### Klaster 5 — Validation dengan User: Not Applicable — internal tooling, tidak ada user eksternal di luar owner sendiri.
### Klaster 6 — Release & Closing: Done
- Deployment: Not Applicable — tidak ada environment rilis terpisah, file langsung dipakai di repo ini.
- Monitoring: Not Applicable — lihat alasan yang sama.
- Post Implementation Review, Lessons Learned: lihat § 7.

### Session Log
- 2026-07-16: TEMP-06 di-claim jadi ENH-0001. `pyproject.toml` +
  `get_version()`/`--version` di `pos.py` + `tests/` (39 case, termasuk
  regression test #1, #2, #3, #5, #6, #11, #12) ditulis dan lolos
  `pytest` bersih dalam sesi yang sama.
- 2026-07-16: `pos.py validate projects/plan-os-maintenance` bersih (0
  error, 1 warning cakupan yang sudah dikenal — lihat `SKILL.md` §9).
  Status dinaikkan ke `done`. Backlog TEMP-06 ditandai `→ moved to ENH-0001`
  (bukan dihapus). Decision Log `DEC-0003` ditambahkan untuk keputusan SSoT
  versi. Ditemukan & dicatat 2 temuan sampingan di luar scope item ini
  (lihat ringkasan ke user): gap penomoran `DEC-0001` yang hilang di
  Decision Log, dan link salah "02-features/" alih-alih "05-features/" di
  `00-INDEX.md` root (kernel, tidak diperbaiki di sesi ini karena butuh
  Governance).

## 6. Mandatory Review Section

### Potential Bugs
- `get_version()` regex (`^version\s*=\s*"([^"]+)"`) bisa salah tangkap
  kalau `pyproject.toml` punya lebih dari satu tabel dengan key `version`
  (mis. `[tool.poetry.version]` semu) — saat ini `pyproject.toml` hanya
  punya satu `[project]` table jadi aman, tapi kalau file ini diperluas
  nanti (mis. tambah `[project.optional-dependencies]` versi dependency),
  regex generik ini berisiko salah match. Mitigasi: regex sengaja dianchor
  ke awal baris (`(?m)^version`) supaya hanya menangkap key top-level, bukan
  nested — cukup untuk struktur saat ini, tapi bukan parser TOML asli.
- `subprocess` test di `test_packaging.py` bergantung pada `sys.executable`
  yang sama dengan yang menjalankan pytest — bisa gagal di environment
  dengan multiple Python interpreter yang tidak konsisten (jarang terjadi di
  VPS/CI tunggal, tapi dicatat).

### Known Risks
- **SSoT ambiguity (bukan bug, tapi risiko konseptual):** `pyproject.toml`
  `version = "1.1.0"` kebetulan sama persis dengan `Versi: 1.1.0` di
  `00-INDEX.md` root — tapi keduanya adalah topik berbeda (versi paket CLI
  vs versi spec kernel Planning-OS). Item ini SENGAJA tidak menyamakan/
  menautkan keduanya karena `00-INDEX.md` adalah file kernel (governance-
  gated). Risiko: kedua angka bisa divergen di masa depan (mis. `pos.py`
  naik ke 1.2.0 karena bug fix tapi kernel docs tidak berubah) tanpa ada
  mekanisme yang memberi tahu bahwa itu memang wajar. Dicatat eksplisit di
  Decision Log (`09-decision-log.md`) supaya tidak jadi asumsi diam-diam sesi
  berikutnya.
- Test suite mem-verifikasi perilaku `pos.py` versi saat ini (termasuk 12 fix
  yang sudah ada) — bukan jaminan bahwa perilaku itu benar secara desain,
  hanya bahwa perilaku itu **stabil** dan regresi akan tertangkap.

### Edge Cases
- `pyproject.toml` hilang total (mis. ter-delete manual) → `get_version()`
  fallback ke `_VERSION_FALLBACK = "0.0.0-unknown"`, tidak crash — diuji di
  `test_get_version_falls_back_when_pyproject_missing`.
- `pos.py` dipindah ke `tools/pos.py` (TEMP-05 di masa depan) sementara
  `pyproject.toml` tetap di root → `get_version()` sudah mengecek 1 level di
  atas folder `pos.py`, diuji lewat simulasi layout di
  `test_version_lookup_also_checks_parent_dir_for_future_tools_layout`.
- Duplicate ID + salah satu file tidak terdaftar di index (issue #12) →
  diuji eksplisit di `test_duplicate_id_does_not_hide_unregistered_orphan`.

### Failure Cases
- `get_version()` gagal baca file (mis. permission error) → tidak di-catch
  eksplisit saat ini; akan naik sebagai `OSError` tak tertangani. Ini gagal
  **tidak graceful** untuk kasus permission error spesifik (beda dari kasus
  "file tidak ada" yang sudah ditangani via `.exists()`). Dicatat di Future
  Improvement, bukan diabaikan.
- `new-id --claim` di path yang belum ada → gagal graceful dengan
  `SystemExit` pesan jelas (issue #11, sudah diregresi-test), bukan
  traceback mentah.

### Negative Test Cases
- ID tipe tidak dikenal (`NOPE`) ke `new_id()` → `SystemExit` (diuji).
- `depgraph` di path yang tidak ada → `graph == {}`, ditangani terpisah oleh
  `run_depgraph()` (guard `root.exists()` sudah ada sebelum item ini, tidak
  diubah).
- File entitas tanpa metadata header sama sekali → error, bukan diam-diam
  dilewati (diuji).

### Regression Risk
- Risiko utama: TEMP-05 (root repo reorg) memindah `pos.py` ke
  `tools/pos.py` dan/atau `pyproject.toml` ikut pindah — `get_version()`
  sudah dirancang antisipatif (cek 2 level), tapi TEMP-05 tetap **wajib**
  menjalankan `pytest tests/` ulang setelah reorg sebagai bagian dari
  Definition of Done-nya sendiri, bukan asumsi "harusnya masih jalan".
- Tidak ada perubahan pada logika `validate_project`/`new_id`/`run_depgraph`
  yang sudah ada — hanya penambahan `get_version()` dan satu argumen CLI
  baru (`--version`) yang independen dari subcommand lain. Risiko regresi ke
  command existing dinilai rendah, dan seluruh 39 test memverifikasi ini.

### Rollback Plan
- Revert 3 perubahan (`pyproject.toml` baru, patch `get_version()`+
  `--version` di `pos.py`, folder `tests/` baru) — seluruhnya file baru atau
  penambahan aditif di `pos.py` (tidak ada baris existing yang dihapus/
  diubah semantiknya), sehingga rollback = hapus file baru + `git checkout`
  `pos.py` ke revisi sebelum item ini. Tidak ada migrasi data/state yang
  perlu dibatalkan (`.pos-id-ledger.json` tidak tersentuh oleh perubahan
  ini).

### Validation Checklist
- [x] `pyproject.toml` valid dan bisa dibaca `get_version()`.
- [x] `pos.py --version` mencetak versi dari `pyproject.toml`, exit 0.
- [x] `python3 -m pytest tests/` → 39 passed, 0 failed.
- [x] Tidak ada perubahan perilaku pada `validate`/`new-id`/`depgraph` yang
      sudah ada (diverifikasi lewat test yang cover perilaku existing, bukan
      cuma perilaku baru).

### Review Checklist
- [x] Self Review — dilakukan (termasuk 1 kali perbaikan nama test yang
      misleading sebelum dianggap selesai, lihat Lessons Learned).
- [x] AI Review — ditulis dan direview oleh Claude dalam sesi eksekusi yang sama.
- [ ] Code Review — Not Applicable (solo developer, dicatat di § 5 Klaster 3).
- [x] Security Review — tidak ada input eksternal/network baru; `get_version()`
      hanya baca file lokal yang sudah ada di repo yang sama.
- [x] Performance Review — Not Applicable secara praktis (baca 1 file kecil
      sekali per invocation CLI, dampak performa nol).
- [x] Compatibility Review — sengaja tidak pakai `tomllib` (3.11+) demi
      kompatibilitas mundur; `requires-python = ">=3.10"` di `pyproject.toml`
      dipilih sebagai batas aman (tidak ada bukti kode existing butuh <3.10,
      tapi juga tidak ada bukti eksplisit didesain untuk <3.10 — lihat Known
      Risks bila ada target environment lebih lama).

### Acceptance Checklist
- [x] `pyproject.toml` dengan `pos --version` sebagai sumber kebenaran versi.
- [x] Folder `tests/` dengan pytest.
- [x] Regression coverage untuk temuan yang sudah di-fix di
      `issue/new-id-claim-orhpan-file.md` (bukan seluruh 12, hanya yang
      benar-benar berupa perilaku `pos.py` yang bisa diuji — lihat § 3 untuk
      daftar yang di luar scope dan alasannya).

### User Testing Result
- Not Applicable — internal tooling untuk 1 developer (owner), tidak ada
  user eksternal untuk pengujian terpisah pada tahap ini.

### Post Implementation Review
- Tujuan awal (test suite sebagai jaring pengaman sebelum TEMP-05) tercapai:
  39 test, seluruhnya lolos, meng-cover 7 dari 12 temuan yang relevan secara
  behavioral (perbaikan #4, #7 murni tentang konsistensi nama file/dokumen,
  bukan logic `pos.py` yang bisa di-assert lewat pytest; #8/#9/#10 memang
  belum diimplementasikan, jadi tidak ada yang bisa diregresi-test).

### Lessons Learned
- Menulis test SEBELUM mengklaim "12 bug sudah fix" lewat komentar kode saja
  ternyata langsung menemukan 1 test yang salah nama (mengklaim
  "first_allocation_is_0001" padahal fixture-nya sudah punya FEAT-0001,
  sehingga hasil sebenarnya 0002) — bukti kecil kenapa aturan "jangan
  menebak, validasi dulu" juga berlaku ke penulis test, bukan cuma ke
  implementasi.
- Builder fixture (`entity_text()` parametrik) jauh lebih murah dipelihara
  daripada file `.md` statis duplikatif — pola yang sama dengan alasan
  Compact Tracking Format di `03` §3.1.1 (hindari boilerplate identik).

### Future Improvement
- Temuan #8 (atomic scaffold generator), #9 (`--count` bulk claim ID), #10
  (metadata parser YAML subset yang lebih ketat) masih terbuka di
  `pos.py` itu sendiri — belum ada item backlog terpisah untuk ini di
  `00-backlog/backlog-features.md`/`backlog-refactor-enhancment.md`
  Planning-OS maintenance; layak diusulkan sebagai TEMP-XX baru bila
  prioritas berubah.
- `get_version()` belum menangani `OSError`/permission error saat membaca
  `pyproject.toml` secara graceful (lihat Failure Cases) — risiko rendah,
  tapi bisa ditambahkan `try/except` sederhana di iterasi berikutnya.
- Pertimbangkan menambah CI (GitHub Actions) yang menjalankan
  `pytest tests/` otomatis tiap push — saat ini test suite ada tapi masih
  dijalankan manual.

## 7. Closing
### Post Implementation Review
Lihat § 6 di atas (heading ini dipertahankan sesuai template § 7, isi
disatukan dengan § 6 untuk menghindari duplikasi SSoT — lihat catatan yang
sama di Lessons Learned).

### Lessons Learned
Lihat § 6 di atas.

### Future Improvement
Lihat § 6 di atas.

