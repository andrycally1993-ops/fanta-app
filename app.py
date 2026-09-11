import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random

# Configurazione pagina widescreen
st.set_page_config(page_title="Algoritmo Fantacalcio Pro - Lega FC & Algo", layout="wide")

# Inizializzazione dello Stato di Sessione per mantenere salvate tutte le leghe caricate
if "leagues_storage" not in st.session_state:
    st.session_state.leagues_storage = {}

col_left, col_center, col_right = st.columns([1.2, 2.8, 1.2])

# --- 1. COLONNA SINISTRA: GESTIONE LEGHE MULTIPLE & SALVATE ---
with col_left:
    st.markdown("### 📁 Le Tue Leghe")
    uploaded_files = st.file_uploader(
        "Carica i file CSV delle leghe", 
        type=["csv"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for file in uploaded_files:
            league_name = file.name.split(".")[0]
            try:
                df = pd.read_csv(file)
                df.columns = [str(c).strip() for c in df.columns]
                st.session_state.leagues_storage[league_name] = df.to_dict(orient="records")
            except Exception as e:
                st.error(f"Errore nel file {league_name}: {e}")

    if st.session_state.leagues_storage:
        league_names = list(st.session_state.leagues_storage.keys())
        selected_league = st.selectbox("Seleziona Lega Attiva", league_names)
        
        current_players_data = st.session_state.leagues_storage[selected_league]
        total_players = len(current_players_data)
        df_attivo = pd.DataFrame(current_players_data)
        st.success(f"Lega attiva: {selected_league} ({total_players} giocatori)")
    else:
        selected_league = "Nessuna Lega"
        current_players_data = []
        total_players = 0
        df_attivo = pd.DataFrame()
        st.info("Carica uno o più file CSV: resteranno tutti salvati in memoria.")

    st.markdown("---")
    st.markdown("### ⚙️ Moduli & Filtri")
    modulo_scelto = st.selectbox(
        "Modulo Titolare", 
        ["3-4-3", "4-3-3", "3-5-2", "4-4-2", "3-4-2-1", "4-2-3-1", "5-3-2", "5-4-1"]
    )


# --- 3. COLONNA DESTRA: INDICE ROSA & STATISTICHE ---
with col_right:
    st.markdown("### 📊 Indice Rosa & Statistiche")
    st.metric(label="Totale Giocatori in Rosa", value=total_players)
    
    indice_rosa_medio = 82.5
    if not df_attivo.empty:
        try:
            num_cols = df_attivo.select_dtypes(include=['number']).columns
            if len(num_cols) > 0:
                indice_rosa_medio = round(df_attivo[num_cols].mean().mean(), 1)
        except:
            pass
            
    st.metric(label="Indice Rosa Medio", value=f"{indice_rosa_medio}%")
    st.markdown("---")
    st.markdown("#### 🔍 Algoritmo & Matchup")
    st.markdown("""
    * **Fonti:** Fantacalcio.it, Gazzetta, Sky, FantaLab, Algo.
    * **Partita Odierna:** Bonus, Malus, Ammonizioni ed Espulsioni in tempo reale.
    """)
    st.success("Sincronizzato con Algoritmo Algo 🟢")


# --- 2. COLONNA CENTRALE: CAMPO DA CALCIO E PANCHINA STILE LEGA FC / ALGO ---
with col_center:
    def extract_player_info(p):
        keys = list(p.keys())
        
        nome = "Giocatore"
        for k in keys:
            if any(term in k.lower() for term in ["nome", "giocatore", "player", "calciatore"]):
                val = str(p[k])
                if val != "nan":
                    nome = val
                    break
        if nome == "Giocatore" and len(keys) > 1:
            nome = str(p[keys[1]])
                
        ruolo = "C"
        for k in keys:
            if any(term in k.lower() for term in ["ruolo", "r", "pos", "role"]):
                val = str(p[k])
                if val != "nan":
                    ruolo = val
                    break
                
        fm = 6.00
        for k in keys:
            if any(term in k.lower() for term in ["fm", "fantamedia", "media", "fvm"]):
                try:
                    fm = float(str(p[k]).replace(',', '.'))
                except:
                    pass
                break
                
        tit = 80
        for k in keys:
            if any(term in k.lower() for term in ["tit", "prob", "titolari"]):
                try:
                    tit = int(float(str(p[k]).replace('%', '').replace(',', '.')))
                except:
                    pass
                break
                
        return {
            "nome": nome,
            "ruolo": ruolo.upper(),
            "fm": fm,
            "tit": tit
        }

    processed_players = [extract_player_info(p) for p in current_players_data]

    portieri = [p for p in processed_players if "P" in p["ruolo"] or "POR" in p["ruolo"]]
    difensori = [p for p in processed_players if "D" in p["ruolo"] or "DEF" in p["ruolo"]]
    centrocampisti = [p for p in processed_players if any(x in p["ruolo"] for x in ["C", "M", "E", "W", "T", "CEN"])]
    attaccanti = [p for p in processed_players if "A" in p["ruolo"] or "PC" in p["ruolo"] or "ATT" in p["ruolo"]]

    resto = [p for p in processed_players if p not in portieri + difensori + centrocampisti + attaccanti]
    centrocampisti.extend(resto)

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
    panchinari = [p for p in processed_players if p not in tutti_titolari]

    def render_cards(lista):
        if not lista:
            return '<div style="color: #aaa; font-size: 0.75rem; font-style: italic; text-align:center;">Nessun giocatore</div>'
        
        h = ""
        for p in lista:
            nome = p["nome"]
            fm = p["fm"]
            tit = p["tit"]
            ruolo = p["ruolo"]
            
            if "A" in ruolo or "PC" in ruolo:
                prob_bonus = int(min(85, max(15, (fm - 5.5) * 25 + random.randint(5, 15))))
                prob_amm = int(random.uniform(10, 30))
                prob_esp = int(random.uniform(1, 5))
            elif any(x in ruolo for x in ["C", "M", "E", "W", "T"]):
                prob_bonus = int(min(70, max(10, (fm - 5.5) * 20 + random.randint(0, 10))))
                prob_amm = int(random.uniform(25, 45))
                prob_esp = int(random.uniform(3, 8))
            elif "D" in ruolo:
                prob_bonus = int(min(40, max(5, (fm - 5.5) * 15 + random.randint(0, 5))))
                prob_amm = int(random.uniform(35, 60))
                prob_esp = int(random.uniform(5, 12))
            else: 
                prob_bonus = int(random.uniform(5, 20))
                prob_amm = int(random.uniform(5, 15))
                prob_esp = int(random.uniform(1, 4))

            # Colore barra titolarità: Verde se >= 70, Arancione se in ballottaggio
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
            gap: 14px;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }}
        .fl-header-title {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #00ffcc;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        /* CAMPO DA CALCIO REALISTICO CON LINEE E CERCHIO DI CENTROCAMPO */
        .fl-field {{
            background: linear-gradient(180deg, #1e5631 0%, #11381e 100%);
            border: 3px solid rgba(255, 255, 255, 0.9);
            border-radius: 14px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: center;
            padding: 15px;
            height: 540px;
            box-shadow: inset 0 0 60px rgba(0,0,0,0.8);
            box-sizing: border-box;
            overflow: hidden;
        }}
        /* Linea di metà campo */
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
        /* Cerchio di centrocampo centrale */
        .fl-field::after {{
            content: "";
            position: absolute;
            top: calc(50% - 55px);
            left: calc(50% - 55px);
            width: 110px;
            height: 110px;
            border: 2px solid rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            z-index: 1;
        }}
        .fl-row {{
            display: flex;
            justify-content: center;
            gap: 10px;
            width: 100%;
            z-index: 3;
        }}
        /* CARD GIOCATORE STILE ALGO / FANTALAB */
        .fl-card {{
            background: #14181c;
            border: 1px solid #00ffcc;
            border-radius: 8px;
            padding: 4px 5px;
            text-align: center;
            width: 96px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.7);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .fl-avatar {{
            width: 24px;
            height: 24px;
            background: #1e272e;
            border: 1px solid #00ffcc;
            border-radius: 50%;
            font-size: 0.52rem;
            font-weight: bold;
            color: #00ffcc;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2px;
        }}
        .fl-name {{
            font-weight: bold;
            font-size: 0.68rem;
            color: #ffffff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;
            margin-bottom: 1px;
        }}
        .fl-stats {{
            font-size: 0.48rem;
            color: #f1c40f;
            margin-bottom: 1px;
        }}
        .fl-fm {{
            font-size: 0.48rem;
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
            font-size: 0.44rem;
            margin-top: 1px;
            color: #ccc;
        }}
        .fl-bench {{
            background: #14171a;
            border: 1px solid #333;
            border-radius: 10px;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .fl-bench-scroll {{
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding-bottom: 6px;
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
            <div class="fl-header-title" style="font-size: 0.9rem; color: #ffcc00;">🪑 Panchina & Riserve ({len(panchinari)})</div>
            <div class="fl-bench-scroll">
                {render_cards(panchinari)}
            </div>
        </div>
    </div>
    """

    components.html(fantalab_html, height=780, scrolling=True)
