import streamlit as st
import plotly.express as px
from PIL import Image
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="PFAD Produksi Biodiesel - Mode Live",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Pengaturan padding halaman utama agar aman di Forio 80%
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.0rem !important; 
        padding-bottom: 1.5rem !important;
        padding-left: 2.0rem !important;
        padding-right: 2.0rem !important;
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================================================================
# 2. STRATEGI TURUNKAN LAYOUT 
# ==============================================================================
st.markdown("<br><br>", unsafe_allow_html=True)

# ==============================================================================
# 3. NAVIGASI & JUDUL SEBARIS (Balanced Design Button & Title)
# ==============================================================================
st.markdown(
    """
    <style>
    /* 1. Mengatur Ukuran & Corak Kotak Tombol Navigasi */
    .stLinkButton > a {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%) !important; /* Gradasi biru premium */
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important; 
        padding: 8px 20px !important; 
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25) !important;
        transition: all 0.3s ease-in-out !important;
        text-decoration: none !important;
        
        /* KUNCI KESEIMBANGAN: Lebar otomatis dan tidak melar penuh */
        display: inline-flex !important;
        width: auto !important;
        max-width: 320px !important; 
    }

    /* 2. Menyesuaikan Ukuran Font di Dalam Tombol */
    .stLinkButton > a p {
        font-size: 16px !important; 
        font-weight: bold !important;
        color: #FFFFFF !important;
        letter-spacing: 0.5px !important;
    }

    /* 3. Efek Hover Interaktif */
    .stLinkButton > a:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* 4. Mengatur Teks Judul Diagram Agar Selaras Sebaris */
    .custom-title {
        font-size: 20px !important; 
        font-weight: 500 !important;
        color: #1E293B;
        margin-top: 8px; 
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Pembagian kolom rasio agar seimbang dan sejajar lurus
col_btn, col_title = st.columns([1.2, 2.8])

with col_btn:
    st.link_button("🏠 Kembali ke Menu Utama", "https://forio.com/app/univ_sumaterautara/research-ptpn", use_container_width=False)

with col_title:
    st.markdown('<p class="custom-title">PFAD Biodiesel</p>', unsafe_allow_html=True)

st.divider()

# ==============================================================================
# 4. MEMUAT BACKGROUND IMAGE
# ==============================================================================
try:
    img = Image.open("rivaldi.png")
except FileNotFoundError:
    st.error("File 'rivaldi.png' tidak ditemukan. Pastikan file gambar ada di root repository GitHub Anda.")
    st.stop()

# ==============================================================================
# 5. KORDINAT AKURAT BERDASARKAN GRID ASLI (x0, y0, x1, y1)
# ==============================================================================
KOTAK_METANOL = [40, 80, 100, 210]
KOTAK_H2SO4   = [40, 240, 100, 370]
KOTAK_NAOH    = [370, 40, 420, 140]

y_arrow = 550 

flow_path = [
    {
        'step_id': 'feedstock_prep',
        'x': 90, 'y': y_arrow, 'label': 'Persiapan Bahan Awal',
        'multiple_areas': [
            KOTAK_METANOL,
            KOTAK_H2SO4,
            [40, 400, 100, 520]
        ]
    },
    {
        'step_id': 'reaktor1',
        'x': 320, 'y': y_arrow, 'label': 'Reaktor 1 Aktif (Esterifikasi)', 
        'tank_area': [295, 400, 360, 510]
    },
    {
        'step_id': 'separator1',
        'x': 420, 'y': y_arrow, 'label': 'Separator 1 Aktif', 
        'tank_area': [430, 400, 500, 500]
    },
    {
        'step_id': 'reaktor2',
        'x': 630, 'y': y_arrow, 'label': 'Reaktor 2 Aktif (TransEsterifikasi)', 
        'tank_area': [600, 400, 660, 500]
    },
    {
        'step_id': 'separator2',
        'x': 745, 'y': y_arrow, 'label': 'Separator 2 Aktif', 
        'tank_area': [770, 410, 820, 500]
    },
    {
        'step_id': 'washdrum',
        'x': 920, 'y': y_arrow, 'label': 'Wash Drum Aktif', 
        'tank_area': [890, 400, 950, 500]
    },
    {
        'step_id': 'evaporator',
        'x': 1025, 'y': y_arrow, 'label': 'Evaporator Aktif', 
        'tank_area': [980, 410, 1050, 500]
    },
    {
        'step_id': 'biodiesel',
        'x': 1200, 'y': y_arrow, 'label': 'Produk Biodiesel', 
        'tank_area': [1150, 400, 1250, 530]
    }
]

# ==============================================================================
# 6. LOGIKA ANIMASI JALUR PROSES DENGAN KOTAK PRESISI
# ==============================================================================
placeholder = st.empty()
render_count = 0

while True:
    for step in range(len(flow_path)):
        current = flow_path[step]
        fig = px.imshow(img)
        
        fig.update_xaxes(visible=False, showgrid=False)
        fig.update_yaxes(visible=False, showgrid=False)
        
        # 1. LOGIKA PEWARNAAN KOTAK HIJAU TRANSPARAN UTAMA
        if 'multiple_areas' in current:
            for area in current['multiple_areas']:
                fig.add_shape(
                    type="rect", x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                    fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2),
                )
        else:
            area = current['tank_area']
            fig.add_shape(
                type="rect", x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2),
            )
            
        # 2. LOGIKA KONDISIONAL TANGKI PROSES TAMBAHAN (ATAS)
        if current['step_id'] == 'reaktor1':
            for area in [KOTAK_METANOL, KOTAK_H2SO4]:
                fig.add_shape(
                    type="rect", x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                    fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
                )
        elif current['step_id'] == 'reaktor2':
            # KUNCI PERUBAHAN: Loop ditambahkan agar KOTAK_NAOH dan KOTAK_METANOL aktif bersamaan
            for area in [KOTAK_NAOH, KOTAK_METANOL]:
                fig.add_shape(
                    type="rect", x0=area[0], y0=area[1], x1=area[2], y1=area[3],
                    fillcolor="rgba(0, 255, 0, 0.4)", line=dict(color="LimeGreen", width=2)
                )

        # 3. PENANDA PANAH SEGITIGA KUNING ANIMASI
        fig.add_scatter(
            x=[current['x']], y=[current['y']], mode="markers+text",
            marker=dict(size=35, color="yellow", symbol="triangle-right", line=dict(width=3, color="orange")),
            text=[current['label']], textposition="bottom center",
            textfont=dict(size=21, color="darkred", family="Arial Black")
        )
        
        fig.update_layout(
            margin=dict(l=0, r=0, t=15, b=0), 
            height=680,
            autosize=True,
            showlegend=False
        )
        
        with placeholder.container():
            st.plotly_chart(
                fig, 
                use_container_width=True, 
                config={'displayModeBar': False, 'responsive': True}, 
                key=f"plotly_render_{render_count}"
            )
        
        render_count += 1
        time.sleep(1.8)
