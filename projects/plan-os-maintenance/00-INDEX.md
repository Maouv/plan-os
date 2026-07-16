---
project: plan-os-maintenance
status: idea
created: 2026-07-16
updated: 2026-07-16
---

# Planning-OS Maintenance — Project Index

> **Summary Block:** Project internal untuk memelihara Plan-OS itu sendiri
> (referensi: `05-SOP-GOVERNANCE-MAINTENANCE.md` § 5.4 — "Planning-OS
> memelihara dirinya sendiri memakai pola yang sama"). Sebelumnya
> direferensikan di §5.4 tapi belum pernah benar-benar dibuat sebagai
> project instance. Semua temuan maintenance, gap tooling, dan usulan
> kernel masuk ke sini dulu sebagai backlog sebelum naik jadi entitas kerja
> penuh.

## Status
Idea — baru capture layer (`00-backlog/`), belum ada satu pun yang naik ke
Requirement/Planning.

## Struktur
- `00-backlog/` — capture layer, dipisah per intent (lihat `04` § 4.2a).
- Folder lain (`05-features/`, `07-bugs-and-fixes/`,
  `08-refactor-and-enhancement/`, `09-decision-log.md`, dst) dibuat saat
  item pertama naik dari backlog ke lifecycle penuh — belum dibuat semua
  sekarang biar tidak ada folder kosong tanpa isi (menghindari orphan
  struktur, lihat `04` § 4.8 rule 2).

## Catatan Penting
- Beberapa item di backlog ini (reader CLI, skill/command layer) **sudah**
  punya draft FEAT lengkap dari sesi sebelumnya di luar project ini —
  begitu di-claim ID resmi via `pos.py new-id`, draft itu tinggal dipindah
  ke `05-features/` project ini, bukan ditulis ulang dari nol.
