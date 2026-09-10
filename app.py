import streamlit as st

# Configurazione della pagina in modalità larga
st.set_page_config(page_title="FantAlgoritmo - Formazione Titolare", layout="wide")

st.title("⚽ FantAlgoritmo - Formazione Titolare")

# Inizializzazione dello state per salvare più rose senza perderle
if "formazioni_salvate" not in st.session_state:
    st.session_state["formazioni_salvate"] = {}

# --- SIDEBAR: GESTIONE E AGGIUNTA NUOVA ROSA ---
st.sidebar.header("📁 Gestione Rosa")
nome_nuova_rosa = st.sidebar.text_input("Nome File Rosa (es. La beneamata ma non troppo)")
modulo_scelto = st.sidebar.selectbox("Seleziona Modulo Titolari", ["3-4-3", "4-3-3", "3-5-2", "4-2-3-1"])

if st.sidebar.button("Carica/Salva Rosa"):
    if nome_nuova_rosa:
        # Salviamo la rosa nel dizionario di sessione
        st.session_state["formazioni_salvate"][nome_nuova_rosa] = {
            "totale_rosa": 25,
            "indice_rosa": "8.6 / 10",
            "modulo": modulo_scelto,
            "titolari": [
                {"nome": "Kvaratskhelia", "ruolo": "A", "perc": "98%"},
                {"nome": "Esposito F.P.", "ruolo": "A", "perc": "85%"},
                {"nome": "Kean", "ruolo": "A", "perc": "92%"},
                {"nome": "Bastoni", "ruolo": "D", "perc": "75%"},
                {"nome": "Mkhitaryan", "ruolo": "C", "perc": "80%"},
                {"nome": "Barella", "ruolo": "C", "perc": "90%"},
                {"nome": "Dimarco", "ruolo": "D", "perc": "95%"}
            ],
            "panchina": [
                {"nome": "Martinez Jo.", "ruolo": "P", "fm": "6.17", "bonus": "+10%"},
                {"nome": "Doekhi", "ruolo": "D", "fm": "6.33", "bonus": "+16%"},
                {"nome": "Scalvini", "ruolo": "D", "fm": "6.17", "bonus": "+10%"},
                {"nome": "Bastoni S.", "ruolo": "D", "fm": "6.0", "bonus": "+5%"},
                {"nome": "Akinsanmiro", "ruolo": "C", "fm": "6.25", "bonus": "+13%"},
                {"nome": "Jones C.", "ruolo": "C", "fm": "6.0", "bonus": "+5%"}
            ]
        }
        st.sidebar.success(f"Rosa '{nome_nuova_rosa}' caricata e salvata correttamente!")
    else:
        st.sidebar.warning("Inserisci il nome della rosa.")

# --- SEZIONE PRINCIPALE ---
if st.session_state["formazioni_salvate"]:
    
    # Menu a tendina per scegliere quale rosa visualizzare tra quelle salvate in memoria
    rosa_attiva = st.selectbox(
        "Seleziona la rosa da visualizzare:",
        list(st.session_state["formazioni_salvate"].keys())
    )
    
    dati = st.session_state["formazioni_salvate"][rosa_attiva]
    
    # Intestazione superiore con Totale Rosa e Indice
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.metric(label="Totale Rosa", value=dati['totale_rosa'])
    with col_info2:
        st.metric(label="Indice Rosa", value=dati['indice_rosa'])

    st.markdown("---")

    # Layout diviso in due colonne: Campo Titolari (sinistra) e Panchina (destra)
    col_campo, col_panchina = st.columns([2.5, 1])

    with col_campo:
        st.subheader(f"Campo Titolari ({dati['modulo']})")
        
        # Creazione di una griglia pulita con le colonne native di Streamlit per i titolari
        num_titolari = len(dati["titolari"])
        colonne_titolari = st.columns(num_titolari)
        
        for idx, t in enumerate(dati["titolari"]):
            with colonne_titolari[idx]:
                # Mostriamo le informazioni del giocatore in modo pulito e nativo
                st.markdown(f"**{t['nome']}**")
                st.caption(f"Ruolo: {t['ruolo']} | 🟢 {t['perc']}")

    with col_panchina:
        st.subheader("Panchina & Riserve")
        
        # Visualizzazione pulita della panchina con FM e Bonus
        for p in dati["panchina"]:
            st.text(f"• {p['nome']} ({p['ruolo']}) - FM: {p['fm']} | Bonus: {p['bonus']}")

else:
    st.info("👋 Usa il menu a sinistra per caricare la tua prima rosa e visualizzare la formazione!")
