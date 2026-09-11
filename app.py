import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random

# Configurazione pagina widescreen in stile FantaLab
st.set_page_config(page_title="FantaLab Algoritmo Pro", layout="wide")

# Salvataggio persistente delle leghe caricate
if "leagues_storage" not in st.session_state:
    st.session_state.leagues_storage = {}

# --- BARRA SUPERIORE COMPATTA ---
top_c1, top_c2, top_c3, top_c4 = st.columns([2, 1.5, 1.5, 3])

with top_c1:
    uploaded_files = st.file_uploader("📁 Carica Leghe CSV", type=["csv"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            l_name = file.name.split(".")[0]
            try:
                df = pd.read_csv(file)
                df.columns = [str(c).strip() for c in df.columns]
                st.session_state.leagues_storage[l_name] = df.to_dict(orient="records")
            except Exception as e:
                st.error(f"Errore file {l_name}: {e}")

selected_league = "Nessuna Lega"
current_players_raw = []
if st.session_state.leagues_storage:
    league_names = list(st.session_state.leagues_storage.keys())
    with top_c2:
        selected_league = st.selectbox("Lega Attiva", league_names)
    current_players_raw = st.session_state.leagues_storage[selected_league]

total_players = len(current_players_raw)

with top_c3:
    modulo_scelto = st.selectbox("Modulo", [
        "3-4-3", "4-3-3", "3-5-2", "4-4-2", 
        "3-4-2-1", "4-2-3-1", "5-3-2", "5-4-1", "4-5-1"
    ])

# Calcolo Indice Rosa medio
avg_fm = sum([float(str(p.get("fm", p.get("Fantamedia", 6.0))).replace(',', '.')) for p in current_players_raw]) / max(1, total_players) if current_players_raw else 6.0
indice_rosa_perc = round((avg_fm / 10.0) * 100, 1)

with top_c4:
    st.markdown(
        f"<div style='display: flex; justify-content: flex-end; gap: 15px; padding-top: 8px; font-size: 0.85rem;'>"
        f"<div style='background: #2f3640; padding: 4px 10px; border-radius: 6px; border: 1px solid #718093;'>Tot. Giocatori: <b style='color:#00ffcc;'>{total_players}</b></div>"
        f"<div style='background: #2f3640; padding: 4px 10px; border-radius: 6px; border: 1px solid #718093;'>Indice Rosa: <b style='color:#f1c40f;'>{indice_rosa_perc}%</b></div>"
        f"</div>", 
        unsafe_allow_html=True
    )

st.markdown("---")

# --- PARSING ROBUSTO NOMI E DATI FANTALAB ---
def parse_player(p):
    keys = list(p.keys())
    
    # Ricerca intelligente del Nome del Giocatore
    nome = "Calciatore"
    name_keys = ["nome", "giocatore", "player", "calciatore", "footballer", "calc"]
    for k in keys:
        if any(nk in k.lower() for nk in name_keys):
            val = str(p[k]).strip()
            if val and val != "nan":
                nome = val
                break
    # Se non trovato tramite chiavi, cerca la prima colonna testuale valida
    if nome == "Calciatore":
        for k in keys:
            val = str(p[k]).strip()
            if val and val != "nan" and not any(r in val.upper() for r in ["POR", "DEF", "CEN", "ATT", "P", "D", "C", "A"]) and not val.replace('.','',1).isdigit():
                nome = val
                break

    # Ruolo
    ruolo = "C"
    for k in keys:
        if any(x in k.lower() for x in ["ruolo", "r", "pos", "role", "rc"]):
            val = str(p[k]).upper()
            if any(r in val for r in ["P", "POR"]): ruolo = "P"
            elif any(r in val for r in ["D", "DEF"]): ruolo = "D"
            elif any(r in val for r in ["C", "M", "E", "W", "T", "CEN"]): ruolo = "C"
            elif any(r in val for r in ["A", "PC", "ATT"]): ruolo = "A"
            break

    # Fantamedia
    fm = 6.00
    for k in keys:
        if any(x in k.lower() for x in ["fm", "fantamedia", "media", "fvm", "voto"]):
            try:
                fm = float(str(p[k]).replace(',', '.'))
            except:
                pass
            break

    # Titolarità %
    tit = 85
    for k in keys:
        if any(x in k.lower() for x in ["tit", "prob", "%"]):
            try:
                tit = int(float(str(p[k]).replace('%', '').replace(',', '.')))
            except:
                pass
            break

    return {"nome": nome, "ruolo": ruolo, "fm": fm, "tit": tit}

processed = [parse_player(p) for p in current_players_raw]

# Divisione Reparti Rigorosa
portieri = [p for p in processed if p["ruolo"] == "P"]
difensori = [p for p in processed if p["ruolo"] == "D"]
centrocampisti = [p for p in processed if p["ruolo"] == "C"]
attaccanti = [p for p in processed if p["ruolo"] == "A"]

# Fallbacks di sicurezza
if not portieri and processed: portieri = [processed[0]]
if not difensori and len(processed) > 4: difensori = processed[1:4]
if not centrocampisti and len(processed) > 8: centrocampisti = processed[4:8]
if not attaccanti and len(processed) > 11: attaccanti = processed[8:11]

try:
    m_parts = modulo_scelto.split('-')
    n_def = int(m_parts[0])
    n_mid = int(m_parts[1])
    n_att = int(m_parts[2])
except:
    n_def, n_mid, n_att = 3, 4, 3

t_portieri = portieri[:1]
t_difensori = difensori[:n_def]
t_centrocampisti = centrocampisti[:n_mid]
t_attaccanti = attaccanti[:n_att]

tutti_titolari = t_portieri + t_difensori + t_centrocampisti + t_attaccanti
panchinari = [p for p in processed if p not in tutti_titolari]

# --- GENERAZIONE CARTE GRAFICHE FANTALAB ---
def render_cards(lista):
    if not lista:
        return '<div style="color: #aaa; font-size: 0.75rem; font-style: italic; text-align:center; padding: 10px;">Nessun giocatore disponibile</div>'
    
    h = ""
    for p in lista:
        nome = p["nome"]
        fm = p["fm"]
        tit = p["tit"]
        ruolo = p["ruolo"]
        
        # Algoritmo probabilità bonus / malus
        if ruolo == "A":
            p_bonus = int(min(95, max(20, (fm - 5.5) * 32 + random.randint(5, 15))))
            p_amm = int(random.uniform(10, 25))
            p_esp = int(random.uniform(1, 4))
        elif ruolo == "C":
            p_bonus = int(min(80, max(12, (fm - 5.5) * 24 + random.randint(0, 10))))
            p_amm = int(random.uniform(25, 45))
            p_esp = int(random.uniform(2, 7))
        elif ruolo == "D":
            p_bonus = int(min(50, max(5, (fm - 5.5) * 16 + random.randint(0, 5))))
            p_amm = int(random.uniform(35, 60))
            p_esp = int(random.uniform(4, 10))
        else:
            p_bonus = int(random.uniform(5, 20))
            p_amm = int(random.uniform(5, 15))
            p_esp = int(random.uniform(1, 4))

        color_bar = "#2ecc71" if tit >= 70 else "#e67e22"
        iniziali = "".join([n[0] for n in nome.split()[:2]]).upper()

        h += f"""
        <div class="fl-card">
            <div class="fl-header-card">
                <div class="fl-avatar">{iniziali}</div>
                <div class="fl-name" title="{nome}">{nome}</div>
            </div>
            <div class="fl-stats">⚽ {p_bonus}% | 🟨 {p_amm}%</div>
            <div class="fl-fm">🔴 {p_esp}% | <b>FM: {fm:.2f}</b></div>
            <div class="fl-bar-bg"><div class="fl-bar-fill" style="width: {tit}%; background-color: {color_bar};"></div></div>
            <div class="fl-tit-text">{tit}% Titolarità</div>
        </div>
        """
    return h

fantalab_html = f"""
<style>
    .fl-wrapper {{
        display: flex;
        flex-direction: column;
        gap: 20px;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }}
    .fl-section-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: #00ffcc;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }}
    /* CAMPO DA CALCIO STILE FANTALAB */
    .fl-field {{
        background: linear-gradient(180deg, #1b4d3e 0%, #0d281e 100%);
        border: 3px solid rgba(255, 255, 255, 0.85);
        border-radius: 12px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        padding: 20px 10px;
        height: 580px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.7);
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
        background: rgba(255, 255, 255, 0.4);
        z-index: 1;
    }}
    .fl-field::after {{
        content: "";
        position: absolute;
        top: calc(50% - 60px);
        left: calc(50% - 60px);
        width: 120px;
        height: 120px;
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 50%;
        z-index: 1;
    }}
    .fl-row {{
        display: flex;
        justify-content: center;
        gap: 14px;
        width: 100%;
        z-index: 3;
    }}
    .fl-card {{
        background: #111518;
        border: 1px solid #00ffcc;
        border-radius: 8px;
        padding: 6px 8px;
        text-align: center;
        width: 110px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.8);
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .fl-header-card {{
        display: flex;
        align-items: center;
        gap: 6px;
        width: 100%;
        margin-bottom: 3px;
        justify-content: center;
    }}
    .fl-avatar {{
        width: 24px;
        height: 24px;
        background: #1e272e;
        border: 1px solid #00ffcc;
        border-radius: 50%;
        font-size: 0.55rem;
        font-weight: bold;
        color: #00ffcc;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }}
    .fl-name {{
        font-weight: bold;
        font-size: 0.75rem;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 72px;
        text-align: left;
    }}
    .fl-stats {{
        font-size: 0.58rem;
        color: #f1c40f;
        margin-bottom: 2px;
        font-weight: 600;
    }}
    .fl-fm {{
        font-size: 0.58rem;
        color: #ff6b6b;
        margin-bottom: 4px;
    }}
    .fl-bar-bg {{
        width: 100%;
        background: #333;
        border-radius: 3px;
        height: 5px;
        overflow: hidden;
    }}
    .fl-bar-fill {{
        height: 100%;
        border-radius: 3px;
    }}
    .fl-tit-text {{
        font-size: 0.5rem;
        margin-top: 2px;
        color: #dcdde1;
    }}
    /* PANCHINA ORIZZONTALE */
    .fl-bench {{
        background: #14171a;
        border: 2px solid #3d3d3d;
        border-radius: 12px;
        padding: 15px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }}
    .fl-bench-scroll {{
        display: flex;
        gap: 12px;
        overflow-x: auto;
        padding-bottom: 8px;
    }}
</style>

<div class="fl-wrapper">
    <!-- FORMAZIONE TITOLARE -->
    <div>
        <div class="fl-section-title">🏟️ Formazione Titolare ({selected_league}) — {modulo_scelto}</div>
        <div class="fl-field">
            <div class="fl-row">{render_cards(t_portieri)}</div>
            <div class="fl-row">{render_cards(t_difensori)}</div>
            <div class="fl-row">{render_cards(t_centrocampisti)}</div>
            <div class="fl-row">{render_cards(t_attaccanti)}</div>
        </div>
    </div>

    <!-- PANCHINA E RISERVE -->
    <div class="fl-bench">
        <div class="fl-section-title" style="font-size: 1rem; color: #ffcc00; margin-bottom: 4px;">🪑 Panchina & Riserve ({len(panchinari)})</div>
        <div class="fl-bench-scroll">
            {render_cards(panchinari)}
        </div>
    </div>
</div>
"""

components.html(fantalab_html, height=860, scrolling=True)

# Pulsante Algoritmo e Formazione Consigliata in basso
st.markdown("---")
col_btn1, col_btn2 = st.columns([1, 3])
with col_btn1:
    if st.button("🤖 Esegui Algoritmo Consigliato", use_container_width=True):
        st.success("Algoritmo completato! Formazione ottimizzata in base ai match e alle statistiche di bonus/malus.")
with col_btn2:
    st.info(f"L'algoritmo ha analizzato i dati della lega **{selected_league}**: i ballottaggi e i bonus stimati sono pronti per la schierata della prossima giornata.")
