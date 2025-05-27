# 🤖 Direktori Otomatisasi

Direktori ini berisi skrip otomatisasi untuk mengelola dan mengoperasikan platform Analitik Data Ekspor Mineral Indonesia.

## 📁 Struktur

### 🐧 `bash/`
Skrip Bash untuk lingkungan Linux/Unix:
- *Siap untuk skrip otomatisasi lintas platform*

### 💻 `powershell/`
Skrip PowerShell untuk lingkungan Windows:
- `install_packages.ps1` - Instal paket Python dan dependensi yang diperlukan
- `open_all_interfaces.ps1` - Buka semua interface web monitoring sekaligus
- `open_web_interfaces.ps1` - Skrip alternatif peluncur interface
- `run_analysis.ps1` - Eksekusi pipeline analisis dengan PowerShell

## 🚀 Perintah Cepat

### Pengaturan Lingkungan
```powershell
# Instal semua paket yang diperlukan
.\automation\powershell\install_packages.ps1
```

### Peluncuran Monitoring
```powershell
# Buka semua interface web untuk monitoring
.\automation\powershell\open_all_interfaces.ps1
```

### Jalankan Analisis
```powershell
# Eksekusi pipeline analisis lengkap
.\automation\powershell\run_analysis.ps1
```

## 🛠️ Fitur
- **Pengaturan satu klik** - Konfigurasi lingkungan otomatis
- **Dashboard monitoring** - Akses cepat ke semua interface web
- **Otomatisasi analisis** - Eksekusi pemrosesan data yang efisien
- **Dukungan lintas platform** - Lingkungan Windows (PowerShell) dan Unix (Bash)
