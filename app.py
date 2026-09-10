import streamlit as st

# Configurazione della pagina in modalità larga
st.set_page_config(page_title="FantAlgoritmo - Formazione Titolare", layout="wide")

st.title("⚽ FantAlgoritmo - Formazione Titolare")

# Inizializzazione dello state per salvare più rose senza perderle
if "formazioni_salvate" not in st.session_state:
    st.session_state["formazioni_salvate"] = {}

# --- SIDEBAR: GESTIONE E AGGIUNTA NUOVA ROSA ---
st.sidebar.header("📁 Gestione Rosa")
nome_nuova_rosa = st.sidebar.text_input("Nome File Rosa (es. Rosa Lega A)")
modulo_scelto = st.sidebar.selectbox("Seleziona Modulo Titolari", ["3-4-3", "4-3-3", "3-5-2", "4-2-3-1"])

if st.sidebar.button("Carica/Salva Rosa"):
    if nome_nuova_rosa:
        # Salviamo la rosa nel dizionario di sessione
        st.session_state["formazioni_salvate"][nome_nuova_rosa] = {
            "totale_rosa": 25,
            "indice_rosa": "8.6 / 10",
            "modulo": modulo_scelto,
            "titolari": [
                {"nome": "Kvaratskhelia", "ruolo": "A", "perc": "98%", "foto": "https://via.placeholder.com/150"},
                {"nome": "Esposito F.P.", "ruolo": "A", "perc": "85%", "foto": "https://via.placeholder.com/150"},
                {"nome": "Kean", "ruolo": "A", "perc": "92%", "foto": "https://via.placeholder.com/150"},
                {"nome": "DB", "ruolo": "D", "perc": "75%", "foto": "https://via.placeholder.com/150"},
                {"nome": "M", "ruolo": "C", "perc": "80%", "foto": "https://via.placeholder.com/150"},
                {"nome": "M", "ruolo": "C", "perc": "90%", "foto": "https://via.placeholder.com/150"},
                {"nome": "A", "ruolo": "A", "perc": "95%", "foto": "https://via.placeholder.com/150"}
            ],
            "panchina": [
                {"nome": "Martinez Jo.", "ruolo": "P", "fm": "6.17", "bonus": "+10%"},
                {"nome": "Doekhi", "ruolo": "D", "fm": "6.33", "bonus": "+16%"},
                {"nome": "Scalvini", "ruolo": "D", "fm": "6.17", "bonus": "+10%"},
                {"nome": "Bastoni", "ruolo": "D", "fm": "6.0", "bonus": "+5%"},
                {"nome": "Akinsanmiro", "ruolo": "C", "fm": "6.25", "bonus": "+13%"},
                {"nome": "Jones C.", "ruolo": "C", "fm": "6.0", "bonus": "+5%"}
            ]
        }
        st.sidebar.success(f"Rosa '{nome_nuova_rosa}' caricata e salvata correttamente!")
    else:
        st.sidebar.warning("Inserisci il nome della rosa.")

# --- SEZIONE PRINCIPALE ---
if st.session_state["formazioni_salvate"]:
    
    # Selezione della rosa attiva tra quelle salvate (evita la sovrascrittura)
    rosa_attiva = st.selectbox(
        "Seleziona la rosa attiva:",
        list(st.session_state["formazioni_salvate"].keys())
    )
    
    dati = st.session_state["formazioni_salvate"][rosa_attiva]
    
    # Intestazione superiore con Totale Rosa e Indice
    col_info1, col_info2 = st.columns([2, 2])
    with col_info1:
        st.write(f"**Totale Rosa:** {dati['totale_rosa']}")
    with col_info2:
        st.write(f"**Indice Rosa:** {dati['indice_rosa']}")

    # Layout principale diviso in due colonne: Campo Titolari (sinistra) e Panchina (destra)
    col_campo, col_panchina = st.columns([2.3, 1])

    with col_campo:
        st.subheader(f"Campo Titolari ({dati['modulo']})")
        
        # Generazione HTML/CSS per i cerchi dei titolari con pallino percentuale in alto a destra
        html_titolari = """
        <div style="display: flex; flex-wrap: wrap; gap: 15px; background-color: #2e7d32; padding: 20px; border-radius: 10px; justify-content: center;">
        """
        
        for t in dati["titolari"]:
            html_titolari += f"""
            <div style="text-align: center; color: white; margin: 5px; position: relative;">
                <!-- Contenitore del cerchio con foto e pallino percentuale sovrapposto -->
                <div style="position: relative; width: 65px; height: 65px; margin: 0 auto;">
                    <!-- Foto Cerchiata -->
                    <div style="border-radius: 50%; width: 65px; height: 65px; overflow: hidden; border: 2px solid white; background: white;">
                        <img src="{t['foto']}" style="width: 100%; height: 100%; object-fit: cover;">
                    </div>
                    <!-- Pallino Percentuale in alto a destra -->
                    <div style="position: absolute; top: -5px; right: -5px; background-color: #ffb300; color: black; font-size: 10px; font-weight: bold; padding: 2px 5px; border-radius: 50px; border: 1px solid white;">
                        {t['perc']}
                    </div>
                    <!-- Ruolo nel cerchietto in basso -->
                    <div style="position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); background-color: #1976d2; color: white; font-size: 9px; font-weight: bold; width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid white;">
                        {t['ruolo']}
                    </div>
                </div>
                <!-- Nome del giocatore sotto -->
                <div style="font-size: 12px; font-weight: bold; margin-top: 5px; white-space: nowrap;">{t['nome']}</div>
            </div>
            """
            
        html_titolari += "</div>"
        st.markdown(html_titolari, unsafe_allow_html=True)

    with col_panchina:
        st.subheader("Panchina & Riserve")
        
        # Visualizzazione pulita della panchina con FM e Bonus/Malus
        for p in dati["panchina"]:
            st.markdown(
                f"<div style='font-size: 13px; border-bottom: 1px solid rgba(255,255,255,0.1); padding: 4px 0;'>"
                f"• <b>{p['nome']}</b> ({p['ruolo']}) - FM: {p['fm']} | <span style='color: #81c784;'>Bonus: {p['bonus']}</span>"
                f"</div>", 
                unsafe_allow_html=True
            )

else:
    st.info("👋 Usa il menu a sinistra per caricare la tua prima rosa e visualizzare la formazione!")
