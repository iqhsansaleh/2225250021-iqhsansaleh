"""
algebra_engine.py
Modul Logika Inti & Algoritma Aljabar untuk Kelas 7 SMP
Mata Kuliah: Algoritma dan Pemrograman - Pendidikan Matematika
"""

import re
from typing import List, Dict, Tuple, Any, Optional

class SukuAljabar:
    """
    Kelas untuk merepresentasikan satu suku aljabar.
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
        """Kunci pembanding untuk suku sejenis: (variabel, pangkat)"""
        if self.is_konstanta:
            return (None, 0)
        return (self.variabel, self.pangkat)

    def format_koefisien(self, koef: float) -> str:
        """Format koefisien agar tidak menampilkan .0 jika bilangan bulat"""
        if koef.is_integer():
            return str(int(koef))
        return f"{koef:.2f}".rstrip('0').rstrip('.')

    def to_latex(self, include_sign: bool = False) -> str:
        """Konversi suku ke notasi LaTeX"""
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

        # Jika koefisien bernilai 1 atau -1 di depan variabel, angka 1 umumnya tidak ditulis
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
    """Membersihkan spasi dan standardisasi karakter input"""
    teks = teks.replace(" ", "").replace("−", "-").replace("×", "*").replace(":", "/")
    return teks


def pisahkan_menjadi_suku(teks_ekspresi: str) -> List[str]:
    """
    Algoritma Tokenizer: Memecah string aljabar menjadi daftar suku bertanda.
    Contoh: '3x + 5 - 2x - 7' -> ['+3x', '+5', '-2x', '-7']
    """
    clean = bersihkan_input(teks_ekspresi)
    if not clean:
        return []

    # Jika suku pertama tidak memiliki tanda '+' atau '-', tambahkan '+'
    if clean[0] not in ('+', '-'):
        clean = '+' + clean

    # Pola regex mencari tanda (+ atau -) diikuti karakter suku hingga tanda berikutnya
    # Regex menangani suku berpangkat misal +3x^2 atau -5y
    pola = r'([+-][^+-]+)'
    tokens = re.findall(pola, clean)
    return tokens


def parse_satu_suku(token: str) -> SukuAljabar:
    """
    Mengurai satu token string menjadi objek SukuAljabar.
    Contoh token:
      '+3x'   -> koef: 3.0, var: 'x', pangkat: 1
      '-x'    -> koef: -1.0, var: 'x', pangkat: 1
      '+7'    -> koef: 7.0, var: None, pangkat: 0
      '+4x^2' -> koef: 4.0, var: 'x', pangkat: 2
    """
    token = token.strip()
    tanda = -1.0 if token[0] == '-' else 1.0
    isi = token[1:]  # Ambil teks setelah tanda + atau -

    # Cek apakah suku berupa konstanta murni (hanya angka)
    if re.fullmatch(r'^\d+(\.\d+)?$', isi):
        return SukuAljabar(koefisien=tanda * float(isi), variabel=None, pangkat=0)

    # Pola variabel dengan atau tanpa pangkat: misal 'x', 'x^2', '2.5x', 'x**2'
    match = re.fullmatch(r'^(\d+(?:\.\d+)?)?([a-zA-Z])(?:\^|\*\*)?(\d+)?$', isi)
    if match:
        angka_str, var_str, pangkat_str = match.groups()
        koef_nilai = float(angka_str) if angka_str else 1.0
        pangkat_nilai = int(pangkat_str) if pangkat_str else 1
        return SukuAljabar(koefisien=tanda * koef_nilai, variabel=var_str, pangkat=pangkat_nilai)

    # Fallback jika pola tidak lazim
    raise ValueError(f"Bentuk suku '{token}' tidak valid untuk materi aljabar kelas 7 SMP.")


def gabungkan_suku_ke_latex(daftar_suku: List[SukuAljabar]) -> str:
    """Menggabungkan daftar objek SukuAljabar menjadi satu string LaTeX yang rapi"""
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
                # suku.to_latex sudah menghasilkan tanda minus
                teks = suku.to_latex(include_sign=False)
                hasil.append(f"- {teks[1:] if teks.startswith('-') else teks}")
    return " ".join(hasil)


def bedah_unsur_aljabar(teks_ekspresi: str) -> Dict[str, Any]:
    """
    Mode 1: Analisis Anatomi Bentuk Aljabar (Kelas 7 SMP)
    Mengidentifikasi variabel, koefisien, konstanta, dan banyak suku.
    """
    tokens = pisahkan_menjadi_suku(teks_ekspresi)
    suku_list = [parse_satu_suku(t) for t in tokens]

    variabel_set = set()
    koefisien_dict = {}
    konstanta_total = 0.0
    ada_konstanta = False

    for s in suku_list:
        if s.is_konstanta:
            konstanta_total += s.koefisien
            ada_konstanta = True
        else:
            variabel_set.add(s.variabel)
            kunci_var = f"{s.variabel}" if s.pangkat == 1 else f"{s.variabel}^{{{s.pangkat}}}"
            koefisien_dict[kunci_var] = koefisien_dict.get(kunci_var, 0.0) + s.koefisien

    # Format koefisien
    koef_terformat = {k: s.format_koefisien(v) for k, v in koefisien_dict.items()}

    banyak_suku = len(suku_list)
    nama_suku = "Suku Tunggal (Monomial)" if banyak_suku == 1 else \
                "Suku Dua (Binomial)" if banyak_suku == 2 else \
                "Suku Tiga (Trinomial)" if banyak_suku == 3 else \
                f"Suku Banyak (Polinomial {banyak_suku} suku)"

    return {
        "ekspresi_latex": gabungkan_suku_ke_latex(suku_list),
        "banyak_suku": banyak_suku,
        "klasifikasi_suku": nama_suku,
        "variabel": sorted(list(variabel_set)) if variabel_set else ["Tidak ada (Konstanta murni)"],
        "koefisien": koef_terformat,
        "konstanta": s.format_koefisien(konstanta_total) if ada_konstanta else "0 (Tidak ada konstanta)",
        "daftar_suku_detail": suku_list
    }


def sederhanakan_aljabar(teks_ekspresi: str) -> Dict[str, Any]:
    """
    Mode 2: Sederhanakan Bentuk Aljabar dengan Penjelasan Langkah demi Langkah
    """
    tokens = pisahkan_menjadi_suku(teks_ekspresi)
    suku_list = [parse_satu_suku(t) for t in tokens]

    langkah_langkah = []
    langkah_langkah.append({
        "judul": "Ekspresi Awal",
        "latex": gabungkan_suku_ke_latex(suku_list),
        "penjelasan": "Tuliskan bentuk aljabar yang akan disederhanakan."
    })

    # Langkah 1: Identifikasi & Kelompokkan Suku Sejenis
    grup_sejenis: Dict[Tuple[Optional[str], int], List[SukuAljabar]] = {}
    for s in suku_list:
        kunci = s.kunci_sejenis
        if kunci not in grup_sejenis:
            grup_sejenis[kunci] = []
        grup_sejenis[kunci].append(s)

    deskripsi_kelompok = []
    kelompok_latex_parts = []

    # Urutkan: Variabel dengan pangkat tertinggi ke terendah, lalu konstanta di akhir
    kunci_terurut = sorted(
        grup_sejenis.keys(),
        key=lambda k: (-1 if k[0] is None else 1, k[0] or "", -k[1]),
        reverse=True
    )

    for kunci in kunci_terurut:
        daftar = grup_sejenis[kunci]
        var, pgt = kunci
        nama_grup = "Konstanta" if var is None else (f"Suku variabel {var}" if pgt == 1 else f"Suku variabel {var}^{pgt}")
        suku_str = ", ".join([s.to_latex(include_sign=True) for s in daftar])
        deskripsi_kelompok.append(f"**{nama_grup}**: {suku_str}")

        # Gabungkan suku-suku dalam satu tanda kurung
        bagian_gabung = gabungkan_suku_ke_latex(daftar)
        kelompok_latex_parts.append(f"({bagian_gabung})")

    langkah_langkah.append({
        "judul": "Langkah 1: Mengelompokkan Suku-suku Sejenis",
        "latex": " + ".join(kelompok_latex_parts),
        "penjelasan": "Kumpulkan suku yang memiliki variabel dan pangkat yang sama:\n" + "\n".join([f"- {d}" for d in deskripsi_kelompok])
    })

    # Langkah 2: Operasikan Koefisien pada Suku Sejenis
    suku_hasil_akhir = []
    detail_perhitungan = []

    for kunci in kunci_terurut:
        daftar = grup_sejenis[kunci]
        var, pgt = kunci
        total_koef = sum(s.koefisien for s in daftar)
        suku_baru = SukuAljabar(koefisien=total_koef, variabel=var, pangkat=pgt)
        if total_koef != 0 or len(kunci_terurut) == 1:
            suku_hasil_akhir.append(suku_baru)

        # Buat teks detail hitungan
        daftar_angka = [s.format_koefisien(s.koefisien) for s in daftar]
        rumus_koef = " + ".join(daftar_angka).replace("+ -", "- ")
        if var is not None:
            var_simbol = f"{var}" if pgt == 1 else f"{var}^{{{pgt}}}"
            detail_perhitungan.append(f"({rumus_koef}){var_simbol} = {suku_baru.to_latex()}")
        else:
            detail_perhitungan.append(f"({rumus_koef}) = {suku_baru.to_latex()}")

    langkah_langkah.append({
        "judul": "Langkah 2: Menjumlahkan Koefisien Suku Sejenis",
        "latex": " + ".join(detail_perhitungan),
        "penjelasan": "Operasikan koefisien (angka di depan variabel) untuk setiap kelompok suku sejenis."
    })

    hasil_akhir_latex = gabungkan_suku_ke_latex(suku_hasil_akhir)

    langkah_langkah.append({
        "judul": "Hasil Akhir (Bentuk Paling Sederhana)",
        "latex": hasil_akhir_latex,
        "penjelasan": "Bentuk aljabar telah disederhanakan secara maksimal."
    })

    return {
        "hasil_latex": hasil_akhir_latex,
        "langkah_langkah": langkah_langkah
    }


def evaluasi_nilai_aljabar(teks_ekspresi: str, nilai_variabel: Dict[str, float]) -> Dict[str, Any]:
    """
    Mode 3: Substitusi / Hitung Nilai Bentuk Aljabar (Jika variabel diketahui)
    Contoh: 3x + 5 dengan x = 4
    """
    tokens = pisahkan_menjadi_suku(teks_ekspresi)
    suku_list = [parse_satu_suku(t) for t in tokens]

    langkah_langkah = []
    langkah_langkah.append({
        "judul": "Bentuk Aljabar Awal",
        "latex": gabungkan_suku_ke_latex(suku_list),
        "penjelasan": f"Substitusikan nilai variabel yang diketahui: " + ", ".join([f"{k} = {v}" for k, v in nilai_variabel.items()])
    })

    # Langkah 1: Substitusi nilai ke variabel
    substitusi_parts = []
    for s in suku_list:
        if s.is_konstanta:
            substitusi_parts.append(s.format_koefisien(s.koefisien))
        else:
            nilai = nilai_variabel.get(s.variabel, 0.0)
            koef_str = s.format_koefisien(s.koefisien)
            nilai_str = s.format_koefisien(nilai)
            if s.koefisien == 1:
                substitusi_parts.append(f"({nilai_str})^{{{s.pangkat}}}" if s.pangkat > 1 else f"({nilai_str})")
            elif s.koefisien == -1:
                substitusi_parts.append(f"-({nilai_str})^{{{s.pangkat}}}" if s.pangkat > 1 else f"-({nilai_str})")
            else:
                substitusi_parts.append(f"{koef_str} \\cdot ({nilai_str})^{{{s.pangkat}}}" if s.pangkat > 1 else f"{koef_str} \\cdot ({nilai_str})")

    subst_latex = " + ".join(substitusi_parts).replace("+ -", "- ")
    langkah_langkah.append({
        "judul": "Langkah 1: Mengganti Variabel dengan Nilai Angka",
        "latex": subst_latex,
        "penjelasan": "Ganti setiap huruf variabel dengan angka yang diberikan menggunakan tanda kurung."
    })

    # Langkah 2: Hitung tiap suku
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
        "judul": "Langkah 2: Menghitung Hasil Perkalian Tiap Suku",
        "latex": step2_latex,
        "penjelasan": "Dahulukan operasi perpangkatan dan perkalian sebelum penjumlahan/pengurangan."
    })

    hasil_total_str = SukuAljabar(total_nilai).format_koefisien(total_nilai)
    langkah_langkah.append({
        "judul": "Hasil Akhir Evaluasi",
        "latex": hasil_total_str,
        "penjelasan": "Jumlahkan seluruh suku untuk memperoleh nilai akhir numerik."
    })

    return {
        "hasil_akhir": hasil_total_str,
        "langkah_langkah": langkah_langkah
    }


def perkalian_distributif(konstanta_k: float, teks_didalam_kurung: str) -> Dict[str, Any]:
    """
    Mode 4: Perkalian Suku Tunggal dengan Suku Dua (Distributif): k(ax + b)
    """
    tokens = pisahkan_menjadi_suku(teks_didalam_kurung)
    suku_dalam = [parse_satu_suku(t) for t in tokens]

    k_str = SukuAljabar(konstanta_k).format_koefisien(konstanta_k)
    dalam_latex = gabungkan_suku_ke_latex(suku_dalam)

    langkah_langkah = []
    langkah_langkah.append({
        "judul": "Bentuk Perkalian Distributif",
        "latex": f"{k_str}\\left({dalam_latex}\\right)",
        "penjelasan": f"Gunakan sifat distributif: kalikan pengali {k_str} dengan setiap suku di dalam kurung."
    })

    # Langkah 1: Tuliskan perkalian tiap suku
    distribusi_parts = []
    suku_hasil = []
    for s in suku_dalam:
        s_latex = s.to_latex(include_sign=False)
        tanda = "+" if s.koefisien > 0 else "-"
        distribusi_parts.append(f"{k_str} \\cdot ({s.to_latex()})")

        koef_baru = konstanta_k * s.koefisien
        suku_hasil.append(SukuAljabar(koef_baru, s.variabel, s.pangkat))

    langkah_langkah.append({
        "judul": "Langkah 1: Menjabarkan Perkalian (Sifat Distributif)",
        "latex": " + ".join(distribusi_parts).replace("+ -", "- "),
        "penjelasan": f"Setiap suku di dalam kurung dikalikan dengan {k_str}."
    })

    hasil_latex = gabungkan_suku_ke_latex(suku_hasil)
    langkah_langkah.append({
        "judul": "Hasil Akhir Perkalian",
        "latex": hasil_latex,
        "penjelasan": "Sederhanakan hasil perkalian koefisien masing-masing suku."
    })

    return {
        "hasil_latex": hasil_latex,
        "langkah_langkah": langkah_langkah
    }


def selesaikan_plsv(teks_persamaan: str) -> Dict[str, Any]:
    """
    Mode 5 (Bonus): Persamaan Linear Satu Variabel (PLSV) sederhana: ax + b = c
    """
    if "=" not in teks_persamaan:
        raise ValueError("Persamaan harus memiliki tanda sama dengan ('=')")

    ruas_kiri_str, ruas_kanan_str = teks_persamaan.split("=", 1)
    suku_kiri = [parse_satu_suku(t) for t in pisahkan_menjadi_suku(ruas_kiri_str)]
    suku_kanan = [parse_satu_suku(t) for t in pisahkan_menjadi_suku(ruas_kanan_str)]

    langkah_langkah = []
    langkah_langkah.append({
        "judul": "Persamaan Awal",
        "latex": f"{gabungkan_suku_ke_latex(suku_kiri)} = {gabungkan_suku_ke_latex(suku_kanan)}",
        "penjelasan": "Tuliskan persamaan linear satu variabel yang akan diselesaikan."
    })

    # Kumpulkan variabel ke kiri, konstanta ke kanan
    var_kiri = [s for s in suku_kiri if not s.is_konstanta]
    konst_kiri = [s for s in suku_kiri if s.is_konstanta]

    var_kanan = [s for s in suku_kanan if not s.is_konstanta]
    konst_kanan = [s for s in suku_kanan if s.is_konstanta]

    # Ambil variabel utama
    semua_var = {s.variabel for s in var_kiri + var_kanan}
    if len(semua_var) > 1:
        raise ValueError("PLSV kelas 7 hanya mendukung 1 jenis variabel (misal 'x').")
    var_utama = list(semua_var)[0] if semua_var else "x"

    # Pindahkan variabel di kanan ke kiri (berubah tanda)
    suku_var_final = list(var_kiri)
    for s in var_kanan:
        suku_var_final.append(SukuAljabar(-s.koefisien, s.variabel, s.pangkat))

    # Pindahkan konstanta di kiri ke kanan (berubah tanda)
    suku_konst_final = list(konst_kanan)
    for s in konst_kiri:
        suku_konst_final.append(SukuAljabar(-s.koefisien, None, 0))

    langkah_langkah.append({
        "judul": "Langkah 1: Mengelompokkan Suku Variabel ke Ruas Kiri dan Konstanta ke Ruas Kanan",
        "latex": f"{gabungkan_suku_ke_latex(suku_var_final)} = {gabungkan_suku_ke_latex(suku_konst_final)}",
        "penjelasan": "Pindahkan semua suku yang memuat variabel ke ruas kiri dan semua bilangan (konstanta) ke ruas kanan dengan membalik tandanya."
    })

    total_koef_var = sum(s.koefisien for s in suku_var_final)
    total_konstanta = sum(s.koefisien for s in suku_konst_final)

    s_var_bersih = SukuAljabar(total_koef_var, var_utama, 1)
    s_konst_bersih = SukuAljabar(total_konstanta, None, 0)

    langkah_langkah.append({
        "judul": "Langkah 2: Menyederhanakan Masing-Masing Ruas",
        "latex": f"{s_var_bersih.to_latex()} = {s_konst_bersih.to_latex()}",
        "penjelasan": "Jumlahkan koefisien variabel di ruas kiri dan jumlahkan konstanta di ruas kanan."
    })

    if total_koef_var == 0:
        if total_konstanta == 0:
            solusi_teks = "Persamaan memiliki tak hingga banyak penyelesaian."
        else:
            solusi_teks = "Persamaan tidak memiliki penyelesaian (kontradiksi)."
        return {"solusi": solusi_teks, "langkah_langkah": langkah_langkah}

    nilai_x = total_konstanta / total_koef_var
    nilai_x_str = SukuAljabar(nilai_x).format_koefisien(nilai_x)
    koef_str = s_var_bersih.format_koefisien(total_koef_var)
    konst_str = s_konst_bersih.format_koefisien(total_konstanta)

    langkah_langkah.append({
        "judul": f"Langkah 3: Membagi Kedua Ruas dengan Koefisien {var_utama} ({koef_str})",
        "latex": f"{var_utama} = \\frac{{{konst_str}}}{{{koef_str}}} = {nilai_x_str}",
        "penjelasan": f"Bagi kedua ruas dengan angka {koef_str} agar nilai {var_utama} berdiri sendiri."
    })

    return {
        "solusi": f"{var_utama} = {nilai_x_str}",
        "langkah_langkah": langkah_langkah
    }
