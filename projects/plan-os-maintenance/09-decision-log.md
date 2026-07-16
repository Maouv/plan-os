# Decision Log — plan-os-maintenance

> **Summary Block:** SSoT seluruh keputusan penting project ini. Entri baru
> ditambah di atas (paling baru paling atas).

---

### DEC-0002: Tidak membuat file `AGENTS.md`/`CLAUDE.md` terpisah sebagai pointer
- **Tanggal:** 2026-07-16
- **Diputuskan oleh:** (isi nama/owner)
- **Konteks/Masalah:** Sesi sebelumnya sempat mengusulkan file pointer
  khusus (`.plan-os/AGENTS.md` + import line di `CLAUDE.md`) supaya agent
  otomatis tahu ada Plan-OS tanpa dijelaskan tiap sesi.
- **Opsi yang dipertimbangkan:**
  1. File pointer terpisah (`AGENTS.md`/stub `CLAUDE.md`).
  2. Andalkan `SKILL.md` yang sudah ada sebagai satu-satunya entry point
     agent, tanpa file tambahan.
- **Keputusan:** Opsi 2 — tidak membuat `AGENTS.md`/`CLAUDE.md` terpisah.
- **Alasan:** Target penggunaan utama adalah host yang skill-capable
  (Claude Code, Codex, OpenCode) yang sudah otomatis membaca `SKILL.md`
  lewat standar Agent Skills — file pointer tambahan jadi redundan untuk
  audiens itu. Trade-off yang disadari: host non-skill-capable (Cursor,
  Copilot, Windsurf, dst) tidak akan dapat context Plan-OS sama sekali
  tanpa `AGENTS.md`, tapi ini diterima karena bukan target utama saat ini.
- **Dampak/Konsekuensi:** TEMP-02 (family skill/command) dipersempit — tidak
  ada lagi sub-scope pointer file terpisah. Kalau nanti ada kebutuhan nyata
  dukungan host non-skill-capable, keputusan ini dibuka ulang lewat entri
  Decision Log baru, bukan diam-diam ditambahkan.
- **Terkait:** TEMP-02 (backlog-features.md)

---
