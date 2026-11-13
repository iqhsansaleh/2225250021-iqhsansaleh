"""
app.py
Aplikasi Web Edukatif: Kalkulator Bentuk Aljabar SMP Kelas 7
Mata Kuliah: Algoritma dan Pemrograman
Program Studi: Pendidikan Matematika

Fitur Khusus:
1. Navigasi Panel Terkunci (Hanya untuk Guru/Peneliti)
2. Sistem Token Akses Registrasi Siswa
3. Penyimpanan Data Siswa ke CSV (Data Guru) & Unduh Rekap
4. Panel Keluar / Akhiri Sesi Belajar Siswa
"""

import os
import csv
import json
from datetime import datetime
import streamlit as st
import pandas as pd
from algebra_engine import (
    bedah_unsur_aljabar,
    sederhanakan_aljabar,
    evaluasi_nilai_aljabar,
    perkalian_distributif,
    selesaikan_plsv
)

# -----------------------------------------------------------------------------
# 1. KONFIGURASI FILE DATA & TOKEN
# -----------------------------------------------------------------------------
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_DATA_SISWA = os.path.join(DATA_DIR, "data_siswa.csv")
FILE_CONFIG = os.path.join(DATA_DIR, "config_guru.json")

# Inisialisasi file CSV data siswa jika belum ada
if not os.path.exists(FILE_DATA_SISWA):
    with open(FILE_DATA_SISWA, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Waktu_Registrasi", "Nama_Siswa", "Kelas", "Asal_Sekolah", "No_Absen", "Pemahaman_Awal"])

def ambil_konfigurasi():
    try:
        with open(FILE_CONFIG, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        try:
            token_aktif = st.secrets.get("token_aktif", "")
            pin_guru = st.secrets.get("pin_guru", "")
        except Exception:
            token_aktif = os.environ.get("ALJABAR_TOKEN_AKTIF", "")
            pin_guru = os.environ.get("ALJABAR_PIN_GURU", "")
        return {"token_aktif": str(token_aktif), "pin_guru": str(pin_guru)}

def simpan_konfigurasi(token_baru, pin_baru):
    with open(FILE_CONFIG, mode="w", encoding="utf-8") as f:
        json.dump({"token_aktif": token_baru.strip().upper(), "pin_guru": pin_baru.strip()}, f, indent=4)

def simpan_data_siswa_ke_csv(nama, kelas, sekolah, absen, pemahaman):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_DATA_SISWA, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([waktu, nama, kelas, sekolah, absen, pemahaman])

# -----------------------------------------------------------------------------
# 2. KONFIGURASI HALAMAN & STATE MANAGEMENT
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AljabarKu - Media Pembelajaran SMP",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Session State
if "current_panel" not in st.session_state:
    st.session_state.current_panel = "1. Selamat Datang"

if "is_guru" not in st.session_state:
    st.session_state.is_guru = False

if "siswa" not in st.session_state:
    st.session_state.siswa = {
        "nama": "",
        "kelas": "7A",
        "sekolah": "",
        "absen": "",
        "terdaftar": False
    }

def pindah_ke(nama_panel):
    st.session_state.current_panel = nama_panel
    st.rerun()

def reset_sesi_siswa():
    st.session_state.siswa = {
        "nama": "",
        "kelas": "7A",
        "sekolah": "",
        "absen": "",
        "terdaftar": False
    }
    st.session_state.current_panel = "1. Selamat Datang"
    st.rerun()

# Styling CSS
st.markdown("""
<style>
    .hero-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        color: white;
        padding: 2.2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
    .hero-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; }
    .hero-desc { font-size: 1.1rem; opacity: 0.95; }
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
# 3. SIDEBAR: MODE GURU (NAVIGASI TERTUTUP) & STATUS SISWA
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📐 AljabarKu SMP")

    # Bagian 1: Informasi Siswa Aktif
    if st.session_state.siswa["terdaftar"]:
        st.success(f"👤 **{st.session_state.siswa['nama']}** ({st.session_state.siswa['kelas']})")
        if st.session_state.siswa["sekolah"]:
            st.caption(f"🏫 {st.session_state.siswa['sekolah']}")

        # Tombol Keluar Cepat untuk Siswa
        if st.session_state.current_panel == "4. Kalkulator Siap Digunakan":
            if st.button("🚪 Keluar / Selesai Sesi", type="secondary", use_container_width=True):
                pindah_ke("5. Keluar")
    else:
        st.info("Status: Sesi Pembelajaran Siswa Baru")

    st.divider()

    # Bagian 2: Panel Khusus Guru / Peneliti (Password Protected)
    with st.expander("🔒 Akses Khusus Guru / Peneliti"):
        cfg = ambil_konfigurasi()

        if not st.session_state.is_guru:
            st.write("Masukkan PIN Guru untuk membuka kontrol panel dan rekap data siswa:")
            pin_input = st.text_input("PIN Guru:", type="password", key="input_pin_guru")
            if st.button("Masuk Mode Guru 🔓", key="btn_login_guru"):
                if cfg["pin_guru"] and pin_input == cfg["pin_guru"]:
                    st.session_state.is_guru = True
                    st.success("Akses Guru Berhasil Diberikan!")
                    st.rerun()
                elif not cfg["pin_guru"]:
                    st.error("PIN Guru belum dikonfigurasi oleh administrator.")
                else:
                    st.error("PIN Guru tidak valid! Akses ditolak.")
        else:
            st.success("✅ **Mode Guru Aktif**")

            # 1. Navigasi Bebas untuk Guru
            st.markdown("#### 🧭 Navigasi Panel (Khusus Guru):")
            semua_panel = [
                "1. Selamat Datang",
                "2. Registrasi",
                "3. Tutorial",
                "4. Kalkulator Siap Digunakan",
                "5. Keluar",
                "📊 Dashboard Data Siswa"
            ]
            panel_pilihan = st.selectbox(
                "Lompat Langsung ke Panel:",
                semua_panel,
                index=semua_panel.index(st.session_state.current_panel) if st.session_state.current_panel in semua_panel else 0
            )
            if st.button("Buka Panel Terpilih ⏩"):
                pindah_ke(panel_pilihan)

            st.divider()

            # 2. Pengaturan Token Aktif
            st.markdown("#### 🔑 Pengaturan Token Ujian:")
            st.info(f"Token Saat Ini: **`{cfg['token_aktif']}`**")
            token_baru = st.text_input("Ubah Token Baru:", value=cfg["token_aktif"], key="input_ubah_token")
            pin_baru = st.text_input("Ubah PIN Guru:", value=cfg["pin_guru"], type="password", key="input_ubah_pin")
            if st.button("Simpan Pengaturan 💾"):
                simpan_konfigurasi(token_baru, pin_baru)
                st.success("Token & PIN berhasil diperbarui!")
                st.rerun()

            st.divider()
            if st.button("Keluar Mode Guru 🔒"):
                st.session_state.is_guru = False
                st.rerun()

    st.caption("Proyek Smt 3 - Pendidikan Matematika")


# =============================================================================
# PANEL 1: SELAMAT DATANG (Tampilan Siswa)
# =============================================================================
if st.session_state.current_panel == "1. Selamat Datang":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">👋 Selamat Datang di AljabarKu!</div>
        <div class="hero-desc">Media Belajar & Kalkulator Bentuk Aljabar Berbantuan Langkah demi Langkah untuk Siswa SMP Kelas 7.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🎯 Petunjuk Awal Siswa")
        st.markdown("""
        Selamat datang di uji coba aplikasi pembelajaran **AljabarKu**!

        Pada sesi ini, Anda akan:
        1. **Mengisi Identitas Diri & Token** yang diberikan oleh Guru/Peneliti.
        2. **Mempelajari Tutorial Singkat** mengenai aturan simbol dan konsep suku sejenis.
        3. **Menggunakan Kalkulator Aljabar** untuk menyelesaikan dan memahami soal secara bertahap.

        *Siapkan **Token Akses** yang telah dibagikan oleh guru sebelum melanjutkan.*
        """)

    with col2:
        st.markdown("### 🚀 Mulai Uji Coba")
        st.info("Pastikan Anda sudah memiliki Token dari Guru.")
        if st.button("👉 Lanjut ke Panel Registrasi ➡️", type="primary", use_container_width=True):
            pindah_ke("2. Registrasi")


# =============================================================================
# PANEL 2: REGISTRASI + TOKEN AKSES (Tampilan Siswa)
# =============================================================================
elif st.session_state.current_panel == "2. Registrasi":
    st.subheader("📝 Panel 2: Registrasi Siswa & Validasi Token")
    st.write("Silakan lengkapi data diri Anda dan masukkan Token Akses dari guru untuk beralih ke Tutorial:")

    cfg = ambil_konfigurasi()
    token_valid = cfg["token_aktif"].strip().upper()
    if not token_valid:
        st.warning("Token akses belum dikonfigurasi oleh administrator.")

    with st.form("form_registrasi_siswa"):
        col_nama, col_kelas = st.columns([3, 1])
        with col_nama:
            nama_input = st.text_input("Nama Lengkap Siswa *", value=st.session_state.siswa["nama"], placeholder="Contoh: Siti Rahmawati")
        with col_kelas:
            kelas_input = st.selectbox("Kelas *", ["7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H", "Lainnya"])

        col_sekolah, col_absen = st.columns([3, 1])
        with col_sekolah:
            sekolah_input = st.text_input("Asal Sekolah / Madrasah *", value=st.session_state.siswa["sekolah"], placeholder="Contoh: SMP Negeri 1")
        with col_absen:
            absen_input = st.text_input("Nomor Presensi / Absen *", value=st.session_state.siswa["absen"], placeholder="Contoh: 18")

        tingkat_paham = st.select_slider(
            "Bagaimana pemahaman awal Anda tentang Bentuk Aljabar saat ini?",
            options=["Belum Paham", "Cukup Paham", "Sangat Paham"],
            value="Belum Paham"
        )

        st.divider()
        # Input Token Pembelajaran
        st.markdown("#### 🔑 Masukkan Token Pembelajaran")
        token_input = st.text_input("Token Akses Guru *", placeholder="Ketik token akses yang diberikan oleh guru").strip().upper()

        btn_submit = st.form_submit_button("💾 Validasi Token & Masuk ke Tutorial ➡️", type="primary")

        if btn_submit:
            if not nama_input.strip() or not sekolah_input.strip() or not absen_input.strip():
                st.warning("⚠️ Mohon lengkapi seluruh data diri (Nama, Sekolah, dan Nomor Presensi)!")
            elif token_input != token_valid:
                st.error("❌ Token Akses Salah! Silakan tanyakan Token yang benar kepada Guru / Peneliti.")
            else:
                # Simpan data ke memori sesi aktif
                st.session_state.siswa["nama"] = nama_input.strip()
                st.session_state.siswa["kelas"] = kelas_input
                st.session_state.siswa["sekolah"] = sekolah_input.strip()
                st.session_state.siswa["absen"] = absen_input.strip()
                st.session_state.siswa["terdaftar"] = True

                # Simpan otomatis ke database file CSV guru
                simpan_data_siswa_ke_csv(
                    nama_input.strip(),
                    kelas_input,
                    sekolah_input.strip(),
                    absen_input.strip(),
                    tingkat_paham
                )

                st.success(f"✅ Token Valid! Data berhasil dicatat ke sistem guru. Selamat datang, {nama_input}!")
                pindah_ke("3. Tutorial")


# =============================================================================
# PANEL 3: TUTORIAL (Tampilan Siswa)
# =============================================================================
elif st.session_state.current_panel == "3. Tutorial":
    nama_siswa = st.session_state.siswa["nama"] if st.session_state.siswa["terdaftar"] else "Siswa"
    st.subheader(f"📖 Panel 3: Tutorial Penggunaan untuk {nama_siswa}")
    st.write("Pelajari aturan penulisan dan konsep aljabar berikut sebelum membuka kalkulator:")

    tab1, tab2, tab3 = st.tabs(["⌨️ Aturan Penulisan Simbol", "🎯 Konsep Suku Sejenis", "💡 Cara Membaca Langkah"])

    with tab1:
        st.markdown("""
        * **Variabel:** Gunakan huruf kecil tunggal seperti `x`, `y`, `a`, atau `b`.
        * **Koefisien 1 atau -1:** Cukup tulis variabelnya saja:
          * ✅ Tulis `x` *(bukan `1x`)*
          * ✅ Tulis `-x` *(bukan `-1x`)*
        * **Pangkat Aljabar:** Gunakan tanda sisip `^`.
          * Contoh: `x^2` untuk $x^2$, atau `3x^2` untuk $3x^2$.
        * **Persamaan Linear (PLSV):** Wajib menggunakan tanda sama dengan `=`. Contoh: `2x + 5 = 15`.
        """)

    with tab2:
        st.info("**Suku Sejenis** adalah suku-suku yang memiliki **variabel sama DAN pangkat yang sama**.")
        st.markdown("""
        * **Bisa Dijumlahkan (Suku Sejenis):**
          * $4x + 3x = 7x$ *(Variabel sama-sama $x$)*
          * $8 - 3 = 5$ *(Sama-sama konstanta)*
        * **TIDAK BISA Dijumlahkan (Bukan Suku Sejenis):**
          * $3x + 4y$ $\\rightarrow$ **Tetap** $3x + 4y$ *(Jangan dijumlahkan jadi $7xy$!)*
          * $2x^2 + 5x$ $\\rightarrow$ **Tetap** $2x^2 + 5x$ *(Pangkat berbeda!)*
        """)

    with tab3:
        st.markdown("""
        Kalkulator AljabarKu dirancang untuk **mengajarkan proses berpikir**:
        1. **Bentuk Paling Sederhana:** Menampilkan jawaban akhir matematis.
        2. **Kotak Langkah demi Langkah:** Membuka rahasia bagaimana suku sejenis dikelompokkan dalam tanda kurung dan dihitung satu per satu.
        """)

    st.divider()
    if st.button("🚀 Saya Sudah Siap, Buka Kalkulator Aljabar! ➡️", type="primary", use_container_width=True):
        pindah_ke("4. Kalkulator Siap Digunakan")


# =============================================================================
# PANEL 4: KALKULATOR SIAP DIGUNAKAN (Tampilan Siswa)
# =============================================================================
elif st.session_state.current_panel == "4. Kalkulator Siap Digunakan":
    nama_siswa = st.session_state.siswa["nama"] if st.session_state.siswa["terdaftar"] else "Pengguna"
    kelas_siswa = f"({st.session_state.siswa['kelas']})" if st.session_state.siswa["terdaftar"] else ""

    col_head1, col_head2 = st.columns([4, 1])
    with col_head1:
        st.markdown(f"""
        <div style="background-color: #ECFDF5; border: 1px solid #10B981; border-radius: 10px; padding: 1.2rem; margin-bottom: 1.2rem;">
            <span class="status-badge">🟢 Kalkulator Siap Digunakan</span>
            <h3 style="color: #065F46; margin-top: 0.5rem; margin-bottom: 0.2rem;">Selamat Belajar, {nama_siswa} {kelas_siswa}!</h3>
            <p style="color: #047857; margin-bottom: 0;">Silakan pilih tab operasi di bawah ini untuk memulai.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_head2:
        st.write("")
        if st.button("🚪 Selesaikan Sesi & Keluar", type="secondary", use_container_width=True):
            pindah_ke("5. Keluar")

    # 5 Tab Kalkulator Aljabar
    tab_sederhana, tab_bedah, tab_distributif, tab_substitusi, tab_plsv = st.tabs([
        "➕ 1. Sederhanakan Aljabar",
        "🔍 2. Bedah Unsur Aljabar",
        "✖️ 3. Perkalian Distributif",
        "🔢 4. Evaluasi / Substitusi",
        "⚖️ 5. Persamaan Linear (PLSV)"
    ])

    with tab_sederhana:
        st.subheader("Operasi Penjumlahan & Pengurangan Suku Sejenis")
        col_in, col_pre = st.columns([3, 1])
        with col_pre:
            contoh = st.selectbox("Contoh Soal:", ["Ketik Sendiri...", "5x + 3 - 2x + 7", "4a - 3b + 2a - 5b", "3x^2 + 5x - 2x^2 + 4"])
        with col_in:
            def_val = "5x + 3 - 2x + 7" if contoh == "Ketik Sendiri..." else contoh
            eks_in = st.text_input("Bentuk Aljabar:", value=def_val, key="in_simp")

        if st.button("🚀 Sederhanakan Sekarang", type="primary", key="btn_simp"):
            try:
                hasil = sederhanakan_aljabar(eks_in)
                st.success("✅ Bentuk Paling Sederhana:")
                st.latex(hasil["hasil_latex"])
                st.markdown("### 📝 Langkah Penyelesaian:")
                for step in hasil["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(f"Format salah: {str(e)}")

    with tab_bedah:
        st.subheader("Mengenal Variabel, Koefisien, Konstanta, dan Suku")
        in_bedah = st.text_input("Masukkan Bentuk Aljabar:", value="3x^2 - 5x + 8", key="in_bedah")
        if st.button("🔍 Bedah Bentuk Aljabar", type="primary", key="btn_bedah"):
            try:
                data = bedah_unsur_aljabar(in_bedah)
                st.latex(data["ekspresi_latex"])
                c1, c2, c3 = st.columns(3)
                c1.info(f"**Banyak Suku:**\n### {data['banyak_suku']}")
                c2.success(f"**Variabel:**\n### {', '.join(data['variabel'])}")
                c3.warning(f"**Konstanta:**\n### {data['konstanta']}")
                st.markdown("#### Koefisien:")
                for k, v in data["koefisien"].items():
                    st.write(f"- Suku **{k}**: {v}")
            except Exception as e:
                st.error(str(e))

    with tab_distributif:
        st.subheader("Perkalian Distributif: $k(ax + b)$")
        col_k, col_kr = st.columns([1, 3])
        with col_k:
            k_val = st.number_input("Pengali (k):", value=3, step=1)
        with col_kr:
            isi_kr = st.text_input("Didalam Kurung:", value="2x - 5")
        if st.button("🚀 Kalikan Distributif", type="primary", key="btn_dist"):
            try:
                hasil_dist = perkalian_distributif(float(k_val), isi_kr)
                st.latex(hasil_dist["hasil_latex"])
                for step in hasil_dist["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(str(e))

    with tab_substitusi:
        st.subheader("Menentukan Nilai Bentuk Aljabar (Substitusi)")
        col_e, col_v = st.columns([2, 1])
        with col_e:
            subst_e = st.text_input("Bentuk Aljabar:", value="2x + 7")
        with col_v:
            subst_x = st.number_input("Nilai x:", value=4, step=1)
        if st.button("🔢 Hitung Nilai", type="primary", key="btn_subst"):
            try:
                res_subst = evaluasi_nilai_aljabar(subst_e, {"x": float(subst_x)})
                st.success(f"Hasil: **{res_subst['hasil_akhir']}**")
                for step in res_subst["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(str(e))

    with tab_plsv:
        st.subheader("Persamaan Linear Satu Variabel: $ax + b = c$")
        in_plsv = st.text_input("Persamaan:", value="2x + 5 = 15")
        if st.button("⚖️ Selesaikan Persamaan", type="primary", key="btn_plsv"):
            try:
                res_plsv = selesaikan_plsv(in_plsv)
                st.success(f"Solusi: **{res_plsv['solusi']}**")
                for step in res_plsv["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(str(e))


# =============================================================================
# PANEL 5: KELUAR DARI APLIKASI
# =============================================================================
elif st.session_state.current_panel == "5. Keluar":
    nama_siswa = st.session_state.siswa["nama"] if st.session_state.siswa["terdaftar"] else "Siswa"

    st.markdown(f"""
    <div style="background-color: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 12px; padding: 2.5rem; text-align: center;">
        <h1 style="color: #1E293B; margin-bottom: 0.5rem;">🎓 Sesi Belajar Telah Selesai</h1>
        <h3 style="color: #475569; margin-bottom: 1.5rem;">Terima kasih, <b>{nama_siswa}</b>!</h3>
        <p style="font-size: 1.1rem; color: #64748B; max-width: 600px; margin: 0 auto 2rem auto;">
            Anda telah berhasil menyelesaikan uji coba media pembelajaran <b>AljabarKu</b>.
            Data registrasi Anda telah tersimpan dengan aman pada sistem Guru/Peneliti.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    col_reset1, col_reset2, col_reset3 = st.columns([1, 2, 1])
    with col_reset2:
        if st.button("🔄 Mulai Sesi Baru untuk Siswa Lain", type="primary", use_container_width=True):
            reset_sesi_siswa()


# =============================================================================
# PANEL 6: DASHBOARD DATA SISWA (Hanya Bisa Dibuka oleh Guru)
# =============================================================================
elif st.session_state.current_panel == "📊 Dashboard Data Siswa":
    if not st.session_state.is_guru:
        st.error("⛔ Akses Ditolak! Panel ini hanya dapat diakses oleh Guru / Peneliti.")
        if st.button("Kembali ke Beranda"):
            pindah_ke("1. Selamat Datang")
    else:
        st.subheader("📊 Rekap Data Registrasi Siswa (Panel Guru)")
        st.write("Semua siswa yang memasukkan token yang valid akan tercatat di tabel ini:")

        if os.path.exists(FILE_DATA_SISWA):
            try:
                df = pd.read_csv(FILE_DATA_SISWA)
                st.markdown(f"**Total Siswa Terdaftar:** `{len(df)} Siswa`")
                st.dataframe(df, use_container_width=True)

                col_d1, col_d2 = st.columns([2, 1])
                with col_d1:
                    # Tombol Unduh CSV
                    csv_data = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Unduh Rekap Data Siswa (Format CSV / Excel)",
                        data=csv_data,
                        file_name=f"rekap_siswa_aljabar_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        type="primary"
                    )
                with col_d2:
                    if st.button("🗑️ Kosongkan Seluruh Data Siswa", type="secondary"):
                        with open(FILE_DATA_SISWA, mode="w", newline="", encoding="utf-8") as f:
                            writer = csv.writer(f)
                            writer.writerow(["Waktu_Registrasi", "Nama_Siswa", "Kelas", "Asal_Sekolah", "No_Absen", "Pemahaman_Awal"])
                        st.warning("Data siswa berhasil dikosongkan.")
                        st.rerun()
            except Exception as e:
                st.error(f"Gagal membaca data: {str(e)}")
        else:
            st.info("Belum ada data siswa yang masuk.")
