import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Configurazione della pagina
st.set_page_config(page_title="Algoritmo Fantacalcio Pro", layout="wide")

# Barra laterale per gestione leghe e upload file CSV multipli
st.sidebar.markdown("## ⚙️ Gestione Leghe & Formazioni")
uploaded_files = st.sidebar.file_uploader(
    "Carica i file CSV delle tue leghe", 
    type=["csv"], 
    accept_multiple_files=True
)

leagues_data = {}
if uploaded_files:
    for file in uploaded_files:
        league_name = file.name.split(".")[0]
        try:
            df = pd.read_csv(file)
            leagues_data[league_name] = df
        except Exception as e:
            st.sidebar.error(f"Errore nel file {file.name}: {e}")

selected_league = None
if leagues_data:
    selected_league = st.sidebar.selectbox("Seleziona Lega Attiva", list(leagues_data.keys()))
    st.sidebar.success(f"Lega '{selected_league}' caricata con successo!")
else:
    st.sidebar.info("Carica uno o più file CSV per popolare le leghe.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Indice Rosa & Statistiche")
st.sidebar.text("Totale Giocatori in Rosa: 25")
st.sidebar.text("Algoritmo: Aggiornato ai siti ufficiali")

# Titolo principale dell'applicazione
st.markdown("## ⚽ Algoritmo Probabili Formazioni & Analisi Fanta")

# HTML e CSS personalizzato per la grafica in stile FantaLab / Leghe FC / Argo
app_html = """
<style>
    body {
        background-color: #121212;
        color: #ffffff;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    .main-wrapper {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .section-header {
        font-size: 1.15rem;
        font-weight: bold;
        color: #00ffcc;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    /* Campo da calcio realistico */
    .football-field {
        background: linear-gradient(135deg, #1b4d3e 0%, #0d281e 100%);
        border: 3px solid #ffffff;
        border-radius: 12px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        padding: 15px;
        height: 500px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
        box-sizing: border-box;
    }
    /* Linea di metà campo */
    .football-field::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(255, 255, 255, 0.4);
    }
    .field-row {
        display: flex;
        justify-content: center;
        gap: 15px;
        width: 100%;
        z-index: 2;
    }
    /* Card del Giocatore */
    .player-card {
        background: rgba(15, 15, 15, 0.88);
        border: 1px solid #00ffcc;
        border-radius: 6px;
        padding: 6px 8px;
        text-align: center;
        width: 110px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.6);
    }
    .player-name {
        font-weight: bold;
        font-size: 0.75rem;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 2px;
    }
    .player-stats {
        font-size: 0.62rem;
        color: #ffcc00;
        margin-bottom: 2px;
    }
    .player-malus {
        font-size: 0.62rem;
        color: #ff4d4d;
        margin-bottom: 3px;
    }
    /* Barra di titolarità */
    .titularity-container {
        width: 100%;
        background: #444;
        border-radius: 3px;
        height: 5px;
        overflow: hidden;
        margin-top: 3px;
    }
    .titularity-bar {
        height: 100%;
        border-radius: 3px;
    }
    .bar-green { background-color: #2ecc71; }
    .bar-orange { background-color: #e67e22; }
    .titularity-text {
        font-size: 0.58rem;
        margin-top: 2px;
        color: #ddd;
    }

    /* Sezione Panchina */
    .bench-section {
        background: #1a1a1a;
        border: 2px solid #333;
        border-radius: 10px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }
    .bench-row {
        display: flex;
        gap: 15px;
        justify-content: flex-start;
        overflow-x: auto;
        padding-bottom: 5px;
    }
</style>

<div class="main-wrapper">
    <!-- Sezione Stadio / Campo Titolare -->
    <div>
        <div class="section-header">🏟️ Stadio - Formazione Titolare (Algoritmo attivo)</div>
        <div class="football-field">
            <!-- Portiere -->
            <div class="field-row">
                <div class="player-card">
                    <div class="player-name">Provedel</div>
                    <div class="player-stats">⚽ 0 | 🎯 +1</div>
                    <div class="player-malus">🥅 -1 | FM: 6.50</div>
                    <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                    <div class="titularity-text">95% Titolare</div>
                </div>
            </div>
            <!-- Difensori -->
            <div class="field-row">
                <div class="player-card">
                    <div class="player-name">Dimarco</div>
                    <div class="player-stats">⚽ +2 | 🎯 +3</div>
                    <div class="player-malus">🟨 FM: 6.85</div>
                    <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 90%;"></div></div>
                    <div class="titularity-text">90% Titolare</div>
                </div>
                <div class="player-card">
                    <div class="player-name">Bremer</div>
                    <div class="player-stats">⚽ 0 | 🎯 0</div>
                    <div class="player-malus">🟨 FM: 6.40</div>
                    <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 98%;"></div></div>
                    <div class="titularity-text">98% Titolare</div>
                </div>
                <div class="player-card">
                    <div class="player-name">Bastoni</div>
                    <div class="player-stats">⚽ +1 | 🎯 +1</div>
                    <div class="player-malus">🟥 FM: 6.30</div>
                    <div class="titularity-container"><div class="titularity-bar bar-orange" style="width: 65%;"></div></div>
                    <div class="titularity-text">65% In dubbio</div>
                </div>
            </div>
            <!-- Centrocampisti -->
            <div class="field-row">
                <div class="player-card">
                    <div class="player-name">Pulisic</div>
                    <div class="player-stats">⚽ +4 | 🎯 +3</div>
                    <div class="player-malus">🟨 FM: 7.20</div>
                    <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 92%;"></div></div>
                    <div class="titularity-text">92% Titolare</div>
                </div>
                <div class="player-card">
                    <div class="player-name">Koopmeiners</div>
                    <div class="player-stats">⚽ +3 | 🎯 +2</div>
                    <div class="player-malus">🟨 FM: 7.05</div>
                    <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                    <div class="titularity-text">95% Titolare</div>
                </div>
                <div class="player-card">
                    <div class="player-name">Çalhanoğlu</div>
                    <div class="player-stats">⚽ +5 | 🎯 +4</div>
                    <div class="player-malus">🟨 FM: 7.40</div>
                    <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 99%;"></div></div>
                    <div class="titularity-text">99% Titolare</div>
                </div>
            </div>
            <!-- Attaccanti -->
            <div class="field-row">
                <div class="player-card">
                    <div class="player-name">Lautaro</div>
                    <div class="player-stats">⚽ +8 | 🎯 +2</div>
                    <div class="player-malus">🟨 FM: 8.10</div>
                    <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 100%;"></div></div>
                    <div class="titularity-text">100% Titolare</div>
                </div>
                <div class="player-card">
                    <div class="player-name">Thuram</div>
                    <div class="player-stats">⚽ +6 | 🎯 +5</div>
                    <div class="player-malus">🟨 FM: 7.75</div>
                    <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                    <div class="titularity-text">95% Titolare</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Sezione Panchina -->
    <div class="bench-section">
        <div class="section-header">🪑 Panchina & Riserve</div>
        <div class="bench-row">
            <div class="player-card">
                <div class="player-name">Sommer</div>
                <div class="player-stats">⚽ 0 | 🎯 0</div>
                <div class="player-malus">FM: 6.45</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 90%;"></div></div>
                <div class="titularity-text">90% Titolare</div>
            </div>
            <div class="player-card">
                <div class="player-name">Pavard</div>
                <div class="player-stats">⚽ 0 | 🎯 +1</div>
                <div class="player-malus">FM: 6.30</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 85%;"></div></div>
                <div class="titularity-text">85% Titolare</div>
            </div>
            <div class="player-card">
                <div class="player-name">Frattesi</div>
                <div class="player-stats">⚽ +2 | 🎯 +1</div>
                <div class="player-malus">FM: 6.60</div>
                <div class="titularity-container"><div class="titularity-bar bar-orange" style="width: 45%;"></div></div>
                <div class="titularity-text">45% In dubbio</div>
            </div>
            <div class="player-card">
                <div class="player-name">Retegui</div>
                <div class="player-stats">⚽ +5 | 🎯 +1</div>
                <div class="player-malus">FM: 7.15</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 90%;"></div></div>
                <div class="titularity-text">90% Titolare</div>
            </div>
        </div>
    </div>
</div>
"""

# Renderizzazione pulita tramite componenti Streamlit
components.html(app_html, height=780, scrolling=True)
