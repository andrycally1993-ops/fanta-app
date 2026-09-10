import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina in modalità widescreen
st.set_page_config(page_title="Gestione Formazione Fanta", layout="wide")

# Layout a due colonne (Sidebar a sinistra, Campo a destra)
col_left, col_right = st.columns([1, 2.5])

with col_left:
    st.markdown("### 📥 Importazione Formazione")
    uploaded_file = st.file_uploader("Carica il file della formazione", type=["txt", "csv", "json"])
    
    if uploaded_file is not None:
        st.success(f"File '{uploaded_file.name}' caricato con successo!")

    st.markdown("---")
    st.markdown("### ⚙️ Opzioni")
    st.info("Il campo si aggiornerà automaticamente dopo l'importazione del file.")

with col_right:
    st.markdown("### ⚽ Campo da Gioco")
    
    # HTML e CSS del campo da calcio con bonus, malus e barre di titolarità
    field_html = """
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }
        .field-container {
            background: linear-gradient(135deg, #1b4d3e 0%, #0d281e 100%);
            border: 3px solid #ffffff;
            border-radius: 12px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: center;
            padding: 20px;
            height: 520px;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.6);
            box-sizing: border-box;
        }
        .field-row {
            display: flex;
            justify-content: center;
            gap: 20px;
            width: 100%;
        }
        .player-card {
            background: rgba(0, 0, 0, 0.85);
            border: 1px solid #00ffcc;
            border-radius: 6px;
            padding: 6px 8px;
            text-align: center;
            width: 115px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
        }
        .player-name {
            font-weight: bold;
            font-size: 0.8rem;
            margin-bottom: 2px;
            color: #ffffff;
        }
        .player-stats {
            font-size: 0.68rem;
            color: #ffcc00;
            margin-bottom: 2px;
            white-space: nowrap;
        }
        .player-malus {
            font-size: 0.68rem;
            color: #ff4d4d;
            margin-bottom: 3px;
        }
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
            font-size: 0.6rem;
            margin-top: 2px;
            color: #ddd;
        }
    </style>

    <div class="field-container">
        <!-- Portiere -->
        <div class="field-row">
            <div class="player-card">
                <div class="player-name">Provedel</div>
                <div class="player-stats">⚽ 0 | 🎯 +1</div>
                <div class="player-malus">🥅 -1 | 🟨 0</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                <div class="titularity-text">95% Titolare</div>
            </div>
        </div>
        
        <!-- Difensori -->
        <div class="field-row">
            <div class="player-card">
                <div class="player-name">Dimarco</div>
                <div class="player-stats">⚽ +2 | 🎯 +3</div>
                <div class="player-malus">🟨 -0.5</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 90%;"></div></div>
                <div class="titularity-text">90% Titolare</div>
            </div>
            <div class="player-card">
                <div class="player-name">Bremer</div>
                <div class="player-stats">⚽ 0 | 🎯 +0</div>
                <div class="player-malus">🟨 -0.5</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 98%;"></div></div>
                <div class="titularity-text">98% Titolare</div>
            </div>
            <div class="player-card">
                <div class="player-name">Bastoni</div>
                <div class="player-stats">⚽ +1 | 🎯 +1</div>
                <div class="player-malus">🟥 -1</div>
                <div class="titularity-container"><div class="titularity-bar bar-orange" style="width: 65%;"></div></div>
                <div class="titularity-text">65% In dubbio</div>
            </div>
        </div>
        
        <!-- Centrocampisti -->
        <div class="field-row">
            <div class="player-card">
                <div class="player-name">Pulisic</div>
                <div class="player-stats">⚽ +4 | 🎯 +3</div>
                <div class="player-malus">🟨 -0.5</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 92%;"></div></div>
                <div class="titularity-text">92% Titolare</div>
            </div>
            <div class="player-card">
                <div class="player-name">Koopmeiners</div>
                <div class="player-stats">⚽ +3 | 🎯 +2</div>
                <div class="player-malus">🟨 0</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                <div class="titularity-text">95% Titolare</div>
            </div>
            <div class="player-card">
                <div class="player-name">Çalhanoğlu</div>
                <div class="player-stats">⚽ +5 | 🎯 +4</div>
                <div class="player-malus">🟨 -0.5</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 99%;"></div></div>
                <div class="titularity-text">99% Titolare</div>
            </div>
        </div>
        
        <!-- Attaccanti -->
        <div class="field-row">
            <div class="player-card">
                <div class="player-name">Lautaro</div>
                <div class="player-stats">⚽ +8 | 🎯 +2</div>
                <div class="player-malus">🟨 0</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 100%;"></div></div>
                <div class="titularity-text">100% Titolare</div>
            </div>
            <div class="player-card">
                <div class="player-name">Thuram</div>
                <div class="player-stats">⚽ +6 | 🎯 +5</div>
                <div class="player-malus">🟨 -0.5</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                <div class="titularity-text">95% Titolare</div>
            </div>
        </div>
    </div>
    """
    
    # Renderizza il campo in modo pulito senza mostrare codice grezzo
    components.html(field_html, height=560)
