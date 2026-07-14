# Templates — Index

> **Summary Block:** Peta 7 template siap pakai. Setiap entitas kerja baru wajib mulai dari sini, bukan dari file kosong.

| Template | Dipakai untuk | Skala |
|---|---|---|
| `TEMPLATE-backlog.md` | Capture ide/laporan sebelum masuk lifecycle, 1 file per intent (Feature/Refactor-Enhancement/Bug) | Sangat kecil, boleh diisi bulk |
| `TEMPLATE-project.md` | Membuat Project baru | Besar (multi-minggu/bulan) |
| `TEMPLATE-feature.md` | Menambah 1 Feature ke Project | Menengah |
| `TEMPLATE-task.md` | Task eksekusi individual | Kecil–menengah |
| `TEMPLATE-bugfix-enhancement-refactor.md` | Bug fix / enhancement / refactor / migration | Kecil–menengah |
| `TEMPLATE-decision-log.md` | Mencatat 1 keputusan penting | Sangat kecil, tapi wajib ada |
| `TEMPLATE-review-checklist.md` | Referensi 14 poin Mandatory Review Section (dipakai di dalam template lain) | Referensi, bukan berdiri sendiri |

**Aturan urutan pemakaian:** ide/laporan baru selalu mulai dari `TEMPLATE-backlog.md` (boleh bulk) → baru saat mulai diproses, pindah ke template entitas kerja penuh yang sesuai (satu-satu, lihat `05` SOP-00).

## Lightweight Mode (untuk task < 1 jam kerja)

Untuk pekerjaan sangat kecil (mis. ubah 1 baris config, perbaikan typo, penyesuaian style), seluruh Mandatory Review Section (`TEMPLATE-review-checklist.md`) boleh diringkas menjadi **1 baris per poin**, contoh:

```
## Mandatory Review Section (Lightweight)
- Potential Bugs: tidak ada, perubahan bersifat kosmetik
- Known Risks: tidak ada
- Edge Cases: n/a
- Failure Cases: n/a
- Negative Test Cases: n/a
- Regression Risk: rendah, hanya 1 file terdampak
- Rollback Plan: revert commit
- Validation Checklist: visual check OK
- Review Checklist: self-review OK
- Acceptance Checklist: sesuai permintaan
- User Testing Result: n/a
- Post Implementation Review: n/a
- Lessons Learned: n/a
- Future Improvement: n/a
```

Heading tetap wajib ada meski isinya singkat — ini menjaga konsistensi struktur untuk retrieval AI di masa depan (lihat `01` ADR-001).
