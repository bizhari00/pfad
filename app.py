import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==========================================
# 1. KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Kalibrasi Animasi Bergerak",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("<h1 style='text-align: center;'>🔧 Mode Kalibrasi Aliran Bergerak</h1>", unsafe_allow_html=True)
st.write("Animasi otomatis tetap berjalan. Perhatikan pergeseran kotak hijau dan catat angka grid x, y yang meleset!")

# ==========================================
# 2. MEMUAT BACKGROUND IMAGE
# ==========================================
try:
    img = Image.open("rivaldi.png")
except FileNotFoundError:
    st.error("File 'rivaldi.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==========================================
# 3. KORDINAT TANGKI PEMBANTU (ATAS)
# ==========================================
TANGKI_METANOL = [245, 370, 285, 470]
TANGKI_H2SO4   = [245, 500, 285, 610]
TANGKI_NAOH    = [410, 335, 455, 435]

# ==========================================
# 4. JALUR ALIRAN LENGKAP (8 TAHAPAN)
# ==========================================
y_flow = 850 

flow_path = [
    {
        'step_id': 'feedstock',
        'x': 100, 'y': y_flow, 'label': 'Feedstock (PFAD)', 
        'tank_area': [50, 100, 100, 450]
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
# 5. LOGIKA ANIMASI JALUR PROSES + TAMPILAN GRID
# ==========================================
placeholder = st.empty()
render_count = 0

while True:
    for step in range(len(flow_path)):
        current = flow_path[step]
        
        fig = px.imshow(img)
        
        # --- AKTIFKAN UTALITAS GRID UNTUK TRACKING ---
        fig.update_xaxes(visible=True, showgrid=True, gridcolor="rgba(255, 0, 0, 0.35)", dtick=50)
        fig.update_yaxes(visible=True, showgrid=True, gridcolor="rgba(255, 0, 0, 0.35)", dtick=50)
        
        # 1. Gambar kotak hijau alur utama yang aktif
        main_area = current['tank_area']
        fig.add_shape(
            type="rect",
            x0=main_area[0], y0=main_area[1], x1=main_area[2], y1=main_area[3],
            fillcolor="rgba(0, 255, 0, 0.4)",  
            line=dict(color="LimeGreen", width=2),
        )
        
        # 2. Logika kondisional tangki atas ikut berubah warna
        if current.get('step_id') == 'reaktor1':
            fig.add_shape(
                type="rect", x0=TANGKI_METANOL[0], y0=TANGKI_METANOL[1], x1=TANGKI_METANOL[2], y1=TANGKI_METANOL[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
            )
            fig.add_shape(
                type="rect", x0=TANGKI_H2SO4[0], y0=TANGKI_H2SO4[1], x1=TANGKI_H2SO4[2], y1=TANGKI_H2SO4[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
            )
        elif current.get('step_id') == 'reaktor2':
            fig.add_shape(
                type="rect", x0=TANGKI_NAOH[0], y0=TANGKI_NAOH[1], x1=TANGKI_NAOH[2], y1=TANGKI_NAOH[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
            )

        # 3. Penanda panah animasi segitiga kuning
        fig.add_scatter(
            x=[current['x']], y=[current['y']],
            mode="markers+text",
            marker=dict(size=35, color="yellow", symbol="triangle-right", line=dict(width=3, color="orange")),
            text=[current['label']],
            textposition="bottom center",
            textfont=dict(size=18, color="darkred", family="Arial Black")
        )
        
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=700,
            hovermode="closest"
        )
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={'displayModeBar': False}, 
                key=f"plotly_render_{render_count}"
            )
        
        render_count += 1
        time.sleep(1.8)
