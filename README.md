# 📐 AljabarKu: Kalkulator Aljabar Edukatif SMP Kelas 7

Proyek Perangkat Lunak Media Pembelajaran Matematika  
**Mata Kuliah:** Algoritma dan Pemrograman  
**Program Studi:** Pendidikan Matematika (Semester 3)  
**Referensi Inspirasi:** [MathPapa Algebra Calculator](https://www.mathpapa.com/algebra-calculator.html)

---

## 🔒 Fitur Baru: Sistem Uji Coba & Manajemen Guru

Aplikasi ini telah dirancang dengan **pemisahan hak akses** antara Siswa dan Guru/Peneliti:

### 1. Hak Akses Siswa (Linear Flow - Terkunci)
* Siswa **TIDAK BISA** melompat antar-panel secara bebas. Mereka harus melalui alur terurut:
  `1. Selamat Datang` $\rightarrow$ `2. Registrasi + Token` $\rightarrow$ `3. Tutorial` $\rightarrow$ `4. Kalkulator Siap Digunakan` $\rightarrow$ `5. Keluar`.
* **Validasi Token:** Pada tahap registrasi, siswa **wajib memasukkan Token Akses** yang telah dikonfigurasi oleh Guru. Jika token salah, siswa tidak dapat melanjutkan ke tutorial.
* **Panel Keluar:** Siswa dapat menyelesaikan sesi dengan menekan tombol `🚪 Selesaikan Sesi & Keluar`.

### 2. Hak Akses Guru / Peneliti (Admin Mode)
* Berada pada bilah sisi (*sidebar*) di bawah menu **`🔒 Akses Khusus Guru / Peneliti`**.
* Dilindungi **PIN Guru** yang diatur secara rahasia oleh administrator.
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
3. Jalankan aplikasi web:
   ```powershell
   python -m streamlit run app.py
   ```
4. Buka di browser pada: `http://localhost:8501`

---

## 🔐 Konfigurasi Rahasia

Jangan unggah `config_guru.json`, `data_siswa.csv`, atau kredensial ke repositori publik. File konfigurasi lokal dan data siswa diabaikan oleh Git.

Untuk Streamlit Community Cloud, buka **App settings → Secrets** dan atur nilai rahasia berikut dengan kredensial pilihan Anda:

```toml
token_aktif = "GANTI_DENGAN_TOKEN_RAHASIA"
pin_guru = "GANTI_DENGAN_PIN_KUAT"
```

Tanpa konfigurasi tersebut, kalkulator tetap dapat dibuka, tetapi validasi token siswa dan akses guru tidak aktif.
