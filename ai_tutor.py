"""
ai_tutor.py
Modul Asisten Tutor AI Berbasis Google Gemini API
Berlandaskan Rigorous Mathematical Thinking (RMT) & Mediated Learning Experience (MLE)
"""

import os
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Optional
import streamlit as st

SYSTEM_PROMPT_RMT = """
Anda adalah "Tutor AI AljabarKu", seorang pendidik matematika SMP yang ramah, interaktif, dan berwawasan luas.
Pendekatan pedagogis Anda didasarkan pada RIGOROUS MATHEMATICAL THINKING (RMT) (Kinard & Kozulin) dan Mediated Learning Experience (Feuerstein):

PEDOMAN UTAMA:
1. Bimbingan Bertahap (Scaffolding): Jangan langsung memberikan jawaban jadi jika siswa menanyakan soal. Ajukan pertanyaan pemantik agar siswa berpikir mandiri.
2. Atribut Kritis Suku Sejenis: Tegaskan bahwa suku sejenis wajib memiliki dua atribut: VARIABEL YANG SAMA dan DERAJAT PANGKAT YANG SAMA. Jelaskan bahwa menggabungkan suku sejenis adalah penerapan SIFAT DISTRIBUTIF KEBALIKAN: ax + bx = (a + b)x.
3. Menolak Miskonsepsi "Pindah Ruas": Jika siswa menyebut 'pindah ruas', perbaiki dengan lembut dan jelaskan PRINSIP KESETARAAN (Timbangan Seimbang) serta penggunaan INVERS ADITIF (lawan tanda) dan INVERS MULTIPLIKATIF (kebalikan) pada KEDUA RUAS.
4. Gaya Komunikasi: Hangat, memotivasi, gunakan bahasa Indonesia yang mudah dipahami anak SMP Kelas 7, serta gunakan notasi matematika yang jelas (LaTeX Markdown seperti $2x + 5 = 15$).
5. Selalu sertakan langkah VERIFIKASI / REFLEKSI SOLUSI di akhir pemecahan masalah persamaan.
"""

def ambil_gemini_api_key() -> str:
    """Mengambil Gemini API Key dari session_state, st.secrets, atau os.environ"""
    # 1. Dari input sesi aktif pengguna
    if "custom_gemini_api_key" in st.session_state and st.session_state.custom_gemini_api_key.strip():
        return st.session_state.custom_gemini_api_key.strip()

    # 2. Dari Streamlit Secrets (.streamlit/secrets.toml)
    try:
        if "GEMINI_API_KEY" in st.secrets and str(st.secrets["GEMINI_API_KEY"]).strip():
            key = str(st.secrets["GEMINI_API_KEY"]).strip()
            if key != "MASUKKAN_GEMINI_API_KEY_ANDA_DI_SINI":
                return key
    except Exception:
        pass

    # 3. Dari Environment Variables
    env_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if env_key:
        return env_key

    return ""

def tanya_tutor_gemini(pesan_siswa: str, api_key: str, riwayat_obrolan: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Mengirimkan prompt ke Google Gemini API menggunakan endpoint resmi Gemini REST API.
    Bekerja langsung menggunakan modul standar Python tanpa ketergantungan paket eksternal yang rumit.
    """
    if not api_key:
        raise ValueError("API Key Google Gemini belum dimasukkan. Silakan pasang API Key Anda.")

    # Model default Google Gemini
    model_name = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    # Susun riwayat percakapan untuk konteks multi-turn
    contents = []
    if riwayat_obrolan:
        for chat in riwayat_obrolan[-6:]:  # Ambil maksimal 6 pertukaran pesan terakhir
            role = "user" if chat.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": chat.get("content", "")}]
            })

    # Tambahkan pesan terbaru siswa
    contents.append({
        "role": "user",
        "parts": [{"text": pesan_siswa}]
    })

    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT_RMT}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 1200
        }
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            resp_bytes = response.read()
            data = json.loads(resp_bytes.decode("utf-8"))

            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts:
                    return parts[0].get("text", "Tutor AI tidak memberikan jawaban teks.")
            return "Maaf, Tutor AI tidak dapat menghasilkan tanggapan saat ini."

    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8", errors="ignore")
        try:
            err_json = json.loads(error_msg)
            pesan_detail = err_json.get("error", {}).get("message", error_msg)
        except Exception:
            pesan_detail = error_msg
        raise RuntimeError(f"Gagal menghubungi Google Gemini API (Kode {e.code}): {pesan_detail}")
    except Exception as e:
        raise RuntimeError(f"Terjadi kendala jaringan/koneksi: {str(e)}")
