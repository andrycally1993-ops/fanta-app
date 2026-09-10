import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="FantAlgoritmo Pro - Leghe FC Style", page_icon="⚽", layout="wide")

class FantAlgoritmoPro:
    def __init__(self):
        if 'giocatori' not in st.session_state:
            st.session_state.giocatori = []

    def carica_da_excel(self, uploaded_file):
        try:
            xls = pd.ExcelFile(uploaded_file)
            df = pd.read_excel(uploaded_file, sheet_name=xls.sheet_names[0])
            
            # Normalizziamo i nomi delle colonne per trovarle facilmente
            col_mapping = {str(c).strip().lower(): c for c in df.columns}
            
            # Cerca colonne chiave
            c_nome = next((col_mapping[c] for c in col_mapping if 'nome' in c or 'giocatore' in c), df.columns[0])
            c_ruolo = next((col_mapping[c] for c in col_mapping if 'ruolo' in c), df.columns[1] if len(df.columns) > 1 else None)
            c_fm = next((col_mapping[c] for c in col_mapping if 'fanta' in c or 'media' in c or 'fm' in c), None)
            c_val = next((col_mapping[c] for c in col_mapping if 'quotazione' in c or 'valore' in c or 'qt' in c), None)
            
            count = 0
            st.session_state.giocatori = [] # Reset e carica la nuova rosa
            
            for _, riga in df.iterrows():
                nome = str(riga[c_nome]).strip() if c_nome in df.columns else "Sconosciuto"
                if not nome or nome == "nan": continue
                
                ruolo = "C"
                if c_ruolo and c_ruolo in df.columns:
                    r_cand = str(riga[c_ruolo]).strip().upper().replace('*', '')
                    if r_cand in ['P', 'D', 'C', 'A']:
                        ruolo = r_cand
                
                fanta_media = 6.5
                if c_fm and c_fm in df.columns:
                    try: fanta_media = float(str(riga[c_fm]).replace(',', '.'))
                    except: pass
                    
                valore_mercato = 10
                if c_val and c_val in df.columns:
                    try: valore_mercato = int(float(str(riga[c_val]).replace(',', '.')))
                    except: pass
                
                # Avatar predefinito pulito (può essere sostituito se il file ha foto)
                avatar_url = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80"
                
                giocatore = {
                    "nome": nome,
                    "ruolo": ruolo,
                    "fanta_media": fanta_media,
                    "valore_mercato": valore_mercato,
                    "titolarita": 90.0 if fanta_media > 6.5 else 70.0,
                    "avatar": avatar_url
                }
                st.session_state.giocatori.append(giocatore)
                count += 1
            return count
        except Exception as e:
            st.error(f"Errore nella lettura del file Excel: {e}")
            return 0

    def calcola_formazione(self, modulo="3-4-3"):
        lista = st.session_state.giocatori
        
        portieri = sorted([g for g in lista if g["ruolo"] == 'P'], key=lambda x: (x["titolarita"], x["fanta_media"]), reverse=True)
        difensori = sorted([g for g in lista if g["ruolo"] == 'D'], key=lambda x: (x["titolarita"], x["fanta_media"]), reverse=True)
        centrocampisti = sorted([g for g in lista if g["ruolo"] == 'C'], key=lambda x: (x["titolarita"], x["fanta_media"]), reverse=True)
        attaccanti = sorted([g for g in lista if g["ruolo"] == 'A'], key=lambda x: (x["titolarita"], x["fanta_media"]), reverse=True)

        try:
            mod_parti = [int(x) for x in modulo.split("-")]
            num_d, num_c, num_a = mod_parti[0], mod_parti[1], mod_parti[2]
        except:
            num_d, num_c, num_a = 3, 4, 3

        formazione = {
            "Portiere": portieri[:1] if portieri else [],
            "Difesa": difensori[:num_d],
            "Centrocampo": centrocampisti[:num_c],
            "Attacco": attaccanti[:num_a]
        }
        
        titolari_nomi = [g['nome'] for reparto in formazione.values() for g in reparto]
        
        panchina_p = [g for g in portieri if g['nome'] not in titolari_nomi][:1]
        panchina_d = [g for g in difensori if g['nome'] not in titolari_nomi][:3]
        panchina_c = [g for g in centrocampisti if g['nome'] not in titolari_nomi][:3]
        panchina_a = [g for g in attaccanti if g['nome'] not in titolari_nomi][:2]

        formazione["Panchina"] = panchina_p + panchina_d + panchina_c + panchina_a
        return formazione

app = FantAlgoritmoPro()

# ==========================================
# STYLING CSS: CAMPO REALISTICO & CARD COMPATTE
# ==========================================
st.markdown("""
<style>
.stApp {
    background-color: #0e1726;
    color: #ffffff;
}
/* Stile Campo da Calcio Realistico */
.campo-reale {
    background: repeating-linear-gradient(
        0deg,
        #1e4d2b,
        #1e4d2b 60px,
        #245e35 60px,
        #245e35 120px
    );
    border: 3px solid #ffffff;
    border-radius: 12px;
    padding: 20px 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    position: relative;
    min-height: 580px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
/* Linea di metà campo e cerchio centrale simulati in CSS */
.campo-reale::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 3px;
    background: rgba(255, 255, 255, 0.6);
}
.campo-reale::after {
    content: "";
    position: absolute;
    top: calc(50% - 50px);
    left: calc(50% - 50px);
    width: 100px;
    height: 100px;
    border: 3px solid rgba(255, 255, 255, 0.6);
    border-radius: 50%;
}

.reparto-line {
    display: flex;
    justify-content: center;
    gap: 14px;
    z-index: 5;
    margin: 5px 0;
    flex-wrap: wrap;
}

/* Card Giocatore Compatta stile Leghe FC (Senza buchi, unita) */
.leghefc-card {
    background: #111827;
    border: 2px solid #374151;
    border-radius: 8px;
    width: 88px;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    overflow: hidden;
    position: relative;
}
.card-header-lf {
    background: #1f2937;
    font-size: 9px;
    font-weight: bold;
    color: #9ca3af;
    padding: 2px 0;
    border-bottom: 1px solid #374151;
}
.card-body-lf {
    padding: 4px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.lf-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 3px;
    border: 2px solid #10b981;
}
.lf-name {
    font-weight: 700;
    font-size: 10px;
    color: #ffffff;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
}
.lf-info {
    font-size: 8px;
    color: #d1d5db;
    margin-top: 1px;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR PER CARICARE IL FILE EXCEL
with st.sidebar:
    st.header("📁 Carica Rosa Excel")
    uploaded_file = st.file_uploader("Carica file .xlsx", type=["xlsx", "xls"])

    if uploaded_file is not None:
        num_caricati = app.carica_da_excel(uploaded_file)
        if num_caricati > 0:
            st.success(f"Caricati con successo {num_caricati} giocatori!")

    if st.button("🗑️ Svuota Rosa"):
        st.session_state.giocatori = []
        st.rerun()

# INTERFACCIA PRINCIPALE
st.title("⚽ FantAlgoritmo - Formazione Leghe FC")

if not st.session_state.giocatori:
    st.info("👈 Carica il file Excel (`.xlsx`) dalla barra laterale per visualizzare il campo e la formazione.")
else:
    c1, c2, c3 = st.columns([2, 2, 3])
    with c1:
        modulo_scelto = st.selectbox("Modulo:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])
    with c2:
        st.metric(label="Totale Calciatori in Rosa", value=len(st.session_state.giocatori))
    with c3:
        st.write("")

    formazione = app.calcola_formazione(modulo_scelto)
    st.markdown("---")

    col_campo, col_panchina = st.columns([3, 2])

    with col_campo:
        st.subheader(f"🏟️ Campo da Gioco ({modulo_scelto})")
        
        # Generazione HTML del Campo Reale
        html_campo = "<div class='campo-reale'>"
        
        def render_card_lf(g):
            return f"""
            <div class='leghefc-card'>
                <div class='card-header-lf'>{g['ruolo']} • {g['fanta_media']}</div>
                <div class='card-body-lf'>
                    <img src='{g['avatar']}' class='lf-avatar' />
                    <div class='lf-name'>{g['nome']}</div>
                    <div class='lf-info'>FM: {g['fanta_media']}</div>
                </div>
            </div>"""

        # Attacco
        html_campo += "<div class='reparto-line'>"
        for g in formazione["Attacco"]: html_campo += render_card_lf(g)
        html_campo += "</div>"

        # Centrocampo
        html_campo += "<div class='reparto-line'>"
        for g in formazione["Centrocampo"]: html_campo += render_card_lf(g)
        html_campo += "</div>"

        # Difesa
        html_campo += "<div class='reparto-line'>"
        for g in formazione["Difesa"]: html_campo += render_card_lf(g)
        html_campo += "</div>"

        # Portiere
        html_campo += "<div class='reparto-line'>"
        for g in formazione["Portiere"]: html_campo += render_card_lf(g)
        html_campo += "</div>"

        html_campo += "</div>"
        st.markdown(html_campo, unsafe_allow_html=True)

    with col_panchina:
        st.subheader("🪑 Panchina & Riserve")
        with st.container(border=True):
            if formazione["Panchina"]:
                for p in formazione["Panchina"]:
                    st.markdown(f"- **{p['nome']}** ({p['ruolo']}) - FM: {p['fanta_media']}")
            else:
                st.write("Nessun panchinaro disponibile.")
