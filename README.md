# 📊 Dashboard Analytics: Catatanku (Streamlit App)

Aplikasi web berbasis **Streamlit** untuk visualisasi dan analisis data keuangan pribadi. Proyek ini merupakan bagian dari Capstone Project **Catatanku** pada trek Data Science. Dashboard ini dibagi menjadi dua modul utama: **Analisis Klasifikasi Pengeluaran** dan **Analisis Regresi Tabungan**.

---

## 🚀 Fitur Utama

Aplikasi ini memiliki dua halaman dashboard utama yang dapat diakses melalui menu navigasi di sidebar:

### 1. 🛍️ Dashboard Analytics Klasifikasi Pengeluaran (`pages/dashboard.py`)
Dashboard ini menyajikan analisis mendalam terkait pengeluaran keuangan, tren pengeluaran, deteksi outlier, serta pengujian hipotesis (A/B Testing).
- **Ringkasan Keuangan**: Menampilkan indikator metrik utama seperti total pengeluaran dan jumlah transaksi.
- **Top 5 Kategori & Tren**: Visualisasi kategori pengeluaran terbesar dan tren pengeluaran dari tahun ke tahun.
- **Exploratory Data Analysis (EDA)**:
  - *Nominal*: Distribusi nominal transaksi (histogram, mean, median, skewness).
  - *Kategori*: Proporsi penyebaran kategori pengeluaran menggunakan *Pie Chart* dan tabel persentase detail.
  - *Waktu*: Tren pengeluaran bulanan/tahunan dan perbandingan rata-rata pengeluaran Hari Kerja (*Weekday*) vs Akhir Pekan (*Weekend*).
  - *Outlier*: Deteksi transaksi janggal menggunakan metode IQR (1.5x) atau 2 Standar Deviasi.
- **Visualisasi Pertanyaan Bisnis**:
  - Analisis bulan dengan total pengeluaran tertinggi beserta rekomendasi finansial.
  - Analisis perbandingan dan penyebab utama perbedaan pengeluaran Hari Kerja vs Akhir Pekan.
  - Analisis potensi penghematan dari transaksi outlier dengan kebijakan *"Tunggu 3 Hari"*.
- **A/B Testing**: Uji hipotesis statistik secara real-time (*T-test*, *P-value*, dan *Cohen's d*) untuk memvalidasi asumsi keuangan.
- **Data Viewer**: Eksplorasi data mentah secara interaktif serta fitur untuk mengunduh dataset dalam format CSV.

### 2. 💰 Dashboard Analytics Regresi Tabungan (`pages/regresi.py`)
Dashboard ini berfokus pada melacak perkembangan tabungan pengguna, pola waktu menabung, serta analisis keberhasilan rencana keuangan (*goals*).
- **Ringkasan Tabungan**: Menampilkan total rencana target, total dana terkumpul, jumlah goal aktif, dan total transaksi menabung.
- **Analisis Tren Waktu**: Visualisasi frekuensi transaksi bulanan dan total nominal tabungan bulanan secara interaktif menggunakan *Plotly*.
- **Exploratory Data Analysis (EDA)**:
  - *Overview & Persentase*: Distribusi persentase pencapaian tabungan.
  - *Distribusi Target*: Distribusi nominal target tabungan pengguna (*right-skewed*).
- **Visualisasi Pertanyaan Bisnis**:
  - *Pertanyaan 1*: Analisis 10 nama goal terpopuler dengan pencapaian rata-rata terendah untuk tabungan belum selesai yang berumur >180 hari.
  - *Pertanyaan 2*: Analisis distribusi jarak hari antar-setoran beserta nilai mediannya untuk tabungan yang sukses diselesaikan pada periode 2022–2025.
- **Data Viewer**: Eksplorasi data transaksi tabungan dan tombol download dataset CSV.

---

## 📁 Struktur Proyek

```text
DS-Streamlit/
├── app.py                  # Entrypoint utama aplikasi Streamlit (navigasi & konfigurasi)
├── requirements.txt        # Daftar dependency pustaka Python yang dibutuhkan
└── pages/
    ├── dashboard.py        # Logika & UI Dashboard Klasifikasi Pengeluaran
    └── regresi.py          # Logika & UI Dashboard Regresi Tabungan
```

---

## 🛠️ Tech Stack & Dependencies

Proyek ini dibangun menggunakan pustaka-pustaka Python populer berikut:
* **Streamlit** (v1.x) - Pembuatan antarmuka web interaktif.
* **Pandas & NumPy** - Manipulasi dan pembersihan data.
* **Plotly Express** - Pembuatan grafik interaktif untuk regresi tabungan.
* **Matplotlib & Seaborn** - Pembuatan grafik statis untuk visualisasi EDA.
* **SciPy (Stats)** - Uji hipotesis statistik (*T-test*).

---

## ⚙️ Cara Menjalankan Aplikasi Secara Lokal

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputer Anda:

### 1. Prasyarat
Pastikan Anda sudah menginstal **Python** (versi 3.8 ke atas direkomendasikan).

### 2. Kloning Repositori
```bash
git clone https://github.com/Capstone-Catatanku/Streamlit-DS.git
cd CS-Streamlit
```

### 3. Instal Dependencies
Gunakan pip untuk memasang semua pustaka yang tertera pada `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi Streamlit
Jalankan perintah berikut untuk memulai server lokal Streamlit:
```bash
streamlit run app.py
```
Aplikasi secara otomatis akan terbuka di peramban (browser) Anda pada alamat: `http://localhost:8501`.

---

## 📊 Sumber Data (Dataset)
Data yang dianalisis pada aplikasi ini diambil langsung secara dinamis dari repositori resmi GitHub organisasi **Capstone Catatanku**:
1. **Data Klasifikasi Pengeluaran**: [Data-clean.csv](https://raw.githubusercontent.com/Capstone-Catatanku/Data-Science/refs/heads/main/Data-clean/Data-clean.csv)
2. **Data Progress Tabungan**: [Data_Progressive_Clean.csv](https://raw.githubusercontent.com/Capstone-Catatanku/Data-Science-Tabungan/refs/heads/main/Clean-data/Data_Progressive_Clean.csv)
