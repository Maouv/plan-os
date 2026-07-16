---
project: plan-os-maintenance
status: in-progress
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
In Progress — [ENH-0001](08-refactor-and-enhancement/enh-0001-pos-py-packaging-test-suite.md)
(TEMP-06, `pos.py` packaging + test suite) `done` per 2026-07-16. 6 item
backlog lain (TEMP-01–05, 07) belum diproses — lihat `00-backlog/` dan
urutan eksekusi disarankan di `SYSTEM-PROMPT.md`.

## Struktur
- `00-backlog/` — capture layer, dipisah per intent (lihat `04` § 4.2a).
- `08-refactor-and-enhancement/` — dibuat saat ENH-0001 (TEMP-06) naik dari
  backlog (2026-07-16).
- `09-decision-log.md` — dibuat sebelum project ini, sudah berisi `DEC-0002`
  (lihat catatan editorial di file tersebut soal gap `DEC-0001`).
- Folder lain (`05-features/`, `07-bugs-and-fixes/`, dst) belum dibuat —
  belum ada item backlog yang butuh folder tersebut (menghindari orphan
  struktur, lihat `04` § 4.8 rule 2).

## Catatan Penting
- Beberapa item di backlog ini (reader CLI, skill/command layer) **sudah**
  punya draft FEAT lengkap dari sesi sebelumnya di luar project ini —
  begitu di-claim ID resmi via `pos.py new-id`, draft itu tinggal dipindah
  ke `05-features/` project ini, bukan ditulis ulang dari nol.

