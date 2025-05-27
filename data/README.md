# 💾 Direktori Data

Direktori ini berisi semua dataset dan file data untuk proyek Analitik Ekspor Mineral Indonesia.

## 📁 Konten

### 📊 Dataset Utama
- `ekspor_mineral_indonesia_WITS.csv` - **Dataset produksi**
  - **Ukuran:** 91.3 MB
  - **Catatan:** 1.000.000 transaksi ekspor
  - **Periode Waktu:** 2020-2024 (5 tahun)
  - **Sumber:** World Integrated Trade Solution (WITS)

## 📋 Skema Data

### Struktur Kolom
```
- Reporter: Negara eksportir (Indonesia)
- TradeFlow: Indikator ekspor/impor
- ProductCode: Kode komoditas HS
- Product Description: Nama produk detail
- Year: Tahun transaksi (2020-2024)
- Partner: Negara tujuan
- Trade Value 1000USD: Nilai dalam ribu USD
- Quantity: Kuantitas ekspor
- Quantity Unit: Unit pengukuran (Kg, Ton, dll.)
```

## 🌍 Cakupan Geografis
**Tujuan Ekspor Utama:**
- Jerman 🇩🇪
- Spanyol 🇪🇸
- Amerika Serikat 🇺🇸
- Italia 🇮🇹
- Kanada 🇨🇦

## 🏭 Produk Ekspor Utama
- Batu bara dan bahan bakar mineral
- Minyak kelapa sawit dan turunannya
- Nikel dan paduan
- Produk tembaga
- Timah dan senyawa
- Zat mineral lainnya

## 📈 Kualitas Data
- **Kelengkapan:** >95% field terisi
- **Konsistensi:** Struktur skema tervalidasi
- **Akurasi:** Statistik perdagangan tingkat produksi
- **Volume:** Dataset volume tinggi cocok untuk analitik big data

## 🔄 Pipeline Data
Data ini memberi makan arsitektur medallion:
- **Lapisan Bronze:** Ingest CSV mentah
- **Lapisan Silver:** Data dibersihkan dan divalidasi
- **Lapisan Gold:** Metrik bisnis teragregasi
