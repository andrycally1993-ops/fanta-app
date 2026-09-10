import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Gestore Fantacalcio", page_icon="⚽", layout="wide")

st.title("⚽ Gestore Completo Fantacalcio - Multi Formazione")
st.write("Gestisci le tue rose, i moduli ufficiali di Lega FC, i bonus/malus e gli indici di titolarità.")

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

# ==========================================
# 2. GESTIONE STATO DELL'APPLICAZIONE (MEMORIA)
# ==========================================
if "formazioni" not in st.session_state:
    # Salvataggio di più formazioni dell'utente
    st.session_state.formazioni = {
        "Formazione Lega A": {
            "modulo": "3-5-2",
            "giocatori": [
                {"nome": "Svilar", "ruolo": "P", "titolarita": 95, "eventi": []},
                {"nome": "Dimarco", "ruolo": "D", "titolarita": 90, "eventi": []},
                {"nome": "Buongiorno", "ruolo": "D", "titolarita": 85, "eventi": []},
                {"nome": "Bastoni", "ruolo": "D", "titolarita": 90, "eventi": []},
                {"nome": "Pulisic", "ruolo": "C", "titolarita": 95, "eventi": ["gol_segnato"]},
                {"nome": "Barella", "ruolo": "C", "titolarita": 85, "eventi": []},
                {"nome": "Calhanoglu", "ruolo": "C", "titolarita": 95, "eventi": []},
                {"nome": "McTominay", "ruolo": "C", "titolarita": 80, "eventi": []},
                {"nome": "Koopmeiners", "ruolo": "C", "titolarita": 90, "eventi": []},
                {"nome": "Retegui", "ruolo": "A", "titolarita": 90, "eventi": ["gol_segnato"]},
                {"nome": "Thuram", "ruolo": "A", "titolarita": 90, "eventi": []}
            ]
        }
    }

# ==========================================
# 3. INTERFACCIA LATERALE (SIDEBAR)
# ==========================================
st.sidebar.header("⚙️ Gestione Squadre e Formazioni")

# Scelta o creazione di una nuova formazione (per gestire più di una squadra)
nomi_formazioni = list(st.session_state.formazioni.keys())
formazione_selezionata = st.sidebar.selectbox("Seleziona la tua Formazione", nomi_formazioni)

# Opzione per aggiungere una nuova formazione
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

# Modifica del modulo per la formazione attiva
formazione_corrente = st.session_state.formazioni[formazione_selezionata]
modulo_scelto = st.sidebar.selectbox(
    "Modulo Ufficiale Lega FC", 
    MODULI_LEGA_FC, 
    index=MODULI_LEGA_FC.index(formazione_corrente["modulo"]) if formazione_corrente["modulo"] in MODULI_LEGA_FC else 0
)
formazione_corrente["modulo"] = modulo_scelto

# ==========================================
# 4. AGGIUNGI GIOCATORE ALLA SQUADRA
# ==========================================
st.sidebar.subheader("➕ Aggiungi Giocatore")
with st.sidebar.form("aggiungi_giocatore_form"):
    nome_giocatore = st.text_input("Nome Giocatore")
    ruolo_giocatore = st.selectbox("Ruolo", ["P", "D", "C", "A"])
    titolarita_giocatore = st.slider("Indice di Titolarità (%)", 0, 100, 85)
    
    submit_giocatore = st.form_submit_button("Aggiungi alla Rosa")
    if submit_giocatore and nome_giocatore:
        formazione_corrente["giocatori"].append({
            "nome": nome_giocatore,
            "ruolo": ruolo_giocatore,
            "titolarita": titolarita_giocatore,
            "eventi": []
        })
        st.sidebar.success(f"Aggiunto {nome_giocatore}!")
        st.rerun()

# ==========================================
# 5. CORPO PRINCIPALE: VISUALIZZAZIONE E ANALISI
# ==========================================
st.subheader(f"📊 Analisi Rosa: {formazione_selezionata} (Modulo: {modulo_scelto})")

giocatori = formazione_corrente["giocatori"]

if not giocatori:
    st.info("La rosa è vuota. Usa il pannello a sinistra per aggiungere i tuoi giocatori.")
else:
    # Calcolo reparti richiesti dal modulo
    pezzi = [int(x) for x in modulo_scelto.split('-')]
    richiesti = {"P": 1, "D": pezzi[0], "C": pezzi[1], "A": pezzi[2]}
    
    # Divisione automatica per reparti per simulare i titolari
    portieri = [g for g in giocatori if g["ruolo"] == "P"]
    difessori = [g for g in giocatori if g["ruolo"] == "D"]
    centrocampisti = [g for g in giocatori if g["ruolo"] == "C"]
    attaccanti = [g for g in giocatori if g["ruolo"] == "A"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 Giocatori in Rosa")
        for idx, g in enumerate(giocatori):
            with st.expander(f"[{g['ruolo']}] {g['nome']} - Titolarità: {g['titolarita']}%"):
                # Gestione eventi bonus/malus al volo
                eventi_selezionati = st.multiselect(
                    "Bonus / Malus", 
                    options=list(TABELLA_MALUS_BONUS.keys()), 
                    default=g["eventi"],
                    key=f"ev_{formazione_selezionata}_{idx}"
                )
                g["eventi"] = eventi_selezionati
                
                # Calcolo fantavoto stimato
                voto = 6.0
                for ev in g["eventi"]:
                    voto += TABELLA_MALUS_BONUS[ev]
                st.write(f"**Fantavoto Stimato:** {voto}")
                
                if st.button("Elimina Giocatore", key=f"del_{formazione_selezionata}_{idx}"):
                    giocatori.pop(idx)
                    st.rerun()

    with col2:
        st.markdown("### 📋 Verifica Schieramento e Titolarità")
        
        # Controllo numerico rispetto al modulo
        ok_numeri = (
            len(portieri) >= richiesti["P"] and 
            len(difessori) >= richiesti["D"] and 
            len(centrocampisti) >= richiesti["C"] and 
            len(attaccanti) >= richiesti["A"]
        )
        
        if not ok_numeri:
            st.warning(f"⚠️ Attenzione: Per il modulo {modulo_scelto} servono almeno {richiesti['P']} P, {richiesti['D']} D, {richiesti['C']} C e {richiesti['A']} A.")
        else:
            st.success("✅ La rosa rispetta i numeri minimi per il modulo scelto!")
            
        # Calcolo indice medio di titolarita complessivo dei titolari ideali
        titolari_utilizzati = portieri[:richiesti["P"]] + difessori[:richiesti["D"]] + centrocampisti[:richiesti["C"]] + attaccanti[:richiesti["A"]]
        
        if titolari_utilizzati:
            media_titolarita = sum(g["titolarita"] for g in titolari_utilizzati) / len(titolari_utilizzati)
            st.metric(label="Indice di Titolarità Medio (Titolari)", value=f"{media_titolarita:.1f}%")
            
            st.markdown("#### ⚽ Undici Ideale Schierato:")
            for g in titolari_utilizzati:
                st.write(f"- **[{g['ruolo']}] {g['nome']}** (Titolarità: {g['titolarita']}%)")
