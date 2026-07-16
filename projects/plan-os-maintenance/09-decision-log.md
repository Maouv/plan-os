# Decision Log — plan-os-maintenance

> **Summary Block:** SSoT seluruh keputusan penting project ini. Entri baru
> ditambah di atas (paling baru paling atas).

---

> **Catatan editorial (2026-07-16):** Ditemukan `DEC-0002` di bawah tanpa
> `DEC-0001` mendahuluinya saat entri ini ditambahkan. Tidak ditebak/diisi
> ulang — mengikuti Mandatory Rule 05 §5.2 poin 9 ("jangan menebak, tanya
> user"). Entri baru di bawah diberi nomor `DEC-0003` untuk menghindari
> collision, bukan `DEC-0001`.

### DEC-0003: Versi paket `pos.py` (pyproject.toml) TIDAK ditautkan otomatis ke `Versi:` kernel di `00-INDEX.md` root
- **Tanggal:** 2026-07-16
- **Diputuskan oleh:** Maou (via sesi eksekusi ENH-0001)
- **Konteks/Masalah:** TEMP-06/ENH-0001 menambahkan `pyproject.toml` dengan
  `version = "1.1.0"` sebagai SSoT versi paket CLI `pos.py`. Angka ini
  kebetulan identik dengan `Versi: 1.1.0` di `00-INDEX.md` root (versi
  kernel spec Planning-OS). Pertanyaannya: apakah keduanya harus disatukan
  jadi satu SSoT tunggal?
- **Opsi yang dipertimbangkan:**
  1. Samakan paksa — jadikan `pyproject.toml` SSoT tunggal, `00-INDEX.md`
     tinggal merujuk ke sana.
  2. Biarkan keduanya independen secara eksplisit, dengan risiko dicatat.
  3. Berhenti dan tanya user sebelum lanjut.
- **Keputusan:** Opsi 2 — dibiarkan independen. Editing `00-INDEX.md` adalah
  perubahan kernel (Governance §5.3), sedangkan `pyproject.toml` adalah
  artefak tooling non-kernel; menyatukan keduanya lewat edit langsung ke
  `00-INDEX.md` di tengah item ENH-0001 (yang secara eksplisit bukan kernel
  change) akan melanggar batas scope yang sudah dikonfirmasi ke user di awal
  item ini.
- **Alasan:** Versi paket CLI (`pos.py`) dan versi spec kernel Planning-OS
  adalah dua topik konseptual berbeda yang kebetulan bernilai sama saat ini
  — bukan satu fakta yang didefinisikan dua kali (jadi tidak melanggar
  Mandatory Rule 05 §5.2 poin 2 secara harfiah), tapi cukup mirip untuk
  berisiko disalahpahami sebagai SSoT yang sama oleh sesi AI berikutnya.
- **Dampak/Konsekuensi:** Kedua angka versi bisa divergen di masa depan
  (mis. `pos.py` naik ke 1.2.0 karena bug fix, tanpa kernel docs berubah)
  — ini WAJAR dan BUKAN bug, dicatat di sini supaya sesi berikutnya tidak
  menganggapnya sebagai drift yang perlu "diperbaiki" tanpa konteks ini.
- **Terkait:** [ENH-0001](08-refactor-and-enhancement/enh-0001-pos-py-packaging-test-suite.md)

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

