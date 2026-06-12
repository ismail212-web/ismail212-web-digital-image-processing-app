import streamlit as st
import json, os
from datetime import datetime

DB_DIR = "data"
DB_FILE = os.path.join(DB_DIR, "sertifikat_db.json")
TEMPLATE_FILE = os.path.join(DB_DIR, "template_cert.html")


def load_database():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"peserta": [], "total_sertifikat": 0}


def save_database(db):
    os.makedirs(DB_DIR, exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def add_participant(name, school, score, correct, total):
    db = load_database()
    cert_id = f"SERT-{db['total_sertifikat'] + 1:04d}"
    date_str = datetime.now().strftime("%d %B %Y, %H:%M:%S")
    db["peserta"].append(
        {
            "nama": name,
            "sekolah": school,
            "nilai": score,
            "benar": correct,
            "total": total,
            "tanggal": date_str,
            "id_sertifikat": cert_id,
        }
    )
    db["total_sertifikat"] += 1
    save_database(db)
    return cert_id, date_str


def generate_certificate_html(name, school, score, correct, total, cert_id, date):
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            template = f.read()

        # PERBAIKAN: Gunakan .replace() agar tidak bentrok dengan kurung kurawal CSS
        template = template.replace("{NAMA}", name)
        template = template.replace("{SEKOLAH}", school)
        template = template.replace("{SCORE}", f"{score:.1f}%")
        template = template.replace("{CORRECT}", f"{correct}/{total}")
        template = template.replace("{TOTAL}", str(total))
        template = template.replace("{CERT_ID}", cert_id)
        template = template.replace("{DATE}", date)

        return template
    return "<h3 style='color:red;'>⚠ template_cert.html tidak ditemukan!</h3>"


QUIZ_QUESTIONS = [
    {
        "id": 1,
        "materi": "Materi 1",
        "pertanyaan": "Rentang nilai uint8?",
        "opsi": {"A": "0-255", "B": "0-256", "C": "1-8", "D": "-128-127"},
        "jawaban_benar": "A",
        "pembahasan": "2^8-1=255",
    },
    {
        "id": 2,
        "materi": "Materi 1",
        "pertanyaan": "Mach Band disebabkan?",
        "opsi": {
            "A": "Distorsi",
            "B": "Warna",
            "C": "Lateral inhibition",
            "D": "Gelap",
        },
        "jawaban_benar": "C",
        "pembahasan": "Ilusi di perbatasan",
    },
    {
        "id": 3,
        "materi": "Materi 1",
        "pertanyaan": "False contouring <?",
        "opsi": {"A": "256", "B": "64", "C": "16", "D": "2"},
        "jawaban_benar": "B",
        "pembahasan": "<64 level",
    },
    {
        "id": 4,
        "materi": "Materi 1",
        "pertanyaan": "Downsample drastis?",
        "opsi": {"A": "Kabur", "B": "Pixelation", "C": "Terbalik", "D": "Besar"},
        "jawaban_benar": "B",
        "pembahasan": "Kotak kasar",
    },
    {
        "id": 5,
        "materi": "Materi 1",
        "pertanyaan": "Bobot G?",
        "opsi": {"A": "0.299", "B": "0.587", "C": "0.114", "D": "0.333"},
        "jawaban_benar": "B",
        "pembahasan": "Mata sensitif hijau",
    },
    {
        "id": 6,
        "materi": "Materi 2",
        "pertanyaan": "Gamma <1?",
        "opsi": {
            "A": "Gelap",
            "B": "Terang area gelap",
            "C": "Negatif",
            "D": "Hilang noise",
        },
        "jawaban_benar": "B",
        "pembahasan": "Angkat low",
    },
    {
        "id": 7,
        "materi": "Materi 2",
        "pertanyaan": "Kelebihan CLAHE?",
        "opsi": {"A": "Cepat", "B": "Clip limit", "C": "Potong", "D": "Hapus"},
        "jawaban_benar": "B",
        "pembahasan": "Batasi noise",
    },
    {
        "id": 8,
        "materi": "Materi 2",
        "pertanyaan": "Bitwise AND?",
        "opsi": {"A": "Halus", "B": "ROI", "C": "Bayang", "D": "Gerak"},
        "jawaban_benar": "B",
        "pembahasan": "Masking",
    },
    {
        "id": 9,
        "materi": "Materi 2",
        "pertanyaan": "DSA?",
        "opsi": {"A": "Tambah", "B": "Kurang", "C": "Kali", "D": "Bagi"},
        "jawaban_benar": "B",
        "pembahasan": "Subtraction",
    },
    {
        "id": 10,
        "materi": "Materi 2",
        "pertanyaan": "Averaging noise?",
        "opsi": {"A": "Statis", "B": "Acak", "C": "Sama", "D": "Merah"},
        "jawaban_benar": "B",
        "pembahasan": "Uncorrelated",
    },
    {
        "id": 11,
        "materi": "Materi 3",
        "pertanyaan": "ILPF dihindari?",
        "opsi": {"A": "Berat", "B": "Pekat", "C": "Ringing", "D": "Putar"},
        "jawaban_benar": "C",
        "pembahasan": "Gibbs",
    },
    {
        "id": 12,
        "materi": "Materi 3",
        "pertanyaan": "Pusat FFT?",
        "opsi": {"A": "AC", "B": "DC", "C": "Nyquist", "D": "Gibbs"},
        "jawaban_benar": "B",
        "pembahasan": "Rata-rata",
    },
    {
        "id": 13,
        "materi": "Materi 3",
        "pertanyaan": "Salt-pepper?",
        "opsi": {"A": "Mean", "B": "Gaussian", "C": "Median", "D": "Laplacian"},
        "jawaban_benar": "C",
        "pembahasan": "Median",
    },
    {
        "id": 14,
        "materi": "Materi 3",
        "pertanyaan": "Gaussian vs Mean?",
        "opsi": {"A": "Bobot", "B": "Biner", "C": "Freq", "D": "Rusak"},
        "jawaban_benar": "A",
        "pembahasan": "Normal",
    },
    {
        "id": 15,
        "materi": "Materi 3",
        "pertanyaan": "Nyquist?",
        "opsi": {"A": "=fmax", "B": "2x", "C": "0.5x", "D": "10x"},
        "jawaban_benar": "B",
        "pembahasan": "2fmax",
    },
    {
        "id": 16,
        "materi": "Materi 4",
        "pertanyaan": "CN=3?",
        "opsi": {"A": "Ending", "B": "Bifurcation", "C": "Lurus", "D": "Isolated"},
        "jawaban_benar": "B",
        "pembahasan": "Cabang",
    },
    {
        "id": 17,
        "materi": "Materi 4",
        "pertanyaan": "Zhang-Suen?",
        "opsi": {"A": "Warna", "B": "Skeleton", "C": "Luas", "D": "Rotasi"},
        "jawaban_benar": "B",
        "pembahasan": "1px",
    },
    {
        "id": 18,
        "materi": "Materi 4",
        "pertanyaan": "SIFT?",
        "opsi": {"A": "Tidak", "B": "Skala rotasi", "C": "Dewasa", "D": "Hapus"},
        "jawaban_benar": "B",
        "pembahasan": "Invariant",
    },
    {
        "id": 19,
        "materi": "Materi 4",
        "pertanyaan": "CN=1?",
        "opsi": {"A": "0", "B": "1", "C": "2", "D": "4"},
        "jawaban_benar": "B",
        "pembahasan": "Ujung",
    },
    {
        "id": 20,
        "materi": "Materi 4",
        "pertanyaan": "Score < threshold?",
        "opsi": {"A": "MISMATCH", "B": "PARTIAL", "C": "MATCH", "D": "UNKNOWN"},
        "jawaban_benar": "A",
        "pembahasan": "Beda",
    },
    {
        "id": 21,
        "materi": "Materi 1",
        "pertanyaan": "Piksel?",
        "opsi": {"A": "Unit terkecil", "B": "Filter", "C": "Format", "D": "Algoritma"},
        "jawaban_benar": "A",
        "pembahasan": "Element",
    },
    {
        "id": 22,
        "materi": "Materi 1",
        "pertanyaan": "Rumus grayscale?",
        "opsi": {"A": "0.5", "B": "0.299R+0.587G+0.114B", "C": "/3", "D": "0.333"},
        "jawaban_benar": "B",
        "pembahasan": "ITU",
    },
    {
        "id": 23,
        "materi": "Materi 1",
        "pertanyaan": "Mach Band biologis?",
        "opsi": {"A": "Resolusi", "B": "Lateral", "C": "Kompresi", "D": "Noise"},
        "jawaban_benar": "B",
        "pembahasan": "Retina",
    },
    {
        "id": 24,
        "materi": "Materi 1",
        "pertanyaan": "Resolusi turun?",
        "opsi": {"A": "Tajam", "B": "Pixelation", "C": "BW", "D": "Besar"},
        "jawaban_benar": "B",
        "pembahasan": "Kotak",
    },
    {
        "id": 25,
        "materi": "Materi 2",
        "pertanyaan": "Gamma <1 efek?",
        "opsi": {"A": "Redup", "B": "Terang", "C": "Negatif", "D": "Tetap"},
        "jawaban_benar": "B",
        "pembahasan": "Angkat",
    },
    {
        "id": 26,
        "materi": "Materi 2",
        "pertanyaan": "CLAHE?",
        "opsi": {"A": "Cepat", "B": "Kontras lokal", "C": "BW", "D": "Hapus"},
        "jawaban_benar": "B",
        "pembahasan": "Adaptif",
    },
    {
        "id": 27,
        "materi": "Materi 2",
        "pertanyaan": "Bitwise AND?",
        "opsi": {"A": "Balik", "B": "ROI", "C": "Gabung", "D": "Hist"},
        "jawaban_benar": "B",
        "pembahasan": "Mask",
    },
    {
        "id": 28,
        "materi": "Materi 2",
        "pertanyaan": "DSA tujuan?",
        "opsi": {"A": "Cerah", "B": "Hilangkan statis", "C": "BW", "D": "Kecil"},
        "jawaban_benar": "B",
        "pembahasan": "Pembuluh",
    },
    {
        "id": 29,
        "materi": "Materi 2",
        "pertanyaan": "Averaging varians?",
        "opsi": {"A": "N", "B": "1/N", "C": "√N", "D": "0"},
        "jawaban_benar": "B",
        "pembahasan": "1/N",
    },
    {
        "id": 30,
        "materi": "Materi 2",
        "pertanyaan": "Mean vs Gaussian?",
        "opsi": {"A": "Lambat", "B": "Bobot pusat", "C": "Warna", "D": "Tidak"},
        "jawaban_benar": "B",
        "pembahasan": "Halus",
    },
    {
        "id": 31,
        "materi": "Materi 3",
        "pertanyaan": "FFT?",
        "opsi": {
            "A": "Fast Fourier Transform",
            "B": "Filtered",
            "C": "Feature",
            "D": "Final",
        },
        "jawaban_benar": "A",
        "pembahasan": "DFT",
    },
    {
        "id": 32,
        "materi": "Materi 3",
        "pertanyaan": "DC?",
        "opsi": {"A": "Tepi", "B": "Noise", "C": "Rata-rata", "D": "Tinggi"},
        "jawaban_benar": "C",
        "pembahasan": "Mean",
    },
    {
        "id": 33,
        "materi": "Materi 3",
        "pertanyaan": "LPF?",
        "opsi": {"A": "Tajam", "B": "Blur", "C": "Kontras", "D": "Negatif"},
        "jawaban_benar": "B",
        "pembahasan": "Smooth",
    },
    {
        "id": 34,
        "materi": "Materi 3",
        "pertanyaan": "Ringing?",
        "opsi": {"A": "Gaussian", "B": "Butterworth", "C": "Ideal", "D": "Median"},
        "jawaban_benar": "C",
        "pembahasan": "Tajam",
    },
    {
        "id": 35,
        "materi": "Materi 3",
        "pertanyaan": "Nyquist?",
        "opsi": {"A": "=", "B": "2x", "C": "0.5", "D": "3x"},
        "jawaban_benar": "B",
        "pembahasan": "2fmax",
    },
    {
        "id": 36,
        "materi": "Materi 4",
        "pertanyaan": "Minutiae?",
        "opsi": {"A": "Warna", "B": "Ending bifurcation", "C": "Ukuran", "D": "Sensor"},
        "jawaban_benar": "B",
        "pembahasan": "Fitur",
    },
    {
        "id": 37,
        "materi": "Materi 4",
        "pertanyaan": "CN=3?",
        "opsi": {"A": "Ending", "B": "Bifurcation", "C": "Lurus", "D": "Isolated"},
        "jawaban_benar": "B",
        "pembahasan": "3",
    },
    {
        "id": 38,
        "materi": "Materi 4",
        "pertanyaan": "Zhang-Suen?",
        "opsi": {"A": "Kontras", "B": "Skeleton", "C": "Warna", "D": "Noise"},
        "jawaban_benar": "B",
        "pembahasan": "Thinning",
    },
    {
        "id": 39,
        "materi": "Materi 4",
        "pertanyaan": "SIFT?",
        "opsi": {
            "A": "Rotasi",
            "B": "Rotasi skala translasi",
            "C": "Warna",
            "D": "Noise",
        },
        "jawaban_benar": "B",
        "pembahasan": "Invariant",
    },
    {
        "id": 40,
        "materi": "Materi 4",
        "pertanyaan": "Match ≥?",
        "opsi": {"A": "MISMATCH", "B": "PARTIAL", "C": "MATCH", "D": "UNKNOWN"},
        "jawaban_benar": "C",
        "pembahasan": "Sama",
    },
]


def run():
    defaults = {
        "quiz_phase": "registration",
        "quiz_submitted": False,
        "quiz_answers": {},
        "participant_name": "",
        "participant_school": "",
        "current_question_idx": 0,
        "cert_id": "",
        "cert_date": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    if st.session_state.quiz_phase == "registration":
        show_registration_page()
    elif st.session_state.quiz_phase == "quiz":
        show_quiz_page()
    else:
        show_result_page()


def show_registration_page():
    total = len(QUIZ_QUESTIONS)
    st.markdown(
        f"""<div style="background:linear-gradient(135deg,#1e3a8a,#3b82f6);color:white;padding:25px;border-radius:12px;text-align:center"><h2>🎓 UJIAN AKHIR KOMPETENSI LABORATORIUM DIP</h2><p>Evaluasi Komprehensif — Total {total} Pertanyaan</p></div>""",
        unsafe_allow_html=True,
    )
    db = load_database()
    c1, c2, c3 = st.columns(3)
    c1.metric("🏆 Sertifikat", db["total_sertifikat"])
    c2.metric("📊 Peserta", len(db["peserta"]))
    c3.metric("📝 Bank Soal", f"{total} Soal")
    st.markdown("---")
    with st.form("reg"):
        name = st.text_input("👤 Nama Lengkap")
        school = st.text_input("🏫 Institusi")
        st.markdown(f"**Syarat:** Nilai minimal **75%** dari total {total} soal")
        if st.form_submit_button("🚀 Mulai", type="primary", use_container_width=True):
            if name and school:
                st.session_state.update(
                    {
                        "participant_name": name,
                        "participant_school": school,
                        "quiz_phase": "quiz",
                        "current_question_idx": 0,
                        "quiz_answers": {},
                    }
                )
                st.rerun()
            else:
                st.error("Isi nama & institusi")


def show_quiz_page():
    total = len(QUIZ_QUESTIONS)
    idx = st.session_state.current_question_idx
    q = QUIZ_QUESTIONS[idx]
    st.subheader(q["materi"])
    st.progress((idx + 1) / total, text=f"Soal {idx+1}/{total}")
    st.markdown(f"**{q['pertanyaan']}**")
    opts = [f"{k}. {v}" for k, v in q["opsi"].items()]
    prev = st.session_state.quiz_answers.get(q["id"])
    idx_def = list(q["opsi"]).index(prev) if prev else None
    pil = st.radio("Pilih:", opts, index=idx_def, key=f"r{q['id']}")
    if pil:
        st.session_state.quiz_answers[q["id"]] = pil[0]
    sudah = q["id"] in st.session_state.quiz_answers
    if not sudah:
        st.warning("Pilih jawaban dulu")
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        if st.button("⬅ Back", disabled=idx == 0):
            st.session_state.current_question_idx -= 1
            st.rerun()
    with c2:
        if idx < total - 1:
            if st.button("Next ➡", type="primary", disabled=not sudah):
                st.session_state.current_question_idx += 1
                st.rerun()
        else:
            all_done = len(st.session_state.quiz_answers) == total
            if st.button("🔒 Submit", type="primary", disabled=not all_done):
                st.session_state.quiz_phase = "result"
                st.rerun()


def show_result_page():
    total = len(QUIZ_QUESTIONS)
    benar = sum(
        1
        for q in QUIZ_QUESTIONS
        if st.session_state.quiz_answers.get(q["id"]) == q["jawaban_benar"]
    )
    skor = benar / total * 100
    lulus = skor >= 75
    st.title("📊 Hasil")
    c1, c2 = st.columns(2)
    c1.metric("Skor", f"{skor:.1f}%", "LULUS" if lulus else "GAGAL")
    c2.metric("Benar", f"{benar}/{total}")
    if lulus:
        st.success(f"Selamat {st.session_state.participant_name}!")
        if not st.session_state.cert_id:
            cid, cd = add_participant(
                st.session_state.participant_name,
                st.session_state.participant_school,
                skor,
                benar,
                total,
            )
            st.session_state.cert_id = cid
            st.session_state.cert_date = cd
        html = generate_certificate_html(
            st.session_state.participant_name,
            st.session_state.participant_school,
            skor,
            benar,
            total,
            st.session_state.cert_id,
            st.session_state.cert_date,
        )
        st.components.v1.html(html, height=800, scrolling=True)
    else:
        st.error("Belum lulus, ulangi")
    st.markdown("---")
    st.markdown("### Pembahasan")
    for q in QUIZ_QUESTIONS:
        ans = st.session_state.quiz_answers.get(q["id"], "-")
        ok = ans == q["jawaban_benar"]
        with st.expander(f"Soal {q['id']}: {'🟢' if ok else '❌'}"):
            st.write(q["pertanyaan"])
            st.write(f"Jawaban Anda: {ans}")
            st.write(f"Benar: {q['jawaban_benar']}")
            st.info(q["pembahasan"])
    if st.button("🔄 Ulangi"):
        st.session_state.quiz_phase = "registration"
        st.session_state.quiz_answers = {}
        st.rerun()
