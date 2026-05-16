import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Kalibrasi Koordinat PFAD",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Menghilangkan margin bawaan Streamlit agar layout grafik lebih luas
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    h1 {
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>🔧 Mode Kalibrasi Koordinat Gambar</h1>", unsafe_allow_html=True)
st.write("Arahkan kursor Anda ke tangki pada gambar untuk melihat koordinat X dan Y yang tepat!")

# ==========================================
# 2. MEMUAT BACKGROUND IMAGE
# ==========================================
try:
    img = Image.open("rivaldi.png")
except FileNotFoundError:
    st.error("File 'rivaldi.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==========================================
# 3. MEMBUAT GRAFIK DENGAN GRID & COORD TUNER
# ==========================================
fig = px.imshow(img)

# Mengaktifkan sumbu koordinat dan grid agar terlihat jelas di layar
fig.update_xaxes(visible=True, showgrid=True, gridcolor="rgba(255, 0, 0, 0.3)", dtick=50)
fig.update_yaxes(visible=True, showgrid=True, gridcolor="rgba(255, 0, 0, 0.3)", dtick=50)

fig.update_layout(
    margin=dict(l=10, r=10, t=10, b=10),
    height=750,
    hovermode="closest"
)

# Render grafik ke Streamlit
st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 4. FORM SIMULASI UJI COBA KOTAK (INPUT MANUAL)
# ==========================================
st.sidebar.header("🎯 Tes Gambar Kotak")
test_x0 = st.sidebar.number_input("X0 (Kiri)", value=100)
test_y0 = st.sidebar.number_input("Y0 (Atas)", value=100)
test_x1 = st.sidebar.number_input("X1 (Kanan)", value=200)
test_y1 = st.sidebar.number_input("Y1 (Bawah)", value=200)

if st.sidebar.button("Tampilkan Kotak Uji Coba"):
    fig.add_shape(
        type="rect",
        x0=test_x0, y0=test_y0, x1=test_x1, y1=test_y1,
        fillcolor="rgba(255, 0, 0, 0.5)",
        line=dict(color="Red", width=3),
    )
    st.rerun()
