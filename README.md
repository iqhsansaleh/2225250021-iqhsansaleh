# 📐 AljabarKu: Kalkulator Aljabar Edukatif SMP Kelas 7

Proyek Perangkat Lunak Media Pembelajaran Matematika  
**Mata Kuliah:** Algoritma dan Pemrograman  
**Program Studi:** Pendidikan Matematika (Semester 3)  
**Referensi Inspirasi:** [MathPapa Algebra Calculator](https://www.mathpapa.com/algebra-calculator.html)

---

## 🧭 4 Panel Alur Pembelajaran (User Workflow)

Aplikasi ini menggunakan alur belajar bertahap (*multi-panel workflow*) dengan *State Management* (`st.session_state`):

1. **👋 Panel 1: Selamat Datang**
   * Sambutan ramah untuk siswa SMP.
   * Penjelasan pentingnya aljabar dan orientasi fitur aplikasi.
   * Tombol navigasi langsung menuju registrasi.

2. **📝 Panel 2: Registrasi Siswa**
   * Formulir identitas siswa: Nama Lengkap, Kelas (7A-7H), Asal Sekolah/Madrasah, No. Absen, dan Tingkat Pemahaman Awal.
   * Data siswa disimpan pada sesi aktif dan ditampilkan pada *sidebar*.

3. **📖 Panel 3: Tutorial Penggunaan**
   * **Aturan Penulisan:** Cara mengetik variabel (`x`, `y`), koefisien $1$ / $-1$, tanda negatif, dan pangkat `^`.
   * **Konsep Suku Sejenis:** Perbedaan mendasar suku sejenis vs tidak sejenis untuk mencegah miskonsepsi (misal: $3x + 4 \neq 7x$).
   * **Cara Membaca Langkah:** Panduan menelaah kartu penjelasan bertahap.

4. **🟢 Panel 4: Kalkulator Siap Digunakan**
   * Banner status hijau personal dengan nama dan kelas siswa.
   * **5 Tab Operasi Aljabar:**
     1. ➕ **Sederhanakan Aljabar** (Penjumlahan & Pengurangan Suku Sejenis)
     2. 🔍 **Bedah Unsur Aljabar** (Koefisien, Variabel, Konstanta, Jumlah Suku)
     3. ✖️ **Perkalian Distributif** ($k(ax + b)$)
     4. 🔢 **Evaluasi / Substitusi Nilai** (Hitung jika $x = c$)
     5. ⚖️ **Persamaan Linear Satu Variabel (PLSV)** ($ax + b = c$)

---

## ⚙️ Arsitektur Algoritma & Struktur Data

### A. Struktur Data Suku (`SukuAljabar`)
Di dalam [algebra_engine.py](file:///c:/2225250021_iqhsansaleh/algebra_engine.py):
* `koefisien` (float): Angka pengali suku.
* `variabel` (str / None): Simbol huruf peubah atau `None` jika konstanta.
* `pangkat` (int): Derajat eksponen variabel.
* `kunci_sejenis`: Mengembalikan *tuple* `(variabel, pangkat)`. Suku dikatakan sejenis jika memiliki kunci yang sama.

### B. Pipeline Eksekusi
1. **Tokenisasi (Regex):** String aljabar dipisahkan menjadi token bertanda (contoh: `3x + 5 - 2x` $\rightarrow$ `['+3x', '+5', '-2x']`).
2. **Parsing:** Setiap token dikonversi menjadi objek `SukuAljabar`.
3. **Grouping (Hash Map / Dictionary):** Suku dengan `kunci_sejenis` sama digabungkan koefisiennya.
4. **Step Logging:** Setiap fase kalkulasi direkam ke daftar riwayat penjelasan lengkap dengan format rumus LaTeX.

---

## 🚀 Cara Menjalankan Aplikasi di Laptop

1. Buka PowerShell atau Command Prompt pada folder proyek:
   ```powershell
   cd c:\2225250021_iqhsansaleh
   ```
2. Pastikan pustaka `streamlit` terpasang:
   ```powershell
   python -m pip install streamlit
   ```
3. Jalankan aplikasi web:
   ```powershell
   python -m streamlit run app.py
   ```
4. Buka browser pada alamat:
   ```
   http://localhost:8501
   ```
