# 📜 Direktori Scripts

Direktori ini berisi semua skrip eksekusi untuk menjalankan analisis ekspor mineral Indonesia dalam berbagai lingkungan.

## 📁 Struktur

### 🐧 `shell/`
Skrip Shell untuk lingkungan Linux/Unix:
- `analyze_minerals.sh` - Menjalankan analisis medallion menggunakan Spark
- `final_verification.sh` - Verifikasi hasil analisis dan output
- `install_packages.sh` - Instalasi paket Python yang diperlukan
- `run_analysis.sh` - Script utama untuk menjalankan pipeline analisis
- `setup_hdfs.sh` - Setup dan konfigurasi HDFS

### 💻 `batch/`
Skrip Batch untuk lingkungan Windows:
- `analyze_minerals.bat` - Analisis medallion dengan command prompt Windows

### 🐍 `python/`
Skrip Python untuk analisis data:
- `final_analysis.py` - Analisis Python kompatibel tanpa Spark (untuk testing lokal)
- `run_medallion_analysis.py` - Implementasi arsitektur medallion dengan PySpark

## 🚀 Penggunaan

### Windows (Batch)
```cmd
# Jalankan analisis lengkap
.\scripts\batch\analyze_minerals.bat
```

### Linux/Unix (Shell)
```bash
# Setup environment
chmod +x scripts/shell/*.sh

# Install packages
./scripts/shell/install_packages.sh

# Jalankan analisis
./scripts/shell/run_analysis.sh
```

### Python Direct
```bash
# Analisis sederhana tanpa Spark
python scripts/python/final_analysis.py

# Analisis medallion dengan Spark
python scripts/python/run_medallion_analysis.py
```

## 🔧 Fungsi Setiap Script

### 📊 Analisis Scripts
- **Tujuan**: Implementasi pipeline analisis big data
- **Input**: Data CSV ekspor mineral Indonesia
- **Output**: Laporan analisis, dashboard, dan insights

### 🛠️ Setup Scripts  
- **Tujuan**: Persiapan environment dan instalasi dependensi
- **Fungsi**: Konfigurasi HDFS, instalasi packages, setup container

### ✅ Verification Scripts
- **Tujuan**: Validasi hasil analisis dan health check
- **Fungsi**: Memastikan data integrity dan output quality

## 🎯 Rekomendasi Penggunaan

1. **Development**: Gunakan Python scripts untuk testing lokal
2. **Production**: Gunakan shell/batch scripts dengan Docker
3. **Debugging**: Gunakan verification scripts untuk troubleshooting
4. **Cross-platform**: Batch untuk Windows, Shell untuk Linux/Mac