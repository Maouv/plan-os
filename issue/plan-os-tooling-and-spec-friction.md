# Plan-OS Tooling and Specification Friction

> **Summary Block:** Catatan ini merangkum friksi nyata saat Plan-OS dipakai untuk mengubah planning Graps dari satu master plan menjadi full project instance. Masalah utama bukan konsep lifecycle atau SSoT, melainkan ketidaksinkronan antara specification, template, dan jangkauan `pos.py`. Akibatnya, command dapat hijau walau artifact belum full Plan-OS compliant.

- Observed: 2026-07-14
- Reporter: Freya / Hermes Agent
- Context: `/workspace/graps/plan/experimental-graps/`
- Plan-OS version: 1.1.0
- Source revision tested: `627a95a`

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

Tidak ada command seperti `pos.py init-project` atau `pos.py add-feature`. Full instance Graps membutuhkan 53 Markdown files, 20 FEAT, 4 TASK, indexes, ledger, Decision Log, lifecycle, dan review sections yang dibuat manual.

Dalam batch pertama, execution environment mencapai limit 50 tool calls. Tiga file terakhir tidak terbentuk, sementara summary batch sempat terlihat sukses. `validate` kemudian menemukan missing task index dan menyelamatkan hasil.

**Impact:** operasi besar rentan partial scaffold, orphan file, index drift, dan reserved ID tanpa entity.

**Suggested fix:**

- Tambahkan `init-project`, `add-feature`, dan `add-task` yang atomic.
- Tulis ke temporary directory lalu rename setelah semua file sukses.
- Cetak manifest `expected/created/failed` dan rollback saat gagal.

### 9. ID allocation satu-per-satu mudah meninggalkan gap

**Severity:** Low–Medium

`new-id --claim` langsung mengubah `.pos-id-ledger.json`. Jika pembuatan entity gagal setelah claim, ID tetap reserved. Membuat banyak entities juga membutuhkan command berulang.

**Impact:** ledger dapat maju tanpa file pasangan dan bulk decomposition menjadi lambat.

**Suggested fix:**

- Tambahkan `--count`, transactional claim, atau claim sebagai bagian `add-feature/add-task`.
- Validator membandingkan ledger dengan entity tertinggi dan melaporkan reserved-but-unused IDs secara informatif.

### 10. Metadata parser hanya mendukung YAML datar terbatas

**Severity:** Low–Medium

`parse_metadata()` memproses setiap baris dengan `partition(":")`; `depends_on` dan `related` efektif hanya aman sebagai inline list. YAML multiline, quoted value kompleks, atau nested metadata tidak didukung walau header terlihat seperti YAML.

**Impact:** pengguna dapat menulis YAML valid yang ditafsirkan berbeda oleh CLI.

**Suggested fix:**

- Dokumentasikan format sebagai “restricted frontmatter”, bukan YAML umum; atau
- Gunakan parser YAML yang dipin secara exact bila zero-dependency bukan requirement mutlak; atau
- Implementasikan parser subset dengan error jelas untuk syntax unsupported.

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
5. Tambahkan atomic scaffold/entity generator.
6. Perketat atau dokumentasikan metadata parser.

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
