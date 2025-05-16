# 📦 Big Data Project: Analisis Ekspor Mineral Indonesia (2020–2024)

Repositori ini berisi proyek analitik ekspor mineral Indonesia menggunakan ekosistem Hadoop dengan pendekatan Medallion Architecture (Bronze → Silver → Gold). Proyek ini memproses data dalam skala besar dan menghasilkan prediksi serta visualisasi tren ekspor untuk mendukung pengambilan kebijakan berbasis data.

---

## 📚 Daftar Isi

- [🎯 Tujuan Proyek](#-tujuan-proyek)
- [📊 Dataset](#-dataset)
- [🏗️ Arsitektur Sistem](#️-arsitektur-sistem)
- [🔁 Alur Pipeline ETL](#-alur-pipeline-etl)
- [📈 Model & Analitik](#-model--analitik)
- [📊 Visualisasi & Konsumsi Data](#-visualisasi--konsumsi-data)
- [⚙️ Deployment](#️-deployment)
- [🧪 Testing](#-testing)
- [📂 Struktur Folder](#-struktur-folder)
- [👨‍👩‍👧‍👦 Tim Pengembang](#-tim-pengembang)
- [📅 Timeline Proyek](#-timeline-proyek)
- [✅ Output](#-output)
- [📄 Lisensi](#-lisensi)

---

## 🎯 Tujuan Proyek

- Mengelola dan menganalisis data ekspor mineral Indonesia (2020–2024).
- Membangun pipeline ETL skala besar menggunakan Apache Spark dan Hadoop.
- Melatih model prediksi tren ekspor mineral menggunakan Spark MLlib.
- Menyajikan dashboard interaktif di Apache Superset.
- Mendukung stakeholder seperti analis, pemerintah, dan pengembang kebijakan.

---

## 📊 Dataset

- **Sumber**: WITS, BPS, ESDM, data sintetis, data cuaca, biaya logistik, kurs, dan permintaan global.
- **Atribut Utama**:
  - `negara_tujuan`, `tahun`, `bulan`, `komoditas`
  - `volume_ton`, `harga_usd_per_ton`, `total_usd`

---

## 🏗️ Arsitektur Sistem

Menggunakan pendekatan **Medallion Architecture**:

| Layer  | Format  | Isi                                                              |
|--------|---------|-------------------------------------------------------------------|
| Bronze | CSV     | Data mentah dari WITS & data sintetis                             |
| Silver | Parquet | Data bersih & terintegrasi via Spark                              |
| Gold   | Parquet | Agregasi, model output, dan dataset siap visualisasi              |

---

## 🔁 Alur Pipeline ETL

### [1] Data Sources

├── WITS (World Integrated Trade Solution)
│ ├── Data ekspor mineral asli 2020–2024 (CSV, 107 baris → disintesis menjadi 1 juta baris)
│ └── Metadata: kode produk, negara, deskripsi komoditas
└── Data Sintetis
├── Tambahan data hingga 1 juta record
├── Dibuat melalui random sampling dari pola data asli
└── Atribut divariasikan: tahun, komoditas, negara tujuan

##[2] Raw Data Layer (Bronze – HDFS Ingestion)

├── Path: `/data/bronze/`
├── Simpan file CSV mentah WITS & data sintesis tanpa modifikasi
└── Hive Metastore menyimpan skema dan lokasi file

## [3] Initial Processing
├── Hive External Tables → Baca data mentah di `/data/bronze/`
└── MapReduce Jobs
    ├── Validasi format & skema (tahun, kode produk, negara, nilai, volume)
    └── Agregasi dasar: total ekspor per tahun → output ke `/data/processing/`

## [4] Cleaned & Integrated Layer (Silver – Spark Processing)
├── Path: `/data/silver/`
├── Engine: Apache Spark (PySpark)
├── Data Cleaning:
│   ├── Hilangkan duplikat & missing values
│   ├── Standarisasi format tanggal (YYYY)
│   └── Konsistensi satuan (1000 USD, Kg)
└── Data Integration:
    ├── Gabungkan WITS + data sintesis
    └── Simpan sebagai Parquet untuk optimasi

## [5] Feature Engineering & Model Training
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

##[6] Analytics-Ready Layer (Gold – Serving)
├── Path: `/data/gold/`
├── Simpan:
│   ├── Dataset terintegrasi bersih (Parquet)
│   ├── Output prediksi & agregasi per tahun/komoditas
│   └── Model terlatih (binary Spark MLlib)
└── Partisi berdasarkan tahun & komoditas

##[7] Consumption & Visualization
├── Query Engines:
│   ├── Apache Hive → OLAP & laporan historis
│   └── Spark SQL → Ad-hoc analysis
└── Dashboard & Reporting:
    ├── Grafis tren ekspor per komoditas
    ├── Tabel top-10 negara tujuan
    └── Prediksi nilai ekspor 2025

##[8] Orchestration & Monitoring
├── Apache Airflow:
│   ├── DAG Bronze→Silver harian
│   ├── DAG retraining model mingguan
│   └── Alert on failure ke email/Slack
├── Apache Ambari → Pantau HDFS, Spark, Hive
└── Health Checks:
    └── Validasi row-count & schema tiap layer

---

## 📈 Model & Analitik

| Analisis                 | Algoritma               | Output                                   |
|--------------------------|-------------------------|------------------------------------------|
| Prediksi volume ekspor   | Linear Regression       | Estimasi ekspor bulan/tahun ke depan     |
| Prediksi time-series     | ARIMA                   | Tren ekspor komoditas tahunan            |
| Segmentasi negara        | KMeans Clustering       | Grup perilaku negara tujuan ekspor       |
| Feature Importance       | Decision Tree           | Fitur paling berpengaruh dalam ekspor    |

---

## 📊 Visualisasi & Konsumsi Data

- **Apache Superset**:
  - Tren ekspor bulanan/tahunan
  - Top-10 negara tujuan
  - Perbandingan komoditas
- **Hive SQL & Spark SQL**:
  - Query OLAP untuk analisis interaktif

---

## ⚙️ Deployment

### Spesifikasi

- OS: Windows 11 + WSL2 Ubuntu 22.04
- Cluster: Docker Compose Hadoop (pseudo-distributed)
- Tools:
  - Hadoop 3.4.1
  - Apache Spark, Hive, Superset, Ambari, Airflow
