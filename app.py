"""
app.py
Aplikasi Web Edukatif: Kalkulator Bentuk Aljabar SMP Kelas 7
Mata Kuliah: Algoritma dan Pemrograman
Program Studi: Pendidikan Matematika
"""

import streamlit as st
from algebra_engine import (
    bedah_unsur_aljabar,
    sederhanakan_aljabar,
    evaluasi_nilai_aljabar,
    perkalian_distributif,
    selesaikan_plsv
)

# -----------------------------------------------------------------------------
# 1. KONFIGURASI HALAMAN
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AljabarKu - Kalkulator Aljabar SMP",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Session State (State Manajemen)
if "current_panel" not in st.session_state:
    st.session_state.current_panel = "1. Selamat Datang"

if "pending_panel" in st.session_state:
    st.session_state.current_panel = st.session_state.pop("pending_panel")
    st.session_state.nav_radio = st.session_state.current_panel
elif "nav_radio" not in st.session_state:
    st.session_state.nav_radio = st.session_state.current_panel

if "siswa" not in st.session_state:
    st.session_state.siswa = {
        "nama": "",
        "kelas": "7A",
        "sekolah": "",
        "absen": "",
        "terdaftar": False
    }

# Kustomisasi CSS Styling
st.markdown("""
<style>
    .hero-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2.2rem;
        border-radius: 12px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .hero-desc {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    .panel-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .status-badge {
        display: inline-block;
        background-color: #10B981;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SIDEBAR NAVIGASI PANEL & PROFIL SISWA
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🧭 Navigasi Panel")
    
    daftar_panel = [
        "1. Selamat Datang",
        "2. Registrasi",
        "3. Tutorial",
        "4. Kalkulator Siap Digunakan"
    ]
    
    # Pilih panel melalui radio button
    pilihan_panel = st.radio(
        "Pilih Tahapan Pembelajaran:",
        options=daftar_panel,
        key="nav_radio"
    )
    
    # Sinkronisasi pilihan sidebar
    st.session_state.current_panel = pilihan_panel

    st.divider()

    # Panel Profil Siswa Aktif
    st.markdown("### 👤 Data Siswa Aktif")
    if st.session_state.siswa["terdaftar"]:
        st.success(f"**Nama:** {st.session_state.siswa['nama']}")
        st.write(f"**Kelas:** {st.session_state.siswa['kelas']}")
        if st.session_state.siswa['sekolah']:
            st.write(f"**Sekolah:** {st.session_state.siswa['sekolah']}")
        if st.session_state.siswa['absen']:
            st.write(f"**No. Presensi:** {st.session_state.siswa['absen']}")
    else:
        st.info("Siswa belum mengisi formulir registrasi.")

    st.divider()
    st.caption("📐 Proyek Algoritma & Pemrograman - Pendidikan Matematika (Smt 3)")


# Fungsi Helper untuk berpindah panel
def pindah_ke(nama_panel):
    st.session_state.pending_panel = nama_panel
    st.rerun()


# =============================================================================
# PANEL 1: SELAMAT DATANG
# =============================================================================
if st.session_state.current_panel == "1. Selamat Datang":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">👋 Selamat Datang di AljabarKu!</div>
        <div class="hero-desc">Media Belajar & Kalkulator Edukatif Bentuk Aljabar untuk Siswa SMP Kelas 7.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🎯 Mengapa Belajar dengan AljabarKu?")
        st.markdown("""
        Belajar aljabar sering kali membingungkan saat pertama kali bertemu huruf dan simbol. **AljabarKu** hadir bukan sekadar memberikan jawaban langsung, melainkan:
        
        * 🔍 **Membedah Bentuk Aljabar:** Mengenali mana yang disebut **koefisien**, **variabel**, dan **konstanta**.
        * ➕ **Menjelaskan Langkah demi Langkah (*Step-by-Step*):** Menunjukkan cara mengelompokkan suku-suku sejenis seperti di papan tulis guru.
        * ✖️ **Melatih Sifat Distributif:** Membantu mempermudah perkalian suku tunggal dengan suku dua $k(ax + b)$.
        * ⚖️ **Menemukan Solusi Persamaan:** Menyelesaikan Persamaan Linear Satu Variabel (PLSV) dengan prinsip keadilan kedua ruas.
        """)

    with col2:
        st.markdown("### 📋 Alur Belajar Anda")
        st.markdown("""
        1. **Selamat Datang** *(Halaman ini)*
        2. **Registrasi Data Siswa** (Isi identitas singkat)
        3. **Tutorial Penggunaan** (Pahami aturan penulisan)
        4. **Kalkulator Siap Digunakan** (Mulai menghitung & belajar)
        """)
        st.write("")
        if st.button("👉 Lanjut ke Panel Registrasi ➡️", type="primary", use_container_width=True):
            pindah_ke("2. Registrasi")


# =============================================================================
# PANEL 2: REGISTRASI SISWA
# =============================================================================
elif st.session_state.current_panel == "2. Registrasi":
    st.subheader("📝 Panel 2: Registrasi Identitas Siswa")
    st.write("Silakan lengkapi formulir di bawah ini agar sesi belajar Anda tercatat dengan baik:")

    with st.container():
        with st.form("form_registrasi"):
            col_nama, col_kelas = st.columns([3, 1])
            with col_nama:
                nama_input = st.text_input(
                    "Nama Lengkap Siswa *",
                    value=st.session_state.siswa["nama"],
                    placeholder="Contoh: Budi Santoso"
                )
            with col_kelas:
                kelas_input = st.selectbox(
                    "Kelas *",
                    options=["7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H", "Lainnya"],
                    index=0
                )

            col_sekolah, col_absen = st.columns([3, 1])
            with col_sekolah:
                sekolah_input = st.text_input(
                    "Asal Sekolah / Madrasah",
                    value=st.session_state.siswa["sekolah"],
                    placeholder="Contoh: SMP Negeri 1"
                )
            with col_absen:
                absen_input = st.text_input(
                    "Nomor Absen / Presensi",
                    value=st.session_state.siswa["absen"],
                    placeholder="Contoh: 14"
                )

            tingkat_paham = st.select_slider(
                "Bagaimana pemahaman awal Anda tentang Bentuk Aljabar?",
                options=["Baru Mulai Belajar", "Cukup Paham", "Sangat Menguasai"],
                value="Baru Mulai Belajar"
            )

            submit_btn = st.form_submit_button("💾 Simpan Data & Lanjut ke Tutorial", type="primary")

            if submit_btn:
                if not nama_input.strip():
                    st.warning("⚠️ Mohon isi Nama Lengkap Siswa terlebih dahulu!")
                else:
                    st.session_state.siswa["nama"] = nama_input.strip()
                    st.session_state.siswa["kelas"] = kelas_input
                    st.session_state.siswa["sekolah"] = sekolah_input.strip()
                    st.session_state.siswa["absen"] = absen_input.strip()
                    st.session_state.siswa["terdaftar"] = True
                    st.success(f"Terima kasih, **{nama_input}**! Data Anda berhasil disimpan.")
                    pindah_ke("3. Tutorial")


# =============================================================================
# PANEL 3: TUTORIAL PENGGUNAAN
# =============================================================================
elif st.session_state.current_panel == "3. Tutorial":
    st.subheader("📖 Panel 3: Tutorial & Panduan Penggunaan Kalkulator")
    st.write("Sebelum masuk ke kalkulator, pelajari aturan penulisan dan cara kerja aplikasi:")

    tab_tutor1, tab_tutor2, tab_tutor3 = st.tabs([
        "⌨️ Aturan Penulisan Simbol",
        "🎯 Konsep Suku Sejenis",
        "💡 Cara Membaca Hasil"
    ])

    with tab_tutor1:
        st.markdown("#### 1. Cara Mengetik Bentuk Aljabar di Kalkulator")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("""
            * **Variabel:** Gunakan huruf kecil seperti `x`, `y`, `a`, atau `b`.
            * **Koefisien 1 atau -1:** Cukup tulis variabelnya saja.
              * ✅ Tulis `x` *(bukan `1x`)*
              * ✅ Tulis `-x` *(bukan `-1x`)*
            * **Suku Negatif:** Gunakan tanda minus biasa `-`.
              * Contoh: `4x - 5y`
            """)
        with col_t2:
            st.markdown("""
            * **Pangkat Aljabar:** Gunakan tanda sisip `^`.
              * Contoh: `x^2` untuk $x^2$, atau `3x^2` untuk $3x^2$.
            * **Perkalian Distributif:** Tulis pengali dan isi tanda kurung secara terpisah pada kolom yang disediakan.
            * **Persamaan (PLSV):** Wajib menggunakan tanda sama dengan `=`.
              * Contoh: `2x + 5 = 15`.
            """)

    with tab_tutor2:
        st.markdown("#### 2. Kunci Utama: Apa itu Suku Sejenis?")
        st.info("""
        **Suku Sejenis** adalah suku-suku dalam aljabar yang memiliki **variabel sama DAN pangkat yang sama**.
        Hanya suku sejenis yang koefisiennya boleh dijumlahkan atau dikurangkan!
        """)
        st.markdown("""
        * **Contoh Suku Sejenis:**
          * $3x$ dan $5x$ *(Sama-sama variabel $x$ pangkat $1$)* $\\rightarrow 3x + 5x = 8x$.
          * $7$ dan $-3$ *(Sama-sama konstanta)* $\\rightarrow 7 - 3 = 4$.
        * **Contoh Suku TIDAK Sejenis:**
          * $3x$ dan $4y$ *(Variabel berbeda, TIDAK BISA dijumlahkan menjadi $7xy$!)*
          * $2x^2$ dan $5x$ *(Pangkat berbeda, TIDAK BISA dijumlahkan menjadi $7x^3$!)*
        """)

    with tab_tutor3:
        st.markdown("#### 3. Membaca Langkah Penyelesaian (*Step-by-Step*)")
        st.markdown("""
        Saat Anda menekan tombol **'Sederhanakan'** atau **'Hitung'**, kalkulator akan menampilkan:
        1. **Bentuk Paling Sederhana:** Jawaban akhir matematis berformat rapi.
        2. **Kartu Langkah demi Langkah:** Penjelasan tertulis lengkap dengan rumus perantara:
           * Mengumpulkan suku sejenis dalam tanda kurung.
           * Menjumlahkan/mengurangkan angka koefisiennya.
           * Menyusun bentuk akhir dari pangkat tertinggi.
        """)

    st.divider()
    nama_panggilan = st.session_state.siswa['nama'] if st.session_state.siswa['terdaftar'] else "Siswa"
    st.write(f"Siap untuk mulai mencoba, **{nama_panggilan}**?")
    
    col_kembali, col_lanjut = st.columns([1, 2])
    with col_kembali:
        if st.button("⬅️ Kembali ke Registrasi"):
            pindah_ke("2. Registrasi")
    with col_lanjut:
        if st.button("🚀 Buka Panel Kalkulator Siap Digunakan! ➡️", type="primary", use_container_width=True):
            pindah_ke("4. Kalkulator Siap Digunakan")


# =============================================================================
# PANEL 4: KALKULATOR SIAP DIGUNAKAN
# =============================================================================
elif st.session_state.current_panel == "4. Kalkulator Siap Digunakan":
    # Header Banner Kalkulator Siap Digunakan
    nama_siswa = st.session_state.siswa["nama"] if st.session_state.siswa["terdaftar"] else "Pengguna"
    kelas_siswa = f"({st.session_state.siswa['kelas']})" if st.session_state.siswa["terdaftar"] else ""
    
    st.markdown(f"""
    <div style="background-color: #ECFDF5; border: 1px solid #10B981; border-radius: 10px; padding: 1.2rem; margin-bottom: 1.5rem;">
        <span class="status-badge">🟢 Kalkulator Siap Digunakan</span>
        <h3 style="color: #065F46; margin-top: 0.5rem; margin-bottom: 0.2rem;">Selamat Belajar, {nama_siswa} {kelas_siswa}!</h3>
        <p style="color: #047857; margin-bottom: 0;">Silakan pilih tab operasi aljabar di bawah ini untuk memulai perhitungan.</p>
    </div>
    """, unsafe_allow_html=True)

    # 5 Tab Operasi Aljabar Kelas 7 SMP
    tab_sederhana, tab_bedah, tab_distributif, tab_substitusi, tab_plsv = st.tabs([
        "➕ 1. Sederhanakan Aljabar",
        "🔍 2. Bedah Unsur Aljabar",
        "✖️ 3. Perkalian Distributif",
        "🔢 4. Evaluasi / Substitusi",
        "⚖️ 5. Persamaan Linear (PLSV)"
    ])

    # -------------------------------------------------------------------------
    # TAB 1: SEDERHANAKAN ALJABAR
    # -------------------------------------------------------------------------
    with tab_sederhana:
        st.subheader("Operasi Penjumlahan & Pengurangan Suku Sejenis")
        st.write("Sederhanakan bentuk aljabar dan pelajari pengelompokan suku sejenisnya:")

        col_input, col_preset = st.columns([3, 1])
        with col_preset:
            contoh = st.selectbox(
                "Contoh Soal Cepat:",
                [
                    "Ketik Sendiri...",
                    "5x + 3 - 2x + 7",
                    "4a - 3b + 2a - 5b",
                    "3x^2 + 5x - 2x^2 + 4",
                    "7y - 2 + 3y - 8"
                ]
            )

        with col_input:
            default_val = "5x + 3 - 2x + 7" if contoh == "Ketik Sendiri..." else contoh
            ekspresi_input = st.text_input("Masukkan Bentuk Aljabar:", value=default_val, key="input_simp_4")

        if st.button("🚀 Sederhanakan Sekarang", type="primary", key="btn_simp_4"):
            try:
                hasil = sederhanakan_aljabar(ekspresi_input)
                st.success("✅ Berhasil Disederhanakan!")

                col_res1, col_res2 = st.columns([1, 2])
                with col_res1:
                    st.metric(label="Bentuk Paling Sederhana", value="")
                    st.latex(hasil["hasil_latex"])

                with col_res2:
                    st.markdown("### 📝 Langkah Penyelesaian Lengkap:")
                    for step in hasil["langkah_langkah"]:
                        with st.expander(f"📌 {step['judul']}", expanded=True):
                            st.write(step["penjelasan"])
                            st.latex(step["latex"])
            except Exception as e:
                st.error(f"⚠️ Terjadi kesalahan format: {str(e)}")
                st.info("Pastikan format input benar, contoh: `3x + 5 - 2x + 7`.")

    # -------------------------------------------------------------------------
    # TAB 2: BEDAH UNSUR ALJABAR
    # -------------------------------------------------------------------------
    with tab_bedah:
        st.subheader("Mengenal Variabel, Koefisien, Konstanta, dan Suku")
        st.write("Identifikasi anatomi unsur pembentuk dari suatu bentuk aljabar:")

        input_bedah = st.text_input("Masukkan Bentuk Aljabar:", value="3x^2 - 5x + 8", key="input_bedah_4")
        if st.button("🔍 Bedah Sekarang", type="primary", key="btn_bedah_4"):
            try:
                data = bedah_unsur_aljabar(input_bedah)
                st.markdown("**Bentuk Matematika:**")
                st.latex(data["ekspresi_latex"])

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"**Banyak Suku:**\n### {data['banyak_suku']}\n*({data['klasifikasi_suku']})*")
                with col2:
                    var_str = ", ".join(data["variabel"])
                    st.success(f"**Variabel:**\n### {var_str}")
                with col3:
                    st.warning(f"**Konstanta:**\n### {data['konstanta']}")

                st.divider()
                st.markdown("#### 📋 Rincian Koefisien Masing-Masing Variabel:")
                for var_name, nilai_koef in data["koefisien"].items():
                    st.write(f"- Koefisien dari suku $\\mathbf{{{var_name}}}$ adalah: **{nilai_koef}**")
            except Exception as e:
                st.error(f"Gagal membedah bentuk aljabar: {str(e)}")

    # -------------------------------------------------------------------------
    # TAB 3: PERKALIAN DISTRIBUTIF
    # -------------------------------------------------------------------------
    with tab_distributif:
        st.subheader("Perkalian Suku Tunggal dengan Suku Dua: $k(ax + b)$")
        st.write("Menjabarkan perkalian dengan sifat distributif:")

        col_k, col_kurung = st.columns([1, 3])
        with col_k:
            k_val = st.number_input("Pengali Luar (k):", value=3, step=1, key="num_k_4")
        with col_kurung:
            isi_kurung = st.text_input("Bentuk Aljabar di dalam Kurung:", value="2x - 5", key="str_kurung_4")

        if st.button("🚀 Kalikan Secara Distributif", type="primary", key="btn_dist_4"):
            try:
                hasil_dist = perkalian_distributif(float(k_val), isi_kurung)
                st.success("✅ Hasil Perkalian:")
                st.latex(hasil_dist["hasil_latex"])

                st.markdown("### 📝 Langkah Penjabaran Distributif:")
                for step in hasil_dist["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(f"Kesalahan pada input perkalian: {str(e)}")

    # -------------------------------------------------------------------------
    # TAB 4: EVALUASI / SUBSTITUSI
    # -------------------------------------------------------------------------
    with tab_substitusi:
        st.subheader("Menentukan Nilai Bentuk Aljabar (Substitusi Nilai Variabel)")
        st.write("Hitung nilai numerik aljabar saat nilai variabel telah diketahui:")

        col_eks, col_var = st.columns([2, 1])
        with col_eks:
            subst_ekspresi = st.text_input("Bentuk Aljabar:", value="2x + 7", key="input_subst_4")
        with col_var:
            nilai_x = st.number_input("Nilai Variabel (x):", value=4, step=1, key="num_x_4")

        if st.button("🔢 Hitung Nilai", type="primary", key="btn_subst_4"):
            try:
                res_subst = evaluasi_nilai_aljabar(subst_ekspresi, {"x": float(nilai_x)})
                st.success(f"✅ Nilai Bentuk Aljabar adalah: **{res_subst['hasil_akhir']}**")

                st.markdown("### 📝 Langkah Substitusi dan Perhitungan:")
                for step in res_subst["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(f"Kesalahan evaluasi nilai: {str(e)}")

    # -------------------------------------------------------------------------
    # TAB 5: PERSAMAAN LINEAR SATU VARIABEL (PLSV)
    # -------------------------------------------------------------------------
    with tab_plsv:
        st.subheader("Penyelesaian Persamaan Linear Satu Variabel: $ax + b = c$")
        st.write("Selesaikan persamaan dengan konsep kesetaraan ruas kiri dan kanan:")

        input_plsv = st.text_input("Masukkan Persamaan (Gunakan tanda '='):", value="2x + 5 = 15", key="input_plsv_4")

        if st.button("⚖️ Selesaikan Persamaan", type="primary", key="btn_plsv_4"):
            try:
                res_plsv = selesaikan_plsv(input_plsv)
                st.success(f"✅ Solusi: **{res_plsv['solusi']}**")

                st.markdown("### 📝 Langkah Penyelesaian:")
                for step in res_plsv["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(f"Kesalahan pada persamaan: {str(e)}")
                st.info("Pastikan persamaan memiliki satu tanda sama dengan (`=`), contoh: `3x - 4 = 11`.")
