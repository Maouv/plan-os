# 01 — Research Summary & Architecture Decision Record (ADR)

> **Summary Block:** Dokumen ini menjawab dua hal: (1) ringkasan riset praktik planning terbaik dari enterprise, startup, SDLC, PM, dan AI context engineering; (2) keputusan arsitektur final — **Hybrid: Index/Summary Layer + Detail Layer per folder** — beserta alasan penuh dan tradeoff yang ditolak.

---

## 1.1 Ringkasan Riset

### A. Bagaimana Enterprise Melakukan Planning
Perusahaan besar (Google, Microsoft, Amazon) memisahkan planning ke **lapisan waktu dan lapisan detail**: Vision/Strategy (tahunan, sangat ringkas) → OKR kuartalan (ringkas, terukur) → Roadmap inisiatif (menengah) → Eksekusi (Epic/Task, sangat detail, hidup di tracker terpisah seperti Jira). Polanya selalu: **dokumen strategis pendek dan stabil, dokumen eksekusi panjang dan sering berubah, dan keduanya saling me-reference, bukan saling menyalin isi.** Amazon menambahkan disiplin "Working Backwards" (PR/FAQ) — mulai dari hasil akhir, bukan dari fitur.

### B. Bagaimana Startup Melakukan Planning
Startup memprioritaskan kecepatan iterasi: Lean Startup (Build-Measure-Learn), Shape Up (Basecamp) dengan siklus 6 minggu tanpa backlog raksasa, dan "just enough documentation". Pelajaran kunci untuk sistem ini: **jangan bebani task kecil dengan proses berat** — tapi tetap simpan disiplin review minimal, hanya diperingan formatnya (lihat MoSCoW/RICE untuk prioritas cepat).

### C. Software Development Lifecycle (SDLC)
Semua model (Waterfall, V-Model, Agile, DevOps) sepakat pada satu invarian: **tidak ada tahap implementasi yang berdiri sendiri tanpa requirement di depannya dan verifikasi di belakangnya.** DevOps menambahkan loop monitoring→feedback yang sering dilupakan dokumentasi tradisional. Sistem ini mewajibkan loop itu secara eksplisit di lifecycle (lihat `03`).

### D. Product Management Lifecycle
Pola umum: Discovery (riset masalah) dipisah tegas dari Delivery (eksekusi solusi). Kesalahan paling umum di tim yang lemah adalah melompat dari "ide" langsung ke "task teknis" tanpa mendefinisikan Problem Statement dan Success Metric. Sistem ini memaksa tahap Idea → Research → Analysis → Requirement sebagai gerbang wajib sebelum Design/Architecture.

### E. Project Management Lifecycle (PMBOK/PRINCE2)
Struktur klasik: Initiating → Planning → Executing → Monitoring & Controlling → Closing. Kontribusi pentingnya ke sistem ini: **Closing adalah fase formal**, bukan "berhenti kerja". Post Implementation Review dan Lessons Learned adalah deliverable wajib, bukan opsional — inilah yang paling sering hilang di tim engineering biasa dan menjadi salah satu pilar wajib sistem ini.

### F. Knowledge Management Terbaik
Praktik terbaik (Confluence/Notion enterprise, Zettelkasten, Diátaxis): pemisahan tegas antara **jenis konten** — Reference (fakta stabil), Explanation (kenapa), How-to (langkah), Tutorial (belajar) — dan **jangan campur** dalam satu dokumen. Prinsip "satu sumber, banyak link" (bukan "banyak sumber, banyak copy") adalah fondasi Single Source of Truth. Sistem ini mengadopsi pemisahan Diátaxis pada level template (lihat `04`).

### G. AI dan Dokumen Besar / Context Window
Fakta teknis yang relevan:
- Context window AI **terbatas dan mahal**; setiap token yang tidak relevan menggeser kapasitas reasoning dan meningkatkan risiko "lost in the middle" (informasi di tengah dokumen panjang cenderung diabaikan model).
- AI membaca folder/banyak file **jauh lebih efisien** ketika ada index/manifest eksplisit dibanding harus membuka semua file untuk tahu isinya (mirip retrieval index vs full scan).
- Model cenderung berhalusinasi lebih tinggi ketika: (a) informasi yang dibutuhkan tersebar tanpa penanda jelas, (b) ada duplikasi informasi yang saling bertentangan, (c) tidak ada sinyal "dokumen mana yang otoritatif".
- Retrieval efektif membutuhkan **chunking yang selaras dengan batas makna** (per-file per-topik), bukan potongan sembarang di tengah bab.

### H. Best Practice Context Engineering & Prompt Engineering
Prinsip inti (selaras dengan panduan resmi Anthropic tentang context engineering): berikan model **konteks minimal-cukup** (minimal sufficient context), bukan maksimal. Gunakan struktur eksplisit (heading, tag, metadata) agar model bisa navigasi tanpa membaca linear. Pisahkan instruksi stabil (jarang berubah) dari data dinamis (sering berubah) — ini alasan Planning-OS memisahkan "kernel" (00–06, jarang berubah) dari "instance" (folder project, berubah terus).

### I. Best Practice Knowledge & Documentation Architecture
Pola yang terbukti scalable: **Summary-first design** — setiap dokumen besar dibuka dengan ringkasan 3–5 baris di paling atas (di sistem ini disebut Summary Block) sehingga baik manusia maupun AI bisa memutuskan apakah perlu membaca lebih jauh tanpa memuat seluruh isi.

---

## 1.2 Analisis: Satu File Besar vs Satu Folder Banyak File vs Hybrid

| Kriteria | A. Satu File Besar | B. Folder Banyak File | C. Hybrid (dipilih) |
|---|---|---|---|
| Context Window | Buruk — seluruh isi harus dimuat meski hanya butuh 1 bagian | Baik — AI muat file sesuai kebutuhan | Baik — index ringan dimuat dulu, detail dimuat sesuai kebutuhan |
| AI Memory / Lost-in-the-middle | Buruk — bagian tengah file panjang mudah terlewat | Baik — tiap file fokus 1 topik | Baik |
| Retrieval | Buruk — pencarian harus full-text scan 1 file raksasa | Baik jika ada index; buruk jika tidak ada | Baik — index eksplisit + isi granular |
| Scalability (bertahun-tahun, ratusan project) | Sangat buruk — file akan menjadi ribuan baris tak terkelola | Baik | Sangat baik |
| Context Hygiene | Buruk — topik tercampur | Baik jika disiplin naming dijaga | Baik + dijaga metadata & naming convention |
| Maintainability | Buruk — 1 edit kecil berisiko merusak struktur besar | Baik — edit terisolasi per file | Baik |
| Modularitas | Tidak ada | Tinggi | Tinggi |
| Human Readability | Baik untuk dokumen pendek, buruk untuk besar | Baik, tapi butuh disiplin navigasi | Baik, dengan index membantu orientasi |
| AI Readability | Buruk untuk besar | Baik, tapi tanpa index AI harus menebak file mana yang relevan (boros tool-call) | Terbaik — index memberi peta langsung |
| Navigation | Buruk untuk dokumen panjang | Bisa membingungkan tanpa index (folder dalam, nama tidak konsisten) | Baik — 1 pintu masuk (`00-INDEX.md`) di tiap level |
| Performance (load/parse) | Buruk untuk besar | Baik | Baik |
| Versioning (git-friendly) | Buruk — diff besar tiap perubahan kecil, conflict tinggi | Baik — diff kecil, jelas file mana yang berubah | Baik |
| Collaboration (multi-orang/multi-agent) | Buruk — rebutan 1 file | Baik — kerja paralel per file | Baik |
| Expansion (project baru, tim baru) | Buruk — file makin membengkak | Baik — tinggal tambah folder baru mengikuti pola | Sangat baik — pola scaffold jelas |
| Knowledge Separation | Tidak ada | Ada, tapi bisa berlebihan (over-fragmentasi jika tanpa aturan) | Ada, dengan batas jelas (lihat `04`) |
| Context Pollution | Tinggi — semua topik tercampur satu ruang | Rendah, tapi bisa muncul via duplikasi antar file | Rendah — dijaga oleh SSoT + no-duplication rule |
| Duplicate Information | Cenderung tinggi (copy-paste dalam 1 file panjang) | Bisa tinggi jika tanpa disiplin | Rendah — dipaksa via SSoT + cross-reference, bukan copy |
| Single Source of Truth | Sulit dijaga di file superpanjang | Bisa dijaga per file, tapi butuh index agar diketahui mana yang otoritatif | Terjaga — index eksplisit menyatakan otoritas tiap topik |

### Tradeoff yang Ditolak
- **Opsi A (satu file besar)** ditolak karena gagal di hampir semua kriteria begitu skala bertambah — cocok hanya untuk dokumen sangat pendek (mis. satu README ringkas), bukan sistem jangka panjang.
- **Opsi B murni (folder tanpa index/metadata terstandar)** ditolak karena risiko *navigation chaos*: AI dan manusia baru akan membuang waktu/tool-call untuk "menebak" struktur, dan file yang berdiri sendiri tanpa index cenderung berujung duplikasi karena orang tidak tahu informasi X sudah ada di file mana.

## 1.3 Keputusan Final (ADR-001)

**Keputusan:** Gunakan **Hybrid — Index/Summary Layer + Detail Layer**, dengan aturan:
1. Setiap folder **wajib** punya 1 file index (`00-INDEX.md` atau README setara) yang memetakan isi folder dan menyatakan otoritas topik.
2. Setiap file detail **wajib** punya Summary Block di baris atas.
3. Dokumen "kernel" (prinsip, lifecycle, vocabulary — jarang berubah) dipisah tegas dari dokumen "instance" (project/feature/task spesifik — sering berubah).
4. Tidak ada topik yang boleh didefinisikan di lebih dari satu tempat; tempat lain hanya boleh me-*link*.
5. Ukuran file detail dijaga wajar (target < ±400 baris/topik) — jika membengkak, dipecah menjadi sub-file dan diberi index baru, bukan dibiarkan tumbuh.

**Status:** Accepted. Reviewed setiap kali sistem terasa berat/lambat dinavigasi (lihat `06-SELF-AUDIT.md`).
