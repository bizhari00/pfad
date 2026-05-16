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
# 3. DEFINISI Bounding Box Tangki Pembantu (Atas)
# ==========================================
TANGKI_METANOL = [245, 370, 285, 470]
TANGKI_H2SO4   = [245, 500, 285, 610]
TANGKI_NAOH    = [410, 335, 455, 435]

# ==========================================
# 4. DEFINISI JALUR ALIRAN LENGKAP (8 TAHAPAN)
# ==========================================
y_flow = 850 

flow_path = [
    {
        'step_id': 'feedstock',
        'x': 100, 'y': y_flow, 'label': 'Feedstock (PFAD)', 
        'tank_area': [50, 150, 150, 350]
    },
    {
        'step_id': 'reaktor1',
        'x': 285, 'y': y_flow, 'label': 'Reaktor 1 Aktif', 
        'tank_area': [240, 680, 330, 830]
    },
    {
        'step_id': 'separator1',
        'x': 410, 'y': y_flow, 'label': 'Separator 1 Aktif', 
        'tank_area': [370, 680, 450, 830]
    },
    {
        'step_id': 'reaktor2',
        'x': 535, 'y': y_flow, 'label': 'Reaktor 2 Aktif', 
        'tank_area': [490, 680, 580, 830]
    },
    {
        'step_id': 'separator2',
        'x': 660, 'y': y_flow, 'label': 'Separator 2 Aktif', 
        'tank_area': [620, 680, 700, 830]
    },
    {
        'step_id': 'washdrum',
        'x': 740, 'y': y_flow, 'label': 'Wash Drum Aktif', 
        'tank_area': [710, 680, 775, 830]
    },
    {
        'step_id': 'evaporator',
        'x': 810, 'y': y_flow, 'label': 'Evaporator Aktif', 
        'tank_area': [780, 680, 845, 830]
    },
    {
        'step_id': 'biodiesel',
        'x': 950, 'y': y_flow, 'label': 'Produk Biodiesel', 
        'tank_area': [900, 680, 1000, 830]
    }
]

# ==========================================
# 5. LOGIKA ANIMASI JALUR PROSES & PERUBAHAN WARNA ATAS
# ==========================================
placeholder = st.empty()
render_count = 0

while True:
    for step in range(len(flow_path)):
        current = flow_path[step]
        
        fig = px.imshow(img)
        
        # 1. Gambar kotak hijau pada tangki alur utama yang sedang aktif
        main_area = current['tank_area']
        fig.add_shape(
            type="rect",
            x0=main_area[0], y0=main_area[1], x1=main_area[2], y1=main_area[3],
            fillcolor="rgba(0, 255, 0, 0.4)",  
            line=dict(color="LimeGreen", width=2),
        )
        
        # 2. LOGIKA KONDISIONAL TANGKI ATAS
        # Jika Reaktor 1 aktif -> Nyalakan Metanol & H2SO4 di atasnya
        if current['step_id'] == 'reaktor1':
            # Highlight Metanol
            fig.add_shape(
                type="rect", x0=TANGKI_METANOL[0], y0=TANGKI_METANOL[1], x1=TANGKI_METANOL[2], y1=TANGKI_METANOL[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
            )
            # Highlight H2SO4
            fig.add_shape(
                type="rect", x0=TANGKI_H2SO4[0], y0=TANGKI_H2SO4[1], x1=TANGKI_H2SO4[2], y1=TANGKI_H2SO4[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
            )
            
        # Jika Reaktor 2 aktif -> Nyalakan NaOH di atasnya
        elif current['step_id'] == 'reaktor2':
            # Highlight NaOH
            fig.add_shape(
                type="rect", x0=TANGKI_NAOH[0], y0=TANGKI_NAOH[1], x1=TANGKI_NAOH[2], y1=TANGKI_NAOH[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
            )

        # 3. Tambahkan Penanda Segitiga Kuning Animasi
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
