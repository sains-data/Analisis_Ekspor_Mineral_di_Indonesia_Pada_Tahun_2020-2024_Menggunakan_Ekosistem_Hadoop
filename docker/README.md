# 🐳 Direktori Docker

Direktori ini berisi konfigurasi Docker untuk infrastruktur analitik Big Data.

## 📁 Konten

### 🔧 File Konfigurasi
- `docker-compose.yml` - **Konfigurasi produksi utama**
  - Stack big data lengkap (7 layanan)
  - Pemetaan port yang dioptimalkan
  - Volume dan network siap produksi

- `docker-compose-simple.yml` - **Konfigurasi pengembangan sederhana**
  - Layanan minimal untuk pengembangan
  - Startup lebih cepat dan penggunaan resource berkurang

## 🏗️ Stack Infrastruktur

### 🐳 Layanan Container
```
┌─────────────────────────────────────────┐
│  🔵 namenode        │ Manajemen HDFS    │
│  🔵 datanode        │ Penyimpanan Data  │  
│  🔵 spark-master    │ Engine Pemrosesan │
│  🔵 spark-worker    │ Node Komputasi    │
│  🔵 hbase           │ Database NoSQL    │
│  🔵 hive-metastore  │ Manajemen Skema   │
│  🔵 hive-server     │ Interface SQL     │
└─────────────────────────────────────────┘
```

## 🚀 Perintah Cepat

### Jalankan Stack Lengkap
```powershell
# Navigasi ke direktori docker
cd docker

# Jalankan semua layanan
docker-compose up -d
```

### Jalankan Stack Pengembangan
```powershell
# Jalankan layanan minimal untuk pengembangan
docker-compose -f docker-compose-simple.yml up -d
```

### Monitor Layanan
```powershell
# Periksa status container
docker ps

# Lihat log
docker-compose logs -f [service-name]
```

### Hentikan Layanan
```powershell
# Hentikan semua layanan
docker-compose down

# Hentikan dan hapus volume (hati-hati: kehilangan data)
docker-compose down -v
```

## 🌐 Interface Web

| Layanan | Port | URL | Tujuan |
|---------|------|-----|---------|
| NameNode | 9870 | http://localhost:9870 | Manajemen HDFS |
| Spark Master | 8080 | http://localhost:8080 | Cluster Spark |
| Spark Worker | 8081 | http://localhost:8081 | Monitoring Worker |
| HBase Master | 16010 | http://localhost:16010 | Database NoSQL |
| DataNode | 9864 | http://localhost:9864 | Penyimpanan Data |

## 🔧 Catatan Konfigurasi
- **Pemetaan Port:** Dikonfigurasi untuk akses pengembangan localhost
- **Persistensi Data:** Volume mount memastikan durabilitas data
- **Network:** Bridge network untuk komunikasi antar-container
- **Health Check:** Monitoring kesehatan built-in untuk layanan kritis
