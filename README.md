# 📐 AljabarKu: Kalkulator Aljabar Berbasis Rigorous Mathematical Thinking (RMT) SMP Kelas 7

Proyek Perangkat Lunak Media Pembelajaran Matematika  
**Mata Kuliah:** Algoritma dan Pemrograman  
**Program Studi:** Pendidikan Matematika (Semester 3)  
**Landasan Teoretis:** *Rigorous Mathematical Thinking* (Kinard & Kozulin, 2008), *Mediated Learning Experience* (Feuerstein), & *Psychological Tools* (Vygotsky)  

---

## 🧠 Integrasi Konsep Rigorous Mathematical Thinking (RMT)

Kalkulator ini dirancang khusus untuk mentransformasikan media kalkulator dari sekadar **"mesin penjawab mekanis instan"** (*black-box solver*) menjadi **alat mediasi kognitif (*cognitive psychological tool*)** yang membangun cara berpikir matematis yang mendalam dan terstruktur:

### 1. Level 1: Qualitative Operations (Berpikir Kualitatif)
* **Pelabelan Matematis (*Labeling*):** Membedakan secara presisi antara variabel (besaran nilai), koefisien (faktor pengali kuantitas), konstanta (kuantitas invarian), dan derajat suku.
* **Analisis Atribut Kritis Suku Sejenis (*Comparing*):** Menegaskan bahwa suku sejenis wajib memenuhi dua atribut kritis: **variabel sama DAN derajat pangkat sama**. Menjelaskan mengapa $3x$ dan $3x^2$ bukan suku sejenis.

### 2. Level 2: Quantitative Operations (Representasi Semi-Konkret)
* **Model Luas Persegi Panjang (*Area Model*):** Menjelaskan perkalian distributif $k(ax + b)$ melalui representasi geometri luas persegi panjang besar berlebar $k$ dan panjang total $(ax + b)$.
* **Model Timbangan Setimbang (*Balance Scale*):** Merepresentasikan persamaan linear satu variabel (PLSV) sebagai sistem kesetimbangan yang harus dijaga keajegannya.

### 3. Level 3: Abstract Mathematical Operations (Penalaran Abstrak & Relasional)
* **Pembersihan Miskonsepsi Fatal "Pindah Ruas":** Menghapus total aturan mekanis "pindah ruas ganti tanda". Menggantikannya dengan **Sifat Kesetaraan (Invariance of Equality)** dan **Invers Aditif ($k + (-k) = 0$)** serta **Invers Multiplikatif ($\frac{1}{a} \cdot a = 1$)**.
* **Landasan Sifat Distributif:** Menjelaskan bahwa penggabungan suku sejenis ($ax + bx = (a + b)x$) berakar dari sifat distributif perkalian terhadap penjumlahan, bukan sekadar aturan acak "jumlahkan koefisien".
* **Refleksi Metakognitif & Verifikasi Solusi (*Proof of Correctness*):** Mewajibkan pengujian balik solusi variabel ke persamaan awal untuk membuktikan $\text{Ruas Kiri (LHS)} = \text{Ruas Kanan (RHS)}$.

---

## 🔒 Sistem Alur Uji Coba & Manajemen Guru

Aplikasi memiliki **pemisahan hak akses** terstruktur antara Siswa dan Guru/Peneliti:

### 1. Hak Akses Siswa (Linear Flow - Terkunci)
* Alur belajar terurut:  
  `1. Selamat Datang` $\rightarrow$ `2. Registrasi + Token` $\rightarrow$ `3. Tutorial RMT` $\rightarrow$ `4. Kalkulator RMT Siap Digunakan` $\rightarrow$ `5. Keluar`.
* **Validasi Token:** Pada tahap registrasi, siswa **wajib memasukkan Token Akses** yang diberikan oleh Guru.
* **Panel Keluar:** Siswa dapat menyelesaikan sesi dengan menekan tombol `🚪 Selesaikan Sesi & Keluar`.

### 2. Hak Akses Guru / Peneliti (Admin Mode)
* Berada pada bilah sisi (*sidebar*) di bawah menu **`🔒 Akses Khusus Guru / Peneliti`**.
* Dilindungi **PIN Guru** yang dapat diatur oleh administrator.
* **Fitur Guru:**
  1. **Navigasi Panel Bebas:** Guru dapat melompat langsung ke panel manapun untuk demonstrasi.
  2. **Pengaturan Token Ujian:** Mengganti token ujian secara berkala.
  3. **📊 Dashboard Rekap Data Siswa:** Menampilkan seluruh nama siswa, kelas, sekolah, absen, dan tingkat pemahaman yang tersimpan ke file `data_siswa.csv`.
  4. **📥 Unduh Data:** Tombol unduh otomatis berkas CSV / Excel untuk analisis penelitian atau penilaian.

---

## 🚀 Cara Menjalankan Aplikasi

1. Buka PowerShell pada folder proyek:
   ```powershell
   cd c:\2225250021_iqhsansaleh
   ```
2. Pastikan dependensi terpasang:
   ```powershell
   python -m pip install -r requirements.txt
   ```
3. Jalankan aplikasi web Streamlit:
   ```powershell
   python -m streamlit run app.py
   ```
4. Buka di browser pada: `http://localhost:8501`

---

## 🤖 Fitur Baru: Tutor AI Berbasis Google Gemini (RMT Scaffolding)

Aplikasi kini dilengkapi dengan **Tab 6: Tanya Tutor AI (RMT)** yang ditenagai oleh model **Google Gemini**:
* Berperan sebagai asisten guru matematika yang membimbing dengan pertanyaan pemantik (*scaffolding*), bukan sekadar pembocor jawaban.
* Membantu siswa mendiskusikan sifat aljabar, menganalisis kesalahan berpikir (*misconception remediation*), dan memberikan teka-teki logika aljabar.

---

## 🔐 Konfigurasi Rahasia & API Key

Aplikasi membaca kunci rahasia secara otomatis melalui `.streamlit/secrets.toml` (lokal) atau **App Settings → Secrets** (Streamlit Cloud).

Format isi file `.streamlit/secrets.toml`:

```toml
# 1. API Key Google Gemini (Gratis di https://aistudio.google.com/)
GEMINI_API_KEY = "AIzaSy..."

# 2. Pengaturan Token Siswa & PIN Guru
token_aktif = "UJICOBA2026"
pin_guru = "123456"
```

*Catatan: Jika API Key belum ditulis di `secrets.toml`, siswa/guru tetap dapat memasukkannya langsung secara fleksibel melalui antarmuka Tab 6 pada aplikasi.*
