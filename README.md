# Analisis Ekspor Mineral Indonesia - Big Data Stack

## 🎯 Gambaran Proyek

Proyek ini mengimplementasikan **arsitektur medallion** (bronze, silver, gold) untuk menganalisis data ekspor mineral Indonesia menggunakan ekosistem big data terdistribusi. Sistem ini memproses **1M+ catatan ekspor mineral** dengan Hadoop, Spark, Hive, dan HBase dalam lingkungan yang sepenuhnya terkontainerisasi.

## 📊 Dataset
- **Sumber**: Data Ekspor Mineral Indonesia (WITS)
- **Ukuran**: 91.3MB, 1.000.000+ catatan
- **Format**: CSV dengan nilai ekspor, kuantitas, tujuan, dan detail produk
- **Periode Waktu**: Transaksi ekspor mineral multi-tahun

## 🏗️ Lapisan Arsitektur

### Lapisan Bronze (Data Mentah)
- **Tujuan**: Menyimpan data CSV asli dalam bentuk mentah
- **Penyimpanan**: HDFS (format Parquet)
- **Tabel**: `bronze_mineral_exports`

### Lapisan Silver (Data Bersih)
- **Tujuan**: Data yang dibersihkan, divalidasi, dan distandarisasi
- **Transformasi**: Filter null, konversi unit (USD, Kg), field turunan
- **Penyimpanan**: HDFS (format Parquet)
- **Tabel**: `silver_mineral_exports`

### Lapisan Gold (Analitik Bisnis)
- **Tujuan**: Agregasi dan wawasan siap bisnis
- **Agregasi**: Ekspor per negara, analisis produk, tren pasar
- **Penyimpanan**: HDFS (format Parquet)
- **Tabel**: `gold_exports_by_country`, `gold_exports_by_product`

## 🛠️ Stack Teknologi

- **🐘 Hadoop HDFS**: Penyimpanan terdistribusi untuk semua lapisan data
- **⚡ Apache Spark**: Pemrosesan data dan transformasi
- **🏗️ Apache Hive**: Interface SQL untuk query data
- **📊 HBase**: Database NoSQL untuk aplikasi real-time
- **🐳 Docker**: Deployment dan orkestrasi terkontainerisasi
- **📈 Jupyter**: Analisis interaktif dan visualisasi

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

- **Docker & Docker Compose**: Orkestrasi container
- **RAM**: Minimum 8GB (16GB direkomendasikan)
- **Penyimpanan**: 10GB+ ruang tersedia
- **Port**: 8080, 8081, 9864, 9870, 16010 (dapat dikonfigurasi)

## 📋 Skrip Tersedia

### Skrip Python (`scripts/python/`)
- **mineral_export_analysis.py**: Pipeline analisis utama
- **data_validation.py**: Pemeriksaan kualitas data
- **export_insights.py**: Query business intelligence

### Otomatisasi (`automation/powershell/`)
- **install_packages.ps1**: Instalasi dependensi
- **open_all_interfaces.ps1**: Buka semua interface web
- **run_analysis.ps1**: Eksekusi pipeline analisis lengkap

### Skrip Shell (`scripts/shell/`)
- **setup_hdfs.sh**: Inisialisasi HDFS
- **start_services.sh**: Otomatisasi startup layanan

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
