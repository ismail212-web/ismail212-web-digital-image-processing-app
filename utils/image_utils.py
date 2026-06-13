import streamlit as st
from matplotlib.figure import Figure


def show_image_centered(image, caption: str = "", width: int = None):
    """Tampilkan gambar atau matplotlib Figure di tengah."""
    st.markdown('<div class="img-center">', unsafe_allow_html=True)

    # Jika yang dikirim adalah Figure matplotlib
    if isinstance(image, Figure):
        st.pyplot(image, clear_figure=True)
        if caption:
            st.caption(caption)
    else:
        # untuk PIL Image / numpy array
        if width:
            st.image(image, caption=caption, width=width)
        else:
            st.image(image, caption=caption, width="content")

    st.markdown("</div>", unsafe_allow_html=True)
