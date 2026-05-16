import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="PFAD Produksi Biodiesel",
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
    /* Style tombol kustom agar serasi dengan UI Streamlit */
    .custom-tab-btn {
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
    .custom-tab-btn:hover {
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
    # Menggunakan target="_blank" agar klik kiri langsung otomatis membuka tab baru (sukses melompati blokir iframe)
    st.markdown(
        f'<a href="{URL_PORTAL_FORIO}" target="_blank" class="custom-tab-btn">🏠 Kembali ke Menu Utama</a>', 
        unsafe_allow_html=True
    )

st.markdown("<h1>PFAD Biodiesel</h1>", unsafe_allow_html=True)

# ==========================================
# 2. MEMUAT BACKGROUND IMAGE
# ==========================================
try:
    img = Image.open("rivaldi.png")
except FileNotFoundError:
    st.error("File 'rivaldi.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==========================================
# 3. DEFINISI JALUR ALIRAN REVISI (URUTAN ASLI DIAGRAM)
# ==========================================
# Koordinat sumbu Y disesuaikan dengan level posisi tangki utama di gambar (sekitar 700 - 800)
y_flow = 740 

flow_path = [
    {
        'x': 90, 'y': 740, 'label': 'Persiapan Bahan (PFAD)', 
        'tank_area': [45, 640, 130, 790]
    },
    {
        'x': 390, 'y': 740, 'label': 'Proses Reaktor', 
        'tank_area': [350, 640, 425, 790]
    },
    {
        'x': 490, 'y': 740, 'label': 'Proses Separator', 
        'tank_area': [455, 640, 525, 790]
    },
    {
        'x': 700, 'y': 740, 'label': 'Wash Drum Aktif', 
        'tank_area': [665, 640, 735, 790]
    },
    {
        'x': 770, 'y': 740, 'label': 'Evaporator Aktif', 
        'tank_area': [740, 640, 805, 790]
    },
    {
        'x': 860, 'y': 740, 'label': 'Produk Biodiesel', 
        'tank_area': [825, 640, 890, 790]
    }
]

# ==========================================
# 4. LOGIKA ANIMASI JALUR PROSES
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
