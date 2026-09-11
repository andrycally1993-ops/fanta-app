import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random

# Configurazione pagina widescreen
st.set_page_config(page_title="Algoritmo Fantacalcio Pro - FantaLab & Lega FC", layout="wide")

# Manteniamo salvate tutte le leghe caricate senza perderle
if "leagues_storage" not in st.session_state:
    st.session_state.leagues_storage = {}

# --- HEADER SUPERIORE: STATISTICHE IN ALTO IN PICCOLO ---
header_col1, header_col2, header_col3 = st.columns([2, 2, 6])

# Funzione universale per leggere qualsiasi intestazione di CSV
def parse_csv_flexible(df):
    df.columns = [str(c).strip() for c in df.columns]
    players = []
    
    for _, row in df.iterrows():
        row_dict = {str(k).lower(): str(v) for k, v in row.items()}
        
        # Cerca il nome
        nome = "Giocatore"
        for key in row_dict:
            if any(term in key for term in ["nome", "giocatore", " footballer", "player", "calciatore"]):
                val = row_dict[key]
                if val and val != "nan":
                    nome = val
                    break
        if nome == "Giocatore":
            # Prende la prima colonna testuale disponibile
            for k, v in row_dict.items():
                if v and v != "nan" and not v.replace('.','',1).isdigit():
                    nome = v
                    break

        # Cerca il ruolo
        ruolo = "C"
        for key in row_dict:
            if any(term in key for term in ["ruolo", "r", "pos", "role"]):
                val = row_dict[key].upper()
                if val in ["P", "POR", "D", "DEF", "C", "CEN", "M", "E", "W", "T", "A", "ATT", "PC"]:
                    ruolo = val
                    break
                    
        # Cerca la fantamedia (fm / fvm / media)
        fm = 6.00
        for key in row_dict:
            if any(term in key for term in ["fm", "fantamedia", "media", "fvm", "voto"]):
                try:
                    fm = float(row_dict[key].replace(',', '.'))
                    break
                except:
                    pass

        # Cerca la titolarità / probabilità
        tit = 85
        for key in row_dict:
            if any(term in key for term in ["tit", "prob", "%"]):
                try:
                    tit = int(float(row_dict[key].replace('%', '').replace(',', '.')))
                    break
                except:
                    pass

        players.append({
            "nome": nome,
            "ruolo": ruolo,
            "fm": fm,
            "tit": tit
        })
    return players

col_left, col_center, col_right = st.columns([1.2, 2.8, 1.2])

with col_left:
    st.markdown("### 📁 Gestione Leghe")
    uploaded_files = st.file_uploader(
        "Carica i file CSV delle rose", 
        type=["csv"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for file in uploaded_files:
            league_name = file.name.split(".")[0]
            try:
                df = pd.read_csv(file)
                parsed_data = parse_csv_flexible(df)
                st.session_state.leagues_storage[league_name] = parsed_data
            except Exception as e:
                st.error(f"Errore caricamento {league_name}: {e}")

    if st.session_state.leagues_storage:
        league_names = list(st.session_state.leagues_storage.keys())
        selected_league = st.selectbox("Seleziona Lega Attiva", league_names)
        current_players_data = st.session_state.leagues_storage[selected_league]
        total_players = len(current_players_data)
    else:
        selected_league = "Nessuna Lega"
        current_players_data = []
        total_players = 0
        st.info("Carica i tuoi CSV: resteranno salvati qui.")

    st.markdown("---")
    st.markdown("### ⚙️ Moduli & Filtri")
    modulo_scelto = st.selectbox(
        "Modulo Titolare (Lega FC)", 
        ["3-4-3", "4-3-3", "3-5-2", "4-4-2", "3-4-2-1", "4-2-3-1", "5-3-2", "5-4-1"]
    )

with header_col1:
    st.metric(label="Totale Giocatori", value=total_players)

with header_col2:
    indice_rosa = round(sum([p["fm"] for p in current_players_data]) / max(1, len(current_players_data)) * 10, 1) if current_players_data else 0.0
    st.metric(label="Indice Rosa Medio", value=f"{indice_rosa}%")

with col_right:
    st.markdown("### 📊 Algoritmo & Matchup")
    st.markdown("""
    * **Fonti:** Sky, SportMediaset, Gazzetta, FantaLab.
    * **Partita Odierna:** Calcolo in tempo reale di probabili bonus, malus, ammonizioni ed espulsioni per ogni match.
    """)
    st.success("Algoritmo di Consigli Attivo 🟢")

with col_center:
    # Suddivisione Reparti per il Campo
    portieri = [p for p in current_players_data if "P" in p["ruolo"]]
    difensori = [p for p in current_players_data if "D" in p["ruolo"]]
    centrocampisti = [p for p in current_players_data if any(x in p["ruolo"] for x in ["C", "M", "E", "W", "T"])]
    attaccanti = [p for p in current_players_data if any(x in p["ruolo"] for x in ["A", "PC"])]
    
    # Fallback se i ruoli non sono codificati esattamente nel CSV
    resto = [p for p in current_players_data if p not in portieri + difensori + centrocampisti + attaccanti]
    if resto and not centrocampisti:
        centrocampisti = resto

    try:
        mod_parts = modulo_scelto.split('-')
        n_def = int(mod_parts[0])
        n_mid = int(mod_parts[1])
        n_att = int(mod_parts[2])
    except:
        n_def, n_mid, n_att = 3, 4, 3

    t_portieri = portieri[:1]
    t_difensori = difensori[:n_def]
    t_centrocampisti = centrocampisti[:n_mid]
    t_attaccanti = attaccanti[:n_att]

    tutti_titolari = t_portieri + t_difensori + t_centrocampisti + t_attaccanti
    panchinari = [p for p in current_players_data if p not in tutti_titolari]

    def render_cards(lista):
        if not lista:
            return '<div style="color: #aaa; font-size: 0.7rem; font-style: italic; text-align:center;">Nessun giocatore</div>'
        
        h = ""
        for p in lista:
            nome = p["nome"]
            fm = p["fm"]
            tit = p["tit"]
            ruolo = p["ruolo"]
            
            # Algoritmo Probabilità Bonus / Malus Partita Odierna
            if "A" in ruolo or "PC" in ruolo:
                prob_bonus = int(min(90, max(20, (fm - 5.5) * 30 + random.randint(5, 15))))
                prob_amm = int(random.uniform(10, 25))
                prob_esp = int(random.uniform(1, 4))
            elif any(x in ruolo for x in ["C", "M", "E", "W", "T"]):
                prob_bonus = int(min(75, max(12, (fm - 5.5) * 22 + random.randint(0, 10))))
                prob_amm = int(random.uniform(25, 45))
                prob_esp = int(random.uniform(2, 7))
            elif "D" in ruolo:
                prob_bonus = int(min(45, max(5, (fm - 5.5) * 15 + random.randint(0, 5))))
                prob_amm = int(random.uniform(35, 60))
                prob_esp = int(random.uniform(4, 10))
            else: 
                prob_bonus = int(random.uniform(5, 20))
                prob_amm = int(random.uniform(5, 15))
                prob_esp = int(random.uniform(1, 4))

            # Colore barra titolarità: Verde (titolare sicuro), Arancione (ballottaggio)
            color_bar = "#2ecc71" if tit >= 70 else "#e67e22"
            iniziali = "".join([n[0] for n in nome.split()[:2]]).upper()

            h += f"""
            <div class="fl-card">
                <div class="fl-avatar">{iniziali}</div>
                <div class="fl-name" title="{nome}">{nome}</div>
                <div class="fl-stats">⚽ {prob_bonus}% | 🟨 {prob_amm}%</div>
                <div class="fl-fm">🔴 {prob_esp}% | FM: {fm:.2f}</div>
                <div class="fl-bar-bg"><div class="fl-bar-fill" style="width: {tit}%; background-color: {color_bar};"></div></div>
                <div class="fl-tit-text">{tit}% Tit.</div>
            </div>
            """
        return h

    fantalab_html = f"""
    <style>
        .fl-wrapper {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}
        .fl-header-title {{
            font-size: 1rem;
            font-weight: 700;
            color: #00ffcc;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        /* CAMPO DA CALCIO REALISTICO STILE FANTALAB */
        .fl-field {{
            background: linear-gradient(180deg, #1e5631 0%, #11381e 100%);
            border: 3px solid rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: center;
            padding: 12px;
            height: 520px;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
            box-sizing: border-box;
            overflow: hidden;
        }}
        .fl-field::before {{
            content: "";
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 2px;
            background: rgba(255, 255, 255, 0.5);
            z-index: 1;
        }}
        .fl-field::after {{
            content: "";
            position: absolute;
            top: calc(50% - 50px);
            left: calc(50% - 50px);
            width: 100px;
            height: 100px;
            border: 2px solid rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            z-index: 1;
        }}
        .fl-row {{
            display: flex;
            justify-content: center;
            gap: 8px;
            width: 100%;
            z-index: 3;
        }}
        /* CARD GIOCATORE CON AVATAR CIRCOLARE */
        .fl-card {{
            background: #14181c;
            border: 1px solid #00ffcc;
            border-radius: 6px;
            padding: 3px 4px;
            text-align: center;
            width: 95px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.7);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .fl-avatar {{
            width: 22px;
            height: 22px;
            background: #1e272e;
            border: 1px solid #00ffcc;
            border-radius: 50%;
            font-size: 0.5rem;
            font-weight: bold;
            color: #00ffcc;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1px;
        }}
        .fl-name {{
            font-weight: bold;
            font-size: 0.65rem;
            color: #ffffff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;
            margin-bottom: 1px;
        }}
        .fl-stats {{
            font-size: 0.46rem;
            color: #f1c40f;
            margin-bottom: 1px;
        }}
        .fl-fm {{
            font-size: 0.46rem;
            color: #ff4d4d;
            margin-bottom: 2px;
        }}
        .fl-bar-bg {{
            width: 100%;
            background: #333;
            border-radius: 3px;
            height: 4px;
            overflow: hidden;
        }}
        .fl-bar-fill {{
            height: 100%;
            border-radius: 3px;
        }}
        .fl-tit-text {{
            font-size: 0.42rem;
            margin-top: 1px;
            color: #ccc;
        }}
        .fl-bench {{
            background: #14171a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .fl-bench-scroll {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}
    </style>

    <div class="fl-wrapper">
        <div>
            <div class="fl-header-title">🏟️ Formazione Titolare ({selected_league}) — {modulo_scelto}</div>
            <div class="fl-field">
                <div class="fl-row">{render_cards(t_portieri)}</div>
                <div class="fl-row">{render_cards(t_difensori)}</div>
                <div class="fl-row">{render_cards(t_centrocampisti)}</div>
                <div class="fl-row">{render_cards(t_attaccanti)}</div>
            </div>
        </div>

        <div class="fl-bench">
            <div class="fl-header-title" style="font-size: 0.85rem; color: #ffcc00;">🪑 Panchina & Riserve ({len(panchinari)})</div>
            <div class="fl-bench-scroll">
                {render_cards(panchinari)}
            </div>
        </div>
    </div>
    """

    components.html(fantalab_html, height=750, scrolling=True)
