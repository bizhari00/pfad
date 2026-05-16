import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from PIL import Image
import os

# Inisialisasi
app = dash.Dash(__name__)
server = app.server  # Penting untuk Forio/Cloud hosting

# Memuat Background - Gunakan path yang relatif agar aman di server
img_path = os.path.join(os.getcwd(), "rivaldi.png")
img = Image.open(img_path)

# ... (Isi flow_path tetap sama seperti kode Anda) ...

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

# Callback tetap sama
@app.callback(
    Output('flow-graph', 'figure'),
    Input('flow-interval', 'n_intervals')
)
def update_flow(n):
    # ... (Logika update_flow Anda) ...
    return fig

if __name__ == '__main__':
    # Saat running di lokal
    app.run(debug=True, use_reloader=False)
