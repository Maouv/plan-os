# 02 — Vocabulary & Frameworks Library

> **Summary Block:** Kamus istilah baku (agar semua orang & AI memakai kata yang sama untuk hal yang sama) dan katalog framework, masing-masing sebagai unit **berdiri sendiri** (tidak dicampur jadi satu daftar tips) sehingga bisa dirujuk satu-per-satu tanpa membaca semuanya.

---

## 2.1 Kamus Istilah (Vocabulary), dikelompokkan per lapisan

### Lapisan Strategis (jarang berubah, level tahunan)
| Istilah | Definisi Baku dalam Sistem Ini |
|---|---|
| Vision | Kondisi jangka panjang (3–5+ tahun) yang ingin dicapai. Tidak terukur secara ketat. |
| Mission | Alasan keberadaan tim/produk saat ini. |
| North Star (Metric) | Satu metrik tunggal yang paling mewakili nilai yang diberikan ke user. |
| Strategy | Pendekatan besar untuk mencapai Vision; pilihan "mana yang TIDAK dikerjakan" termasuk di sini. |

### Lapisan Tujuan Terukur (level kuartal)
| Istilah | Definisi |
|---|---|
| Goal | Tujuan kualitatif jangka menengah. |
| Objective | Pernyataan tujuan dalam OKR — kualitatif, inspiratif. |
| Key Result | Ukuran kuantitatif keberhasilan Objective. |
| KPI | Metrik operasional berkelanjutan (bukan sekali capai lalu selesai, beda dengan Key Result). |
| OKR | Objective + Key Result, kerangka penetapan tujuan kuartalan. |

### Lapisan Eksekusi (roadmap → task)
| Istilah | Definisi |
|---|---|
| Roadmap | Urutan Initiative dari waktu ke waktu untuk mencapai Strategy. |
| Initiative | Upaya besar lintas-Epic yang menggerakkan satu Key Result. |
| Epic | Kumpulan Feature yang menyelesaikan satu Initiative. |
| Capability | Kemampuan sistem yang dihasilkan (lebih abstrak dari Feature, bisa berisi banyak Feature). |
| Feature | Unit fungsi yang dirasakan langsung oleh user. |
| Project | Unit kerja dengan awal-akhir jelas untuk menghasilkan satu atau lebih Feature/Capability. |
| Phase | Segmen waktu dalam Project (mis. Discovery Phase, Build Phase). |
| Milestone | Titik checkpoint terukur di dalam Phase, bukan pekerjaan itu sendiri. |
| Task | Unit kerja actionable oleh satu orang/agent dalam waktu terbatas. |
| Subtask | Pecahan Task yang lebih kecil, opsional. |
| Checklist | Daftar item verifikasi biner (selesai/belum) di dalam Task. |
| Deliverable | Artefak nyata hasil dari Task/Project. |

### Lapisan People & Accountability
| Istilah | Definisi |
|---|---|
| Owner | Penanggung jawab hasil akhir (accountable). |
| PIC | Person in Charge — pelaksana harian (responsible), bisa beda dari Owner. |
| Stakeholder | Pihak yang terdampak/berkepentingan tapi tidak selalu mengerjakan. |
| RACI | Responsible, Accountable, Consulted, Informed — pemetaan peran per keputusan/task. |

### Lapisan Prioritas & Risiko
| Istilah | Definisi |
|---|---|
| Priority | Urutan kepentingan relatif. |
| Impact | Besaran manfaat/dampak jika dikerjakan. |
| Effort | Estimasi usaha/biaya pengerjaan. |
| Risk | Potensi kejadian negatif di masa depan (belum terjadi). |
| Issue | Masalah yang **sudah terjadi** dan butuh penanganan. |
| Dependency | Ketergantungan terhadap pihak/komponen lain agar bisa berjalan. |
| Constraint | Batasan tetap yang tidak bisa diubah (waktu, budget, regulasi). |
| Assumption | Hal yang dianggap benar tanpa bukti penuh saat planning; wajib divalidasi. |

### Lapisan Waktu & Eksekusi Agile
| Istilah | Definisi |
|---|---|
| Timeline / Schedule | Susunan waktu Project/Phase. |
| Sprint / Iteration | Blok waktu tetap untuk mengeksekusi sejumlah Task. |
| Backlog | Kumpulan Task/Feature yang belum dikerjakan, terurut prioritas. |
| Requirement | Kebutuhan yang harus dipenuhi sistem (functional/non-functional). |
| Acceptance Criteria | Syarat spesifik agar satu Task/Feature dianggap benar. |
| Definition of Ready (DoR) | Syarat minimal sebelum Task boleh mulai dikerjakan. |
| Definition of Done (DoD) | Syarat minimal sebelum Task boleh dianggap selesai. |

### Lapisan Evaluasi & Penutupan
| Istilah | Definisi |
|---|---|
| Review | Aktivitas memeriksa hasil kerja terhadap kriteria. |
| Retrospective | Evaluasi proses tim (bukan hasil teknis) setelah satu siklus. |
| Lessons Learned | Insight terdokumentasi dari pengalaman, untuk dipakai ulang. |
| Decision Log | Catatan keputusan penting: apa, kenapa, siapa, kapan. |
| Action Items | Daftar tindak lanjut konkret hasil Review/Retro. |
| Resources | Orang/alat/anggaran yang dipakai. |
| Budget | Alokasi biaya. |
| Metrics | Ukuran kuantitatif hasil. |
| QA | Quality Assurance — proses memastikan kualitas selama pengerjaan. |
| QC | Quality Control — pemeriksaan hasil akhir terhadap standar. |
| Validation | Memastikan solusi memecahkan masalah yang tepat ("did we build the right thing"). |
| Verification | Memastikan solusi dibangun sesuai spesifikasi ("did we build it right"). |
| Release | Perilisan hasil ke user/production. |
| Deployment | Proses teknis memindahkan kode ke environment target. |
| Monitoring | Pengawasan sistem berjalan pasca-rilis. |
| Maintenance | Pemeliharaan berkelanjutan pasca-rilis. |
| Archive | Status akhir entitas kerja yang sudah tidak aktif, disimpan untuk referensi historis. |

### Istilah Tambahan yang Diperlukan (ditambahkan oleh sistem ini)
| Istilah | Definisi |
|---|---|
| Rollback Plan | Rencana konkret membatalkan perubahan jika gagal di production. |
| Regression Risk | Risiko fitur lama rusak akibat perubahan baru. |
| Edge Case | Skenario input/kondisi ekstrem/jarang yang harus tetap ditangani. |
| Negative Test Case | Skenario uji yang sengaja memasukkan input salah untuk memastikan sistem menolak dengan benar. |
| Technical Debt | Konsekuensi jangka panjang dari solusi cepat/tidak ideal yang diambil sekarang. |
| Blast Radius | Cakupan dampak jika suatu perubahan gagal. |
| SSoT (Single Source of Truth) | Satu tempat otoritatif untuk satu informasi. |
| Freshness | Ukuran seberapa baru/valid suatu dokumen terhadap kondisi nyata saat ini. |

---

## 2.2 Framework Library (masing-masing berdiri sendiri — pilih sesuai konteks, jangan dicampur)

**SMART** — Goal-setting. Pakai saat merumuskan Objective/Goal individual: Specific, Measurable, Achievable, Relevant, Time-bound.

**OKR** — Goal-setting tim/organisasi level kuartal. Pakai untuk menyelaraskan banyak tim ke satu arah, bukan untuk task harian.

**KPI** — Metrik operasional berkelanjutan. Pakai untuk memantau kesehatan sistem/proses yang sudah berjalan (bukan target yang "selesai" seperti OKR).

**PDCA (Plan-Do-Check-Act)** — Siklus perbaikan berkelanjutan. Pakai untuk continuous improvement pada proses yang berulang.

**Agile** — Filosofi payung: iteratif, adaptif, feedback cepat. Pakai sebagai mindset umum eksekusi, bukan metodologi teknis spesifik.

**Scrum** — Implementasi Agile dengan Sprint tetap, role (PO/SM/Dev), ritual (planning, standup, review, retro). Pakai saat tim butuh ritme kerja terstruktur & prediktabel.

**Kanban** — Implementasi Agile berbasis alur kerja kontinu (WIP limit), tanpa Sprint tetap. Pakai untuk kerja yang sifatnya terus-menerus masuk (mis. support, bug fix).

**Lean** — Menghilangkan pemborosan, fokus pada value stream. Pakai saat mengevaluasi efisiensi proses end-to-end.

**Six Sigma / DMAIC** (Define, Measure, Analyze, Improve, Control) — Pakai untuk masalah kualitas berulang yang butuh analisis data statistik mendalam, biasanya di skala operasi besar.

**WBS (Work Breakdown Structure)** — Memecah Project menjadi Phase → Task hierarkis. Pakai di tahap Planning setiap Project (lihat `03`).

**RACI** — Memetakan peran per keputusan/deliverable. Pakai saat Project melibatkan banyak stakeholder lintas tim.

**MoSCoW** (Must/Should/Could/Won't) — Prioritas cepat berbasis kategori. Pakai untuk scoping Requirement di awal Project, terutama saat waktu terbatas.

**RICE** (Reach, Impact, Confidence, Effort) — Prioritas kuantitatif untuk membandingkan banyak Feature/Initiative dalam Backlog.

**ICE** (Impact, Confidence, Ease) — Versi ringan RICE, cocok untuk startup/keputusan cepat dengan data terbatas.

**CPM (Critical Path Method)** — Menentukan jalur task yang menentukan durasi total Project. Pakai untuk Project dengan banyak dependency antar-task.

**Balanced Scorecard** — Mengukur performa dari 4 perspektif (finansial, customer, proses internal, pembelajaran). Pakai di level organisasi/strategi tahunan.

**SWOT** — Strengths, Weaknesses, Opportunities, Threats. Pakai di tahap Analysis awal Project/Strategy.

**PESTLE** — Political, Economic, Social, Technological, Legal, Environmental. Pakai untuk analisis konteks eksternal sebelum Strategy besar.

**Jobs To Be Done (JTBD)** — Memahami "pekerjaan" yang ingin diselesaikan user, bukan fitur yang diminta. Pakai di tahap Research/Discovery.

**Design Thinking** — Empathize–Define–Ideate–Prototype–Test. Pakai untuk masalah user-centric yang solusinya belum jelas.

**Double Diamond** — Discover–Define–Develop–Deliver. Pakai sebagai payung proses Design Thinking di level Project.

**User Story Mapping** — Memetakan alur user end-to-end untuk menentukan urutan rilis Feature. Pakai saat merancang Roadmap Feature.

**Impact Mapping** — Menghubungkan Goal bisnis → Actor → Impact → Deliverable. Pakai untuk memastikan Feature yang dibangun benar-benar terhubung ke Goal.

**Opportunity Solution Tree** — Memetakan satu Outcome ke banyak Opportunity (masalah) ke banyak kandidat Solution. Pakai di tahap Discovery produk untuk mencegah loncat langsung ke satu solusi.

> **Aturan pemilihan framework:** jangan gunakan lebih dari 2–3 framework aktif dalam satu entitas kerja. Framework dipilih sesuai tahap lifecycle (lihat pemetaan di `03-LIFECYCLE-AND-REVIEW-SYSTEM.md` § 3.3).
