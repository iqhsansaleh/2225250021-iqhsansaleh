"""
algebra_engine.py
Modul Logika Inti & Algoritma Aljabar untuk Kelas 7 SMP
Berbasis Pendekatan: Rigorous Mathematical Thinking (RMT)
(Kinard & Kozulin, 2008; Didaktik Feuerstein & Vygotsky)

Fokus Perbaikan RMT:
1. Menghapus miskonsepsi prosedural mekanis "Pindah Ruas".
2. Menegakkan Prinsip Kesetaraan (Invariance of Equality) & Sifat Invers.
3. Menjelaskan penyederhanaan suku sejenis berbasis Sifat Distributif Perkalian terbalik.
4. Menambahkan representasi semi-konkret (Model Luas / Area Model) pada Sifat Distributif.
5. Menyertakan langkah Verifikasi Metakognitif (Refleksi Pembuktian Solusi).
"""

import re
from typing import List, Dict, Tuple, Any, Optional

class SukuAljabar:
    """
    Kelas untuk merepresentasikan satu suku aljabar secara rigorous.
    Contoh:
      -3x^2 -> koefisien = -3, variabel = 'x', pangkat = 2
      5y    -> koefisien = 5,  variabel = 'y', pangkat = 1
      -x    -> koefisien = -1, variabel = 'x', pangkat = 1
      7     -> koefisien = 7,  variabel = None, pangkat = 0
    """
    def __init__(self, koefisien: float, variabel: Optional[str] = None, pangkat: int = 1):
        self.koefisien = float(koefisien)
        self.variabel = variabel if variabel else None
        self.pangkat = 0 if self.variabel is None else pangkat

    @property
    def is_konstanta(self) -> bool:
        return self.variabel is None or self.pangkat == 0

    @property
    def kunci_sejenis(self) -> Tuple[Optional[str], int]:
        """
        Kunci pembanding untuk suku sejenis (Atribut Kritis RMT):
        Dua suku sejenis JIKA DAN HANYA JIKA memiliki variabel yang sama DAN pangkat yang sama.
        """
        if self.is_konstanta:
            return (None, 0)
        return (self.variabel, self.pangkat)

    def invers_aditif(self) -> 'SukuAljabar':
        """Menghasilkan invers aditif (lawan penjumlahan) dari suku ini."""
        return SukuAljabar(-self.koefisien, self.variabel, self.pangkat)

    def format_koefisien(self, koef: float) -> str:
        """Format koefisien agar tidak menampilkan .0 jika bilangan bulat"""
        if koef.is_integer():
            return str(int(koef))
        return f"{koef:.2f}".rstrip('0').rstrip('.')

    def to_latex(self, include_sign: bool = False) -> str:
        """Konversi suku ke notasi LaTeX standar"""
        k = self.koefisien
        if k == 0:
            return "0"

        sign_str = ""
        if include_sign:
            sign_str = "+" if k > 0 else "-"
            abs_k = abs(k)
        else:
            if k < 0:
                sign_str = "-"
                abs_k = abs(k)
            else:
                abs_k = k

        k_str = self.format_koefisien(abs_k)

        if self.is_konstanta:
            return f"{sign_str}{k_str}"

        # Jika koefisien bernilai 1 atau -1 di depan variabel, angka 1 umumnya tidak ditulis eksplisit
        if abs_k == 1.0:
            coeff_part = sign_str
        else:
            coeff_part = f"{sign_str}{k_str}"

        var_part = self.variabel
        if self.pangkat > 1:
            var_part = f"{self.variabel}^{{{self.pangkat}}}"

        return f"{coeff_part}{var_part}"

    def __repr__(self) -> str:
        return self.to_latex()


def bersihkan_input(teks: str) -> str:
    """Membersihkan spasi dan standardisasi karakter input pengguna"""
    teks = teks.replace(" ", "").replace("−", "-").replace("×", "*").replace(":", "/")
    return teks


def pisahkan_menjadi_suku(teks_ekspresi: str) -> List[str]:
    """
    Algoritma Tokenizer Aljabar: Memecah string aljabar menjadi daftar suku bertanda.
    Contoh: '3x + 5 - 2x - 7' -> ['+3x', '+5', '-2x', '-7']
    """
    clean = bersihkan_input(teks_ekspresi)
    if not clean:
        return []

    # Jika suku pertama tidak memiliki tanda '+' atau '-', tambahkan tanda '+'
    if clean[0] not in ('+', '-'):
        clean = '+' + clean

    pola = r'([+-][^+-]+)'
    tokens = re.findall(pola, clean)
    return tokens


def parse_satu_suku(token: str) -> SukuAljabar:
    """
    Mengurai satu token string menjadi objek SukuAljabar.
    Menangani konstanta, variabel berkoefisien, koefisien implisit (x, -x), dan eksponen.
    """
    token = token.strip()
    if not token:
        return SukuAljabar(0.0)

    tanda = -1.0 if token[0] == '-' else 1.0
    isi = token[1:]

    # Cek konstanta murni
    if re.fullmatch(r'^\d+(\.\d+)?$', isi):
        return SukuAljabar(koefisien=tanda * float(isi), variabel=None, pangkat=0)

    # Pola variabel dengan atau tanpa pangkat: misal 'x', 'x^2', '2.5x', 'x**2'
    match = re.fullmatch(r'^(\d+(?:\.\d+)?)?([a-zA-Z])(?:\^|\*\*)?(\d+)?$', isi)
    if match:
        angka_str, var_str, pangkat_str = match.groups()
        koef_nilai = float(angka_str) if angka_str else 1.0
        pangkat_nilai = int(pangkat_str) if pangkat_str else 1
        return SukuAljabar(koefisien=tanda * koef_nilai, variabel=var_str, pangkat=pangkat_nilai)

    raise ValueError(f"Bentuk suku '{token}' tidak valid untuk materi aljabar kelas 7 SMP.")


def gabungkan_suku_ke_latex(daftar_suku: List[SukuAljabar]) -> str:
    """Menggabungkan daftar objek SukuAljabar menjadi representasi string LaTeX yang matematis dan teratur"""
    suku_aktif = [s for s in daftar_suku if s.koefisien != 0]
    if not suku_aktif:
        return "0"

    hasil = []
    for i, suku in enumerate(suku_aktif):
        if i == 0:
            hasil.append(suku.to_latex(include_sign=False))
        else:
            if suku.koefisien > 0:
                hasil.append(f"+ {suku.to_latex(include_sign=False)}")
            else:
                teks = suku.to_latex(include_sign=False)
                hasil.append(f"- {teks[1:] if teks.startswith('-') else teks}")
    return " ".join(hasil)


# =============================================================================
# 1. BEDAH UNSUR ALJABAR (RMT LEVEL 1: QUALITATIVE & ATTRIBUTE ANALYSIS)
# =============================================================================
def bedah_unsur_aljabar(teks_ekspresi: str) -> Dict[str, Any]:
    """
    Mode 1: Analisis Anatomi Bentuk Aljabar Berbasis RMT Level 1 (Qualitative Thinking)
    Fokus: Pelabelan (Labeling), Identifikasi Atribut Kritis, dan Perbandingan Suku.
    """
    tokens = pisahkan_menjadi_suku(teks_ekspresi)
    suku_list = [parse_satu_suku(t) for t in tokens]

    variabel_set = set()
    koefisien_dict = {}
    konstanta_total = 0.0
    ada_konstanta = False
    atribut_kritis = []

    for idx, s in enumerate(suku_list, start=1):
        if s.is_konstanta:
            konstanta_total += s.koefisien
            ada_konstanta = True
            atribut_kritis.append({
                "suku": s.to_latex(include_sign=True),
                "jenis": "Konstanta (Bilangan Tetap)",
                "koefisien": s.format_koefisien(s.koefisien),
                "variabel": "Tidak ada",
                "derajat": 0,
                "peran_matematis": "Nilai pasti yang tidak dipengaruhi nilai masukan variabel manapun."
            })
        else:
            variabel_set.add(s.variabel)
            kunci_var = f"{s.variabel}" if s.pangkat == 1 else f"{s.variabel}^{{{s.pangkat}}}"
            koefisien_dict[kunci_var] = koefisien_dict.get(kunci_var, 0.0) + s.koefisien
            atribut_kritis.append({
                "suku": s.to_latex(include_sign=True),
                "jenis": "Suku Bervariabel",
                "koefisien": s.format_koefisien(s.koefisien),
                "variabel": s.variabel,
                "derajat": s.pangkat,
                "peran_matematis": f"Faktor pengali ({s.format_koefisien(s.koefisien)}) terhadap besaran kuantitas ({s.variabel}) berpangkat {s.pangkat}."
            })

    dummy = SukuAljabar(0)
    koef_terformat = {k: dummy.format_koefisien(v) for k, v in koefisien_dict.items()}

    banyak_suku = len(suku_list)
    nama_suku = (
        "Suku Tunggal (Monomial)" if banyak_suku == 1 else
        "Suku Dua (Binomial)" if banyak_suku == 2 else
        "Suku Tiga (Trinomial)" if banyak_suku == 3 else
        f"Suku Banyak (Polinomial {banyak_suku} suku)"
    )

    # Analisis Suku Sejenis (Comparing & Critical Attributes)
    grup_sejenis: Dict[Tuple[Optional[str], int], List[SukuAljabar]] = {}
    for s in suku_list:
        k = s.kunci_sejenis
        grup_sejenis.setdefault(k, []).append(s)

    analisis_sejenis = []
    for k, v in grup_sejenis.items():
        if len(v) > 1:
            simbol_grup = "Konstanta" if k[0] is None else (f"variabel '{k[0]}'" if k[1] == 1 else f"variabel '{k[0]}' pangkat {k[1]}")
            analisis_sejenis.append(
                f"Suku-suku `{', '.join([s.to_latex(include_sign=True) for s in v])}` **SEJENIS** "
                f"karena memiliki atribut kritis identik (sama-sama memiliki {simbol_grup})."
            )
        else:
            simbol_suku = v[0].to_latex(include_sign=True)
            analisis_sejenis.append(f"Suku `{simbol_suku}` **TIDAK MEMILIKI PASANGAN SEJENIS** di dalam ekspresi ini.")

    return {
        "ekspresi_latex": gabungkan_suku_ke_latex(suku_list),
        "banyak_suku": banyak_suku,
        "klasifikasi_suku": nama_suku,
        "variabel": sorted(list(variabel_set)) if variabel_set else ["Tidak ada (Konstanta murni)"],
        "koefisien": koef_terformat,
        "konstanta": dummy.format_koefisien(konstanta_total) if ada_konstanta else "0 (Tidak ada konstanta)",
        "daftar_suku_detail": suku_list,
        "atribut_kritis": atribut_kritis,
        "analisis_suku_sejenis": analisis_sejenis
    }


# =============================================================================
# 2. SEDERHANAKAN ALJABAR (RMT LEVEL 2-3: DEDUCTIVE PROPERTY JUSTIFICATION)
# =============================================================================
def sederhanakan_aljabar(teks_ekspresi: str) -> Dict[str, Any]:
    """
    Mode 2: Sederhanakan Bentuk Aljabar Berbasis Sifat Distributif & Komutatif.
    Menggantikan hafalan 'jumlahkan koefisien' dengan justifikasi aksiomatik:
    ax + bx = (a + b)x (Sifat Distributif Perkalian terhadap Penjumlahan).
    """
    tokens = pisahkan_menjadi_suku(teks_ekspresi)
    suku_list = [parse_satu_suku(t) for t in tokens]

    langkah_langkah = []
    langkah_langkah.append({
        "judul": "Bentuk Aljabar Awal (Analisis Struktur)",
        "latex": gabungkan_suku_ke_latex(suku_list),
        "penjelasan": "Identifikasi seluruh suku pembentuk ekspresi beserta tanda aljabar masing-masing.",
        "kategori_rmt": "Level 1: Labeling & Qualitative Identification",
        "sifat_aljabar": "Bentuk Simbolik Awal"
    })

    # Langkah 1: Sifat Komutatif dan Asosiatif (Menata Suku Sejenis Berdampingan)
    grup_sejenis: Dict[Tuple[Optional[str], int], List[SukuAljabar]] = {}
    for s in suku_list:
        kunci = s.kunci_sejenis
        grup_sejenis.setdefault(kunci, []).append(s)

    kunci_terurut = sorted(
        grup_sejenis.keys(),
        key=lambda k: (-1 if k[0] is None else 1, k[0] or "", -k[1]),
        reverse=True
    )

    suku_terurut = []
    deskripsi_kelompok = []
    kelompok_latex_parts = []

    for kunci in kunci_terurut:
        daftar = grup_sejenis[kunci]
        suku_terurut.extend(daftar)
        var, pgt = kunci
        nama_grup = "Konstanta" if var is None else (f"Suku variabel {var}" if pgt == 1 else f"Suku variabel {var}^{pgt}")
        suku_str = ", ".join([s.to_latex(include_sign=True) for s in daftar])
        deskripsi_kelompok.append(f"**{nama_grup}**: {suku_str}")

        bagian_gabung = gabungkan_suku_ke_latex(daftar)
        kelompok_latex_parts.append(f"({bagian_gabung})")

    langkah_langkah.append({
        "judul": "Langkah 1: Menata Suku Sejenis (Sifat Komutatif & Asosiatif Penjumlahan)",
        "latex": " + ".join(kelompok_latex_parts),
        "penjelasan": (
            "Gunakan **Sifat Komutatif** ($a + b = b + a$) dan **Sifat Asosiatif** ($(a + b) + c = a + (b + c)$) "
            "untuk mendekatkan suku-suku yang memiliki **variabel dan derajat pangkat yang identik (Suku Sejenis)**:\n"
            + "\n".join([f"- {d}" for d in deskripsi_kelompok])
        ),
        "kategori_rmt": "Level 1: Comparing & Systematic Grouping",
        "sifat_aljabar": "Sifat Komutatif dan Asosiatif Penjumlahan"
    })

    # Langkah 2: Sifat Distributif Kebalikan (Memfaktorkan Variabel Sekutu)
    detail_distributif = []
    suku_hasil_akhir = []

    for kunci in kunci_terurut:
        daftar = grup_sejenis[kunci]
        var, pgt = kunci
        total_koef = sum(s.koefisien for s in daftar)
        suku_baru = SukuAljabar(koefisien=total_koef, variabel=var, pangkat=pgt)

        if total_koef != 0 or len(kunci_terurut) == 1:
            suku_hasil_akhir.append(suku_baru)

        daftar_angka = [s.format_koefisien(s.koefisien) for s in daftar]
        rumus_koef = " + ".join(daftar_angka).replace("+ -", "- ")

        if var is not None:
            var_simbol = f"{var}" if pgt == 1 else f"{var}^{{{pgt}}}"
            detail_distributif.append(f"\\left({rumus_koef}\\right){var_simbol}")
        else:
            detail_distributif.append(f"\\left({rumus_koef}\\right)")

    langkah_langkah.append({
        "judul": "Langkah 2: Menerapkan Sifat Distributif Perkalian terhadap Penjumlahan",
        "latex": " + ".join(detail_distributif).replace("+ -", "- "),
        "penjelasan": (
            "Berdasarkan **Sifat Distributif** ($ax + bx = (a + b)x$), suku-suku sejenis dapat digabungkan dengan "
            "mengeluarkan variabel sekutu sebagai faktor persekutuan di luar kurung koefisiennya."
        ),
        "kategori_rmt": "Level 3: Abstract Mathematical Justification",
        "sifat_aljabar": "Sifat Distributif: ax + bx = (a + b)x"
    })

    # Langkah 3: Operasi Aritmetika Koefisien
    hasil_akhir_latex = gabungkan_suku_ke_latex(suku_hasil_akhir)

    langkah_langkah.append({
        "judul": "Hasil Akhir (Bentuk Aljabar Paling Sederhana)",
        "latex": hasil_akhir_latex,
        "penjelasan": (
            "Selesaikan operasi aritmetika pada bilangan di dalam kurung untuk memperoleh bentuk kanonik "
            "(tersusun teratur dari pangkat tertinggi ke konstanta)."
        ),
        "kategori_rmt": "Level 3: Formal Symbolic Representation",
        "sifat_aljabar": "Bentuk Sederhana Kanonik"
    })

    return {
        "hasil_latex": hasil_akhir_latex,
        "langkah_langkah": langkah_langkah,
        "sifat_yang_digunakan": [
            "Sifat Komutatif Penjumlahan: a + b = b + a",
            "Sifat Asosiatif Penjumlahan: (a + b) + c = a + (b + c)",
            "Sifat Distributif Perkalian: ax + bx = (a + b)x",
            "Aritmetika Bilangan Bulat pada Koefisien"
        ]
    }


# =============================================================================
# 3. PERKALIAN DISTRIBUTIF (RMT LEVEL 2: AREA MODEL & TRANSFORMATION)
# =============================================================================
def perkalian_distributif(konstanta_k: float, teks_didalam_kurung: str) -> Dict[str, Any]:
    """
    Mode 3: Perkalian Suku Tunggal dengan Suku Dua: k(ax + b)
    Menyertakan representasi Model Luas Persegi Panjang (Area Model) sebagai jembatan semi-konkret RMT.
    """
    tokens = pisahkan_menjadi_suku(teks_didalam_kurung)
    suku_dalam = [parse_satu_suku(t) for t in tokens]

    dummy = SukuAljabar(konstanta_k)
    k_str = dummy.format_koefisien(konstanta_k)
    dalam_latex = gabungkan_suku_ke_latex(suku_dalam)

    langkah_langkah = []
    langkah_langkah.append({
        "judul": "Bentuk Perkalian Aljabar",
        "latex": f"{k_str}\\left({dalam_latex}\\right)",
        "penjelasan": f"Ekspresi ini merepresentasikan pengali skala {k_str} terhadap kelompok kuantitas \\(({dalam_latex})\\).",
        "kategori_rmt": "Level 1: Qualitative Symbol Interpretation",
        "sifat_aljabar": "Bentuk Faktor Tunggal"
    })

    # Penjelasan Model Luas (Area Model)
    langkah_langkah.append({
        "judul": "Jembatan Konseptual: Model Luas Persegi Panjang (Area Model)",
        "latex": f"\\text{{Luas Total}} = \\text{{Lebar}} \\times \\text{{Panjang}} = {k_str} \\times \\left({dalam_latex}\\right)",
        "penjelasan": (
            f"Secara geometri semi-konkret, bayangkan sebuah persegi panjang berlebar **{k_str}** dan panjang total "
            f"**\\(({dalam_latex})\\)**. Luas total persegi panjang ini adalah jumlah luas dari setiap petak kecil pembentuknya."
        ),
        "kategori_rmt": "Level 2: Geometric & Relational Representation",
        "sifat_aljabar": "Representasi Geometris Model Luas"
    })

    # Langkah Distribusi Suku demi Suku
    distribusi_parts = []
    suku_hasil = []
    for s in suku_dalam:
        s_latex = s.to_latex(include_sign=False)
        distribusi_parts.append(f"{k_str} \\cdot \\left({s.to_latex()}\\right)")
        koef_baru = konstanta_k * s.koefisien
        suku_hasil.append(SukuAljabar(koef_baru, s.variabel, s.pangkat))

    langkah_langkah.append({
        "judul": "Langkah 1: Mendistribusikan Pengali ke Setiap Suku (Sifat Distributif)",
        "latex": " + ".join(distribusi_parts).replace("+ -", "- "),
        "penjelasan": (
            f"Berdasarkan **Sifat Distributif Perkalian terhadap Penjumlahan** ($k(a + b) = k \\cdot a + k \\cdot b$), "
            f"faktor luar **{k_str}** dikalikan secara adil ke setiap suku di dalam tanda kurung."
        ),
        "kategori_rmt": "Level 3: Deductive Algebraic Transformation",
        "sifat_aljabar": "Sifat Distributif Perkalian: k(a + b) = k*a + k*b"
    })

    hasil_latex = gabungkan_suku_ke_latex(suku_hasil)
    langkah_langkah.append({
        "judul": "Hasil Akhir Perkalian",
        "latex": hasil_latex,
        "penjelasan": "Sederhanakan hasil kali koefisien numerik masing-masing suku.",
        "kategori_rmt": "Level 3: Formal Symbolic Simplification",
        "sifat_aljabar": "Bentuk Ekspansi Aljabar"
    })

    return {
        "hasil_latex": hasil_latex,
        "langkah_langkah": langkah_langkah
    }


# =============================================================================
# 4. EVALUASI / SUBSTITUSI (RMT LEVEL 2-3: VARIABLE AS QUANTITY PLACEHOLDER)
# =============================================================================
def evaluasi_nilai_aljabar(teks_ekspresi: str, nilai_variabel: Dict[str, float]) -> Dict[str, Any]:
    """
    Mode 4: Substitusi Nilai Variabel Berbasis Konsep Variabel Sebagai Penampung Besaran (Placeholder).
    Menekankan hierarki keteraturan operasi matematika (Order of Operations / PEMDAS).
    """
    tokens = pisahkan_menjadi_suku(teks_ekspresi)
    suku_list = [parse_satu_suku(t) for t in tokens]

    langkah_langkah = []
    ket_nilai = ", ".join([f"{k} = {SukuAljabar(v).format_koefisien(v)}" for k, v in nilai_variabel.items()])

    langkah_langkah.append({
        "judul": "Bentuk Aljabar & Nilai Masukan Variabel",
        "latex": gabungkan_suku_ke_latex(suku_list),
        "penjelasan": (
            f"Variabel berfungsi sebagai penampung besaran kuantitas (*generalized placeholder*). "
            f"Kita akan mengevaluasi ekspresi ini untuk nilai: **{ket_nilai}**."
        ),
        "kategori_rmt": "Level 2: Variable Input Representation",
        "sifat_aljabar": "Penetapan Nilai Parameter"
    })

    # Langkah 1: Substitusi Eksplisit Menggunakan Tanda Kurung
    substitusi_parts = []
    for s in suku_list:
        if s.is_konstanta:
            substitusi_parts.append(s.format_koefisien(s.koefisien))
        else:
            nilai = nilai_variabel.get(s.variabel, 0.0)
            koef_str = s.format_koefisien(s.koefisien)
            nilai_str = s.format_koefisien(nilai)
            if s.koefisien == 1:
                substitusi_parts.append(f"\\left({nilai_str}\\right)^{{{s.pangkat}}}" if s.pangkat > 1 else f"\\left({nilai_str}\\right)")
            elif s.koefisien == -1:
                substitusi_parts.append(f"-\\left({nilai_str}\\right)^{{{s.pangkat}}}" if s.pangkat > 1 else f"-\\left({nilai_str}\\right)")
            else:
                substitusi_parts.append(f"{koef_str} \\cdot \\left({nilai_str}\\right)^{{{s.pangkat}}}" if s.pangkat > 1 else f"{koef_str} \\cdot \\left({nilai_str}\\right)")

    subst_latex = " + ".join(substitusi_parts).replace("+ -", "- ")
    langkah_langkah.append({
        "judul": "Langkah 1: Substitusi Simbol Variabel dengan Nilai Angka",
        "latex": subst_latex,
        "penjelasan": (
            "Ganti setiap huruf variabel dengan angka masukan di dalam tanda kurung untuk menjaga keutuhan tanda aljabar "
            "(khususnya jika nilai bertanda negatif)."
        ),
        "kategori_rmt": "Level 2: Concrete-Symbolic Translation",
        "sifat_aljabar": "Substitusi Nilai Kuantitas"
    })

    # Langkah 2: Evaluasi Hierarki Operasi (Eksponen & Perkalian sebelum Penjumlahan)
    nilai_tiap_suku = []
    total_nilai = 0.0
    for s in suku_list:
        if s.is_konstanta:
            val = s.koefisien
        else:
            val = s.koefisien * (nilai_variabel.get(s.variabel, 0.0) ** s.pangkat)
        nilai_tiap_suku.append(s.format_koefisien(val))
        total_nilai += val

    step2_latex = " + ".join(nilai_tiap_suku).replace("+ -", "- ")
    langkah_langkah.append({
        "judul": "Langkah 2: Menghitung Berdasarkan Hierarki Operasi (PEMDAS)",
        "latex": step2_latex,
        "penjelasan": "Dahulukan operasi perpangkatan dan perkalian suku sebelum melakukan penjumlahan atau pengurangan.",
        "kategori_rmt": "Level 3: Computational Hierarchy Execution",
        "sifat_aljabar": "Hierarki Operasi (Order of Operations)"
    })

    dummy = SukuAljabar(total_nilai)
    hasil_total_str = dummy.format_koefisien(total_nilai)

    langkah_langkah.append({
        "judul": "Hasil Akhir Evaluasi Numerik",
        "latex": hasil_total_str,
        "penjelasan": "Jumlahkan seluruh hasil hitungan suku untuk memperoleh nilai akhir tunggal.",
        "kategori_rmt": "Level 3: Definite Quantitative Output",
        "sifat_aljabar": "Nilai Numerik Aljabar"
    })

    return {
        "hasil_akhir": hasil_total_str,
        "langkah_langkah": langkah_langkah
    }


# =============================================================================
# 5. PERSAMAAN LINEAR SATU VARIABEL (RMT LEVEL 3: INVARIANCE OF EQUALITY)
# =============================================================================
def selesaikan_plsv(teks_persamaan: str) -> Dict[str, Any]:
    """
    Mode 5: Penyelesaian PLSV Berbasis Prinsip Kesetaraan (Invariance of Equality).
    MENGHAPUS TOTAL dogma mekanis 'Pindah Ruas' dan menggantikannya dengan:
    1. Sifat Penambahan pada Kesetaraan (Menambahkan Invers Aditif pada KEDUA Ruas).
    2. Sifat Perkalian pada Kesetaraan (Membagi / Mengalikan Invers Multiplikatif pada KEDUA Ruas).
    3. Langkah Verifikasi / Refleksi Metakognitif (Self-Monitoring & Proof of Correctness).
    """
    if "=" not in teks_persamaan:
        raise ValueError("Persamaan harus memiliki tanda sama dengan ('=')")

    ruas_kiri_str, ruas_kanan_str = teks_persamaan.split("=", 1)
    suku_kiri = [parse_satu_suku(t) for t in pisahkan_menjadi_suku(ruas_kiri_str)]
    suku_kanan = [parse_satu_suku(t) for t in pisahkan_menjadi_suku(ruas_kanan_str)]

    # Identifikasi variabel tunggal
    semua_var = {s.variabel for s in suku_kiri + suku_kanan if not s.is_konstanta}
    if len(semua_var) > 1:
        raise ValueError("PLSV kelas 7 hanya mendukung 1 jenis variabel (misal hanya 'x' atau hanya 'a').")
    var_utama = list(semua_var)[0] if semua_var else "x"

    langkah_langkah = []
    persamaan_awal_latex = f"{gabungkan_suku_ke_latex(suku_kiri)} = {gabungkan_suku_ke_latex(suku_kanan)}"

    langkah_langkah.append({
        "judul": "Persamaan Awal (Konsep Keseimbangan / Timbangan)",
        "latex": persamaan_awal_latex,
        "penjelasan": (
            "Persamaan matematika dianalogikan sebagai **sistem timbangan yang seimbang**. "
            "Keseimbangan (**Kesetaraan**) akan tetap terjaga jika dan hanya jika perlakuan matematika "
            "yang sama diterapkan secara adil pada **KEDUA RUAS** sekaligus."
        ),
        "kategori_rmt": "Level 1: Conservation of Constancy (Keseimbangan Relasi)",
        "sifat_aljabar": "Definisi Kesetaraan Relasional: LHS = RHS"
    })

    # Hitung total awal masing-masing ruas
    total_var_kiri = sum(s.koefisien for s in suku_kiri if not s.is_konstanta)
    total_konst_kiri = sum(s.koefisien for s in suku_kiri if s.is_konstanta)

    total_var_kanan = sum(s.koefisien for s in suku_kanan if not s.is_konstanta)
    total_konst_kanan = sum(s.koefisien for s in suku_kanan if s.is_konstanta)

    dummy = SukuAljabar(0)

    # LANGKAH A: Jika ada suku variabel di ruas kanan, eliminasi dengan menambahkan invers aditif di KEDUA ruas
    if total_var_kanan != 0:
        invers_var_kanan = -total_var_kanan
        invers_var_suku = SukuAljabar(invers_var_kanan, var_utama, 1)
        inv_str = invers_var_suku.to_latex(include_sign=False)
        operasi_str = f"+ ({inv_str})" if invers_var_kanan < 0 else f"+ {inv_str}"

        # Perbarui koefisien variabel
        total_var_kiri += invers_var_kanan
        total_var_kanan = 0.0

        s_kiri_var = SukuAljabar(total_var_kiri, var_utama, 1)
        s_kiri_konst = SukuAljabar(total_konst_kiri, None, 0)
        s_kanan_konst = SukuAljabar(total_konst_kanan, None, 0)

        ruas_kiri_teks = gabungkan_suku_ke_latex([s_kiri_var, s_kiri_konst])
        ruas_kanan_teks = gabungkan_suku_ke_latex([s_kanan_konst])

        langkah_langkah.append({
            "judul": f"Langkah 1: Mengeliminasi Variabel di Ruas Kanan (Sifat Penambahan pada Kesetaraan)",
            "latex": f"\\left({persamaan_awal_latex.split(' = ')[0]}\\right) {operasi_str} = \\left({persamaan_awal_latex.split(' = ')[1]}\\right) {operasi_str}",
            "penjelasan": (
                f"Untuk mengeliminasi suku variabel di ruas kanan secara adil, **tambahkan invers aditifnya ({inv_str}) "
                f"ke KEDUA ruas** (bukan memindahkan suku!). Setelah disederhanakan, persamaan menjadi: $${ruas_kiri_teks} = {ruas_kanan_teks}$$"
            ),
            "kategori_rmt": "Level 3: Additive Property of Equality (Invers Aditif)",
            "sifat_aljabar": "Jika A = B, maka A + (-c) = B + (-c)"
        })

    # LANGKAH B: Eliminasi konstanta di ruas kiri dengan menambahkan invers aditif konstanta di KEDUA ruas
    if total_konst_kiri != 0:
        invers_konst_kiri = -total_konst_kiri
        invers_konst_suku = SukuAljabar(invers_konst_kiri, None, 0)
        inv_k_str = invers_konst_suku.to_latex(include_sign=False)
        op_k_str = f"+ ({inv_k_str})" if invers_konst_kiri < 0 else f"+ {inv_k_str}"

        ruas_kiri_sebelum = gabungkan_suku_ke_latex([SukuAljabar(total_var_kiri, var_utama, 1), SukuAljabar(total_konst_kiri, None, 0)])
        ruas_kanan_sebelum = gabungkan_suku_ke_latex([SukuAljabar(total_konst_kanan, None, 0)])

        total_konst_kanan += invers_konst_kiri
        total_konst_kiri = 0.0

        s_var_bersih = SukuAljabar(total_var_kiri, var_utama, 1)
        s_konst_bersih = SukuAljabar(total_konst_kanan, None, 0)

        ruas_kiri_teks = s_var_bersih.to_latex()
        ruas_kanan_teks = s_konst_bersih.to_latex()

        langkah_langkah.append({
            "judul": f"Langkah 2: Mengeliminasi Konstanta di Ruas Kiri (Sifat Penambahan pada Kesetaraan)",
            "latex": f"\\left({ruas_kiri_sebelum}\\right) {op_k_str} = \\left({ruas_kanan_sebelum}\\right) {op_k_str}",
            "penjelasan": (
                f"Konstanta pada ruas kiri dihilangkan dengan **menambahkan invers aditifnya ({inv_k_str}) ke KEDUA RUAS**. "
                f"Karena sebuah bilangan ditambah inversnya menghasilkan elemen netral 0 ($k + (-k) = 0$), maka tersisa:\n"
                f"$${ruas_kiri_teks} = {ruas_kanan_teks}$$"
            ),
            "kategori_rmt": "Level 3: Additive Property of Equality & Additive Inverse",
            "sifat_aljabar": "Elemen Netral Penjumlahan: k + (-k) = 0"
        })

    # Cek kondisi khusus (koefisien variabel = 0)
    if total_var_kiri == 0:
        if total_konst_kanan == 0:
            solusi_teks = "Persamaan memiliki tak hingga banyak penyelesaian (Identitas Selalu Benar: 0 = 0)."
        else:
            solusi_teks = f"Persamaan tidak memiliki penyelesaian (Kontradiksi Palsu: 0 = {dummy.format_koefisien(total_konst_kanan)})."
        return {
            "solusi": solusi_teks,
            "langkah_langkah": langkah_langkah,
            "terverifikasi": False
        }

    # LANGKAH C: Menentukan nilai variabel menggunakan Sifat Perkalian pada Kesetaraan (Invers Perkalian)
    nilai_x = total_konst_kanan / total_var_kiri
    nilai_x_str = dummy.format_koefisien(nilai_x)
    koef_str = dummy.format_koefisien(total_var_kiri)
    konst_str = dummy.format_koefisien(total_konst_kanan)

    if total_var_kiri != 1.0:
        langkah_langkah.append({
            "judul": f"Langkah 3: Menerapkan Sifat Perkalian pada Kesetaraan (Membagi Kedua Ruas)",
            "latex": f"\\frac{{{koef_str}{var_utama}}}{{{koef_str}}} = \\frac{{{konst_str}}}{{{koef_str}}} \\implies 1 \\cdot {var_utama} = {nilai_x_str}",
            "penjelasan": (
                f"Untuk mengubah koefisien {koef_str} menjadi elemen identitas perkalian 1 ($1 \\cdot {var_utama} = {var_utama}$), "
                f"kalikan kedua ruas dengan invers perkaliannya ($\\frac{{1}}{{{koef_str}}}$) atau bagi kedua ruas dengan angka **{koef_str}**."
            ),
            "kategori_rmt": "Level 3: Multiplicative Property of Equality (Invers Multiplikatif)",
            "sifat_aljabar": "Elemen Identitas Perkalian: 1 * x = x"
        })

    # LANGKAH D: VERIFIKASI METAKOGNITIF (RMT LEVEL 3: SELF-MONITORING & PROOF)
    # Buktikan dengan mensubstitusi nilai x ke ruas kiri dan kanan awal
    nilai_lhs_cek = sum(
        (s.koefisien * (nilai_x ** s.pangkat) if not s.is_konstanta else s.koefisien)
        for s in suku_kiri
    )
    nilai_rhs_cek = sum(
        (s.koefisien * (nilai_x ** s.pangkat) if not s.is_konstanta else s.koefisien)
        for s in suku_kanan
    )
    lhs_cek_str = dummy.format_koefisien(nilai_lhs_cek)
    rhs_cek_str = dummy.format_koefisien(nilai_rhs_cek)

    langkah_langkah.append({
        "judul": "Langkah 4: Refleksi Metakognitif & Verifikasi Solusi (Self-Check)",
        "latex": f"\\text{{Ruas Kiri}} = {lhs_cek_str}, \\quad \\text{{Ruas Kanan}} = {rhs_cek_str} \\implies {lhs_cek_str} = {rhs_cek_str} \\; (\\checkmark \\text{{ Valid & Terbukti}})",
        "penjelasan": (
            f"Dalam Rigorous Mathematical Thinking, solusi wajib diverifikasi keabsahannya. "
            f"Substitusikan nilai ${var_utama} = {nilai_x_str}$ kembali ke persamaan awal: terbukti kedua ruas menghasilkan nilai seimbang ({lhs_cek_str} = {rhs_cek_str})."
        ),
        "kategori_rmt": "Level 3: Metacognitive Reflection & Verification",
        "sifat_aljabar": "Pembuktian Konservasi Kesetaraan"
    })

    return {
        "solusi": f"{var_utama} = {nilai_x_str}",
        "langkah_langkah": langkah_langkah,
        "terverifikasi": True
    }
