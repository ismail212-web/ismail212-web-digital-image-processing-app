import streamlit as st

def run_kuis_modul(materi: str) -> bool:
    """Kuis sederhana per materi - return True kalau lulus"""

    # cek sudah lulus belum
    key = f"kuis_modul_passed_{materi}"
    if st.session_state.get(key, False):
        return True

    st.markdown("### 📝 Kuis Singkat")
    st.write(f"Selesaikan kuis untuk membuka materi berikutnya setelah **{materi}**")

    # Contoh 2 soal dummy (ganti nanti)
    j1 = st.radio("1. Operasi piksel mengubah?", ["Ukuran file", "Nilai intensitas", "Format gambar"], key=f"q1_{materi}")
    j2 = st.radio("2. Fingerprint unik karena?", ["Warna kulit", "Pola ridge", "Ukuran jari"], key=f"q2_{materi}")

    if st.button("Submit Kuis", key=f"submit_{materi}"):
        benar = (j1 == "Nilai intensitas") + (j2 == "Pola ridge")
        if benar >= 1: # lulus minimal 1 benar (untuk development)
            st.session_state[key] = True
            st.success("✅ Lulus! Materi berikutnya terbuka.")
            st.rerun()
        else:
            st.error("❌ Coba lagi")

    return st.session_state.get(key, False)
