# Contoh Terisi — Planning-OS

> **Summary Block:** Folder ini berisi contoh nyata tiap template di `templates/` sudah diisi penuh, memakai kasus project **graps** (code dependency visualization tool) sebagai studi kasus. Tujuannya: referensi konkret, bukan dokumen aktif — jangan diedit sebagai project sungguhan.

| File | Template Acuan | Isi |
|---|---|---|
| `EXAMPLE-project-graps.md` | `TEMPLATE-project.md` | Contoh project penuh: discovery → closing |
| `EXAMPLE-feature-dom-tree-renderer.md` | `TEMPLATE-feature.md` | Contoh feature: Phase 6 DOM tree-view renderer |
| `EXAMPLE-task-fix-edge-rendering.md` | `TEMPLATE-task.md` | Contoh task turunan dari feature di atas |
| `EXAMPLE-bug-file-node-not-rectangle.md` | `TEMPLATE-bugfix-enhancement-refactor.md` | Contoh bugfix dengan root cause analysis |
| `EXAMPLE-decision-log.md` | `TEMPLATE-decision-log.md` | Contoh decision log dengan 2 entri |
| `EXAMPLE-lifecycle-walkthrough-bug-0012.md` | `03-LIFECYCLE-AND-REVIEW-SYSTEM.md` § 3.1 | Contoh audit trail eksplisit ke-27 tahap lifecycle untuk 1 entitas kerja (BUG-0012) |

Alur baca yang disarankan: `EXAMPLE-project-graps.md` → `EXAMPLE-feature-*.md` → `EXAMPLE-task-*.md` → `EXAMPLE-bug-*.md` → `EXAMPLE-decision-log.md`. Ini mencerminkan hierarki nyata: project berisi feature, feature dipecah jadi task, bug ditemukan saat implementasi, keputusan dicatat terpisah di decision log.

`EXAMPLE-lifecycle-walkthrough-bug-0012.md` adalah dokumen terpisah (opsional) — dipakai hanya saat butuh audit trail tahap-per-tahap secara eksplisit (compliance/post-mortem besar), bukan pengganti dokumen bugfix harian di `EXAMPLE-bug-file-node-not-rectangle.md`.
