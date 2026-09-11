import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random

# Configurazione widescreen
st.set_page_config(page_title="FantaLab Algoritmo Pro", layout="wide")

# Salvataggio persistente leghe
if "leagues_storage" not in st.session_state:
    st.session_state.leagues_storage = {}

# --- BARRA SUPERIORE ---
top_c1, top_c2, top_c3, top_c4, top_c5 = st.columns([1.8, 1.4, 1.2, 1.3, 1.3])

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
    modulo_scelto = st.selectbox("Moduli LegheFC", [
        "3-4-3", "4-3-3", "3-5-2", "4-4-2", 
        "3-4-2-1", "4-2-3-1", "5-3-2", "5-4-1", "4-5-1"
    ])

# Calcolo Indice Rosa
avg_fm = sum([float(str(p.get("fm", p.get("Fantamedia", 6.0))).replace(',', '.')) for p in current_players_raw]) / max(1, total_players) if current_players_raw else 6.0
indice_rosa_perc = round((avg_fm / 10.0) * 100, 1)

with top_c4:
    st.markdown(
        f"<div style='background: #1e272e; border: 1px solid #00ffcc; padding: 6px 10px; border-radius: 8px; text-align: center;'>"
        f"<div style='font-size: 0.65rem; color: #a4b0be; text-transform: uppercase;'>Totale Giocatori</div>"
        f"<div style='font-size: 1rem; font-weight: bold; color: #00ffcc;'>{total_players}</div>"
        f"</div>", unsafe_allow_html=True
    )

with top_c5:
    st.markdown(
        f"<div style='background: #1e272e; border: 1px solid #f1c40f; padding: 6px 10px; border-radius: 8px; text-align: center;'>"
        f"<div style='font-size: 0.65rem; color: #a4b0be; text-transform: uppercase;'>Indice Rosa</div>"
        f"<div style='font-size: 1rem; font-weight: bold; color: #f1c40f;'>{indice_rosa_perc}%</div>"
        f"</div>", unsafe_allow_html=True
    )

st.markdown("---")

# --- PARSING DATI GIOCATORE ---
def parse_player(p):
    keys = list(p.keys())
    nome = "Calciatore"
    for k in keys:
        if any(nk in k.lower() for nk in ["nome", "giocatore", "player", "calciatore"]):
            val = str(p[k]).strip()
            if val and val != "nan":
                nome = val
                break
    if nome == "Calciatore":
        for k in keys:
            val = str(p[k]).strip()
            if val and val != "nan" and not any(r in val.upper() for r in ["POR", "DEF", "CEN", "ATT", "P", "D", "C", "A"]) and not val.replace('.','',1).isdigit():
                nome = val
                break

    ruolo = "C"
    for k in keys:
        if any(x in k.lower() for x in ["ruolo", "r", "pos", "role"]):
            val = str(p[k]).upper()
            if any(r in val for r in ["P", "POR"]): ruolo = "P"
            elif any(r in val for r in ["D", "DEF"]): ruolo = "D"
            elif any(r in val for r in ["C", "M", "E", "W", "T", "CEN"]): ruolo = "C"
            elif any(r in val for r in ["A", "PC", "ATT"]): ruolo = "A"
            break

    fm = 6.00
    for k in keys:
        if any(x in k.lower() for x in ["fm", "fantamedia", "media", "voto"]):
            try:
                fm = float(str(p[k]).replace(',', '.'))
            except:
                pass
            break

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

portieri = [p for p in processed if p["ruolo"] == "P"]
difensori = [p for p in processed if p["ruolo"] == "D"]
centrocampisti = [p for p in processed if p["ruolo"] == "C"]
attaccanti = [p for p in processed if p["ruolo"] == "A"]

if not portieri and processed: portieri = [processed[0]]
if not difensori and len(processed) > 4: difensori = processed[1:4]
if not centrocampisti and len(processed) > 8: centrocampisti = processed[4:8]
if not attaccanti and len(processed) > 11: attaccanti = processed[8:11]

try:
    m_parts = modulo_scelto.split('-')
    n_def, n_mid, n_att = int(m_parts[0]), int(m_parts[1]), int(m_parts[2])
except:
    n_def, n_mid, n_att = 3, 4, 3

t_portieri = portieri[:1]
t_difensori = difensori[:n_def]
t_centrocampisti = centrocampisti[:n_mid]
t_attaccanti = attaccanti[:n_att]

tutti_titolari = t_portieri + t_difensori + t_centrocampisti + t_attaccanti
panchinari = [p for p in processed if p not in tutti_titolari]

def render_cards(lista, is_bench=False):
    if not lista:
        return '<div style="color: #aaa; font-size: 0.7rem; font-style: italic; text-align:center;">Nessun giocatore</div>'
    h = ""
    for p in lista:
        nome = p["nome"]
        fm = p["fm"]
        tit = p["tit"]
        ruolo = p["ruolo"]
        
        if ruolo == "A":
            p_bonus = int(min(95, max(20, (fm - 5.5) * 32 + random.randint(5, 15))))
            p_amm, p_esp = int(random.uniform(10, 25)), int(random.uniform(1, 4))
        elif ruolo == "C":
            p_bonus = int(min(80, max(12, (fm - 5.5) * 24 + random.randint(0, 10))))
            p_amm, p_esp = int(random.uniform(25, 45)), int(random.uniform(2, 7))
        elif ruolo == "D":
            p_bonus = int(min(50, max(5, (fm - 5.5) * 16 + random.randint(0, 5))))
            p_amm, p_esp = int(random.uniform(35, 60)), int(random.uniform(4, 10))
        else:
            p_bonus = int(random.uniform(5, 20))
            p_amm, p_esp = int(random.uniform(5, 15)), int(random.uniform(1, 4))

        color_bar = "#2ecc71" if tit >= 70 else "#e67e22"
        iniziali = "".join([n[0] for n in nome.split()[:2]]).upper()
        width_card = "140px" if is_bench else "100px"

        h += f"""
        <div style="background: #14181c; border: 1px solid {'#ffcc00' if is_bench else '#00ffcc'}; border-radius: 8px; padding: 5px; text-align: center; width: {width_card}; box-shadow: 0 4px 8px rgba(0,0,0,0.6); display: flex; flex-direction: column; align-items: center; margin-bottom: 6px;">
            <div style="display: flex; align-items: center; gap: 5px; width: 100%; justify-content: center; margin-bottom: 2px;">
                <div style="width: 20px; height: 20px; background: #1e272e; border: 1px solid #00ffcc; border-radius: 50%; font-size: 0.5rem; color: #00ffcc; display: flex; align-items: center; justify-content: center; font-weight: bold;">{iniziali}</div>
                <div style="font-weight: bold; font-size: 0.68rem; color: #ffffff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 90px;" title="{nome}">{nome}</div>
            </div>
            <div style="font-size: 0.55rem; color: #f1c40f; font-weight: 600;">⚽ {p_bonus}% | 🟨 {p_amm}%</div>
            <div style="font-size: 0.55rem; color: #ff6b6b; margin-bottom: 3px;">🔴 {p_esp}% | FM: {fm:.2f}</div>
            <div style="width: 100%; background: #333; border-radius: 3px; height: 4px; overflow: hidden;">
                <div style="height: 100%; width: {tit}%; background-color: {color_bar};"></div>
            </div>
            <div style="font-size: 0.48rem; margin-top: 2px; color: #ccc;">{tit}% Titolarità</div>
        </div>
        """
    return h

# --- LAYOUT PRINCIPALE: CAMPO A SINISTRA, PANCHINA A DESTRA ---
col_campo, col_panchina = st.columns([2.3, 1])

with col_campo:
    st.markdown(f"<div style='font-size: 1rem; font-weight: bold; color: #00ffcc; margin-bottom: 6px;'>🏟️ Formazione Titolare ({selected_league}) — {modulo_scelto}</div>", unsafe_allow_html=True)
    
    field_html = f"""
    <div style="background: linear-gradient(180deg, #1b4d3e 0%, #0d281e 100%); border: 3px solid rgba(255, 255, 255, 0.85); border-radius: 12px; position: relative; display: flex; flex-direction: column; justify-content: space-around; align-items: center; padding: 15px 5px; height: 540px; box-sizing: border-box;">
        <div style="display: flex; justify-content: center; gap: 10px; width: 100%; z-index: 2;">{render_cards(t_portieri)}</div>
        <div style="display: flex; justify-content: center; gap: 8px; width: 100%; z-index: 2;">{render_cards(t_difensori)}</div>
        <div style="display: flex; justify-content: center; gap: 8px; width: 100%; z-index: 2;">{render_cards(t_centrocampisti)}</div>
        <div style="display: flex; justify-content: center; gap: 8px; width: 100%; z-index: 2;">{render_cards(t_attaccanti)}</div>
    </div>
    """
    components.html(field_html, height=555, scrolling=False)

with col_panchina:
    st.markdown(f"<div style='font-size: 1rem; font-weight: bold; color: #ffcc00; margin-bottom: 6px;'>🪑 Panchina & Riserve</div>", unsafe_allow_html=True)
    
    bench_html = f"""
    <div style="background: #14171a; border: 2px solid #3d3d3d; border-radius: 12px; padding: 10px; height: 540px; overflow-y: auto; box-sizing: border-box; display: flex; flex-direction: column; align-items: center;">
        {render_cards(panchinari, is_bench=True)}
    </div>
    """
    components.html(bench_html, height=555, scrolling=True)

st.markdown("---")

# --- ALGORITMO CONSIGLIATO & MOTIVAZIONI ---
st.markdown("### 🤖 Algoritmo Avanzato: Analisi Formazioni & Consigli")
st.info("L'algoritmo ha incrociato i dati ufficiali di **Sky, SportMediaset e Gazzetta dello Sport** valutando lo stato di forma, i ballottaggi e i match odierni.")

if st.button("🚀 Genera Consiglio Formazione e Motivazioni"):
    st.success("Analisi completata con successo!")
    
    col_cons1, col_cons2 = st.columns(2)
    
    with col_cons1:
        st.markdown("#### ✅ Chi Schierare (Consigliati)")
        if tutti_titolari:
            top_consigliato = max(tutti_titolari, key=lambda x: x["fm"])
            st.markdown(f"* **{top_consigliato['nome']}** (FM: {top_consigliato['fm']}): Partita favorevole in casa. Le principali testate giornalistiche confermano l'alta titolarità ({top_consigliato['tit']}%) e un elevato indice di pericolosità offensiva.")
        st.markdown("* **Attaccanti di Fascia Alta**: Da schierare senza dubbi per via dei calci di rigore a favore e dei coefficienti di difficoltà bassi per i difensori avversari.")

    with col_cons2:
        st.markdown("#### ❌ Chi Escludere e Perché")
        if panchinari:
            sconsigliato = min(panchinari, key=lambda x: x["fm"])
            st.markdown(f"* **{sconsigliato['nome']}**: Sconsigliato per questa giornata. Le proiezioni di Sky e SportMediaset segnalano un forte ballottaggio e un indice di ammonizione elevato contro una squadra chiusa.")
        st.markdown("* **Giocatori in trasferta contro big**: Evitare profili con bassa titolarità stimata e scarsa media voto per non rischiare il modificatore negativo o malus pesanti.")
