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
# y_flow = 740 

flow_path = [
    {
        'step_id': 'pre_treatment',
        'x': 100, 'y': 850, 'label': 'Persiapan Metanol, H2SO4, PFAD', 
        # Area tangki yang menyala bersamaan di langkah 1 (koordinat presisi dari grid)
        'metanol_area': [145, 80, 310, 210], # Kiri-Atas (Metanol + H2SO4 dalam satu kotak)
        'pfad_area': [135, 400, 215, 520]     # Kiri-Bawah (PFAD)
    },
    {
        'step_id': 'reaktor',
        'x': 320, 'y': 850, 'label': 'Proses Reaktor', 
        'tank_area': [290, 340, 375, 500]     # Tangki Reaktor di tengah
    },
    {
        'step_id': 'separator',
        'x': 420, 'y': 850, 'label': 'Proses Separator', 
        'tank_area': [380, 420, 460, 520]     # Tangki Separator di kanan reaktor
    },
    {
        'step_id': 'washdrum',
        'x': 600, 'y': 850, 'label': 'Wash Drum Aktif', 
        'tank_area': [560, 420, 640, 520]     # Tangki Wash Drum
    },
    {
        'step_id': 'evaporator',
        'x': 710, 'y': 850, 'label': 'Evaporator Aktif', 
        'tank_area': [670, 420, 750, 520]     # Tangki Evaporator
    },
    {
        'step_id': 'biodiesel',
        'x': 860, 'y': 850, 'label': 'Produk Biodiesel', 
        'tank_area': [800, 420, 920, 520]     # Tangki Produk Akhir
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
        
        # LOGIKA KHUSUS LANGKAH 1: MENYALAKAN METANOL, H2SO4, DAN PFAD BERSAMAAN
        if current.get('step_id') == 'pre_treatment':
            # Gambar kotak hijau untuk area Metanol & H2SO4
            area_mtl = current['metanol_area']
            fig.add_shape(
                type="rect",
                x0=area_mtl[0], y0=area_mtl[1], x1=area_mtl[2], y1=area_mtl[3],
                fillcolor="rgba(0, 255, 0, 0.4)",  # Hijau transparan
                line=dict(color="LimeGreen", width=2),
            )
            # Gambar kotak hijau untuk area PFAD
            area_pfd = current['pfad_area']
            fig.add_shape(
                type="rect",
                x0=area_pfd[0], y0=area_pfd[1], x1=area_pfd[2], y1=area_pfd[3],
                fillcolor="rgba(0, 255, 0, 0.4)",  # Hijau transparan
                line=dict(color="LimeGreen", width=2),
            )
        else:
            # Langkah-langkah lain hanya menyalakan satu kotak hijau
            area = current['tank_area']
            fig.add_shape(
                type="rect",
                x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                fillcolor="rgba(0, 255, 0, 0.4)",  
                line=dict(color="LimeGreen", width=2),
            )
        
        # Tambahkan panah animasi segitiga kuning (sumbu Y di 850 sesuai gambar grid Anda)
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
