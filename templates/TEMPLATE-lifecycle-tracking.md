# Lifecycle Stage Tracking (Reference Block)

> Salin **salah satu** varian di bawah ini apa adanya ke bagian
> `## Lifecycle Stage Tracking` di Project/Feature/Task/Bug Fix/Enhancement/
> Refactor. Jangan enumerasi ke-27 tahap di § 3.1 satu per satu selama
> entitas belum `in-progress` — itu boilerplate, bukan sinyal, dan bikin
> file jadi ratusan baris tanpa nambah informasi (lihat catatan di
> `03-LIFECYCLE-AND-REVIEW-SYSTEM.md` § 3.1.1).

## Compact Form
**Wajib dipakai** selama `status:` masih salah satu dari:
`idea | discovery | backlog | ready | planning`.

```
## Lifecycle Stage Tracking
Compact — belum ada stage yang dimulai (27 tahap, lihat 03 §3.1).
Akan di-expand ke Expanded Form begitu `status` naik ke `in-progress`.
```

## Expanded Form
**Wajib dipakai** begitu `status:` mencapai `in-progress`, `review`, `done`,
atau status "lebih lanjut" lain yang setara. Hanya tulis baris **per-stage**
untuk klaster yang **sedang atau sudah** dijalani; klaster yang belum
tersentuh sama sekali tetap 1 baris ringkas per klaster (bukan per stage) —
jangan tulis 27 baris "Not started" sekaligus.

```
## Lifecycle Stage Tracking
### Klaster 1 — Discovery: Done (lihat § 1)
### Klaster 2 — Planning & Design: Done (lihat § 3–4)
### Klaster 3 — Build: In Progress
- Implementation: In Progress
- Self Review: Not started
- AI Review: Not started
- Code Review: Not started
### Klaster 4 — Verification: Not started
### Klaster 5 — Validation dengan User: Not started
### Klaster 6 — Release & Closing: Not started

### Session Log
_(append 1–3 baris per sesi kerja — JANGAN ditimpa, ini histori. Wajib
diisi sebelum sesi AI berhenti kerja di entitas ini, lihat 05 SOP-05)_
- 2026-07-14: Implementation komponen X dimulai, Y dari Z sub-task selesai.
```

Begitu sebuah klaster selesai 100%, boleh diringkas balik jadi satu baris
`Klaster N — <nama>: Done (lihat § ...)`. Yang wajib dipertahankan bukan
riwayat 27 baris selamanya — yang wajib adalah **tidak ada stage yang
dilewati tanpa pernah tercatat statusnya** saat entitas sedang aktif
dikerjakan. Session Log, sebaliknya, memang wajib diakumulasi (append-only)
selama entitas aktif — itu pengganti murah untuk histori chat yang hilang
antar sesi.

> Aturan dasar dari § 3.1 tetap berlaku: heading tahap/klaster tidak boleh
> dihapus sepenuhnya, dan `Not Applicable — <alasan>` tetap sah untuk stage
> yang memang tidak relevan bagi entitas ini (mis. "User Testing: Not
> Applicable — internal tooling, tidak ada user eksternal").

> **Dilarang mengarang istilah status/gate baru** di luar `VALID_STATUSES`
> (`pos.py`) dan nama 27 tahap di `03` § 3.1 — contoh yang DILARANG: "Not
> started — implementation is not yet authorized". `status:` field di
> metadata **sudah** menyatakan boleh/tidaknya implementasi mulai
> (`planning` = belum boleh, `in-progress` = sedang jalan); menambahkan
> kalimat gate sendiri di lifecycle tracking cuma menambah ambiguitas yang
> harus ditebak ulang tiap sesi. Kalau memang ada gate approval manusia yang
> sungguhan di luar status field, catat di Decision Log (`09-decision-log.md`),
> bukan di sini.

