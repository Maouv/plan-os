# Backlog — Features (plan-os-maintenance)

> **Summary Block:** Kapabilitas baru yang belum ada di Plan-OS sama
> sekali. Item di sini murah dicatat, belum tentu dikerjakan.

- [ ] TEMP-01 — `pos.py show <ID>` / `pos.py tree <slug>` — reader CLI
  read-only, cetak metadata + status review section tanpa buka file mentah
  — dicatat 2026-07-16 — sudah ada draft FEAT lengkap di luar sistem
  (belum diberi ID resmi).
- [ ] TEMP-02 — Family skill/command `plan-os` (`.claude/skills/`, dan
  integrasi ke Codex/OpenCode sesuai pola Agent Skills yang sudah
  dikonfirmasi ke Claude Code/Codex/OpenCode/Gemini CLI/Cursor) — dicatat
  2026-07-16 — sudah ada draft FEAT, perlu direvisi: bagian "slash command
  layer custom" dibuang, diganti "distribusi SKILL.md ke folder discovery
  tiap tool" + `pos.py install-integration <tool>` sebagai helper install.
- [ ] TEMP-03 — `pos.py checkpoint` — auto `git add` + commit dengan pesan
  terstandar berisi ID entity (mis. `[FEAT-0042] status → in-progress`),
  dipanggil di titik SOP-04 (closing) dan SOP-05 (end-of-session
  checkpoint) yang sudah ada — dicatat 2026-07-16 — menjawab kebutuhan
  "commit history" tanpa membangun sistem versioning sendiri (`04` § 4.7
  sudah menyatakan sistem git-friendly by design, ini yang mengoperasikan
  niat itu jadi SOP konkret).
- [ ] TEMP-04 — Archive compaction — mekanisme supaya
  `99-archive/00-INDEX.md` tetap ringkas setelah bertahun-tahun (mis. digest
  periodik per kuartal/tahun, isi ringkas 1 baris per entitas lama, file
  detail aslinya tetap ada tidak dihapus) — dicatat 2026-07-16 — celah nyata
  di `05` § 5.4 Maintenance Strategy yang belum membahas pertumbuhan
  archive jangka panjang.
