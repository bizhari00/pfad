import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Monitoring Produksi Biodiesel",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# URL Portal Publik Forio Epicenter Anda
URL_PORTAL_FORIO = "https://forio.com/app/bustamiizhari/inl"

# Menghilangkan margin bawaan Streamlit agar layout grafik lebih luas
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
    }
    h1 {
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-bottom: 20px;
    }
    /* Style tombol kustom agar menyatu rapi dengan UI Streamlit */
    .custom-parent-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: #ffffff;
        color: #31333F;
        border: 1px solid rgba(49, 51, 63, 0.2);
        padding: 0.4rem 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        font-size: 1rem;
        text-decoration: none;
        cursor: pointer;
        transition: background-color 0.16s ease-in-out;
        width: 100%;
        height: 42px;
    }
    .custom-parent-btn:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
        background-color: rgba(255, 75, 75, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- NAVIGASI KEMBALI & JUDUL HALAMAN ---
col_nav, _ = st.columns([2, 5])
with col_nav:
    # Menggunakan target="_parent" untuk memindahkan frame satu tingkat di atas iframe Streamlit
    st.markdown(
        f'<a href="{URL_PORTAL_FORIO}" target="_parent" class="custom-parent-btn">🏠 Kembali ke Menu Utama</a>', 
        unsafe_allow_html=True
    )

st.markdown("<h1>Monitoring Produksi Biodiesel</h1>", unsafe_allow_html=True)

# ==========================================
# 2. MEMUAT BACKGROUND IMAGE
# ==========================================
try:
    img = Image.open("rivaldi.png")
except FileNotFoundError:
    st.error("File 'rivaldi.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==========================================
# 3. DEFINISI JALUR ALIRAN & BOUNDING BOX
# ==========================================
y_flow = 850 
flow_path = [
    {
        'x': 100, 'y': y_flow, 'label': 'Persiapan Bahan', 
        'tank_area': [50, 150, 150, 350]
    },
    {
        'x': 285, 'y': y_flow, 'label': 'Reaktor 1 Aktif', 
        'tank_area': [240, 680, 330, 830]
    },
    {
        'x': 410, 'y': y_flow, 'label': 'Separator 1 Aktif', 
        'tank_area': [370, 680, 450, 830]
    },
    {
        'x': 535, 'y': y_flow, 'label': 'Reaktor 2 Aktif', 
        'tank_area': [490, 680, 580, 830]
    },
    {
        'x': 660, 'y': y_flow, 'label': 'Separator 2 Aktif', 
        'tank_area': [620, 680, 700, 830]
    },
    {
        'x': 950, 'y': y_flow, 'label': 'Produk Biodiesel', 
        'tank_area': [900, 680, 1000, 830]
    }
]

# ==========================================
# 4. LOGIKA ANIMASI JALUR PROSES (DENGAN KEY DINAMIS)
# ==========================================
placeholder = st.empty()
render_count = 0

while True:
    for step in range(len(flow_path)):
        current = flow_path[step]
        
        fig = px.imshow(img)
        
        area = current['tank_area']
        fig.add_shape(
            type="rect",
            x0=area[0], y0=area[1], x1=area[2], y1=area[3],
            fillcolor="rgba(0, 255, 0, 0.4)",  
            line=dict(color="LimeGreen", width=2),
        )
        
        fig.add_scatter(
            x=[current['x']], y=[current['y']],
            mode="markers+text",
            marker=dict(size=35, color="yellow", symbol="triangle-right", line=dict(width=3, color="orange")),
            text=[current['label']],
            textposition="bottom center",
            textfont=dict(size=18, color="darkred", family="Arial Black")
        )
        
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(
            margin=dict(l=5, r=5, t=5, b=5),
            height=650
        )
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={'displayModeBar': False}, 
                key=f"plotly_render_{render_count}"
            )
        
        render_count += 1
        time.sleep(1.5)
