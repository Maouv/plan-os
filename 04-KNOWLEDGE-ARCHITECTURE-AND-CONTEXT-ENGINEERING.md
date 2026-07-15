# 04 — Knowledge Architecture & Context Engineering Strategy

> **Summary Block:** Struktur folder/file nyata untuk Planning-OS dan untuk setiap Project instance, aturan metadata & naming, serta strategi konkret agar AI tidak kehilangan context, tidak halusinasi, dan tidak membaca file yang tidak perlu.

---

## 4.1 Struktur Folder Kernel (repo Planning-OS ini sendiri)

```
planning-os/
├── 00-INDEX.md                                  ← pintu masuk wajib
├── 01-RESEARCH-AND-ARCHITECTURE-DECISION.md
├── 02-VOCABULARY-AND-FRAMEWORKS.md
├── 03-LIFECYCLE-AND-REVIEW-SYSTEM.md
├── 04-KNOWLEDGE-ARCHITECTURE-AND-CONTEXT-ENGINEERING.md
├── 05-SOP-GOVERNANCE-MAINTENANCE.md
├── 06-SELF-AUDIT.md
└── templates/
    ├── 00-INDEX.md                              ← index khusus template
    ├── TEMPLATE-project.md
    ├── TEMPLATE-feature.md
    ├── TEMPLATE-task.md
    ├── TEMPLATE-bugfix-enhancement-refactor.md
    ├── TEMPLATE-decision-log.md
    └── TEMPLATE-review-checklist.md
```

Kernel ini **stabil** — hanya berubah lewat proses Governance (lihat `05`), bukan diedit bebas per project.

## 4.2 Struktur Folder Instance (per Project, contoh nyata)

```
projects/
└── <project-slug>/
    ├── 00-INDEX.md                 ← index & status project ini (SSoT status)
    ├── 00-backlog/                 ← capture layer, TERPISAH per intent (lihat § 4.2a)
    │   ├── 00-INDEX.md
    │   ├── backlog-features.md
    │   ├── backlog-refactor-enhancement.md
    │   └── backlog-bugs.md
    ├── 01-discovery/
    │   ├── idea.md
    │   ├── research.md
    │   └── analysis.md
    ├── 02-requirement/
    │   └── requirement.md          ← FR/NFR + Acceptance Criteria
    ├── 03-planning/
    │   ├── wbs.md
    │   ├── timeline.md
    │   └── raci.md
    ├── 04-design-architecture/
    │   ├── design.md
    │   └── architecture.md
    ├── 05-features/
    │   ├── 00-INDEX.md             ← daftar semua feature (ringkas, 1 baris/feature + status + link)
    │   ├── feature-<slug>.md       ← 1 file = 1 feature, pakai TEMPLATE-feature.md
    │   └── ...
    ├── 06-tasks/
    │   ├── 00-INDEX.md
    │   └── task-<id>-<slug>.md
    ├── 07-bugs-and-fixes/          ← khusus intent BUG, tidak dicampur refactor/enhancement
    │   ├── 00-INDEX.md
    │   └── bug-<id>-<slug>.md
    ├── 08-refactor-and-enhancement/ ← khusus intent REFACTOR/ENHANCEMENT, terpisah dari bug
    │   ├── 00-INDEX.md
    │   └── <ref|enh>-<id>-<slug>.md
    ├── 09-decision-log.md          ← SSoT semua keputusan penting project ini
    ├── 10-review-and-retro/
    │   ├── post-implementation-review.md
    │   └── retrospective-<sprint-id>.md
    └── 99-archive/                 ← entitas kerja yang sudah non-aktif dipindah ke sini, bukan dihapus
```

**Prinsip kunci:** setiap subfolder yang berisi lebih dari 3 file **wajib** punya `00-INDEX.md` sendiri. Ini mencegah AI harus membuka semua file untuk tahu apa isinya — cukup baca index folder tersebut.

## 4.2a Backlog Terpisah per Intent (Capture Layer)

Backlog **tidak boleh** jadi satu daftar campur-aduk berisi feature, refactor, dan bug sekaligus — tiap intent punya risk profile dan Definition of Ready yang beda (lihat `05` § 5.2 Mandatory Rules tambahan). Tiga file terpisah di `00-backlog/`:

- `backlog-features.md` — ide feature baru, status masih `idea`, belum tentu dikerjakan.
- `backlog-refactor-enhancement.md` — usulan perbaikan struktur/kualitas pada sesuatu yang sudah ada dan berjalan.
- `backlog-bugs.md` — laporan masalah pada sesuatu yang seharusnya sudah berfungsi tapi tidak.

Format tiap baris backlog: `[ ] <ID sementara> — <judul singkat> — dicatat <tanggal>`. Item backlog **boleh** ditambahkan bulk/sekaligus oleh user — ini murah dan belum masuk lifecycle. Begitu 1 item backlog mulai diproses (masuk Planning/Requirement), item dipindah jadi file entitas kerja penuh di folder terkait (`05-features/`, `07-bugs-and-fixes/`, atau `08-refactor-and-enhancement/`) dan baris di backlog ditandai `→ moved to <link>`, bukan dihapus.

## 4.3 Metadata Wajib (header setiap file detail)

Setiap file di `05-features/`, `06-tasks/`, `07-bugs-and-fixes/` wajib diawali blok metadata berikut sebelum Summary Block:

```markdown
---
id: FEAT-0042
type: feature
status: in-progress        # idea | planning | in-progress | review | done | archived
owner: <nama>
created: 2026-07-14
updated: 2026-07-14
depends_on: [FEAT-0031]
related: [TASK-0102, TASK-0103]
---
```

Metadata ini berfungsi sebagai **manifest** — AI bisa membaca metadata banyak file sekaligus (murah secara token) sebelum memutuskan file mana yang perlu dibuka penuh (mahal secara token).

## 4.4 Summary Layer vs Detail Layer

- **Summary Layer** = seluruh `00-INDEX.md` di semua level + metadata header. Total ukurannya kecil, murah dibaca AI, selalu jadi titik masuk pertama.
- **Detail Layer** = isi penuh tiap file (`feature-*.md`, `task-*.md`, dst). Hanya dibuka saat benar-benar relevan dengan tugas saat ini.

Alur retrieval standar untuk AI/agent:
`00-INDEX.md` root → `00-INDEX.md` folder terkait → metadata file kandidat → baru buka 1–3 file detail yang benar-benar relevan.

## 4.5 Naming Convention

- Semua file/folder: `kebab-case`, huruf kecil, tanpa spasi.
- Index folder selalu bernama `00-INDEX.md` (angka 00 memastikan selalu tampil paling atas secara alfabetis).
- File berurutan-proses diberi prefix angka 2 digit (`01-`, `02-`, …) agar urutan baca tersirat dari nama file, tidak perlu dijelaskan ulang.
- Entitas kerja individual pakai ID unik + slug: `feature-0042-checkout-redesign.md`, `task-0102-fix-null-pointer.md`, `bug-0007-race-condition.md`. ID unik mencegah tabrakan nama dan memudahkan cross-reference.

## 4.6 Cross-Reference, bukan Duplikasi

- Referensi antar dokumen memakai **link relatif + ID**, contoh: `Lihat [FEAT-0031](../05-features/feature-0031-login.md)`.
- Dilarang menyalin isi requirement/keputusan ke file lain. Jika informasi dibutuhkan di banyak tempat, tempat lain wajib berupa link, bukan salinan.
- Decision Log (`09-decision-log.md`) adalah satu-satunya SSoT untuk histori keputusan — tidak boleh ada "keputusan" tercatat hanya di komentar task atau chat pribadi.

## 4.7 Versioning

- Sistem ini didesain git-friendly: 1 entitas kerja = 1 file → diff kecil, history jelas per entitas.
- Perubahan besar pada kernel (`00`–`06` di root) wajib naik versi semantik di `00-INDEX.md` (`MAJOR.MINOR.PATCH`) dan dicatat di `06-SELF-AUDIT.md` § histori revisi.
- Field `updated` di metadata (§ 4.3) wajib diperbarui setiap kali file detail diubah substansial.

## 4.8 Strategi Context Engineering untuk AI (ringkasan actionable)

1. **Minimal-sufficient context**: AI/agent memuat index dulu, baru detail yang relevan — jangan pernah memuat seluruh `projects/` sekaligus.
2. **No orphan file**: setiap file detail wajib terdaftar di index folder induknya — file yang tidak terdaftar dianggap tidak resmi/harus diperbaiki.
3. **Metadata-first scanning**: saat mencari "task mana yang masih open", AI cukup scan metadata `status`, bukan isi penuh tiap task.
4. **Summary Block wajib**: 3–5 baris di atas tiap file detail berisi inti isi file, agar AI bisa memutuskan relevansi tanpa membaca full body.
5. **Otoritas eksplisit**: index selalu menyatakan file mana yang SSoT untuk topik apa, mencegah AI mengarang jawaban dari sumber yang salah/duplikat.
6. **Ukuran file dibatasi**: file detail yang membengkak >~400 baris dipecah menjadi sub-file + index baru (lihat ADR-001 di `01`), supaya satu file tidak pernah menjadi terlalu besar untuk dibaca utuh dengan efisien.
7. **Status eksplisit di metadata**: mencegah AI menganggap entitas kerja lama yang `status: archived` sebagai masih berlaku.

