# pos.py — Planning-OS Enforcer

Empat hal yang tadinya cuma aturan/niat tertulis di Planning-OS, sekarang
divalidasi otomatis:

1. **Orphan file, index nggak sinkron, metadata hilang, file kegedean, ID
   duplikat, link rusak** → dicek dengan `validate`.
2. **ID tabrakan** (dua entitas kebetulan dapat `TASK-0102` yang sama karena
   dua sesi AI jalan terpisah) → dicegah dengan `new-id --claim`.
3. **Circular dependency** antar entitas (`FEAT-0001 depends_on FEAT-0002`
   dan sebaliknya) yang bikin SOP-00 poin 4/5 ("urutan pemrosesan berdasarkan
   dependency") mustahil dijalankan → dideteksi dengan `depgraph`.
4. **Entitas yang diam-diam mangkrak** — status masih `in-progress`/`planning`
   tapi field `updated` sudah lama nggak berubah → di-flag dengan
   `validate --stale-days N`, nutup gap "Freshness check berkala" di 05 §5.4
   yang di dokumen aslinya nggak pernah didefinisikan jadi angka konkret.

Tidak butuh install apa-apa (stdlib only) — cocok dijalankan langsung di
Contabo VPS via Termux.

## Pakai

```bash
# Validasi satu project instance (folder projects/<slug>/)
python3 pos.py validate projects/graps

# Sama, plus flag entitas aktif yang tidak diupdate > 14 hari
python3 pos.py validate projects/graps --stale-days 14

# Minta ID baru (cuma scan, tidak mengunci)
python3 pos.py new-id projects/graps FEAT

# Minta ID baru DAN kunci di ledger — pakai ini kalau beneran mau dipakai
# supaya sesi lain nggak dapat ID yang sama
python3 pos.py new-id projects/graps TASK --claim

# Cek dependency graph: circular dependency + urutan pemrosesan yang aman
python3 pos.py depgraph projects/graps
```

Exit code `0` = bersih, `1` = ada error (termasuk circular dependency di
`depgraph`). Bisa dipasang di pre-commit hook atau dijadikan bagian dari
SOP-04 (closing) sebelum status diubah jadi `done`.

## Yang dicek `validate`

| Cek | Sumber aturan di Planning-OS |
|---|---|
| Folder >3 file wajib punya `00-INDEX.md` | 05 §5.2 poin 3 |
| File detail wajib punya metadata header | 04 §4.3 |
| File detail wajib punya Summary Block | 04 §4.8 rule 4 |
| ID di metadata tidak boleh duplikat | temuan audit (ID collision) |
| File wajib terdaftar di index folder induk (bukan orphan) | 04 §4.8 rule 2 |
| File > 400 baris → warning untuk dipecah | 01 ADR-001 rule 5 |
| Status `done` tapi tidak ada Post Implementation Review | 03 §3.4 DoD |
| Link relatif ke file yang tidak ada (dead link) | 04 §4.6 |
| Backlog item dicentang tapi tidak ditandai `→ moved to` | 04 §4.2a |

## Yang dicek `depgraph`

- Membaca field `depends_on` di semua entitas (FEAT/TASK/BUG/ENH/REF), bangun
  graph-nya.
- Kalau ada circular dependency (A→B→A, atau siklus lebih panjang) →
  dilaporkan sebagai **error**, exit code 1, karena ini bikin urutan
  pemrosesan (SOP-00 poin 4/5) mustahil dihitung — harus dibetulkan dulu
  sebelum lanjut.
- Kalau `depends_on` menunjuk ke ID yang nggak ada file-nya sama sekali →
  warning (mungkin typo ID, atau entitasnya belum dibuat).
- Kalau graph bersih → cetak **urutan pemrosesan yang valid** (topological
  sort): dependency selalu muncul lebih dulu dari yang bergantung padanya.
  Ini yang dulunya cuma dikerjakan manual/ditebak oleh AI/manusia yang baca
  file satu-satu.

## Kenapa dibuat

Audit sebelumnya nemuin satu titik lemah paling nyata di Planning-OS:
semua "wajib" di dokumen itu cuma teks, nggak ada yang benar-benar
memvalidasi. Dokumentasi tanpa enforcement biasanya membusuk pelan-pelan
begitu disiplin menurun. Script ini nggak menggantikan Planning-OS —
cuma memastikan aturan yang sudah ditulis beneran dipatuhi, otomatis,
tiap kali dicek.

## Batasan yang jujur diakui

- Cek "Post Implementation Review" itu heuristik teks (`cari substring`),
  bukan parser semantik — bisa false positive/negative kalau isinya beda
  format.
- Belum ada auto-fix — cuma laporan. Masih manual untuk perbaikannya
  (sengaja, biar nggak diam-diam mengubah keputusan orang).
- `new-id` tidak tahu soal ID yang di-reserve tapi belum ditulis ke file
  manapun — makanya ada `--claim` + ledger lokal (`.pos-id-ledger.json`)
  untuk kasus itu.
