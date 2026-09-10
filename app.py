import streamlit as st
import streamlit.components.v1 as components

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
        # Salviamo la rosa nel dizionario di sessione (senza Kvaratskhelia e con i giocatori corretti)
        st.session_state["formazioni_salvate"][nome_nuova_rosa] = {
            "totale_rosa": 25,
            "indice_rosa": "8.6 / 10",
            "modulo": modulo_scelto,
            "titolari": [
                {"nome": "Malen", "ruolo": "A", "perc": "90%", "colore_perc": "#4caf50", "foto": "https://via.placeholder.com/150"},
                {"nome": "Hojlund", "ruolo": "A", "perc": "100%", "colore_perc": "#4caf50", "foto": "https://via.placeholder.com/150"},
                {"nome": "Martinez L.", "ruolo": "A", "perc": "100%", "colore_perc": "#4caf50", "foto": "https://via.placeholder.com/150"},
                {"nome": "Mkhitaryan", "ruolo": "C", "perc": "80%", "colore_perc": "#ff9800", "foto": "https://via.placeholder.com/150"},
                {"nome": "Barella", "ruolo": "C", "perc": "90%", "colore_perc": "#4caf50", "foto": "https://via.placeholder.com/150"},
                {"nome": "Dimarco", "ruolo": "D", "perc": "95%", "colore_perc": "#4caf50", "foto": "https://via.placeholder.com/150"}
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
        st.write(f"**Totale Rosa:** {dati['totale_rosa']}")
    with col_info2:
        st.write(f"**Indice Rosa:** {dati['indice_rosa']}")

    st.markdown("---")

    # Layout diviso in due colonne: Campo Titolari (sinistra) e Panchina (destra)
    col_campo, col_panchina = st.columns([2.3, 1])

    with col_campo:
        st.subheader(f"Campo Titolari ({dati['modulo']})")
        
        # HTML ottimizzato con griglia flessibile e pulita per evitare sovrapposizioni o errori di layout
        html_campo = f"""
        <html>
        <head>
        <style>
            body {{
                background-color: #2e7d32;
                margin: 0;
                padding: 15px;
                font-family: sans-serif;
                border-radius: 12px;
            }}
            .field-grid {{
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                justify-content: center;
                align-items: center;
            }}
            .player-card {{
                text-align: center;
                color: white;
                width: 85px;
                background: rgba(0, 0, 0, 0.2);
                padding: 8px;
                border-radius: 8px;
            }}
            .avatar-container {{
                position: relative;
                width: 55px;
                height: 55px;
                margin: 0 auto;
            }}
            .avatar {{
                width: 55px;
                height: 55px;
                border-radius: 50%;
                object-fit: cover;
                border: 2px solid white;
                background: white;
            }}
            .badge-perc {{
                position: absolute;
                top: -6px;
                right: -10px;
                background-color: #ffb300;
                color: black;
                font-size: 9px;
                font-weight: bold;
                padding: 2px 4px;
                border-radius: 10px;
                border: 1px solid white;
            }}
            .player-name {{
                font-size: 11px;
                font-weight: bold;
                margin-top: 6px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}
            .status-box {{
                font-size: 9px;
                font-weight: bold;
                padding: 2px 5px;
                border-radius: 4px;
                display: inline-block;
                margin-top: 4px;
                color: white;
            }}
        </style>
        </head>
        <body>
            <div class="field-grid">
        """
        
        for t in dati["titolari"]:
            html_campo += f"""
                <div class="player-card">
                    <div class="avatar-container">
                        <img src="{t['foto']}" class="avatar">
                        <div class="badge-perc">{t['perc']}</div>
                    </div>
                    <div class="player-name">{t['nome']}</div>
                    <div>
                        <span class="status-box" style="background-color: {t['colore_perc']};">{t['ruolo']} • {t['perc']}</span>
                    </div>
                </div>
            """
            
        html_campo += """
            </div>
        </body>
        </html>
        """
        
        # Renderizza il campo in modo sicuro e pulito
        components.html(html_campo, height=210, scrolling=False)

    with col_panchina:
        st.subheader("Panchina & Riserve")
        
        # Visualizzazione pulita della panchina con FM e Bonus
        for p in dati["panchina"]:
            st.markdown(
                f"<div style='font-size: 13px; border-bottom: 1px solid rgba(100,100,100,0.2); padding: 5px 0;'>"
                f"• <b>{p['nome']}</b> ({p['ruolo']}) - FM: {p['fm']} | <span style='color: #2e7d32; font-weight:bold;'>Bonus: {p['bonus']}</span>"
                f"</div>", 
                unsafe_allow_html=True
            )

else:
    st.info("👋 Usa il menu a sinistra per caricare la tua prima rosa e visualizzare la formazione!")
