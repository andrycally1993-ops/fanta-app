import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Configurazione della pagina
st.set_page_config(page_title="Algoritmo Fantacalcio Pro", layout="wide")

# Barra laterale per gestione leghe e upload file CSV
st.sidebar.markdown("## ⚙️ Gestione Leghe & Formazioni")
uploaded_files = st.sidebar.file_uploader(
    "Carica i file CSV delle tue leghe", 
    type=["csv"], 
    accept_multiple_files=True
)

players_list = []
selected_league = "Nessuna Lega"

if uploaded_files:
    league_names = [f.name.split(".")[0] for f in uploaded_files]
    selected_league = st.sidebar.selectbox("Seleziona Lega Attiva", league_names)
    
    # Trova il file corrispondente alla lega selezionata
    for file in uploaded_files:
        if file.name.split(".")[0] == selected_league:
            try:
                # Legge il CSV caricato
                df = pd.read_csv(file)
                # Converte le righe del CSV in una lista di dizionari per l'app
                players_list = df.to_dict(orient="records")
                st.sidebar.success(f"Lega '{selected_league}' caricata ({len(players_list)} giocatori)!")
            except Exception as e:
                st.sidebar.error(f- "Errore di lettura CSV: {e}")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Indice Rosa & Statistiche")
st.sidebar.text(f"Giocatori in Rosa: {len(players_list)}")

# Se non ci sono giocatori caricati, mettiamo dei dati di fallback o un avviso
if not players_list:
    st.warning("⚠️ Carica il file CSV della tua formazione nella barra a sinistra per visualizzare i tuoi giocatori reali sul campo!")
    # Dati di esempio minimi se il file non è ancora caricato
    players_list = [
        {"Nome": "Carica il tuo CSV", "Ruolo": "P", "Titolarità": 0, "FM": 0, "Bonus": "", "Malus": ""}
    ]

# Generiamo l'HTML dinamico basato sui dati reali (o mostra un messaggio)
players_html = ""
for p in players_list:
    nome = p.get("Nome", "Sconosciuto")
    ruolo = p.get("Ruolo", "C")
    titolarita = int(p.get("Titolarità", 80))
    fm = p.get("FM", 6.0)
    bonus = p.get("Bonus", "⚽ 0")
    malus = p.get("Malus", "🟨 0")
    
    bar_color = "bar-green" if titolarita >= 70 else "bar-orange"
    
    players_html += f"""
    <div class="player-card">
        <div class="player-name">{nome} ({ruolo})</div>
        <div class="player-stats">{bonus}</div>
        <div class="player-malus">{malus} | FM: {fm}</div>
        <div class="titularity-container"><div class="titularity-bar {bar_color}" style="width: {titolarita}%;"></div></div>
        <div class="titularity-text">{titolarita}% Titolare</div>
    </div>
    """

# HTML e CSS completo della grafica FantaLab / Leghe FC / Argo
app_html = f"""
<style>
    body {{
        background-color: #121212;
        color: #ffffff;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }}
    .main-wrapper {{
        display: flex;
        flex-direction: column;
        gap: 20px;
    }}
    .section-header {{
        font-size: 1.15rem;
        font-weight: bold;
        color: #00ffcc;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    /* Campo da calcio realistico */
    .football-field {{
        background: linear-gradient(135deg, #1b4d3e 0%, #0d281e 100%);
        border: 3px solid #ffffff;
        border-radius: 12px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        padding: 15px;
        height: 450px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
        box-sizing: border-box;
    }}
    .football-field::before {{
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(255, 255, 255, 0.4);
    }}
    .field-row {{
        display: flex;
        justify-content: center;
        gap: 15px;
        width: 100%;
        z-index: 2;
        flex-wrap: wrap;
    }}
    /* Card del Giocatore */
    .player-card {{
        background: rgba(15, 15, 15, 0.88);
        border: 1px solid #00ffcc;
        border-radius: 6px;
        padding: 6px 8px;
        text-align: center;
        width: 110px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.6);
    }}
    .player-name {{
        font-weight: bold;
        font-size: 0.75rem;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 2px;
    }}
    .player-stats {{
        font-size: 0.62rem;
        color: #ffcc00;
        margin-bottom: 2px;
    }}
    .player-malus {{
        font-size: 0.62rem;
        color: #ff4d4d;
        margin-bottom: 3px;
    }}
    .titularity-container {{
        width: 100%;
        background: #444;
        border-radius: 3px;
        height: 5px;
        overflow: hidden;
        margin-top: 3px;
    }}
    .titularity-bar {{
        height: 100%;
        border-radius: 3px;
    }}
    .bar-green {{ background-color: #2ecc71; }}
    .bar-orange {{ background-color: #e67e22; }}
    .titularity-text {{
        font-size: 0.58rem;
        margin-top: 2px;
        color: #ddd;
    }}
    /* Sezione Panchina */
    .bench-section {{
        background: #1a1a1a;
        border: 2px solid #333;
        border-radius: 10px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }}
    .bench-row {{
        display: flex;
        gap: 15px;
        justify-content: flex-start;
        overflow-x: auto;
        padding-bottom: 5px;
    }}
</style>

<div class="main-wrapper">
    <!-- Sezione Stadio / Campo Titolare -->
    <div>
        <div class="section-header">🏟️ Stadio - Formazione Titolare ({selected_league})</div>
        <div class="football-field">
            <div class="field-row">
                {players_html}
            </div>
        </div>
    </div>

    <!-- Sezione Panchina -->
    <div class="bench-section">
        <div class="section-header">🪑 Panchina & Riserve</div>
        <div class="bench-row">
            <!-- I giocatori della panchina caricati dal file verranno mostrati qui -->
            <div class="player-card">
                <div class="player-name">In attesa CSV</div>
                <div class="player-stats">⚽ 0</div>
                <div class="player-malus">FM: 0.0</div>
                <div class="titularity-container"><div class="titularity-bar bar-orange" style="width: 50%;"></div></div>
                <div class="titularity-text">50%</div>
            </div>
        </div>
    </div>
</div>
"""

components.html(app_html, height=750, scrolling=True)
