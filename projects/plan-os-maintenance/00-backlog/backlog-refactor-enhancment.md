# Backlog — Refactor/Enhancement (plan-os-maintenance)

> **Summary Block:** Perbaikan struktur/kualitas pada sesuatu yang sudah
> ada dan berjalan — bukan kapabilitas baru.

- [ ] TEMP-05 — Root repo reorg: `issue/` → `field-reports/` (plural,
  hindari tabrakan makna dengan GitHub Issues), `_examples/` → `examples/`
  (buang underscore, konsisten dengan `templates/`), `pos.py` → `tools/
  pos.py` (pisah implementasi enforcer dari spec yang di-enforce). `00`–`06`
  di root **tidak** dipindah — tetap flat, konsisten dengan pola scaffold
  project sendiri (`00-backlog/`, `01-discovery/`, dst juga flat bernomor
  di root project). Wajib update semua path reference di `SKILL.md`/README
  yang nyebut `issue/...` — kalau lupa, ini persis kelas bug yang sudah
  pernah ketemu sendiri (dead link di Quick Start, severity High) — dicatat
  2026-07-16 — ini perubahan kernel, wajib lewat Governance § 5.3 (Change
  Proposal di `06-SELF-AUDIT.md`), bukan edit langsung.
- [x] TEMP-06 — `pos.py` packaging + test suite → moved to
  [ENH-0001](../08-refactor-and-enhancement/enh-0001-pos-py-packaging-test-suite.md)
- [ ] TEMP-07 — SOP-07 baru di `05` (SOP-06 sudah dipakai "Mengubah Kernel
  Planning-OS Itu Sendiri" — jangan tabrakan nomor): "Git Checkpoint
  Convention" — format pesan commit wajib terikat ID entity, kapan wajib
  commit (tiap SOP-04/SOP-05). Ini perubahan kernel (nambah SOP di `05`),
  butuh Change Proposal § 5.3 sebelum dieksekusi — bergantung pada TEMP-03
  (`pos.py checkpoint`) supaya konvensinya dienforce otomatis (mis. gate
  commit sampai `updated:` + Session Log terisi), bukan cuma aturan di
  kertas yang bergantung AI inget sendiri — dicatat 2026-07-16.

