# 📦 Analisis Ekspor Mineral Indonesia (2020–2024) - Big Data Stack

Proyek ini mengimplementasikan **arsitektur medallion** (bronze, silver, gold) untuk menganalisis data ekspor mineral Indonesia menggunakan ekosistem big data terdistribusi. Sistem ini memproses **1M+ catatan ekspor mineral** dengan Hadoop, Spark, Hive, dan HBase dalam lingkungan yang sepenuhnya terkontainerisasi.

---

## 📚 Daftar Isi

- [🎯 Tujuan Proyek](#-tujuan-proyek)
- [📊 Dataset](#-dataset)
- [🏗️ Arsitektur Sistem](#️-arsitektur-sistem)
- [🛠️ Stack Teknologi](#️-stack-teknologi)
- [🔁 Alur Pipeline ETL](#-alur-pipeline-etl)
- [🚀 Panduan Memulai](#-Ypanduan-memulai)
- [🌐 Interface Web](#-interface-web)
- [📈 Model & Analitik](#-model--analitik)
- [📊 Visualisasi & Konsumsi Data](#-visualisasi--konsumsi-data)
- [📁 Struktur Proyek](#-struktur-proyek)
- [🔧 Persyaratan Sistem](#-persyaratan-sistem)
- [📋 Skrip Tersedia](#-skrip-tersedia)
- [🔍 Monitoring & Kesehatan](#-monitoring--kesehatan)
- [📚 Dokumentasi](#-dokumentasi)
- [🎯 Nilai Bisnis](#-nilai-bisnis)

---

## 🎯 Tujuan Proyek

- Mengelola dan menganalisis data ekspor mineral Indonesia (2020–2024)
- Membangun pipeline ETL skala besar menggunakan Apache Spark dan Hadoop
- Mengimplementasikan arsitektur medallion untuk pemrosesan data bertingkat
- Melatih model prediksi tren ekspor mineral menggunakan Spark MLlib
- Menyajikan dashboard interaktif dan analisis real-time
- Mendukung stakeholder seperti analis, pemerintah, dan pengembang kebijakan

---

## 📊 Dataset

- **Sumber**: Data Ekspor Mineral Indonesia (WITS), data sintetis, dan metadata pendukung
- **Ukuran**: 91.3MB, 1.000.000+ catatan (disintesis dari 107 baris asli)
- **Format**: CSV dengan nilai ekspor, kuantitas, tujuan, dan detail produk
- **Periode Waktu**: Transaksi ekspor mineral 2020-2024
- **Atribut Utama**:
  - `negara_tujuan`, `tahun`, `bulan`, `komoditas`
  - `volume_ton`, `harga_usd_per_ton`, `total_usd`

---

## 🏗️ Arsitektur Sistem

Menggunakan pendekatan **Medallion Architecture**:

| Layer  | Format  | Tujuan | Isi |
|--------|---------|--------|-----|
| Bronze | CSV | Data Mentah | Data CSV asli WITS & data sintetis tanpa modifikasi |
| Silver | Parquet | Data Bersih | Data yang dibersihkan, divalidasi, dan distandarisasi |
| Gold   | Parquet | Analitik Bisnis | Agregasi, model output, dan dataset siap visualisasi |

### Lapisan Bronze (Data Mentah)
- **Tujuan**: Menyimpan data CSV asli dalam bentuk mentah
- **Penyimpanan**: HDFS (path: `/data/bronze/`)
- **Tabel**: `bronze_mineral_exports`

### Lapisan Silver (Data Bersih)
- **Tujuan**: Data yang dibersihkan, divalidasi, dan distandarisasi
- **Transformasi**: Filter null, konversi unit (USD, Kg), field turunan
- **Penyimpanan**: HDFS (path: `/data/silver/`)
- **Tabel**: `silver_mineral_exports`

### Lapisan Gold (Analitik Bisnis)
- **Tujuan**: Agregasi dan wawasan siap bisnis
- **Agregasi**: Ekspor per negara, analisis produk, tren pasar
- **Penyimpanan**: HDFS (path: `/data/gold/`)
- **Tabel**: `gold_exports_by_country`, `gold_exports_by_product`

---

## 🛠️ Stack Teknologi

- **🐘 Hadoop HDFS**: Penyimpanan terdistribusi untuk semua lapisan data
- **⚡ Apache Spark**: Pemrosesan data dan transformasi
- **🏗️ Apache Hive**: Interface SQL untuk query data
- **📊 HBase**: Database NoSQL untuk aplikasi real-time
- **🐳 Docker**: Deployment dan orkestrasi terkontainerisasi
- **📈 Jupyter**: Analisis interaktif dan visualisasi
- **🔄 Apache Airflow**: Orkestrasi pipeline (opsional)
- **📊 Apache Superset**: Dashboard dan visualisasi (opsional)

---

## 🔁 Alur Pipeline ETL

### [1] Data Sources
```
├── WITS (World Integrated Trade Solution)
│   ├── Data ekspor mineral asli 2020–2024 (CSV, 107 baris → disintesis menjadi 1 juta baris)
│   └── Metadata: kode produk, negara, deskripsi komoditas
└── Data Sintetis
    ├── Tambahan data hingga 1 juta record
    ├── Dibuat melalui random sampling dari pola data asli
    └── Atribut divariasikan: tahun, komoditas, negara tujuan
```

### [2] Raw Data Layer (Bronze – HDFS Ingestion)
```
├── Path: `/data/bronze/`
├── Simpan file CSV mentah WITS & data sintesis tanpa modifikasi
└── Hive Metastore menyimpan skema dan lokasi file
```

### [3] Initial Processing
```
├── Hive External Tables → Baca data mentah di `/data/bronze/`
└── MapReduce Jobs
    ├── Validasi format & skema (tahun, kode produk, negara, nilai, volume)
    └── Agregasi dasar: total ekspor per tahun → output ke `/data/processing/`
```

### [4] Cleaned & Integrated Layer (Silver – Spark Processing)
```
├── Path: `/data/silver/`
├── Engine: Apache Spark (PySpark)
├── Data Cleaning:
│   ├── Hilangkan duplikat & missing values
│   ├── Standarisasi format tanggal (YYYY)
│   └── Konsistensi satuan (1000 USD, Kg)
└── Data Integration:
    ├── Gabungkan WITS + data sintesis
    └── Simpan sebagai Parquet untuk optimasi
```

### [5] Feature Engineering & Model Training
```
├── Engine: Spark MLlib
├── Join & Transform:
│   ├── Hitung tren pertumbuhan nilai & volume
│   ├── Rasio nilai per volume
│   └── Feature seasonality (year-over-year)
├── Pelatihan Model:
│   ├── Regresi Linear (prediksi nilai ekspor)
│   ├── ARIMA (forecast time-series)
│   └── Decision Tree (klasifikasi produk utama)
└── Evaluasi & Tuning (MAE, MSE)
```

### [6] Analytics-Ready Layer (Gold – Serving)
```
├── Path: `/data/gold/`
├── Simpan:
│   ├── Dataset terintegrasi bersih (Parquet)
│   ├── Output prediksi & agregasi per tahun/komoditas
│   └── Model terlatih (binary Spark MLlib)
└── Partisi berdasarkan tahun & komoditas
```

### [7] Consumption & Visualization
```
├── Query Engines:
│   ├── Apache Hive → OLAP & laporan historis
│   └── Spark SQL → Ad-hoc analysis
└── Dashboard & Reporting:
    ├── Grafis tren ekspor per komoditas
    ├── Tabel top-10 negara tujuan
    └── Prediksi nilai ekspor 2025
```

### [8] Orchestration & Monitoring
```
├── Apache Airflow:
│   ├── DAG Bronze→Silver harian
│   ├── DAG retraining model mingguan
│   └── Alert on failure ke email/Slack
├── Apache Ambari → Pantau HDFS, Spark, Hive
└── Health Checks:
    └── Validasi row-count & schema tiap layer
```

---

## 📁 Struktur Proyek

```
📦 abdskuy/
├── 📁 analysis/           # Notebook Jupyter dan hasil analisis
│   ├── 📁 notebooks/      # Notebook analisis interaktif
│   └── 📁 results/        # Output analisis dan laporan
├── 📁 automation/         # Skrip otomatisasi
│   ├── 📁 powershell/     # Otomatisasi Windows PowerShell
│   └── 📁 bash/           # Otomatisasi shell Linux/Mac
├── 📁 data/               # Penyimpanan dataset
│   └── ekspor_mineral_indonesia_WITS.csv
├── 📁 docker/             # Konfigurasi Docker
│   ├── docker-compose.yml
│   └── docker-compose-simple.yml
├── 📁 docs/               # Dokumentasi dan laporan
│   ├── File README untuk setiap komponen
│   └── Dokumentasi teknis
├── 📁 scripts/            # Skrip pemrosesan dan analisis
│   ├── 📁 python/         # Skrip pemrosesan data Python
│   ├── 📁 shell/          # Skrip shell untuk otomatisasi
│   └── 📁 batch/          # Skrip batch Windows
└── README.md              # File ini
```

## 🚀 Panduan Memulai

### 1. Pengaturan Sistem
```bash
# Jalankan semua container
cd docker/
docker-compose up -d

# Verifikasi semua layanan berjalan
docker ps
```

### 2. Inisialisasi Lingkungan
```bash
# Siapkan direktori HDFS
docker exec -it namenode bash -c "bash /data/setup_hdfs.sh"

# Instal paket yang diperlukan (Windows)
.\automation\powershell\install_packages.ps1
```

### 3. Jalankan Analisis
```bash
# Eksekusi analisis ekspor mineral
docker exec -it spark-master bash -c "python /data/mineral_export_analysis.py"

# Atau gunakan skrip otomatisasi (Windows)
.\automation\powershell\run_analysis.ps1
```

## 🌐 Interface Web

Semua interface web dapat diakses dan beroperasi:

| Layanan | URL | Tujuan |
|---------|-----|---------|
| **Hadoop NameNode** | http://localhost:9870 | Manajemen dan monitoring HDFS |
| **Spark Master** | http://localhost:8080 | Manajemen cluster Spark |
| **Spark Worker** | http://localhost:8081 | Status node worker |
| **HBase Master** | http://localhost:16010 | Manajemen cluster HBase |
| **DataNode** | http://localhost:9864 | Status node data HDFS |

### Akses Cepat
Gunakan skrip otomatisasi untuk membuka semua interface:
```powershell
.\automation\powershell\open_all_interfaces.ps1
```

## 📈 Fitur Utama

- **✅ Beroperasi Penuh**: Semua 7 container Docker berjalan sehat
- **✅ Interface Web**: Semua 5 interface web dapat diakses (verified HTTP 200)
- **✅ Pemrosesan Data**: 1M+ catatan diproses melalui arsitektur medallion
- **✅ Monitoring Real-time**: Observabilitas lengkap melalui dashboard web
- **✅ Alur Kerja Otomatis**: Skrip otomatisasi PowerShell dan shell
- **✅ Analisis Interaktif**: Notebook Jupyter untuk eksplorasi data

## 🔧 Persyaratan Sistem

- **OS**: Windows 11 + WSL2 Ubuntu 22.04
- **Docker & Docker Compose**: Orkestrasi container
- **RAM**: Minimum 8GB (16GB direkomendasikan)
- **Penyimpanan**: 10GB+ ruang tersedia
- **Port**: 8080, 8081, 9864, 9870, 16010 (dapat dikonfigurasi)
- **Tools**: Hadoop 3.4.1, Apache Spark, Hive, Superset, Ambari, Airflow

---

## 📋 Skrip Tersedia

### Skrip Python (`scripts/python/`)
- **final_analysis.py**: Pipeline analisis utama
- **run_medallion_analysis.py**: Eksekusi arsitektur medallion

### Otomatisasi (`automation/powershell/`)
- **install_packages.ps1**: Instalasi dependensi
- **open_all_interfaces.ps1**: Buka semua interface web
- **run_analysis.ps1**: Eksekusi pipeline analisis lengkap
- **open_web_interfaces.ps1**: Akses cepat ke dashboard

### Skrip Shell (`scripts/shell/`)
- **setup_hdfs.sh**: Inisialisasi HDFS
- **analyze_minerals.sh**: Analisis mineral otomatis
- **final_verification.sh**: Verifikasi akhir sistem
- **install_packages.sh**: Instalasi dependensi Linux
- **run_analysis.sh**: Eksekusi analisis lengkap

### Skrip Batch (`scripts/batch/`)
- **analyze_minerals.bat**: Analisis Windows batch

---

## 📈 Model & Analitik

| Analisis | Algoritma | Output |
|----------|-----------|--------|
| Prediksi volume ekspor | Linear Regression | Estimasi ekspor bulan/tahun ke depan |
| Prediksi time-series | ARIMA | Tren ekspor komoditas tahunan |
| Segmentasi negara | KMeans Clustering | Grup perilaku negara tujuan ekspor |
| Feature Importance | Decision Tree | Fitur paling berpengaruh dalam ekspor |

---

## 📊 Visualisasi & Konsumsi Data

- **Apache Superset**:
  - Tren ekspor bulanan/tahunan
  - Top-10 negara tujuan
  - Perbandingan komoditas
- **Hive SQL & Spark SQL**:
  - Query OLAP untuk analisis interaktif
- **Jupyter Notebooks**:
  - Analisis eksplorasi data interaktif
  - Visualisasi dan dashboard khusus

---

## 📊 Kemampuan Analisis

- **Analisis Negara**: Tujuan ekspor, volume perdagangan, penetrasi pasar
- **Analisis Produk**: Jenis mineral, nilai ekspor, tren kuantitas
- **Time Series**: Pola ekspor historis dan tren musiman
- **Market Intelligence**: Mitra dagang utama, analisis harga, metrik pertumbuhan

## 🔍 Monitoring & Kesehatan

Sistem mencakup monitoring komprehensif:
- **Kesehatan Container**: Semua 7 container dimonitor
- **Status Layanan**: Pemeriksaan kesehatan interface web real-time
- **Pipeline Data**: Verifikasi pemrosesan end-to-end
- **Metrik Performa**: Pelacakan utilisasi resource

## 📚 Dokumentasi

Dokumentasi detail tersedia di folder `docs/`:
- File README spesifik komponen
- Dokumentasi arsitektur teknis
- Panduan troubleshooting
- Prosedur operasional

## 🎯 Nilai Bisnis

Sistem ini memungkinkan:
- **Analisis Perdagangan**: Wawasan ekspor mineral komprehensif
- **Riset Pasar**: Analisis negara tujuan
- **Product Intelligence**: Tren ekspor spesifik mineral
- **Wawasan Ekonomi**: Analitik volume dan nilai perdagangan
- **Perencanaan Strategis**: Strategi ekspor berbasis data

---

**Status**: ✅ **BEROPERASI PENUH** - Semua layanan berjalan, interface web dapat diakses, 1M+ catatan diproses
