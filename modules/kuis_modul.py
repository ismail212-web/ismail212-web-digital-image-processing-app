import streamlit as st


def run_kuis_modul(materi: str) -> bool:
    """Kuis interaktif satu soal per satu. Return True jika lulus."""

    # State untuk mengelola progress kuis modul per materi
    if f"kuis_modul_state_{materi}" not in st.session_state:
        st.session_state[f"kuis_modul_state_{materi}"] = {
            "current_question": 0,
            "answers": {},  # Dictionary untuk menyimpan jawaban {nomor_soal: jawaban}
            "submitted": False,  # Flag untuk menandai apakah kuis sudah disubmit
            "score": 0,  # Skor akhir
        }

    state = st.session_state[f"kuis_modul_state_{materi}"]

    # Jika sudah submit, tampilkan hasil dan cek kelulusan
    if state["submitted"]:
        st.success("✅ Kuis Selesai!")
        st.metric(
            "Skor", f"{state['score']}/2"
        )  # Asumsi 2 soal, sesuaikan jika berbeda

        # Tentukan kelulusan (misal: minimal 1 benar)
        passing_score = 1
        if state["score"] >= passing_score:
            st.success("🎉 Selamat! Anda lulus kuis ini.")
            # Set flag lulus di session state utama di app.py
            st.session_state[f"kuis_modul_passed_{materi}"] = True
            # Kembalikan ke app utama untuk update progress
            return True
        else:
            st.error("❌ Maaf, Anda belum lulus. Skor Anda di bawah ambang batas.")
            if st.button("🔁 Ulangi Kuis"):
                # Reset state untuk mengulang
                st.session_state[f"kuis_modul_state_{materi}"] = {
                    "current_question": 0,
                    "answers": {},
                    "submitted": False,
                    "score": 0,
                }
                st.rerun()  # Refresh halaman untuk memulai ulang
        return False  # Belum lulus, tidak update flag utama

    # Definisikan soal-soal di sini. Ganti dengan soal sesuai materi.
    # Contoh untuk Materi 1:
    if materi == "Materi 1":
        soal_list = [
            {
                "no": 1,
                "pertanyaan": "Operasi piksel mengubah?",
                "opsi": ["Ukuran file", "Nilai intensitas", "Format gambar"],
                "jawaban_benar": 1,  # Index dari opsi yang benar (0-indexed)
            },
            {
                "no": 2,
                "pertanyaan": "Fingerprint unik karena?",
                "opsi": ["Warna kulit", "Pola ridge", "Ukuran jari"],
                "jawaban_benar": 1,
            },
        ]
    # Contoh untuk Materi 2:
    elif materi == "Materi 2":
        soal_list = [
            {
                "no": 1,
                "pertanyaan": "Transformasi Gamma < 1 digunakan untuk?",
                "opsi": [
                    "Mencerahkan citra gelap",
                    "Menggelapkan citra terang",
                    "Mengurangi noise",
                ],
                "jawaban_benar": 0,
            },
            {
                "no": 2,
                "pertanyaan": "CLAHE adalah teknik untuk?",
                "opsi": [
                    "Mengurangi noise",
                    "Enhancement kontras lokal",
                    "Deteksi tepi",
                ],
                "jawaban_benar": 1,
            },
        ]
    # Tambahkan elif untuk Materi 3, 4, 5 sesuai kebutuhan Anda
    else:
        # Default jika materi tidak dikenali
        soal_list = [
            {
                "no": 1,
                "pertanyaan": "Soal default untuk materi ini.",
                "opsi": ["Opsi A", "Opsi B", "Opsi C"],
                "jawaban_benar": 0,
            },
            {
                "no": 2,
                "pertanyaan": "Soal kedua default.",
                "opsi": ["Opsi X", "Opsi Y", "Opsi Z"],
                "jawaban_benar": 1,
            },
        ]

    # Ambil soal saat ini dari list
    q = soal_list[state["current_question"]]

    # Header soal
    st.markdown(f"### Soal {q['no']} dari {len(soal_list)}")
    st.write(q["pertanyaan"])

    # Radio button untuk jawaban - tanpa pilihan default (index=None)
    # Gunakan key unik agar tidak konflik antar soal dan materi
    key_radio = f"q{q['no']}_radio_{materi}_idx{state['current_question']}"

    # Cek apakah jawaban untuk soal ini sudah disimpan sebelumnya
    jawaban_sebelumnya = state["answers"].get(q["no"])
    index_awal = None
    if jawaban_sebelumnya is not None:
        try:
            index_awal = q["opsi"].index(jawaban_sebelumnya)
        except ValueError:
            # Jika jawaban yang disimpan tidak ditemukan di opsi (mungkin karena perubahan soal), reset
            index_awal = None

    pil = st.radio(
        "Pilih jawaban Anda:",
        options=q["opsi"],
        index=index_awal,  # Gunakan jawaban sebelumnya jika ada
        key=key_radio,
        # Optional: Disable jika sudah dipilih dan ingin pindah soal
        # disabled=state["current_question"] != state["current_question"]
    )

    # Kolom untuk tombol navigasi
    col_prev, col_next = st.columns([1, 1])

    with col_prev:
        # Tombol "Sebelumnya" hanya muncul jika bukan soal pertama
        if state["current_question"] > 0:
            if st.button(
                "◀ Sebelumnya", use_container_width=True, key=f"prev_{key_radio}"
            ):
                # Simpan jawaban sebelum pindah
                if pil is not None:
                    state["answers"][q["no"]] = pil
                # Pindah ke soal sebelumnya
                state["current_question"] -= 1
                st.rerun()  # Refresh untuk menampilkan soal sebelumnya

    with col_next:
        # Tombol "Berikutnya" atau "Submit"
        if pil is not None:  # Hanya aktifkan jika jawaban dipilih
            if state["current_question"] < len(soal_list) - 1:  # Bukan soal terakhir
                if st.button(
                    "➡ Berikutnya", use_container_width=True, key=f"next_{key_radio}"
                ):
                    # Simpan jawaban untuk soal saat ini
                    state["answers"][q["no"]] = pil
                    # Pindah ke soal berikutnya
                    state["current_question"] += 1
                    st.rerun()  # Refresh untuk menampilkan soal berikutnya
            else:  # Ini adalah soal terakhir
                if st.button(
                    "✅ Submit Kuis",
                    use_container_width=True,
                    key=f"submit_{key_radio}",
                ):
                    # Simpan jawaban soal terakhir
                    state["answers"][q["no"]] = pil

                    # Hitung skor setelah semua jawaban dikumpulkan
                    score = 0
                    for soal in soal_list:
                        no_soal = soal["no"]
                        if no_soal in state["answers"]:
                            jawaban_pengguna = state["answers"][no_soal]
                            idx_jawaban_pengguna = soal["opsi"].index(jawaban_pengguna)
                            if idx_jawaban_pengguna == soal["jawaban_benar"]:
                                score += 1
                    state["score"] = score

                    # Tandai bahwa kuis telah disubmit
                    state["submitted"] = True

                    # Refresh untuk menampilkan hasil
                    st.rerun()
        else:
            # Non-aktifkan tombol jika belum memilih jawaban
            st.button(
                "➡ Berikutnya / Submit",
                disabled=True,
                use_container_width=True,
                key=f"disabled_next_{key_radio}",
            )

    # (Opsional) Tampilkan jawaban sebelumnya
    # if state["current_question"] > 0:
    #     prev_q_no = state["current_question"]
    #     if prev_q_no in state["answers"]:
    #         st.caption(f"Anda menjawab soal {prev_q_no} dengan: {state['answers'][prev_q_no]}")

    # Fungsi ini akan selalu return False kecuali jika state["submitted"] dan skor lulus
    # Kondisi lulus dicek di awal fungsi dan return True jika memenuhi syarat
    return False
