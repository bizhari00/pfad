import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from PIL import Image

app = dash.Dash(__name__)
server = app.server
app = dash.Dash(__name__)


# 1. Memuat Background
img = Image.open("rivaldi.png")

# 2. Definisi Jalur Aliran & Area Blok (Bounding Box)
# tank_area berisi koordinat [x0, y0, x1, y1] untuk membuat kotak warna
y_flow = 850 
flow_path = [
    {
        'x': 100, 'y': y_flow, 'label': 'Persiapan Bahan', 
        'tank_area': [50, 150, 150, 350] # Area tangki awal
    },
    {
        'x': 285, 'y': y_flow, 'label': 'Reaktor 1 Aktif', 
        'tank_area': [240, 680, 330, 830] # Area Reaktor 1
    },
    {
        'x': 410, 'y': y_flow, 'label': 'Separator 1 Aktif', 
        'tank_area': [370, 680, 450, 830] # Area Separator 1
    },
    {
        'x': 535, 'y': y_flow, 'label': 'Reaktor 2 Aktif', 
        'tank_area': [490, 680, 580, 830] # Area Reaktor 2
    },
    {
        'x': 660, 'y': y_flow, 'label': 'Separator 2 Aktif', 
        'tank_area': [620, 680, 700, 830] # Area Separator 2
    },
    {
        'x': 950, 'y': y_flow, 'label': 'Produk Biodiesel', 
        'tank_area': [900, 680, 1000, 830] # Area Tangki Akhir
    }
]

# 3. Layout Dashboard
app.layout = html.Div(
    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'backgroundColor': '#f4f7f6'}, 
    children=[
        html.H1("Monitoring Produksi Biodiesel", style={'fontFamily': 'Arial'}),
        html.Div([
            dcc.Graph(id='flow-graph', config={'displayModeBar': False}, style={'width': '90vw', 'height': '75vh'}),
        ], style={'padding': '10px', 'backgroundColor': 'white', 'borderRadius': '15px', 'boxShadow': '0px 10px 30px rgba(0,0,0,0.1)'}),
        dcc.Interval(id='flow-interval', interval=1500, n_intervals=0)
    ]
)

# 4. Callback untuk Mengubah Warna Blok & Aliran
@app.callback(
    Output('flow-graph', 'figure'),
    Input('flow-interval', 'n_intervals')
)
def update_flow(n):
    step = n % len(flow_path)
    current = flow_path[step]
    
    fig = px.imshow(img)
    
    # --- EFEK PERUBAHAN WARNA BLOK ---
    # Menambahkan kotak transparan di atas area unit yang aktif
    area = current['tank_area']
    fig.add_shape(
        type="rect",
        x0=area[0], y0=area[1], x1=area[2], y1=area[3],
        fillcolor="rgba(0, 255, 0, 0.4)", # Hijau transparan
        line=dict(color="LimeGreen", width=2),
    )
    
    # --- INDIKATOR ALIRAN ---
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
    fig.update_layout(margin=dict(l=5, r=5, t=5, b=5))
    
    return fig

if __name__ == '__main__':
    # Menambahkan host='0.0.0.0' agar server terbuka untuk jaringan luar
    app.run(debug=True, host='0.0.0.0', port=8050)
