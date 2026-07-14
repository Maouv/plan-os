# PLANNING OPERATING SYSTEM (Planning-OS) — Master Index

> Versi: 1.1.0 · Status: Active · Owner: PMO/Architecture Council
> Dokumen ini adalah **entry point tunggal**. Baik manusia maupun AI harus mulai dari sini sebelum membaca dokumen lain.

## 0.1 Apa Ini

Planning-OS bukan template project plan. Ini adalah **sistem operasi untuk perencanaan** — aturan, struktur, vocabulary, lifecycle, dan mekanisme review yang dipakai berulang untuk *setiap* project, feature, task, bug fix, enhancement, refactor, migration, experiment, maupun produk baru, selama bertahun-tahun ke depan.

Analogi: 00–06 di folder ini adalah "kernel + dokumentasi OS". Folder `templates/` adalah "aplikasi bawaan" yang dijalankan di atas kernel itu. Setiap project baru = instance baru yang mengikuti kontrak yang sama.

## 0.2 Peta Dokumen (baca sesuai kebutuhan, bukan berurutan)

| # | File | Isi | Kapan Dibaca |
|---|------|-----|---------------|
| 00 | `00-INDEX.md` | Peta navigasi, quick start | Selalu, pertama kali |
| 01 | `01-RESEARCH-AND-ARCHITECTURE-DECISION.md` | Riset best-practice + keputusan arsitektur (kenapa hybrid) | Saat onboarding / saat mempertanyakan struktur |
| 02 | `02-VOCABULARY-AND-FRAMEWORKS.md` | Kamus istilah + library framework (OKR, RICE, WBS, dst) | Saat menulis dokumen planning, butuh istilah baku |
| 03 | `03-LIFECYCLE-AND-REVIEW-SYSTEM.md` | Lifecycle wajib 27 tahap + sistem review wajib | Setiap kali memulai/mengeksekusi pekerjaan |
| 04 | `04-KNOWLEDGE-ARCHITECTURE-AND-CONTEXT-ENGINEERING.md` | Struktur folder/file nyata, metadata, strategi context AI | Saat membuat project/folder baru |
| 05 | `05-SOP-GOVERNANCE-MAINTENANCE.md` | SOP operasional, aturan wajib, governance, maintenance, scalability | Saat menjalankan proses sehari-hari, audit, atau scaling |
| 06 | `06-SELF-AUDIT.md` | Audit desain sistem ini sendiri + histori revisi | Saat mengevaluasi/mengubah Planning-OS itu sendiri |
| — | `templates/` | Template siap pakai (project, feature, task, bugfix, decision log, review checklist) | Setiap kali membuat entitas kerja baru |

## 0.3 Aturan Baca untuk AI (Context Hygiene)

1. **Jangan pernah load seluruh folder sekaligus.** Muat hanya file yang relevan dengan tugas saat ini.
2. Untuk *membuat entitas kerja baru* (project/feature/task/bug): cukup baca `00-INDEX.md` → `04` (struktur folder) → template terkait di `templates/`. Tidak perlu baca `01` atau `06`.
3. Untuk *menjawab pertanyaan "kenapa sistem ini begini"*: baca `01` dan `06`.
4. Untuk *audit/compliance*: baca `03` (review system) dan `05` (governance).
5. Setiap file di sistem ini punya **Summary Block** di baris paling atas (setelah judul) — AI cukup baca Summary Block dulu untuk memutuskan apakah perlu baca full body.
6. Sumber kebenaran (Single Source of Truth) untuk tiap topik hanya ada di **satu file**. Jika informasi tampak terduplikasi di file lain, itu adalah **link/reference**, bukan definisi ulang — laporkan sebagai bug dokumentasi jika ditemukan duplikasi nyata.

## 0.4 Quick Start — 4 Skenario Umum

- **"Saya mau mulai project baru"** → `04` (struktur folder) § Project Scaffold → `templates/TEMPLATE-project.md`
- **"Saya mau tambah 1 feature ke project yang sudah ada"** → `templates/TEMPLATE-feature.md`, taruh di `project-x/02-features/`
- **"Ada bug"** → `templates/TEMPLATE-bugfix.md`
- **"Saya mau tahu apakah proses saya sudah sesuai standar"** → `03-LIFECYCLE-AND-REVIEW-SYSTEM.md`
- **"Saya mau catat banyak ide/fitur/bug sekaligus"** → `05-SOP-GOVERNANCE-MAINTENANCE.md` SOP-00 → `templates/TEMPLATE-backlog.md` (pisahkan per intent, jangan campur feature/refactor/bug dalam satu daftar)

## 0.5 Prinsip Inti (non-negotiable, lihat detail di 05)

1. Single Source of Truth per topik.
2. Tidak ada pekerjaan yang "selesai" tanpa melalui Review System wajib (lihat 03).
3. Setiap file besar wajib punya Summary Block agar context-efficient bagi AI.
4. Struktur adalah hybrid: index/summary layer (ringan) + detail layer (folder per entitas) — lihat `01` untuk rasionalnya.
5. Semua keputusan besar dicatat di Decision Log — tidak boleh hanya di chat/memory personal.
