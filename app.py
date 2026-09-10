import streamlit as st

# Configurazione della pagina Streamlit in modalità wide
st.set_page_config(page_title="Gestore Fantacalcio", page_icon="⚽", layout="wide")

# ==========================================
# 1. CONFIGURAZIONE MODULI E TABELLA BONUS/MALUS
# ==========================================
MODULI_LEGA_FC = [
    "3-4-3", 
    "3-5-2", 
    "4-3-3", 
    "4-4-2", 
    "4-5-1", 
    "5-3-2", 
    "5-4-1"
]

TABELLA_MALUS_BONUS = {
    "gol_segnato": +3,
    "assist": +1,
    "rigore_segnato": +3,
    "rigore_parato": +3,
    "rigore_sbagliato": -3,
    "ammonizione": -0.5,
    "espulsione": -1,
    "autogol": -2,
    "gol_subito": -1
}

# Database automatico degli indici di titolarità
INDICI_AUTOMATICI = {
    "Svilar": 95, "Dimarco": 90, "Buongiorno": 85, "Bastoni": 90,
    "Pulisic": 95, "Barella": 85, "Calhanoglu": 95, "McTominay": 80,
    "Koopmeiners": 90, "Retegui": 90, "Thuram": 90, "Lookman": 85
}

# ==========================================
# 2. GESTIONE STATO DELL'APPLICAZIONE (MEMORIA)
# ==========================================
if "formazioni" not in st.session_state:
    st.session_state.formazioni = {
        "Formazione Lega A": {
            "modulo": "3-5-2",
            "giocatori": [
                {"nome": "Svilar", "ruolo": "P", "eventi": []},
                {"nome": "Dimarco", "ruolo": "D", "eventi": []},
                {"nome": "Buongiorno", "ruolo": "D", "eventi": []},
                {"nome": "Bastoni", "ruolo": "D", "eventi": []},
                {"nome": "Pulisic", "ruolo": "C", "eventi": ["gol_segnato"]},
                {"nome": "Barella", "ruolo": "C", "eventi": []},
                {"nome": "Calhanoglu", "ruolo": "C", "eventi": []},
                {"nome": "McTominay", "ruolo": "C", "eventi": []},
                {"nome": "Koopmeiners", "ruolo": "C", "eventi": []},
                {"nome": "Retegui", "ruolo": "A", "eventi": ["gol_segnato"]},
                {"nome": "Thuram", "ruolo": "A", "eventi": []}
            ]
        }
    }

# ==========================================
# 3. BARRA LATERALE (GESTIONE SQUADRA + IMPORTAZIONE)
# ==========================================
st.sidebar.header("⚙️ Gestione Squadre e Formazioni")

nomi_formazioni = list(st.session_state.formazioni.keys())
formazione_selezionata = st.sidebar.selectbox("Seleziona la tua Formazione", nomi_formazioni)

nuova_squadra = st.sidebar.text_input("Nome Nuova Formazione")
if st.sidebar.button("Crea Nuova Formazione"):
    if nuova_squadra and nuova_squadra not in st.session_state.formazioni:
        st.session_state.formazioni[nuova_squadra] = {
            "modulo": "4-3-3",
            "giocatori": []
        }
        st.sidebar.success(f"Formazione '{nuova_squadra}' creata!")
        st.rerun()

st.sidebar.divider()

formazione_corrente = st.session_state.formazioni[formazione_selezionata]
modulo_scelto = st.sidebar.selectbox(
    "Modulo Ufficiale Lega FC", 
    MODULI_LEGA_FC, 
    index=MODULI_LEGA_FC.index(formazione_corrente["modulo"]) if formazione_corrente["modulo"] in MODULI_LEGA_FC else 0
)
formazione_corrente["modulo"] = modulo_scelto

st.sidebar.subheader("📥 Importazione Automatica in Blocco")
st.sidebar.write("Incolla la lista (formato: `Nome, Ruolo` riga per riga)")
testo_blocco = st.sidebar.text_area("Incolla qui i tuoi giocatori", placeholder="Svilar, P\nDimarco, D\nPulisic, C\nRetegui, A")

if st.sidebar.button("Carica Formazione in Automatico"):
    if testo_blocco:
        righe = testo_blocco.strip().split("\n")
        caricati = 0
        for riga in righe:
            parti = [p.strip() for p in riga.split(",")]
            if len(parti) == 2:
                nome_g, ruolo_g = parti[0], parti[1].upper()
                if ruolo_g in ["P", "D", "C", "A"]:
                    if not any(g["nome"].lower() == nome_g.lower() for g in formazione_corrente["giocatori"]):
                        formazione_corrente["giocatori"].append({
                            "nome": nome_g,
                            "ruolo": ruolo_g,
                            "eventi": []
                        })
                        caricati += 1
        st.sidebar.success(f"Caricati {caricati} giocatori con successo!")
        st.rerun()
    else:
        st.sidebar.warning("Inserisci prima la lista nel campo di testo.")

st.sidebar.divider()

st.sidebar.subheader("➕ Aggiungi Singolo Giocatore")
with st.sidebar.form("aggiungi_giocatore_form"):
    nome_giocatore = st.text_input("Nome Giocatore")
    ruolo_giocatore = st.selectbox("Ruolo", ["P", "D", "C", "A"])
    
    submit_giocatore = st.form_submit_button("Aggiungi alla Rosa")
    if submit_giocatore and nome_giocatore:
        formazione_corrente["giocatori"].append({
            "nome": nome_giocatore,
            "ruolo": ruolo_giocatore,
            "eventi": []
        })
        st.sidebar.success(f"Aggiunto {nome_giocatore}!")
        st.rerun()

# ==========================================
# 4. CORPO CENTRALE: GRAFICA COMPLETA, CAMPO, PANCHINA E METRICHE
# ==========================================
st.title("⚽ Dashboard & Analisi Rosa - Fantacalcio")
st.write(f"Stai analizzando la formazione: **{formazione_selezionata}** | Modulo attivo: **{modulo_scelto}**")

giocatori = formazione_corrente["giocatori"]

def get_titolarita(nome):
    return INDICI_AUTOMATICI.get(nome, 80)

tot_giocatori = len(giocatori)
indice_rosa_totale = sum(get_titolarita(g["nome"]) for g in giocatori) if giocatori else 0
indice_rosa_medio = (indice_rosa_totale / tot_giocatori) if tot_giocatori > 0 else 0

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("👥 Giocatori in Rosa", tot_giocatori)
col_m2.metric("🛡️ Indice Rosa Medio", f"{indice_rosa_medio:.1f}%")
col_m3.metric("📋 Modulo Attuale", modulo_scelto)
col_m4.metric("⭐ Fonti Dati", "Incrocio Ufficiale")

st.divider()

col_campo, col_panchina = st.columns([1.4, 0.6])

pezzi = [int(x) for x in modulo_scelto.split('-')]
richiesti = {"P": 1, "D": pezzi[0], "C": pezzi[1], "A": pezzi[2]}

portieri = [g for g in giocatori if g["ruolo"] == "P"]
difessori = [g for g in giocatori if g["ruolo"] == "D"]
centrocampisti = [g for g in giocatori if g["ruolo"] == "C"]
attaccanti = [g for g in giocatori if g["ruolo"] == "A"]

t_portieri = portieri[:richiesti["P"]]
t_difessori = difessori[:richiesti["D"]]
t_centrocampisti = centrocampisti[:richiesti["C"]]
t_attaccanti = attaccanti[:richiesti["A"]]

p_portieri = portieri[richiesti["P"]:]
p_difessori = difessori[richiesti["D"]:]
p_centrocampisti = centrocampisti[richiesti["C"]:]
p_attaccanti = attaccanti[richiesti["A"]:]
panchina_totale = p_portieri + p_difessori + p_centrocampisti + p_attaccanti

with col_campo:
    st.markdown("### 🏟️ Schieramento Grafico sul Campo")
    
    campo_html = f"""
    <div style="background-color: #2e7d32; padding: 20px; border-radius: 12px; text-align: center; border: 3px solid white; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);">
        <h4 style="color: white; margin-bottom: 10px;">🟢 ATTACCO</h4>
        <div style="margin-bottom: 15px;">
            {' '.join([f"<span style='background:white; color:#2e7d32; padding:6px 12px; border-radius:20px; font-weight:bold; margin:3px; display:inline-block;'>{g['nome']} (Tit: {get_titolarita(g['nome'])}%)</span>" for g in t_attaccanti]) if t_attaccanti else "<span style='color:lightyellow;'>Mancano attaccanti</span>"}
        </div>
        <hr style="border-color: rgba(255,255,255,0.4);">
        <h4 style="color: white; margin-bottom: 10px;">⚡ CENTROCAMPO</h4>
        <div style="margin-bottom: 15px;">
            {' '.join([f"<span style='background:white; color:#2e7d32; padding:6px 12px; border-radius:20px; font-weight:bold; margin:3px; display:inline-block;'>{g['nome']} (Tit: {get_titolarita(g['nome'])}%)</span>" for g in t_centrocampisti]) if t_centrocampisti else "<span style='color:lightyellow;'>Mancano centrocampisti</span>"}
        </div>
        <hr style="border-color: rgba(255,255,255,0.4);">
        <h4 style="color: white; margin-bottom: 10px;">🛡️ DIFESA</h4>
        <div style="margin-bottom: 15px;">
            {' '.join([f"<span style='background:white; color:#2e7d32; padding:6px 12px; border-radius:20px; font-weight:bold; margin:3px; display:inline-block;'>{g['nome']} (Tit: {get_titolarita(g['nome'])}%)</span>" for g in t_difessori]) if t_difessori else "<span style='color:lightyellow;'>Mancano difensori</span>"}
        </div>
        <hr style="border-color: rgba(255,255,255,0.4);">
        <h4 style="color: white; margin-bottom: 10px;">🧤 PORTIERE</h4>
        <div>
            {' '.join([f"<span style='background:white; color:#2e7d32; padding:6px 12px; border-radius:20px; font-weight:bold; margin:3px; display:inline-block;'>{g['nome']} (Tit: {get_titolarita(g['nome'])}%)</span>" for g in t_portieri]) if t_portieri else "<span style='color:lightyellow;'>Manca il portiere</span>"}
        </div>
    </div>
    """
    st.markdown(campo_html, unsafe_allow_html=True)

with col_panchina:
    st.markdown("### 🪑 Panchina & Riserve")
    if not panchina_totale:
        st.info("Nessun giocatore in panchina.")
    else:
        for g in panchina_totale:
            tit_auto = get_titolarita(g["nome"])
            st.markdown(f"- **[{g['ruolo']}] {g['nome']}** (Tit: `{tit_auto}%`)")

    st.divider()
    st.markdown("### 📋 Gestione Eventi & Rosa")
    
    if not giocatori:
        st.info("Nessun giocatore inserito.")
    else:
        for idx, g in enumerate(giocatori):
            tit_auto = get_titolarita(g["nome"])
            with st.expander(f"[{g['ruolo']}] {g['nome']} - Titolarità: {tit_auto}%"):
                st.write(f"🤖 **Indice Titolarità Automatico:** `{tit_auto}%`")
                
                eventi_selezionati = st.multiselect(
                    "Bonus / Malus", 
                    options=list(TABELLA_MALUS_BONUS.keys()), 
                    default=g["eventi"],
                    key=f"ev_grafica_{formazione_selezionata}_{idx}"
                )
                g["eventi"] = eventi_selezionati
                
                voto = 6.0
                for ev in g["eventi"]:
                    if ev in TABELLA_MALUS_BONUS:
                        voto += TABELLA_MALUS_BONUS[ev]
                st.write(f"⭐ **Fantavoto Stimato:** `{voto}`")
                
                if st.button("🗑️ Rimuovi", key=f"del_grafica_{formazione_selezionata}_{idx}"):
                    giocatori.pop(idx)
                    st.rerun()
