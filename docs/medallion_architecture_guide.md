# 🏗️ Panduan Arsitektur Medallion untuk Analisis Ekspor Mineral

## 📊 Gambaran Arsitektur

```
┌───────────────────────────────────────────────────┐
│                                                   │
│                   Sumber Data                     │
│                                                   │
└───────────────────┬───────────────────────────────┘
                    │
                    │ Raw Data
                    ▼
┌───────────────────────────────────────────────────┐
│                                                   │
│               LAPISAN BRONZE (Raw)                │
│                                                   │
│  • Data CSV asli tanpa modifikasi                 │
│  • Mempertahankan integritas data sumber          │
│  • Sumber: ekspor_mineral_indonesia_WITS.csv      │
│                                                   │
└───────────────────┬───────────────────────────────┘
                    │
                    │ Bersihkan & Transformasi
                    ▼
┌───────────────────────────────────────────────────┐
│                                                   │
│            LAPISAN SILVER (Tervalidasi)           │
│                                                   │
│  • Pembersihan dan standardisasi data             │
│  • Jenis data dan unit yang konsisten             │
│  • Menambahkan field turunan (mis. harga satuan)  │
│  • Filter untuk ekspor mineral Indonesia saja     │
│                                                   │
└───────────────────┬───────────────────────────────┘
                    │
                    │ Agregasi & Turunkan Metrik
                    ▼
┌───────────────────────────────────────────────────┐
│                                                   │
│             LAPISAN GOLD (Bisnis)                 │
│                                                   │
│  • Agregasi tingkat bisnis                        │
│  • Analisis Ekspor berdasarkan Negara             │
│  • Analisis Ekspor berdasarkan Produk             │
│  • Siap untuk visualisasi dan wawasan bisnis      │
│                                                   │
└───────────────────────────────────────────────────┘
```

## 🔄 Proses Alur Data

1. **Ingest Data (Bronze)**:
   - Muat data CSV mentah dari sumber
   - Tidak ada transformasi data
   - Simpan dalam format parquet untuk efisiensi

2. **Pemrosesan Data (Silver)**:
   - Bersihkan dan validasi data
   - Standardisasi jenis data dan unit
   - Hitung field turunan
   - Filter record yang tidak relevan

3. **Analitik dan Pelaporan (Gold)**:
   - Buat agregasi tingkat bisnis
   - Hitung statistik ringkasan
   - Siapkan data untuk dashboard dan laporan

## 🛠️ Stack Teknologi

- **Penyimpanan**: HDFS
- **Pemrosesan**: Apache Spark
- **Interface SQL**: Apache Hive
- **Database NoSQL**: HBase
- **Manajemen Container**: Docker

## 💡 Manfaat Medallion

- **Monitoring Kualitas Data**: Pemisahan yang jelas antara data mentah dan bersih
- **Pelacakan Lineage Data**: Mudah melacak data dari sumber hingga metrik akhir
- **Reprodusibilitas**: Tahapan yang terdefinisi dengan baik untuk analisis yang dapat direproduksi
- **Optimisasi Performa**: Analitik yang lebih cepat pada data yang sudah diproses
- **Analitik Layanan Mandiri**: Pengguna bisnis dapat bekerja dengan data lapisan gold
