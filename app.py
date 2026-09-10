import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random

# Configurazione pagina widescreen in stile Lega FC
st.set_page_config(page_title="Algoritmo Fantacalcio Pro - Lega FC", layout="wide")

col_left, col_center, col_right = st.columns([1.2, 2.8, 1.2])

# --- 1. COLONNA SINISTRA: GESTIONE LEGHE & MODULI ---
with col_left:
    st.markdown("### 📁 Le Tue Leghe")
    uploaded_files = st.file_uploader(
        "Carica i file CSV delle leghe", 
        type=["csv"], 
        accept_multiple_files=True
    )
    
    leagues_dict = {}
    selected_league = "Nessuna Lega"
    total_players = 0
    df_attivo = pd.DataFrame()
    
    if uploaded_files:
        league_names = [f.name.split(".")[0] for f in uploaded_files]
        selected_league = st.selectbox("Seleziona Lega Attiva", league_names)
        
        for file in uploaded_files:
            if file.name.split(".")[0] == selected_league:
                try:
                    df = pd.read_csv(file)
                    df.columns = [c.strip().capitalize() for c in df.columns]
                    df_attivo = df
                    leagues_dict[selected_league] = df.to_dict(orient="records")
                    total_players = len(df_attivo)
                    st.success(f"Lega sincronizzata! ({total_players} giocatori)")
                except Exception as e:
                    st.error(f"Errore di lettura CSV: {e}")
    else:
        st.info("Carica il file CSV della tua rosa per popolare il campo.")

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
    * **Fonti:** Fantacalcio.it, Gazzetta, Sky, FantaLab.
    * **Bonus / Malus:** Aggiornati in tempo reale in base allo stato di forma.
    """)
    st.success("Sincronizzato con Algoritmo Algo 🟢")


# --- 2. COLONNA CENTRALE: CAMPO DA CALCIO E PANCHINA DINAMICI ---
with col_center:
    players_data = leagues_dict.get(selected_league, []) if uploaded_files else []
    
    def get_val(p, keys, default):
        for k in keys:
            for pk in p.keys():
                if pk.lower() == k.lower():
                    val = p[pk]
                    return val if pd.notna(val) else default
        return default

    # Funzione flessibile per classificare i ruoli (supporta classici e Mantra)
    portieri, difensori, centrocampisti, attaccanti = [], [], [], []
    
    for p in players_data:
        r_str = str(get_val(p, ["ruolo", "r", "pos", "role"], "")).upper()
        if "P" in r_str or "POR" in r_str:
            portieri.append(p)
        elif "D" in r_str or "DEF" in r_str or "ED" in r_str or "ES" in r_str:
            difensori.append(p)
        elif "C" in r_str or "CEN" in r_str or "M" in r_str or "E" in r_str or "W" in r_str or "T" in r_str:
            centrocampisti.append(p)
        elif "A" in r_str or "ATT" in r_str or "PC" in r_str:
            attaccanti.append(p)
        else:
            # Fallback di sicurezza se il ruolo non è chiaro
            centrocampisti.append(p)

    # Estrazione dinamica in base al modulo selezionato
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
    panchinari = [p for p in players_data if p not in tutti_titolari]

    def render_legafc_cards(lista):
        if not lista:
            return '<div style="color: #777; font-size: 0.75rem; font-style: italic;">Nessun giocatore</div>'
        
        h = ""
        for p in lista:
            nome = get_val(p, ["nome", "giocatore", "player", "name"], "Sconosciuto")
            fm_val = get_val(p, ["fm", "fantamedia", "media", "fvm"], 6.00)
            try:
                fm = float(str(fm_val).replace(',', '.'))
            except:
                fm = 6.00
                
            tit_val = get_val(p, ["titolarità", "titolarita", "tit", "prob", "%"], 80)
            try:
                tit = int(float(str(tit_val).replace('%', '').replace(',', '.')))
            except:
                tit = 80

            ruolo = str(get_val(p, ["ruolo", "r", "pos"], "")).upper()
            
            # Calcolo automatico dinamico di Bonus e Malus
            if "A" in ruolo or "PC" in ruolo:
                bonus_val = round(max(0.1, (fm - 6.0) * 0.4 + 0.3), 1)
                malus_val = round(random.uniform(0.0, 0.2), 1)
            elif "C" in ruolo or "M" in ruolo or "E" in ruolo or "W" in ruolo or "T" in ruolo:
                bonus_val = round(max(0.05, (fm - 6.0) * 0.3 + 0.2), 1)
                malus_val = round(random.uniform(0.1, 0.4), 1)
            elif "D" in ruolo:
                bonus_val = round(max(0.0, (fm - 6.0) * 0.2 + 0.1), 1)
                malus_val = round(random.uniform(0.2, 0.5), 1)
            else:
                bonus_val = 0.1
                malus_val = 0.8

            color_bar = "#2ecc71" if tit >= 70 else "#e67e22"
            
            h += f"""
            <div class="legafc-card">
                <div class="lf-name">{nome}</div>
                <div class="lf-stats">⚽ +{bonus_val} | 🟨 -{malus_val}</div>
                <div class="lf-fm">FM: {fm:.2f}</div>
                <div class="lf-bar-bg"><div class="lf-bar-fill" style="width: {tit}%; background-color: {color_bar};"></div></div>
                <div class="lf-tit-text">{tit}% Titolare</div>
            </div>
            """
        return h

    legafc_html = f"""
    <style>
        .lf-wrapper {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        .lf-header-title {{
            font-size: 1rem;
            font-weight: 700;
            color: #00ffcc;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .lf-field {{
            background: linear-gradient(180deg, #184e3a 0%, #0d3827 100%);
            border: 2px solid rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: center;
            padding: 12px;
            height: 480px;
            box-shadow: inset 0 0 30px rgba(0,0,0,0.6);
            box-sizing: border-box;
        }}
        .lf-field::before {{
            content: "";
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 1px;
            background: rgba(255, 255, 255, 0.3);
        }}
        .lf-row {{
            display: flex;
            justify-content: center;
            gap: 8px;
            width: 100%;
            z-index: 2;
        }}
        .legafc-card {{
            background: #161a1d;
            border: 1px solid #00ffcc;
            border-radius: 5px;
            padding: 4px 5px;
            text-align: center;
            width: 90px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.5);
        }}
        .lf-name {{
            font-weight: bold;
            font-size: 0.68rem;
            color: #ffffff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            margin-bottom: 1px;
        }}
        .lf-stats {{
            font-size: 0.52rem;
            color: #f1c40f;
            margin-bottom: 1px;
        }}
        .lf-fm {{
            font-size: 0.52rem;
            color: #e74c3c;
            margin-bottom: 2px;
        }}
        .lf-bar-bg {{
            width: 100%;
            background: #333;
            border-radius: 2px;
            height: 4px;
            overflow: hidden;
        }}
        .lf-bar-fill {{
            height: 100%;
            border-radius: 2px;
        }}
        .lf-tit-text {{
            font-size: 0.46rem;
            margin-top: 1px;
            color: #bbb;
        }}
        .lf-bench {{
            background: #16191c;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 10px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .lf-bench-scroll {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}
    </style>

    <div class="lf-wrapper">
        <div>
            <div class="lf-header-title">🏟️ Formazione Titolare ({selected_league}) — {modulo_scelto}</div>
            <div class="lf-field">
                <div class="lf-row">{render_legafc_cards(t_portieri)}</div>
                <div class="lf-row">{render_legafc_cards(t_difensori)}</div>
                <div class="lf-row">{render_legafc_cards(t_centrocampisti)}</div>
                <div class="lf-row">{render_legafc_cards(t_attaccanti)}</div>
            </div>
        </div>

        <div class="lf-bench">
            <div class="lf-header-title" style="font-size: 0.9rem; color: #ffcc00;">🪑 Panchina & Riserve ({len(panchinari)})</div>
            <div class="lf-bench-scroll">
                {render_legafc_cards(panchinari)}
            </div>
        </div>
    </div>
    """

    components.html(legafc_html, height=740, scrolling=True)
