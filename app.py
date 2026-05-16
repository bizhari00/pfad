import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

import os
import sys

# Menambahkan direktori aktif saat ini ke dalam sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Baru setelah itu lakukan import
from streamlit_dash import streamlit_dash


# 1. Inisialisasi Aplikasi Dash
app = dash.Dash(__name__)

# [Opsional] Jika Anda membutuhkan objek server untuk WSGI (tidak masalah dibiarkan)
server = app.server 

# 2. Arsitektur Layout Aplikasi Dash Anda
app.layout = html.Div(
    style={
        'backgroundImage': 'url("/assets/rivaldi.png")', # Pastikan folder & file sesuai di GitHub
        'backgroundSize': 'cover',
        'backgroundPosition': 'center',
        'padding': '20px',
        'color': '#ffffff',
        'fontFamily': 'Arial, sans-serif'
    },
    children=[
        html.H1("Simulasi Model Biodiesel PFAD", style={'textAlign': 'center', 'color': '#f1c40f'}),
        html.P("Analisis kelayakan teknis dan hasil konversi Palm Fatty Acid Distillate.", style={'textAlign': 'center'}),
        
        html.Hr(style={'borderColor': '#f1c40f'}),
        
        # Area Kontrol / Input
        html.Div([
            html.Label("Kapasitas Umpan PFAD (Ton/Tahun):"),
            dcc.Slider(
                id='feedstock-slider',
                min=10000,
                max=200000,
                step=5000,
                value=50000,
                marks={i: f'{i//1000}K' for i in range(10000, 200001, 30000)}
            ),
        ], style={'padding': '20px', 'backgroundColor': 'rgba(0,0,0,0.7)', 'borderRadius': '10px', 'marginBottom': '20px'}),
        
        # Area Output / Hasil
        html.Div([
            html.H3("Hasil Proyeksi Simulasi", style={'color': '#2ecc71'}),
            html.Div(id='simulation-output', style={'fontSize': '18px', 'marginTop': '10px'})
        ], style={'padding': '20px', 'backgroundColor': 'rgba(0,0,0,0.7)', 'borderRadius': '10px'})
    ]
)

# 3. Logika Callback Simulasi (Contoh Rekayasa Proses Makro)
@app.callback(
    Output('simulation-output', 'js_string' if dash.__version__ >= '2.0.0' else 'children'),
    Input('feedstock-slider', 'value')
)
def update_simulation(feedstock_value):
    # Asumsi rasio konversi PFAD ke Biodiesel rata-rata ~ 85% - 90%
    conversion_ratio = 0.88
    biodiesel_yield = feedstock_value * conversion_ratio
    gliserol_co_product = feedstock_value * 0.10
    
    return [
        html.P(f"Total Bahan Baku (PFAD): {feedstock_value:,} Ton/Tahun"),
        html.P(f"Proyeksi Hasil Biodiesel: {biodiesel_yield:,.2f} Ton/Tahun (Rasio: {conversion_ratio*100}%)"),
        html.P(f"Produk Sampingan (Gliserol Crude): {gliserol_co_product:,.2f} Ton/Tahun")
    ]

# ==============================================================================
# Bagian Krusial: Jembatan Penyesuai untuk Server Streamlit Cloud
# ==============================================================================
import streamlit as st
from streamlit_dash import streamlit_dash

# Mengatur agar tampilan halaman Streamlit menggunakan mode melebar (wide)
st.set_page_config(layout="wide", page_title="PFAD Biodiesel Simulation")

# Perintah ini menggantikan jalurnya app.run(debug=True) yang memicu crash kemarin
streamlit_dash(app)
