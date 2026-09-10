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
        # Salviamo la rosa nel dizionario di sessione
        st.session_state["formazioni_salvate"][nome_nuova_rosa] = {
            "totale_rosa": 25,
            "indice_rosa": "8.6 / 10",
            "modulo": modulo_scelto,
            "titolari": [
                {"nome": "Kvaratskhelia", "ruolo": "A", "perc": "98%", "foto": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"},
                {"nome": "Esposito F.P.", "ruolo": "A", "perc": "85%", "foto": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"},
                {"nome": "Kean", "ruolo": "A", "perc": "92%", "foto": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150"},
                {"nome": "Bastoni", "ruolo": "D", "perc": "75%", "foto": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=150"},
                {"nome": "Mkhitaryan", "ruolo": "C", "perc": "80%", "foto": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150"},
                {"nome": "Barella", "ruolo": "C", "perc": "90%", "foto": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150"},
                {"nome": "Dimarco", "ruolo": "D", "perc": "95%", "foto": "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=150"}
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
        
        # HTML incapsulato nel componente nativo per evitare la stampa del codice a schermo
        html_content = """
        <html>
        <head>
        <style>
            body {
                background-color: #2e7d32;
                margin: 0;
                padding: 15px;
                font-family: sans-serif;
                border-radius: 10px;
            }
            .field-container {
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                justify-content: center;
                align-items: center;
            }
            .player-card {
                text-align: center;
                color: white;
                margin: 5px;
                width: 75px;
            }
            .avatar-box {
                position: relative;
                width: 60px;
                height: 60px;
                margin: 0 auto;
            }
            .avatar-img {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                object-fit: cover;
                border: 2px solid #ffd700;
                background: white;
                box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
            }
            .badge-perc {
                position: absolute;
                top: -6px;
                right: -10px;
                background-color: #ffb300;
                color: black;
                font-size: 10px;
                font-weight: bold;
                padding: 2px 5px;
                border-radius: 20px;
                border: 1px solid white;
            }
            .badge-ruolo {
                position: absolute;
                bottom: -2px;
                left: 50%;
                transform: translateX(-50%);
                background-color: #1976d2;
                color: white;
                font-size: 9px;
                font-weight: bold;
                width: 22px;
                height: 18px;
                border-radius: 10px;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid white;
            }
            .player-name {
                font-size: 11px;
                font-weight: bold;
                margin-top: 8px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                text-shadow: 1px 1px 2px black;
            }
        </style>
        </head>
        <body>
            <div class="field-container">
        """
        
        for t in dati["titolari"]:
            html_content += f"""
                <div class="player-card">
                    <div class="avatar-box">
                        <img src="{t['foto']}" class="avatar-img">
                        <div class="badge-perc">{t['perc']}</div>
                        <div class="badge-ruolo">{t['ruolo']}</div>
                    </div>
                    <div class="player-name">{t['nome']}</div>
                </div>
            """
            
        html_content += """
            </div>
        </body>
        </html>
        """
        
        # Renderizziamo il campo in modo sicuro al 100%
        components.html(html_content, height=190, scrolling=False)

    with col_panchina:
        st.subheader("Panchina & Riserve")
        
        # Visualizzazione pulita della panchina con FM e Bonus
        for p in dati["panchina"]:
            st.markdown(
                f"<div style='font-size: 13px; border-bottom: 1px solid rgba(100,100,100,0.2); padding: 6px 0;'>"
                f"• <b>{p['nome']}</b> ({p['ruolo']}) - FM: {p['fm']} | <span style='color: #2e7d32; font-weight:bold;'>Bonus: {p['bonus']}</span>"
                f"</div>", 
                unsafe_allow_html=True
            )

else:
    st.info("👋 Usa il menu a sinistra per caricare la tua prima rosa e visualizzare la formazione!")
