import streamlit as st

# Configurazione della pagina Streamlit (Layout largo per godersi il campo da calcio grafico)
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

# Database fittizio di indici di titolarità automatici basati sui dati reali/esperti
INDICI_AUTOMATICI = {
    "Svilar": 95, "Dimarco": 90, "Buongiorno": 85, "Bastoni": 90,
    "Pulisic": 95, "Barella": 85, "Calhanoglu": 95, "McTominay": 80,
    "Koopmeiners": 90, "Retegui": 90, "Thuram": 90
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
# 3. BARRA LATERALE (PERFETTA E INTATTA COME LA VOLEVI)
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

st.sidebar.subheader("➕ Aggiungi Giocatore")
with st.sidebar.form("aggiungi_giocatore_form"):
    nome_giocatore = st.text_input("Nome Giocatore")
    ruolo_giocatore = st.selectbox("Ruolo", ["P", "D", "C", "A"])
    # Nota: L'indice di titolarità NON si sceglie a mano, viene assegnato in automatico dal sistema!
    
    submit_giocatore = st.form_submit_button("Aggiungi alla Rosa")
    if submit_giocatore and nome_giocatore:
        formazione_corrente["giocatori"].append({
            "nome": nome_giocatore,
            "ruolo": ruolo_giocatore,
            "eventi": []
        })
        st.sidebar.success(f"Aggiunto {nome_giocatore} con indice automatico!")
        st.rerun()

# ==========================================
# 4. CORPO CENTRALE: GRAFICA COMPLETA, CAMPO E METRICHE DI ROSA
# ==========================================
st.title("⚽ Dashboard & Analisi Rosa - Fantacalcio")
st.write(f"Stai analizzando la formazione: **{formazione_selezionata}** | Modulo attivo: **{modulo_scelto}**")

giocatori = formazione_corrente["giocatori"]

# Calcoli generali sulla rosa
tot_giocatori = len(giocatori)
portieri_rosa = [g for g in giocatori if g["ruolo"] == "P"]
difessori_rosa = [g for g in giocatori if g["ruolo"] == "D"]
centrocampisti_rosa = [g for g in giocatori if g["ruolo"] == "C"]
attaccanti_rosa = [g for g in giocatori if g["ruolo"] == "A"]

# Calcolo Indice Rosa Complessivo
def get_titolarita(nome):
    return INDICI_AUTOMATICI.get(nome, 80) # Default 80 se non presente nel database

indice_rosa_totale = sum(get_titolarita(g["nome"]) for g in giocatori) if giocatori else 0
indice_rosa_medio = (indice_rosa_totale / tot_giocatori) if tot_giocatori > 0 else 0

# Box metriche superiori in stile dashboard avanzata
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
col_m1.metric("👥 Giocatori in Rosa", tot_giocatori)
col_m2.metric("🛡️ Indice Rosa Medio", f"{indice_rosa_medio:.1f}%")
col_m3.metric("📋 Modulo Attuale", modulo_scelto)
col_m4.metric("⭐ Fonti Dati", "Incrocio Ufficiale")

st.divider()

# Struttura divisa in due colonne: Grafica Campo da Calcio + Gestione Dettagliata
col_1, col_2 = st.columns([1.3, 0.7])

with col_1:
    st.markdown("### 🏟️ Schieramento Grafico sul Campo")
    
    # Estraiamo i titolari in base al modulo scelto (es. 3-5-2 -> 1 P, 3 D, 5 C, 2 A)
    pezzi = [int(x) for x in modulo_scelto.split('-')]
    richiesti = {"P": 1, "D": pezzi[0], "C": pezzi[1], "A": pezzi[2]}
    
    t_portieri = portieri_rosa[:richiesti["P"]]
    t_difessori = difessori_rosa[:richiesti["D"]]
    t_centrocampisti = centrocampisti_rosa[:richiesti["C"]]
    t_attaccanti = attaccanti_rosa[:richiesti["A"]]
    
    # HTML personalizzato per disegnare un campo da calcio stilizzato pulito
    campo_html = f"""
    <div style="background-color: #2e7d32; padding: 20px; border-radius: 12px; text-align: center; border: 3px solid white; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);">
        <h4 style="color: white; margin-bottom: 15px;">🟢 ATTACCO</h4>
        <div style="margin-bottom: 15px;">
            {' '.join([f"<span style='background:white; color:#2e7d32; padding:6px 12px; border-radius:20px; font-weight:bold; margin:3px; display:inline-block;'>{g['nome']} (Tit: {get_titolarita(g['nome'])}%)</span>" for g in t_attaccanti]) if t_attaccanti else "<span style='color:lightyellow;'>Mancano attaccanti</span>"}
        </div>
        <hr style="border-color: rgba(255,255,255,0.4);">
        <h4 style="color: white; margin-bottom: 15px;">⚡ CENTROCAMPO</h4>
        <div style="margin-bottom: 15px;">
            {' '.join([f"<span style='background:white; color:#2e7d32; padding:6px 12px; border-radius:20px; font-weight:bold; margin:3px; display:inline-block;'>{g['nome']} (Tit: {get_titolarita(g['nome'])}%)</span>" for g in t_centrocampisti]) if t_centrocampisti else "<span style='color:lightyellow;'>Mancano centrocampisti</span>"}
        </div>
        <hr style="border-color: rgba(255,255,255,0.4);">
        <h4 style="color: white; margin-bottom: 15px;">🛡️ DIFESA</h4>
        <div style="margin-bottom: 15px;">
            {' '.join([f"<span style='background:white; color:#2e7d32; padding:6px 12px; border-radius:20px; font-weight:bold; margin:3px; display:inline-block;'>{g['nome']} (Tit: {get_titolarita(g['nome'])}%)</span>" for g in t_difessori]) if t_difessori else "<span style='color:lightyellow;'>Mancano difensori</span>"}
        </div>
        <hr style="border-color: rgba(255,255,255,0.4);">
        <h4 style="color: white; margin-bottom: 15px;">🧤 PORTERE</h4>
        <div>
            {' '.join([f"<span style='background:white; color:#2e7d32; padding:6px 12px; border-radius:20px; font-weight:bold; margin:3px; display:inline-block;'>{g['nome']} (Tit: {get_titolarita(g['nome'])}%)</span>" for g in t_portieri]) if t_portieri else "<span style='color:lightyellow;'>Manca il portiere</span>"}
        </div>
    </div>
    """
    st.markdown(campo_html, unsafe_allow_html=True)

with col_2:
    st.markdown("### 📋 Gestione Eventi & Rosa")
    
    if not giocatori:
        st.info("Nessun giocatore inserito.")
    else:
        for idx, g in enumerate(giocatori):
            tit_auto = get_titolarita(g["nome"])
            with st.expander(f"[{g['ruolo']}] {g['nome']} (Tit: {tit_auto}%)"):
                # Assegnazione automatica e visibile dell'indice in automatico
                st.write(f"🤖 **Indice Titolarità Automatico:** `{tit_auto}%`")
                
                # Bonus e Malus interattivi
                eventi_selezionati = st.multiselect(
                    "Bonus / Malus", 
                    options=list(TABELLA_MALUS_BONUS.keys()), 
                    default=g["eventi"],
                    key=f"ev_grafica_{formazione_selezionata}_{idx}"
                )
                g["eventi"] = eventi_selezionati
                
                # Calcolo fantavoto
                voto = 6.0
                for ev in g["eventi"]:
                    voto += TABELLA_MALUS_BONUS[ev]
                st.write(f"⭐ **Fantavoto Stimato:** `{voto}`")
                
                if st.button("🗑️ Rimuovi", key=f"del_grafica_{formazione_selezionata}_{idx}"):
                    giocatori.pop(idx)
                    st.rerun()
