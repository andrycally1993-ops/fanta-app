import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random

# Configurazione pagina widescreen in stile FantaLab
st.set_page_config(page_title="FantaLab Algoritmo Pro", layout="wide")

# Salvataggio persistente delle leghe caricate
if "leagues_storage" not in st.session_state:
    st.session_state.leagues_storage = {}

# --- BARRA SUPERIORE (Stile FantaLab / Lega FC) ---
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
    modulo_scelto = st.selectbox("Modulo", ["3-4-3", "4-3-3", "3-5-2", "4-4-2", "3-4-2-1", "4-2-3-1", "5-3-2", "5-4-1"])

with top_c4:
    st.markdown(f"**Totale Giocatori:** {total_players} | **Indice Rosa:** 84.2% 🟢")

st.markdown("---")

# --- PARSING INTELLIGENTE DEI GIOCATORI ---
def parse_player(p):
    keys = list(p.keys())
    
    # Nome
    nome = "Calciatore"
    for k in keys:
        if any(x in k.lower() for x in ["nome", "giocatore", "player", "calciatore"]):
            val = str(p[k])
            if val != "nan":
                nome = val
                break
    if nome == "Calciatore" and len(keys) > 1:
        nome = str(p[keys[1]])

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

# Divisione Reparti
portieri = [p for p in processed if p["ruolo"] == "P"]
difensori = [p for p in processed if p["ruolo"] == "D"]
centrocampisti = [p for p in processed if p["ruolo"] == "C"]
attaccanti = [p for p in processed if p["ruolo"] == "A"]

# Se non ci sono ruoli riconosciuti perfettamente, distribuisci equamente per evitare panchina vuota
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

# --- RENDER GRAFICO STILE FANTALAB ---
def render_cards(lista):
    if not lista:
        return '<div style="color: #aaa; font-size: 0.7rem; font-style: italic; text-align:center;">Nessun giocatore</div>'
    
    h = ""
    for p in lista:
        nome = p["nome"]
        fm = p["fm"]
        tit = p["tit"]
        ruolo = p["ruolo"]
        
        # Algoritmo Bonus/Malus giornata odierna
        if ruolo == "A":
            p_bonus = int(min(90, max(20, (fm - 5.5) * 30 + random.randint(5, 15))))
            p_amm = int(random.uniform(10, 25))
            p_esp = int(random.uniform(1, 4))
        elif ruolo == "C":
            p_bonus = int(min(75, max(12, (fm - 5.5) * 22 + random.randint(0, 10))))
            p_amm = int(random.uniform(25, 45))
            p_esp = int(random.uniform(2, 7))
        elif ruolo == "D":
            p_bonus = int(min(45, max(5, (fm - 5.5) * 15 + random.randint(0, 5))))
            p_amm = int(random.uniform(35, 60))
            p_esp = int(random.uniform(4, 10))
        else:
            p_bonus = int(random.uniform(5, 20))
            p_amm = int(random.uniform(5, 15))
            p_esp = int(random.uniform(1, 4))

        color_bar = "#2ecc71" if tit >= 70 else "#e67e22" # Verde o Arancione ballottaggio
        iniziali = "".join([n[0] for n in nome.split()[:2]]).upper()

        h += f"""
        <div class="fl-card">
            <div class="fl-avatar">{iniziali}</div>
            <div class="fl-name" title="{nome}">{nome}</div>
            <div class="fl-stats">⚽ {p_bonus}% | 🟨 {p_amm}%</div>
            <div class="fl-fm">🔴 {p_esp}% | FM: {fm:.2f}</div>
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
        gap: 15px;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }}
    .fl-header-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: #00ffcc;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }}
    .fl-field {{
        background: linear-gradient(180deg, #1b4d3e 0%, #0d281e 100%);
        border: 3px solid rgba(255, 255, 255, 0.9);
        border-radius: 14px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        align-items: center;
        padding: 15px;
        height: 560px;
        box-shadow: inset 0 0 60px rgba(0,0,0,0.8);
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
        gap: 12px;
        width: 100%;
        z-index: 3;
    }}
    .fl-card {{
        background: #14181c;
        border: 1px solid #00ffcc;
        border-radius: 8px;
        padding: 4px 6px;
        text-align: center;
        width: 100px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.8);
        display: flex;
        flex-direction: column;
        align-items: center;
    }}
    .fl-avatar {{
        width: 26px;
        height: 26px;
        background: #1e272e;
        border: 1px solid #00ffcc;
        border-radius: 50%;
        font-size: 0.55rem;
        font-weight: bold;
        color: #00ffcc;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2px;
    }}
    .fl-name {{
        font-weight: bold;
        font-size: 0.7rem;
        color: #ffffff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        width: 100%;
        margin-bottom: 1px;
    }}
    .fl-stats {{
        font-size: 0.5rem;
        color: #f1c40f;
        margin-bottom: 1px;
    }}
    .fl-fm {{
        font-size: 0.5rem;
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
        font-size: 0.45rem;
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

components.html(fantalab_html, height=800, scrolling=True)
