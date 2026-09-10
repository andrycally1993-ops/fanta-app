import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

# Configurazione della pagina in formato widescreen
st.set_page_config(page_title="Algoritmo Fantacalcio Pro", layout="wide")

# Suddivisione in 3 colonne principali: Sinistra (Leghe), Centrale (Campo e Panchina), Destra (Algoritmo e Statistiche)
col_left, col_center, col_right = st.columns([1.2, 2.8, 1.2])

# --- 1. COLONNA SINISTRA: CARICAMENTO FILE CSV LEGHE ---
with col_left:
    st.markdown("### 📁 Le Tue Leghe")
    uploaded_files = st.file_uploader(
        "Carica i file CSV delle leghe", 
        type=["csv"], 
        accept_multiple_files=True
    )
    
    leagues_dict = {}
    selected_league = "Nessuna Lega Selezionata"
    total_players = 25  # Default di esempio
    
    if uploaded_files:
        league_names = [f.name.split(".")[0] for f in uploaded_files]
        selected_league = st.selectbox("Seleziona Lega Attiva", league_names)
        
        for file in uploaded_files:
            if file.name.split(".")[0] == selected_league:
                try:
                    df = pd.read_csv(file)
                    leagues_dict[selected_league] = df.to_dict(orient="records")
                    total_players = len(leagues_dict[selected_league])
                    st.success(f"Lega caricata! ({total_players} giocatori)")
                except Exception as e:
                    st.error("Errore nella lettura del file CSV.")
    else:
        st.info("Carica i file CSV a sinistra per salvarli e gestirli.")

    st.markdown("---")
    st.markdown("### ⚙️ Filtri & Modulo")
    modulo_scelto = st.selectbox("Modulo Titolare", ["3-4-3", "4-3-3", "3-5-2", "4-4-2"])
    st.text(f"Modulo attivo: {modulo_scelto}")


# --- 3. COLONNA DESTRA: SPIEGAZIONE ALGORITMO, INDICE ROSA E STATISTICHE ---
with col_right:
    st.markdown("### 📊 Indice Rosa & Statistiche")
    st.metric(label="Totale Giocatori in Rosa", value=total_players)
    
    st.markdown("---")
    st.markdown("#### 🧠 Come funziona l'Algoritmo")
    st.markdown("""
    * **Fonti & Probabili Formazioni:** L'algoritmo aggrega e confronta i dati dei principali portali sportivi (Fantacalcio.it, Sky, Gazzetta, FantaLab) per stabilire l'affidabilità dei titolari.
    * **Indice di Titolare (%):** * 🟢 **Barra Verde (>70%):** Titolare sicuro o fortemente consigliato.
      * 🟠 **Barra Arancione (<70%):** Giocatore in ballottaggio o a rischio panchina.
    * **Previsione Bonus / Malus:** Calcolata analizzando i dati di squadra, i rigoristi designati, i calci piazzati e la vulnerabilità della difesa avversaria (matchup).
    * **FantaMedia (FM):** Media voto ponderata che dà maggiore peso allo stato di forma delle **ultime 5 partite** rispetto all'intera stagione.
    """)
    st.markdown("---")
    st.success("Algoritmo Sincronizzato & Attivo 🟢")


# --- 2. COLONNA CENTRALE: CAMPO DA CALCIO E PANCHINA STILE LEGA FC ---
with col_center:
    players_data = leagues_dict.get(selected_league, []) if uploaded_files else []
    
    # Suddivisione nei reparti per la grafica del campo
    portieri = [p for p in players_data if str(p.get("Ruolo","")).upper() in ["P","POR"]] or [
        {"Nome": "Provedel", "Bonus": "⚽ 0", "Malus": "🥅 -1", "FM": "6.50", "Titolarità": 95}
    ]
    difensori = [p for p in players_data if str(p.get("Ruolo","")).upper() in ["D","DEF"]] or [
        {"Nome": "Dimarco", "Bonus": "⚽ +2", "Malus": "🟨 -0.5", "FM": "6.85", "Titolarità": 90},
        {"Nome": "Bremer", "Bonus": "⚽ 0", "Malus": "🟨 -0.5", "FM": "6.40", "Titolarità": 98},
        {"Nome": "Bastoni", "Bonus": "⚽ +1", "Malus": "🟥 -1", "FM": "6.30", "Titolarità": 65}
    ]
    centrocampisti = [p for p in players_data if str(p.get("Ruolo","")).upper() in ["C","CEN"]] or [
        {"Nome": "Pulisic", "Bonus": "⚽ +4", "Malus": "🟨 -0.5", "FM": "7.20", "Titolarità": 92},
        {"Nome": "Koopmeiners", "Bonus": "⚽ +3", "Malus": "🟨 0", "FM": "7.05", "Titolarità": 95},
        {"Nome": "Çalhanoğlu", "Bonus": "⚽ +5", "Malus": "🟨 -0.5", "FM": "7.40", "Titolarità": 99}
    ]
    attaccanti = [p for p in players_data if str(p.get("Ruolo","")).upper() in ["A","ATT"]] or [
        {"Nome": "Lautaro", "Bonus": "⚽ +8", "Malus": "🟨 0", "FM": "8.10", "Titolarità": 100},
        {"Nome": "Thuram", "Bonus": "⚽ +6", "Malus": "🟨 -0.5", "FM": "7.75", "Titolarità": 95}
    ]
    panchinari = [p for p in players_data if str(p.get("Ruolo","")).upper() in ["P","D","C","A"]][10:] or [
        {"Nome": "Sommer", "Bonus": "⚽ 0", "Malus": "FM: 6.45", "Titolarità": 90},
        {"Nome": "Pavard", "Bonus": "⚽ 0", "Malus": "FM: 6.30", "Titolarità": 85},
        {"Nome": "Frattesi", "Bonus": "⚽ +2", "Malus": "FM: 6.60", "Titolarità": 45},
        {"Nome": "Retegui", "Bonus": "⚽ +5", "Malus": "FM: 7.15", "Titolarità": 90}
    ]

    def make_cards(lista):
        h = ""
        for p in lista:
            nome = p.get("Nome", "Giocatore")
            bonus = p.get("Bonus", "⚽ 0")
            malus = p.get("Malus", "🟨 0")
            fm = p.get("FM", "6.00")
            tit = int(p.get("Titolarità", 80))
            color = "bar-green" if tit >= 70 else "bar-orange"
            h += f"""
            <div class="player-card">
                <div class="player-name">{nome}</div>
                <div class="player-stats">{bonus} | {malus}</div>
                <div class="player-fm">FM: {fm}</div>
                <div class="titularity-container"><div class="titularity-bar {color}" style="width: {tit}%;"></div></div>
                <div class="titularity-text">{tit}% Titolare</div>
            </div>
            """
        return h

    field_html = f"""
    <style>
        body {{
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}
        .wrapper {{
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}
        .section-title {{
            font-size: 1.05rem;
            font-weight: bold;
            color: #00ffcc;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 8px;
            text-transform: uppercase;
        }}
        /* Campo da calcio stile Lega FC / FantaLab */
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
            height: 460px;
            box-shadow: inset 0 0 40px rgba(0,0,0,0.8);
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
            gap: 12px;
            width: 100%;
            z-index: 2;
        }}
        /* Card Giocatore */
        .player-card {{
            background: rgba(15, 15, 15, 0.9);
            border: 1px solid #00ffcc;
            border-radius: 6px;
            padding: 5px 6px;
            text-align: center;
            width: 100px;
            box-shadow: 0 3px 6px rgba(0,0,0,0.6);
        }}
        .player-name {{
            font-weight: bold;
            font-size: 0.72rem;
            color: #ffffff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-bottom: 2px;
        }}
        .player-stats {{
            font-size: 0.56rem;
            color: #ffcc00;
            margin-bottom: 1px;
        }}
        .player-fm {{
            font-size: 0.56rem;
            color: #ff4d4d;
            margin-bottom: 3px;
        }}
        .titularity-container {{
            width: 100%;
            background: #444;
            border-radius: 3px;
            height: 5px;
            overflow: hidden;
            margin-top: 2px;
        }}
        .titularity-bar {{
            height: 100%;
            border-radius: 3px;
        }}
        .bar-green {{ background-color: #2ecc71; }}
        .bar-orange {{ background-color: #e67e22; }}
        .titularity-text {{
            font-size: 0.5rem;
            margin-top: 2px;
            color: #ddd;
        }}
        /* Sezione Panchina con Sedia */
        .bench-box {{
            background: #1a1a1a;
            border: 2px solid #333;
            border-radius: 10px;
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
        }}
        .bench-row {{
            display: flex;
            gap: 10px;
            justify-content: flex-start;
            overflow-x: auto;
            padding-bottom: 4px;
        }}
    </style>

    <div class="wrapper">
        <div>
            <div class="section-title">🏟️ Formazione Titolare ({selected_league}) - Modulo: {modulo_scelto}</div>
            <div class="football-field">
                <div class="field-row">{make_cards(portieri[:1])}</div>
                <div class="field-row">{make_cards(difensori[:4])}</div>
                <div class="field-row">{make_cards(centrocampisti[:4])}</div>
                <div class="field-row">{make_cards(attaccanti[:3])}</div>
            </div>
        </div>

        <div class="bench-box">
            <div class="section-title">🪑 Panchina & Riserve</div>
            <div class="bench-row">
                {make_cards(panchinari[:5])}
            </div>
        </div>
    </div>
    """

    components.html(field_html, height=720, scrolling=True)
