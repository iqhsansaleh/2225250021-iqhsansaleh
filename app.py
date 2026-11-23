"""
app.py
Aplikasi Web Edukatif: Kalkulator Bentuk Aljabar SMP Kelas 7
Berbasis Pendekatan: Rigorous Mathematical Thinking (RMT)
Mata Kuliah: Algoritma dan Pemrograman
Program Studi: Pendidikan Matematika
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
from ai_tutor import ambil_gemini_api_key, tanya_tutor_gemini

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
    konfigurasi = {
        "token_aktif": os.environ.get("ALJABAR_TOKEN_AKTIF", "").strip().upper(),
        "pin_guru": os.environ.get("ALJABAR_PIN_GURU", "").strip(),
    }
    if os.path.exists(FILE_CONFIG):
        try:
            with open(FILE_CONFIG, mode="r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    if data.get("token_aktif"):
                        konfigurasi["token_aktif"] = str(data["token_aktif"]).strip().upper()
                    if data.get("pin_guru"):
                        konfigurasi["pin_guru"] = str(data["pin_guru"]).strip()
        except Exception:
            pass
    try:
        if "pin_guru" in st.secrets and str(st.secrets["pin_guru"]).strip():
            konfigurasi["pin_guru"] = str(st.secrets["pin_guru"]).strip()
        if "token_aktif" in st.secrets and str(st.secrets["token_aktif"]).strip():
            konfigurasi["token_aktif"] = str(st.secrets["token_aktif"]).strip().upper()
    except Exception:
        pass

    return konfigurasi

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
    page_title="AljabarKu - Media RMT SMP Kelas 7",
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

if "chat_history_ai" not in st.session_state:
    st.session_state.chat_history_ai = []

if "custom_gemini_api_key" not in st.session_state:
    st.session_state.custom_gemini_api_key = ""

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

# Styling CSS Khusus untuk Pendidikan Matematika & RMT
st.markdown("""
<style>
    .hero-container {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 50%, #3B82F6 100%);
        color: white;
        padding: 2.2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .hero-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem; }
    .hero-desc { font-size: 1.05rem; opacity: 0.95; line-height: 1.6; }
    .status-badge {
        display: inline-block;
        background-color: #10B981;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .rmt-tag {
        display: inline-block;
        background-color: #4F46E5;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .axiom-tag {
        display: inline-block;
        background-color: #0284C7;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .rmt-box {
        background-color: #F8FAFC;
        border-left: 4px solid #4F46E5;
        padding: 1rem 1.2rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SIDEBAR: MODE GURU (NAVIGASI TERTUTUP) & STATUS SISWA
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 📐 AljabarKu (RMT)")
    st.caption("Media Pembelajaran Berbasis *Rigorous Mathematical Thinking*")

    # Bagian 1: Informasi Siswa Aktif
    if st.session_state.siswa["terdaftar"]:
        st.success(f"👤 **{st.session_state.siswa['nama']}** ({st.session_state.siswa['kelas']})")
        if st.session_state.siswa["sekolah"]:
            st.caption(f"🏫 {st.session_state.siswa['sekolah']}")

        if st.session_state.current_panel == "4. Kalkulator Siap Digunakan":
            if st.button("🚪 Keluar / Selesai Sesi", type="secondary", use_container_width=True):
                pindah_ke("5. Keluar")
    else:
        st.info("Status: Sesi Pembelajaran Siswa Baru")

    st.divider()

    # Bagian 2: Panel Khusus Guru / Peneliti
    with st.expander("🔒 Akses Khusus Guru / Peneliti"):
        cfg = ambil_konfigurasi()

        if not st.session_state.is_guru:
            st.write("Masukkan PIN Guru untuk membuka kontrol panel dan rekap data siswa:")
            pin_input = st.text_input("PIN Guru:", type="password", key="input_pin_guru")
            if st.button("Masuk Mode Guru 🔓", key="btn_login_guru"):
                pin_tersimpan = cfg.get("pin_guru", "").strip()
                if pin_tersimpan and pin_input.strip() == pin_tersimpan:
                    st.session_state.is_guru = True
                    st.success("Akses Guru Berhasil Diberikan!")
                    st.rerun()
                elif not pin_tersimpan:
                    st.error("PIN Guru belum dikonfigurasi oleh administrator.")
                else:
                    st.error("PIN Guru tidak valid! Akses ditolak.")
        else:
            st.success("✅ **Mode Guru Aktif**")

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
        <div class="hero-desc">
            Media Pembelajaran & Kalkulator Edukatif Aljabar SMP Kelas 7 Berbasis 
            <b>Rigorous Mathematical Thinking (RMT)</b> — Melatih nalar matematika secara sistematis, 
            memahami aksioma aljabar, dan menolak cara hafalan mekanis tanpa makna.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🎯 Mengapa Belajar Aljabar dengan RMT?")
        st.markdown("""
        Dalam pendekatan **Rigorous Mathematical Thinking (RMT)**:
        * 🔍 **Bukan Sekadar Menghafal Jawaban:** Anda akan dilatih melihat **mengapa** suatu operasi sah dilakukan.
        * ⚖️ **Menghapus Miskonsepsi "Pindah Ruas":** Persamaan dipahami sebagai **timbangan seimbang** yang dijaga dengan prinsip kesetaraan dan invers bilangan.
        * 🧩 **Memahami Suku Sejenis:** Menjumlahkan suku sejenis sejatinya adalah penerapan **Sifat Distributif** $ax + bx = (a + b)x$.
        * 📐 **Verifikasi Solusi:** Membiasakan diri memeriksa kebenaran (*self-monitoring*) di setiap akhir penyelesaian.
        """)

    with col2:
        st.markdown("### 🚀 Mulai Pembelajaran")
        st.info("Siapkan Token Akses yang telah dibagikan oleh Guru/Peneliti sebelum melanjutkan.")
        if st.button("👉 Lanjut ke Registrasi Siswa ➡️", type="primary", use_container_width=True):
            pindah_ke("2. Registrasi")


# =============================================================================
# PANEL 2: REGISTRASI + TOKEN AKSES (Tampilan Siswa)
# =============================================================================
elif st.session_state.current_panel == "2. Registrasi":
    st.subheader("📝 Panel 2: Registrasi Siswa & Validasi Token Akses")
    st.write("Silakan lengkapi identitas diri dan masukkan Token Akses dari guru untuk beralih ke Tutorial:")

    cfg = ambil_konfigurasi()
    token_valid = cfg.get("token_aktif", "").strip().upper()
    if not token_valid:
        st.warning("⚠️ Token akses belum dikonfigurasi oleh administrator.")

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
        st.markdown("#### 🔑 Masukkan Token Pembelajaran")
        token_input = st.text_input("Token Akses Guru *", placeholder="Ketik token akses yang diberikan oleh guru").strip().upper()

        btn_submit = st.form_submit_button("💾 Validasi Token & Lanjut ke Tutorial ➡️", type="primary")

        if btn_submit:
            if not nama_input.strip() or not sekolah_input.strip() or not absen_input.strip():
                st.warning("⚠️ Mohon lengkapi seluruh data diri (Nama, Sekolah, dan Nomor Presensi)!")
            elif token_input != token_valid:
                st.error("❌ Token Akses Salah! Silakan tanyakan Token yang benar kepada Guru / Peneliti.")
            else:
                st.session_state.siswa["nama"] = nama_input.strip()
                st.session_state.siswa["kelas"] = kelas_input
                st.session_state.siswa["sekolah"] = sekolah_input.strip()
                st.session_state.siswa["absen"] = absen_input.strip()
                st.session_state.siswa["terdaftar"] = True

                simpan_data_siswa_ke_csv(
                    nama_input.strip(),
                    kelas_input,
                    sekolah_input.strip(),
                    absen_input.strip(),
                    tingkat_paham
                )

                st.success(f"✅ Token Valid! Data berhasil dicatat. Selamat datang, {nama_input}!")
                pindah_ke("3. Tutorial")


# =============================================================================
# PANEL 3: TUTORIAL BERBASIS RMT (Tampilan Siswa)
# =============================================================================
elif st.session_state.current_panel == "3. Tutorial":
    nama_siswa = st.session_state.siswa["nama"] if st.session_state.siswa["terdaftar"] else "Siswa"
    st.subheader(f"📖 Panel 3: Tutorial Berpikir Matematis Ketat (RMT) untuk {nama_siswa}")
    st.write("Pelajari prinsip konseptual berikut sebelum menggunakan kalkulator:")

    tab1, tab2, tab3, tab4 = st.tabs([
        "⌨️ 1. Bahasa Simbolik Aljabar",
        "🎯 2. Atribut Kritis Suku Sejenis",
        "⚖️ 3. Prinsip Kesetaraan (Bukan Pindah Ruas!)",
        "🧠 4. Tiga Tingkat Berpikir RMT"
    ])

    with tab1:
        st.markdown("#### ⌨️ Bahasa Simbolik & Pelabelan (Labeling)")
        st.markdown("""
        Dalam aljabar, huruf adalah alat psikologis (*psychological tools*) untuk melambangkan besaran kuantitas:
        * **Variabel:** Simbol huruf kecil (misal $x, y, a, b$) yang mewakili nilai kuantitas yang belum diketahui atau dapat berubah.
        * **Koefisien:** Angka pengali di depan variabel. 
          * Contoh: Pada $5x$, angka $5$ adalah koefisien (artinya $5 \\times x$).
          * Jika koefisien bernilai $1$, cukup ditulis $x$ *(bukan $1x$)*.
          * Jika bernilai $-1$, cukup ditulis $-x$ *(bukan $-1x$)*.
        * **Konstanta:** Suku yang bernilai tetap berupa angka murni tanpa variabel (misal $+7$, $-4$).
        * **Pangkat (Derajat):** Menunjukkan perpangkatan variabel, misal $x^2$ ($x$ kuadrat).
        """)

    with tab2:
        st.markdown("#### 🎯 Atribut Kritis Suku Sejenis (*Comparing & Critical Attributes*)")
        st.info("""
        **Definisi Ketat:** Dua atau lebih suku dikatakan **SEJENIS** jika dan hanya jika memenuhi **DUA ATRIBUT KRITIS**:
        1. Memiliki **variabel yang sama**, **DAN**
        2. Memiliki **derajat pangkat yang sama**.
        """)
        
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.success("""
            **✅ SUKU SEJENIS (Dapat Disederhanakan):**
            * $4x$ dan $3x$ $\\rightarrow$ Variabel sama ($x$), pangkat sama ($1$).
            * $5x^2$ dan $-2x^2$ $\\rightarrow$ Variabel sama ($x$), pangkat sama ($2$).
            * $8$ dan $-3$ $\\rightarrow$ Sama-sama konstanta (pangkat nol).
            """)
        with col_t2:
            st.error("""
            **❌ BUKAN SUKU SEJENIS (TIDAK Boleh Dijumlahkan!):**
            * $3x$ dan $4y$ $\\rightarrow$ Variabel berbeda ($x$ vs $y$). Tetap $3x + 4y$!
            * $2x^2$ dan $5x$ $\\rightarrow$ Pangkat berbeda ($2$ vs $1$). Tetap $2x^2 + 5x$!
            """)

        st.markdown("""
        > **💡 Landasan Sifat Aljabar:**  
        > Mengapa $4x + 3x = 7x$? Karena kita menerapkan **Sifat Distributif Kebalikan (Memfaktorkan variabel sekutu)**:
        > $$4x + 3x = (4 + 3)x = 7x$$
        """)

    with tab3:
        st.markdown("#### ⚖️ Prinsip Kesetaraan Persamaan (Keseimbangan Timbangan)")
        st.warning("""
        **🚫 STOP Mengatakan "Pindah Ruas Ganti Tanda"!**  
        Dalam matematika tidak ada konsep "memindahkan angka melompati tanda sama dengan". Konsep mekanis ini sering menimbulkan miskonsepsi.
        """)

        st.markdown("""
        Persamaan linear adalah **timbangan yang setimbang**. Jika piringan kiri diubah, piringan kanan **wajib diubah secara identik**:
        
        1. **Sifat Penambahan pada Kesetaraan (Invers Aditif):**  
           Jika $A = B$, maka $A + (-c) = B + (-c)$.  
           * Contoh: Pada $x + 5 = 12$, kita ingin mengeliminasi $+5$. Tambahkan invers aditifnya ($-5$) pada **KEDUA RUAS**:
             $$(x + 5) + (-5) = 12 + (-5) \\implies x + 0 = 7 \\implies x = 7$$
             
        2. **Sifat Perkalian pada Kesetaraan (Invers Multiplikatif):**  
           Jika $ax = d$, kalikan kedua ruas dengan $\\frac{1}{a}$ atau bagi kedua ruas dengan $a$ ($a \\neq 0$):
           $$\\frac{3x}{3} = \\frac{15}{3} \\implies 1 \\cdot x = 5 \\implies x = 5$$
        """)

    with tab4:
        st.markdown("#### 🧠 Kerangka Berpikir Rigorous Mathematical Thinking (RMT)")
        st.markdown("""
        RMT (Kinard & Kozulin, 2008) memandu proses berpikir siswa melalui 3 tingkatan terpadu:
        
        ```
        Level 1: Qualitative Operations  (Identifikasi simbol, pelabelan, pemilahan atribut kritis suku)
                                ↓
        Level 2: Quantitative Operations (Model semi-konkret: Timbangan Seimbang, Model Luas Persegi Panjang)
                                ↓
        Level 3: Abstract Relational     (Justifikasi aksioma aljabar, pembuktian kesetaraan, verifikasi solusi)
        ```
        Kalkulator ini dirancang bukan sekadar untuk menyalin jawaban, melainkan sebagai **alat mediasi kognitif** agar Anda memahami alur berpikir matematis tersebut.
        """)

    st.divider()
    if st.button("🚀 Saya Paham Konsep RMT, Buka Kalkulator Aljabar! ➡️", type="primary", use_container_width=True):
        pindah_ke("4. Kalkulator Siap Digunakan")


# =============================================================================
# PANEL 4: KALKULATOR RMT SIAP DIGUNAKAN (Tampilan Siswa)
# =============================================================================
elif st.session_state.current_panel == "4. Kalkulator Siap Digunakan":
    nama_siswa = st.session_state.siswa["nama"] if st.session_state.siswa["terdaftar"] else "Pengguna"
    kelas_siswa = f"({st.session_state.siswa['kelas']})" if st.session_state.siswa["terdaftar"] else ""

    col_head1, col_head2 = st.columns([4, 1])
    with col_head1:
        st.markdown(f"""
        <div style="background-color: #ECFDF5; border: 1px solid #10B981; border-radius: 10px; padding: 1.2rem; margin-bottom: 1.2rem;">
            <span class="status-badge">🟢 Kalkulator RMT Siap Digunakan</span>
            <h3 style="color: #065F46; margin-top: 0.5rem; margin-bottom: 0.2rem;">Selamat Belajar, {nama_siswa} {kelas_siswa}!</h3>
            <p style="color: #047857; margin-bottom: 0;">Gunakan kalkulator ini untuk meneliti struktur aljabar dan membiasakan justifikasi matematis.</p>
        </div>
        """, unsafe_allow_html=True)
    with col_head2:
        st.write("")
        if st.button("🚪 Selesaikan Sesi & Keluar", type="secondary", use_container_width=True):
            pindah_ke("5. Keluar")

    # 6 Tab Kalkulator Berbasis RMT
    tab_sederhana, tab_bedah, tab_distributif, tab_substitusi, tab_plsv, tab_ai = st.tabs([
        "➕ 1. Sederhanakan Aljabar",
        "🔍 2. Bedah Unsur Aljabar",
        "✖️ 3. Perkalian Distributif",
        "🔢 4. Evaluasi / Substitusi",
        "⚖️ 5. Persamaan Linear (PLSV)",
        "🤖 6. Tanya Tutor AI (RMT)"
    ])

    # -------------------------------------------------------------------------
    # TAB 1: SEDERHANAKAN ALJABAR
    # -------------------------------------------------------------------------
    with tab_sederhana:
        st.subheader("Operasi Penjumlahan & Pengurangan Berbasis Sifat Distributif")
        st.caption("RMT Level 1-3: Pemilahan Atribut Kritis Suku $\\rightarrow$ Komutatif/Asosiatif $\\rightarrow$ Sifat Distributif $ax + bx = (a + b)x$.")

        col_in, col_pre = st.columns([3, 1])
        with col_pre:
            contoh = st.selectbox("Pilih Contoh Soal:", ["Ketik Sendiri...", "5x + 3 - 2x + 7", "4a - 3b + 2a - 5b", "3x^2 + 5x - 2x^2 + 4"])
        with col_in:
            def_val = "5x + 3 - 2x + 7" if contoh == "Ketik Sendiri..." else contoh
            eks_in = st.text_input("Bentuk Aljabar:", value=def_val, key="in_simp")

        with st.expander("🧠 Uji Nalar RMT (Pikirkan Sejenak Sebelum Melihat Solusi)"):
            st.markdown("**Pertanyaan Pemantik:** Sifat aljabar apa yang mendasari penggabungan suku sejenis seperti $5x - 2x = 3x$?")
            pilihan_sifat = st.radio(
                "Pilih jawaban:",
                [
                    "A. Sifat Distributif Perkalian terhadap Penjumlahan/Pengurangan: (5 - 2)x",
                    "B. Aturan mekanis pindah ruas dan ganti tanda",
                    "C. Sifat Asosiatif Perkalian semata"
                ],
                key="kuis_simp"
            )
            if pilihan_sifat.startswith("A"):
                st.success("🎯 **Tepat Sekali!** Suku sejenis dapat digabung karena memiliki variabel sekutu yang sama, sehingga berlaku $ax + bx = (a + b)x$.")
            else:
                st.info("💡 Pilihan A adalah yang benar. Penjumlahan suku sejenis bersandar langsung pada sifat distributif!")

        if st.button("🚀 Sederhanakan Secara Rigorous", type="primary", key="btn_simp"):
            try:
                hasil = sederhanakan_aljabar(eks_in)
                st.success("✅ Bentuk Paling Sederhana (Kanonik):")
                st.latex(hasil["hasil_latex"])

                st.markdown("#### 📜 Sifat Aljabar Formal yang Digunakan:")
                for sifat in hasil.get("sifat_yang_digunakan", []):
                    st.markdown(f"- `{sifat}`")

                st.markdown("### 📝 Langkah demi Langkah (Justifikasi RMT):")
                for step in hasil["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.markdown(f"<span class='rmt-tag'>{step.get('kategori_rmt', 'RMT')}</span> <span class='axiom-tag'>{step.get('sifat_aljabar', 'Aksioma')}</span>", unsafe_allow_html=True)
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(f"Format penulisan salah: {str(e)}")

    # -------------------------------------------------------------------------
    # TAB 2: BEDAH UNSUR ALJABAR
    # -------------------------------------------------------------------------
    with tab_bedah:
        st.subheader("Mengenal Anatomi Bentuk Aljabar & Analisis Atribut Kritis")
        st.caption("RMT Level 1: Pelabelan (Labeling), Pemilahan Derajat Pangkat, dan Analisis Perbandingan Suku Sejenis.")

        in_bedah = st.text_input("Masukkan Bentuk Aljabar:", value="3x^2 - 5x + 8 + 2x", key="in_bedah")
        if st.button("🔍 Bedah Atribut Kritis Aljabar", type="primary", key="btn_bedah"):
            try:
                data = bedah_unsur_aljabar(in_bedah)
                st.latex(data["ekspresi_latex"])

                c1, c2, c3 = st.columns(3)
                c1.info(f"**Klasifikasi Suku:**\n### {data['klasifikasi_suku']}")
                c2.success(f"**Variabel (Besaran):**\n### {', '.join(data['variabel'])}")
                c3.warning(f"**Konstanta (Tetap):**\n### {data['konstanta']}")

                st.markdown("#### 📋 Tabel Identifikasi Atribut Kritis Suku (RMT Level 1):")
                df_atribut = pd.DataFrame(data["atribut_kritis"])
                st.dataframe(df_atribut, use_container_width=True)

                st.markdown("#### 🔍 Analisis Komparasi Suku Sejenis:")
                for analisis in data["analisis_suku_sejenis"]:
                    st.markdown(f"- {analisis}")

            except Exception as e:
                st.error(str(e))

    # -------------------------------------------------------------------------
    # TAB 3: PERKALIAN DISTRIBUTIF
    # -------------------------------------------------------------------------
    with tab_distributif:
        st.subheader("Perkalian Distributif & Jembatan Semi-Konkret Model Luas")
        st.caption("RMT Level 2-3: Model Luas Persegi Panjang (Area Model) $\\rightarrow$ Ekspansi Distributif $k(a + b) = k \\cdot a + k \\cdot b$.")

        col_k, col_kr = st.columns([1, 3])
        with col_k:
            k_val = st.number_input("Faktor Pengali Luar (k):", value=3, step=1)
        with col_kr:
            isi_kr = st.text_input("Suku di Dalam Kurung:", value="2x - 5")

        if st.button("🚀 Jabarkan Secara Distributif", type="primary", key="btn_dist"):
            try:
                hasil_dist = perkalian_distributif(float(k_val), isi_kr)
                st.success("✅ Bentuk Hasil Ekspansi:")
                st.latex(hasil_dist["hasil_latex"])

                for step in hasil_dist["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.markdown(f"<span class='rmt-tag'>{step.get('kategori_rmt', 'RMT')}</span> <span class='axiom-tag'>{step.get('sifat_aljabar', 'Aksioma')}</span>", unsafe_allow_html=True)
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(str(e))

    # -------------------------------------------------------------------------
    # TAB 4: EVALUASI / SUBSTITUSI
    # -------------------------------------------------------------------------
    with tab_substitusi:
        st.subheader("Evaluasi Nilai Aljabar (Variabel sebagai Besaran Masukan)")
        st.caption("RMT Level 2-3: Penerjemahan Simbol $\\rightarrow$ Nilai Konkret $\\rightarrow$ Hierarki Keteraturan Operasi (PEMDAS).")

        col_e, col_v = st.columns([2, 1])
        with col_e:
            subst_e = st.text_input("Bentuk Aljabar:", value="2x^2 - 3x + 7")
        with col_v:
            subst_x = st.number_input("Nilai Input Variabel x:", value=3, step=1)

        if st.button("🔢 Hitung Nilai Numerik", type="primary", key="btn_subst"):
            try:
                res_subst = evaluasi_nilai_aljabar(subst_e, {"x": float(subst_x)})
                st.success(f"Nilai Numerik Akhir: **{res_subst['hasil_akhir']}**")

                for step in res_subst["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.markdown(f"<span class='rmt-tag'>{step.get('kategori_rmt', 'RMT')}</span> <span class='axiom-tag'>{step.get('sifat_aljabar', 'Aksioma')}</span>", unsafe_allow_html=True)
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(str(e))

    # -------------------------------------------------------------------------
    # TAB 5: PERSAMAAN LINEAR SATU VARIABEL (PLSV)
    # -------------------------------------------------------------------------
    with tab_plsv:
        st.subheader("Persamaan Linear Satu Variabel: Prinsip Kesetaraan (Invariance of Equality)")
        st.caption("RMT Level 3: Menghapus total mitos 'Pindah Ruas', menerapkan Invers Aditif/Multiplikatif, dan Verifikasi Pembuktian.")

        in_plsv = st.text_input("Persamaan Linear:", value="2x + 5 = 15", key="in_plsv")

        with st.expander("⚖️ Uji Nalar RMT: Mengapa Tidak Boleh Ada Istilah 'Pindah Ruas'?"):
            st.markdown("""
            **Pertanyaan Refleksi:** Pada persamaan $2x + 5 = 15$, apa alasan matematis yang sebenarnya terjadi ketika angka $+5$ dieliminasi dari ruas kiri?
            """)
            opsi_plsv = st.radio(
                "Pilih pemahaman yang benar:",
                [
                    "A. Kedua ruas ditambahkan invers aditif dari +5 (yaitu -5) agar timbangan tetap setara: (2x + 5) + (-5) = 15 + (-5)",
                    "B. Angka 5 dipindahkan melompati sama dengan lalu otomatis berganti tanda menjadi minus"
                ],
                key="kuis_plsv"
            )
            if opsi_plsv.startswith("A"):
                st.success("🎯 **Luar Biasa!** Anda berpikir secara matematis ketat (*Rigorous*). Kesetaraan hanya terjaga jika perlakuan yang sama diterapkan pada kedua ruas.")
            else:
                st.warning("⚠️ Opsi B adalah jalan pintas mekanis yang menghilangkan esensi keseimbangan persamaan matematika!")

        if st.button("⚖️ Selesaikan dengan Prinsip Kesetaraan", type="primary", key="btn_plsv"):
            try:
                res_plsv = selesaikan_plsv(in_plsv)
                st.success(f"Solusi Terbukti: **{res_plsv['solusi']}**")

                for step in res_plsv["langkah_langkah"]:
                    with st.expander(f"📌 {step['judul']}", expanded=True):
                        st.markdown(f"<span class='rmt-tag'>{step.get('kategori_rmt', 'RMT')}</span> <span class='axiom-tag'>{step.get('sifat_aljabar', 'Aksioma')}</span>", unsafe_allow_html=True)
                        st.write(step["penjelasan"])
                        st.latex(step["latex"])
            except Exception as e:
                st.error(str(e))

    # -------------------------------------------------------------------------
    # TAB 6: TANYA TUTOR AI (RMT)
    # -------------------------------------------------------------------------
    with tab_ai:
        st.subheader("🤖 Tutor AI AljabarKu (Berbasis Rigorous Mathematical Thinking)")
        st.caption("Didukung oleh Google Gemini API — Dibimbing untuk memahami alasan logis di balik konsep aljabar.")

        key_aktif = ambil_gemini_api_key()

        # Konfigurasi Kunci API jika belum ada
        if not key_aktif:
            st.warning("⚠️ **Google Gemini API Key belum terpasang.**")
            with st.expander("🔑 Pasang API Key Google Gemini (Gratis)", expanded=True):
                st.markdown("""
                Anda dapat memperoleh **Google Gemini API Key secara gratis** melalui Google AI Studio:
                1. Buka [Google AI Studio (aistudio.google.com)](https://aistudio.google.com/).
                2. Masuk dengan akun Google Anda.
                3. Klik **Get API Key** lalu buat kunci baru (**Create API Key**).
                4. Salin dan tempelkan kuncinya pada kolom di bawah ini:
                """)
                input_key = st.text_input("Tempel Gemini API Key Anda:", type="password", key="input_key_ui", placeholder="AIzaSy...")
                if st.button("Aktifkan API Key untuk Sesi Ini 🚀", type="primary", key="btn_simpan_key"):
                    if input_key.strip():
                        st.session_state.custom_gemini_api_key = input_key.strip()
                        st.success("✅ API Key berhasil diaktifkan untuk sesi belajar ini!")
                        st.rerun()
                    else:
                        st.error("Mohon masukkan API Key yang valid!")
                st.caption("💡 *Tips: Anda juga bisa menyimpannya secara permanen di file `.streamlit/secrets.toml`.*")
        else:
            col_k1, col_k2 = st.columns([4, 1])
            with col_k1:
                st.success("🟢 **Google Gemini API Aktif & Siap Membantu Belajar!**")
            with col_k2:
                if st.button("Ubah API Key 🔄", key="btn_ubah_key"):
                    st.session_state.custom_gemini_api_key = ""
                    st.rerun()

            st.markdown("#### 💡 Pertanyaan Pemantik Cepat (Klik untuk Mencoba):")
            c_p1, c_p2 = st.columns(2)
            prompt_terpilih = None
            with c_p1:
                if st.button("❓ Mengapa istilah 'pindah ruas' keliru?", use_container_width=True):
                    prompt_terpilih = "Jelaskan mengapa istilah 'pindah ruas' keliru dalam aljabar dan apa konsep yang benar menurut prinsip kesetaraan?"
                if st.button("🧩 Mengapa 3x dan 3x^2 tidak bisa dijumlahkan?", use_container_width=True):
                    prompt_terpilih = "Jelaskan mengapa 3x dan 3x^2 tidak bisa dijumlahkan ditinjau dari atribut kritis suku sejenis!"
            with c_p2:
                if st.button("⚖️ Bagaimana cara menyelesaikan 2x + 7 = 19?", use_container_width=True):
                    prompt_terpilih = "Bimbing saya menyelesaikan persamaan 2x + 7 = 19 langkah demi langkah menggunakan sifat invers dan kesetaraan!"
                if st.button("🎯 Berikan 1 teka-teki aljabar kelas 7!", use_container_width=True):
                    prompt_terpilih = "Berikan saya satu teka-teki cerita aljabar seru untuk siswa kelas 7 SMP yang melatih nalar!"

            # Tampilkan riwayat percakapan sebelumnya
            st.divider()
            st.markdown("### 💬 Percakapan dengan Tutor AI:")

            if not st.session_state.chat_history_ai:
                st.info("👋 Halo! Saya Tutor AI AljabarKu. Tanyakan materi aljabar yang ingin kamu pahami atau ketik soal yang sedang kamu pelajari.")
            else:
                for pesan in st.session_state.chat_history_ai:
                    with st.chat_message(pesan["role"]):
                        st.markdown(pesan["content"])

            # Input pesan dari siswa
            teks_input = st.chat_input("Tulis pertanyaan atau tanggapan Anda di sini...")
            pesan_untuk_dikirim = prompt_terpilih or teks_input

            if pesan_untuk_dikirim:
                st.session_state.chat_history_ai.append({"role": "user", "content": pesan_untuk_dikirim})
                with st.chat_message("user"):
                    st.markdown(pesan_untuk_dikirim)

                with st.chat_message("assistant"):
                    with st.spinner("Tutor AI sedang menalar jawaban matematis..."):
                        try:
                            jawaban_ai = tanya_tutor_gemini(
                                pesan_siswa=pesan_untuk_dikirim,
                                api_key=key_aktif,
                                riwayat_obrolan=st.session_state.chat_history_ai[:-1]
                            )
                            st.markdown(jawaban_ai)
                            st.session_state.chat_history_ai.append({"role": "assistant", "content": jawaban_ai})
                        except Exception as e:
                            st.error(f"⚠️ Terjadi kendala: {str(e)}")

            if st.session_state.chat_history_ai:
                if st.button("🗑️ Hapus Riwayat Obrolan", type="secondary"):
                    st.session_state.chat_history_ai = []
                    st.rerun()


# =============================================================================
# PANEL 5: KELUAR DARI APLIKASI
# =============================================================================
elif st.session_state.current_panel == "5. Keluar":
    nama_siswa = st.session_state.siswa["nama"] if st.session_state.siswa["terdaftar"] else "Siswa"

    st.markdown(f"""
    <div style="background-color: #F1F5F9; border: 1px solid #CBD5E1; border-radius: 12px; padding: 2.5rem; text-align: center;">
        <h1 style="color: #1E293B; margin-bottom: 0.5rem;">🎓 Sesi Belajar Telah Selesai</h1>
        <h3 style="color: #475569; margin-bottom: 1.5rem;">Terima kasih, <b>{nama_siswa}</b>!</h3>
        <p style="font-size: 1.05rem; color: #64748B; max-width: 600px; margin: 0 auto 2rem auto; line-height: 1.6;">
            Anda telah berhasil menyelesaikan eksplorasi aljabar dengan pendekatan <b>Rigorous Mathematical Thinking (RMT)</b>.
            Data partisipasi Anda telah dicatat pada sistem Guru/Peneliti.
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
        st.write("Daftar siswa yang telah mengisi identitas dan token akses yang valid:")

        if os.path.exists(FILE_DATA_SISWA):
            try:
                df = pd.read_csv(FILE_DATA_SISWA)
                st.markdown(f"**Total Siswa Terdaftar:** `{len(df)} Siswa`")
                st.dataframe(df, use_container_width=True)

                col_d1, col_d2 = st.columns([2, 1])
                with col_d1:
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
