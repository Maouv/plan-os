# Plan-OS Tooling and Specification Friction

> **Summary Block:** Catatan ini merangkum friksi nyata saat Plan-OS dipakai untuk mengubah planning Graps dari satu master plan menjadi full project instance. Masalah utama bukan konsep lifecycle atau SSoT, melainkan ketidaksinkronan antara specification, template, dan jangkauan `pos.py`. Akibatnya, command dapat hijau walau artifact belum full Plan-OS compliant.

- Observed: 2026-07-14 (findings #1–10), updated 2026-07-15 (findings #11–12)
- Reporter: Freya / Hermes Agent (#1–10); Claude, onboarding a new user
  through the full skill workflow end-to-end (#11–12)
- Context: `/workspace/graps/plan/experimental-graps/` (#1–10);
  `projects/wow-game-webapp/` — fresh project created from scratch to test
  every `pos.py` command plus deliberately broken edge cases (#11–12)
- Plan-OS version: 1.1.0
- Source revision tested: `627a95a` (#1-10, all confirmed fixed in the
  revision tested 2026-07-15); findings #11–12 are new, still open

## Executive Summary

Plan-OS membantu memaksa planning menjadi eksplisit: SSoT terpisah, lifecycle, review, dependency, dan Decision Log. Namun penggunaan riil menemukan dua kelas masalah:

1. **False confidence dari enforcer:** `validate` dan `depgraph` dapat exit `0` walau master plan monolitik tidak diperiksa atau dependency graph kosong.
2. **Specification drift:** scaffold, template, quick start, status, ID allocator, dan nama Decision Log tidak sepenuhnya konsisten.

Outcome di Graps baru benar-benar dapat dipercaya setelah full scaffold dibuat manual, 20 feature + 4 task dipopulasi, kemudian dilengkapi custom audit di luar `pos.py`.

## Findings

### 1. Validator melewatkan project-level dan top-level detail

**Severity:** High

`entity_detail_files()` hanya memeriksa file di:

- `05-features/`
- `06-tasks/`
- `07-bugs-and-fixes/`
- `08-refactor-and-enhancement/`

Master plan yang berada langsung di root project tidak diperiksa untuk metadata detail, Summary Block, orphan registration, batas 400 baris, lifecycle, atau review completeness.

**Observed behavior:** master plan Graps sekitar 1.179 baris menghasilkan:

```text
✅ ... bersih — tidak ada pelanggaran Mandatory Rules terdeteksi.
```

**Impact:** pengguna dapat menyebut artifact “validated/full compliant” padahal validator hanya memeriksa subset yang kosong.

**Suggested fix:**

- Validasi project root dan semua SSoT scaffold, bukan hanya entity folders.
- Tampilkan summary scope: jumlah file ditemukan, jumlah file diperiksa penuh, dan file yang dilewati.
- Exit non-zero atau warning kuat jika scaffold wajib tidak lengkap.

### 2. `depgraph` kosong dianggap sukses

**Severity:** High

Ketika tidak ada entity file, `depgraph` mencetak:

```text
Tidak ada entitas dengan metadata id di <path>.
```

namun exit code tetap `0`.

**Impact:** mudah disalahartikan sebagai dependency graph yang valid. Ini benar-benar terjadi saat audit awal Graps.

**Suggested fix:**

- Tambahkan output eksplisit `entities=0; graph not validated`.
- Gunakan exit code berbeda atau flag `--allow-empty`.
- Untuk full project instance, empty graph seharusnya warning/error bila feature/task sudah direncanakan.

### 3. Enforcer belum memvalidasi 27 lifecycle stages dan 14 review sections

**Severity:** High

Dokumen `03-LIFECYCLE-AND-REVIEW-SYSTEM.md` menyebut heading lifecycle dan seluruh 14 review subsection wajib. `pos.py` hanya memeriksa keberadaan string `Summary Block`; untuk status `done`, pemeriksaan tambahan hanya mencari `Post Implementation Review`.

**Impact:** entity dapat lolos validator walau lifecycle atau hampir seluruh Mandatory Review Section hilang.

**Suggested fix:**

- Tambahkan pemeriksaan 27 heading lifecycle untuk entity yang diwajibkan.
- Tambahkan pemeriksaan 14 review heading.
- Izinkan `Not Applicable — <reason>`, tetapi heading tetap wajib sesuai specification.

### 4. Nama Decision Log tidak konsisten

**Severity:** Medium

Referensi berbeda menggunakan dua nama:

- Scaffold §4.2: `09-decision-log.md`
- `TEMPLATE-project.md`: `08-decision-log.md`
- §4.6 juga menyebut `08-decision-log.md`

**Impact:** agent harus memilih diam-diam atau berhenti meminta keputusan untuk struktur yang seharusnya deterministic.

**Suggested fix:** tetapkan satu canonical filename, direkomendasikan `09-decision-log.md` agar selaras dengan urutan scaffold, lalu update semua referensi dan template.

### 5. `PROJ` ada di template tetapi tidak didukung `new-id`

**Severity:** Medium

`TEMPLATE-project.md` memakai `PROJ-XXXX`, tetapi `ID_PREFIXES` hanya mendukung:

```text
FEAT, TASK, BUG, ENH, REF, MIG, BKLG
```

**Impact:** project ID harus dibuat manual, sehingga mekanisme ledger tidak melindungi collision pada project.

**Suggested fix:** tambahkan `PROJ` ke allocator atau jelaskan bahwa project ID memakai namespace/allocator berbeda.

### 6. Status project tidak sinkron dengan status CLI

**Severity:** Medium

`TEMPLATE-project.md` mengizinkan status `discovery`, tetapi `VALID_STATUSES` di `pos.py` tidak memuat `discovery`. Sebaliknya validator saat ini tidak memeriksa project root, sehingga konflik ini tersembunyi.

**Impact:** ketika project-level validation ditambahkan, template resmi akan langsung memicu warning kecuali vocabulary diselaraskan.

**Suggested fix:** jadikan daftar status satu SSoT yang dipakai docs, template, dan CLI.

### 7. Quick Start merujuk template bugfix yang tidak ada

**Severity:** Medium

`00-INDEX.md` mengarahkan pengguna ke `templates/TEMPLATE-bugfix.md`, sedangkan file aktual adalah:

```text
templates/TEMPLATE-bugfix-enhancement-refactor.md
```

**Impact:** retrieval route resmi berujung dead end dan memaksa pengguna mencari manual.

**Suggested fix:** perbaiki link/nama file dan tambahkan automated internal-link check untuk kernel Plan-OS sendiri.

### 8. Full scaffold harus dibuat manual dan tidak atomic

**Severity:** Medium
**Status:** masih terbuka — dikonfirmasi ulang 2026-07-15. Saat scaffold
`wow-game-webapp` dari nol untuk onboarding session ini, tidak ada
`init-project`/`add-feature`/`add-task`; semua folder, index, backlog, dan
Decision Log dibuat manual satu per satu persis seperti yang dikeluhkan di
finding ini.

Tidak ada command seperti `pos.py init-project` atau `pos.py add-feature`. Full instance Graps membutuhkan 53 Markdown files, 20 FEAT, 4 TASK, indexes, ledger, Decision Log, lifecycle, dan review sections yang dibuat manual.

Dalam batch pertama, execution environment mencapai limit 50 tool calls. Tiga file terakhir tidak terbentuk, sementara summary batch sempat terlihat sukses. `validate` kemudian menemukan missing task index dan menyelamatkan hasil.

**Impact:** operasi besar rentan partial scaffold, orphan file, index drift, dan reserved ID tanpa entity.

**Suggested fix:**

- Tambahkan `init-project`, `add-feature`, dan `add-task` yang atomic.
- Tulis ke temporary directory lalu rename setelah semua file sukses.
- Cetak manifest `expected/created/failed` dan rollback saat gagal.

### 9. ID allocation satu-per-satu mudah meninggalkan gap

**Severity:** Low–Medium
**Status:** masih terbuka — dikonfirmasi ulang 2026-07-15. `new-id --claim`
masih satu-per-satu tanpa `--count`, dan (lihat finding #11 baru di atas)
bahkan langkah pertamanya sendiri bisa crash kalau folder belum ada — jadi
gap ini belum tersentuh sama sekali.

`new-id --claim` langsung mengubah `.pos-id-ledger.json`. Jika pembuatan entity gagal setelah claim, ID tetap reserved. Membuat banyak entities juga membutuhkan command berulang.

**Impact:** ledger dapat maju tanpa file pasangan dan bulk decomposition menjadi lambat.

**Suggested fix:**

- Tambahkan `--count`, transactional claim, atau claim sebagai bagian `add-feature/add-task`.
- Validator membandingkan ledger dengan entity tertinggi dan melaporkan reserved-but-unused IDs secara informatif.

### 10. Metadata parser hanya mendukung YAML datar terbatas

**Severity:** Low–Medium
**Status:** masih terbuka — dikonfirmasi ulang 2026-07-15. `parse_metadata()`
di `pos.py` (revisi yang sama, `627a95a`) belum berubah; masih line-based
`partition(":")`, tidak ada perubahan ke arah restricted-frontmatter yang
didokumentasikan atau parser YAML subset.

`parse_metadata()` memproses setiap baris dengan `partition(":")`; `depends_on` dan `related` efektif hanya aman sebagai inline list. YAML multiline, quoted value kompleks, atau nested metadata tidak didukung walau header terlihat seperti YAML.

**Impact:** pengguna dapat menulis YAML valid yang ditafsirkan berbeda oleh CLI.

**Suggested fix:**

- Dokumentasikan format sebagai “restricted frontmatter”, bukan YAML umum; atau
- Gunakan parser YAML yang dipin secara exact bila zero-dependency bukan requirement mutlak; atau
- Implementasikan parser subset dengan error jelas untuk syntax unsupported.

### 11. `new-id --claim` crashes with an unhandled traceback when the project folder doesn't exist yet

**Severity:** High

**Observed:** 2026-07-15
**Context:** fresh onboarding session, brand-new project `wow-game-webapp`, before any scaffold folder was created.

`validate` and `depgraph` both correctly guard on `root.exists()` and print a
clean error when the project path doesn't exist yet. `new_id()` has no such
guard: with `--claim`, it proceeds straight to `save_ledger()`, which calls
`(root / LEDGER_NAME).write_text(...)` against a directory that doesn't
exist, raising an unhandled `FileNotFoundError` all the way to the shell:

```text
Traceback (most recent call last):
  ...
  File "pos.py", line 476, in save_ledger
    (root / LEDGER_NAME).write_text(...)
FileNotFoundError: [Errno 2] No such file or directory: '<project>/.pos-id-ledger.json'
```

**Impact:** this hits the single most common "new project" path — allocating
a `PROJ` id before the scaffold folder exists. `new-id` *without* `--claim`
works fine on a nonexistent path (it just doesn't write anything), so the
crash is specific to the `--claim` branch, making it an easy trap for anyone
following the SOP literally (allocate ID → then scaffold).

**Suggested fix:** add the same `root.exists()` check used in
`validate_project()`/`run_depgraph()` to `new_id()` before attempting to
write the ledger, and raise a clean `SystemExit` message instead of letting
the traceback surface.

### 12. Orphan-file check can be bypassed when a duplicate ID is involved

**Severity:** Medium

**Observed:** 2026-07-15
**Context:** deliberate edge-case test — two feature files both declaring
`id: FEAT-0001`, only one of them registered in `05-features/00-INDEX.md`.

The orphan check in `validate_project()` is:

```python
if f.name not in idx_text and (meta or {}).get("id", "") not in idx_text:
    report.error(rel, f"File tidak disebut di {relpath(root, parent_index)} — dianggap orphan ...")
```

It checks whether the file's `id` appears *anywhere* in the parent index
text, not whether the specific line registering *this file* exists. When two
files share the same (duplicate) ID and only one is registered, the
unregistered one still finds its ID as a substring elsewhere in the index
(from the *other* file's registration line) and silently passes the orphan
check. Confirmed by isolating the case: the same file with a *unique* ID not
present anywhere in the index is correctly flagged as orphan — the bug is
specific to the duplicate-ID + partially-registered combination.

**Impact:** the duplicate-ID error itself still fires (so this isn't a
completely silent pass), but it means a genuinely unregistered file can hide
behind a duplicate ID and dodge the orphan finding, understating the number
of real violations in the report.

**Suggested fix:** tie the registration check to a specific expected line
(e.g. match `id` together with the file's own name/slug, or require each
registered ID to map to exactly one filename in the index) rather than a
bare substring search over the whole index text.

## What Worked Well

- Root/folder indexes membuat retrieval lebih terarah.
- Pemisahan requirement, architecture, feature, task, dan Decision Log mengurangi duplikasi.
- `depends_on` + topological sort berguna setelah entity folders benar-benar populated.
- Broken-link detection menangkap partial scaffold yang nyata.
- Batas sekitar 400 baris mendorong pemecahan master plan monolitik.
- Mandatory Review Section memaksa fallback, security, rollback, dan negative testing dipikirkan sebelum implementasi.

## Recommended Fix Order

1. Perjelas empty/scope result pada `validate` dan `depgraph`.
2. Sinkronkan Decision Log, template bugfix, project status, dan `PROJ` ID.
3. Enforce 27 lifecycle + 14 review sections.
4. Tambahkan project-level scaffold validation.
5. `new-id --claim` guard `root.exists()` sebelum `save_ledger()` (#11) —
   quick fix, high severity, langsung kena di jalur "project baru".
6. Perbaiki orphan-check jadi per-baris registrasi, bukan substring ID global
   (#12).
7. Tambahkan atomic scaffold/entity generator.
8. Perketat atau dokumentasikan metadata parser.

## Acceptance Criteria for Plan-OS Improvements

- [ ] `validate` melaporkan jumlah file discovered, fully checked, dan skipped.
- [ ] Master plan >400 baris di project root menghasilkan warning.
- [ ] Full-instance mode gagal bila scaffold wajib tidak lengkap.
- [ ] `depgraph` kosong tidak dapat disalahartikan sebagai graph tervalidasi.
- [ ] 27 lifecycle headings dan 14 review headings diperiksa.
- [ ] Decision Log memakai satu canonical filename di seluruh docs/template.
- [ ] Semua template yang disebut Quick Start benar-benar ada.
- [ ] Project ID dan status konsisten antara template dan CLI.
- [ ] Scaffold generation bersifat atomic dan mencetak manifest hasil.
- [ ] Kernel Plan-OS lolos self-validation untuk internal links dan specification consistency.
- [ ] `new-id --claim` gagal dengan pesan bersih (bukan traceback) kalau project path belum ada.
- [ ] Orphan-file check di `validate` terikat ke baris registrasi spesifik per file, tidak lagi rentan di-bypass oleh duplicate ID.
