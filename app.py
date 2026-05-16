import streamlit as st
import pandas as pd
import numpy as np

# 1. Konfigurasi Halaman Utama Streamlit
st.set_page_config(
    page_title="PFAD Biodiesel Simulation",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Gaya Visual / Background (Menggantikan CSS Dash Layout)
# Memastikan background gambar tetap bekerja menggunakan custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("/assets/rivaldi.png");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .custom-container {
        background-color: rgba(0, 0, 0, 0.75);
        padding: 25px;
        border-radius: 10px;
        color: #ffffff;
        margin-bottom: 20px;
        border: 1px solid #f1c40f;
    }
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_index=True
)

# 3. Struktur Header Aplikasi
st.markdown('<h1 style="text-align: center; color: #f1c40f;">Simulasi Model Biodiesel PFAD</h1>', unsafe_allow_index=True)
st.markdown('<p style="text-align: center; color: #ffffff;">Analisis kelayakan teknis dan hasil konversi Palm Fatty Acid Distillate.</p>', unsafe_allow_index=True)
st.markdown('<hr style="border-color: #f1c40f;">', unsafe_allow_index=True)

# 4. Area Kontrol / Input (Menggantikan dcc.Slider & Callback)
st.markdown('<div class="custom-container">', unsafe_allow_index=True)
st.subheader("⚙️ Parameter Kontrol Umpan")

feedstock_value = st.slider(
    label="Kapasitas Umpan PFAD (Ton/Tahun):",
    min_value=10000,
    max_value=200000,
    value=50000,
    step=5000,
    format="%d"
)
st.markdown('</div>', unsafe_allow_index=True)

# 5. Logika Perhitungan Rekayasa Proses (Pengganti Fungsi Callback)
conversion_ratio = 0.88
biodiesel_yield = feedstock_value * conversion_ratio
gliserol_co_product = feedstock_value * 0.10

# 6. Area Output / Hasil Proyeksi Simulasi
st.markdown('<div class="custom-container">', unsafe_allow_index=True)
st.markdown('<h3 style="color: #2ecc71;">📊 Hasil Proyeksi Simulasi</h3>', unsafe_allow_index=True)
st.write("") # Memberi space kosong

# Menampilkan metrik hasil dengan format yang rapi
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Bahan Baku (PFAD)", 
        value=f"{feedstock_value:,} Ton/Tahun"
    )

with col2:
    st.metric(
        label="Proyeksi Hasil Biodiesel", 
        value=f"{biodiesel_yield:,.2f} Ton/Tahun",
        delta=f"Rasio: {conversion_ratio*100}%",
        delta_color="normal"
    )

with col3:
    st.metric(
        label="Produk Sampingan (Gliserol Crude)", 
        value=f"{gliserol_co_product:,.2f} Ton/Tahun"
    )

st.markdown('</div>', unsafe_allow_index=True)
