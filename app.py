import streamlit as st
import pandas as pd
import io
import csv

st.set_page_config(page_title="FantAlgoritmo Pro - FantaLab Style", page_icon="⚽", layout="wide")

class FantAlgoritmoPro:
    def __init__(self):
        if 'giocatori' not in st.session_state:
            st.session_state.giocatori = []

    def carica_file(self, uploaded_file):
        try:
            file_name = uploaded_file.name.lower()
            
            if file_name.endswith(('.xlsx', '.xls')):
                xls = pd.ExcelFile(uploaded_file)
                df = pd.read_excel(uploaded_file, sheet_name=xls.sheet_names[0])
            else:
                stringa_dati = uploaded_file.getvalue().decode("utf-8", errors="ignore")
                f = io.StringIO(stringa_dati)
                sample = f.read(2048)
                f.seek(0)
                delimiter = ';' if ';' in sample else ','
                df = pd.read_csv(f, delimiter=delimiter)

            col_mapping = {str(c).strip().lower(): c for c in df.columns}
            
            c_nome = next((col_mapping[c] for c in col_mapping if 'nome' in c or 'giocatore' in c), df.columns[0])
            c_ruolo = next((col_mapping[c] for c in col_mapping if 'ruolo' in c), None)
            c_fm = next((col_mapping[c] for c in col_mapping if 'fanta' in c or 'media' in c or 'fm' in c), None)
            c_val = next((col_mapping[c] for c in col_mapping if 'quotazione' in c or 'valore' in c or 'qt' in c), None)
            c_foto = next((col_mapping[c] for c in col_mapping if 'foto' in c or 'img' in c or 'immagine' in c or 'url' in c), None)
            
            count = 0
            temp_giocatori = []
            
            for _, riga in df.iterrows():
                nome = str(riga[c_nome]).strip() if c_nome in df.columns else ""
                if not nome or nome.lower() == "nan": continue
                
                ruolo = "C"
                if c_ruolo and c_ruolo in df.columns:
                    r_cand = str(riga[c_ruolo]).strip().upper().replace('*', '')
                    if r_cand in ['P', 'D', 'C', 'A']:
                        ruolo = r_cand
                else:
                    for val in riga.values:
                        v_str = str(val).strip().upper().replace('*', '')
                        if v_str in ['P', 'D', 'C', 'A']:
                            ruolo = v_str
                            break

                fanta_media = 6.5
                if c_fm and c_fm in df.columns:
                    try: fanta_media = float(str(riga[c_fm]).replace(',', '.'))
                    except: pass
                    
                valore_mercato = 10
                if c_val and c_val in df.columns:
                    try: valore_mercato = int(float(str(riga[c_val]).replace(',', '.')))
                    except: pass
                
                # Cerca l'immagine reale dal file, altrimenti usa un'icona di default neutra
                avatar_url = ""
                if c_foto and c_foto in df.columns:
                    val_foto = str(riga[c_foto]).strip()
                    if val_foto and val_foto.lower() != "nan":
                        avatar_url = val_foto
                
                if not avatar_url:
                    # Avatar generico con sagoma o stile caricaturale pulito
                    avatar_url = "https://cdn-icons-png.flaticon.com/512/149/149071.png"

                titolarita = 95.0 if fanta_media > 6.8 else (65.0 if fanta_media > 6.0 else 30.0)
                
                giocatore = {
                    "nome": nome,
                    "ruolo": ruolo,
                    "fanta_media": fanta_media,
                    "valore_mercato": valore_mercato,
                    "titolarita": titolarita,
                    "avatar": avatar_url
                }
                temp_giocatori.append(giocatore)
                count += 1
                
            if count > 0:
                st.session_state.giocatori = temp_giocatori
            return count
        except Exception as e:
            st.error(f"Errore nel caricamento del file: {e}")
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
# STYLING CSS
# ==========================================
st.markdown("""
<style>
.stApp {
    background-color: #0d1523;
    color: #ffffff;
}
.campo-reale {
    background: repeating-linear-gradient(
        0deg,
        #1e4d2b,
        #1e4d2b 60px,
        #245e35 60px,
        #245e35 120px
    );
    border: 4px solid #ffffff;
    border-radius: 14px;
    padding: 30px 10px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.7);
    position: relative;
    min-height: 640px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.campo-reale::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 0;
    width: 100%;
    height: 3px;
    background: rgba(255, 255, 255, 0.75);
}
.campo-reale::after {
    content: "";
    position: absolute;
    top: calc(50% - 55px);
    left: calc(50% - 55px);
    width: 110px;
    height: 110px;
    border: 3px solid rgba(255, 255, 255, 0.75);
    border-radius: 50%;
}
.reparto-line {
    display: flex;
    justify-content: center;
    gap: 14px;
    z-index: 5;
    margin: 6px 0;
    flex-wrap: wrap;
}
.fantalab-player-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 82px;
    text-align: center;
}
.fl-avatar-container {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    overflow: hidden;
    background: #2a4365;
    border: 2px solid #ffffff;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.fl-avatar-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.fl-player-name {
    font-weight: 700;
    font-size: 10px;
    color: #ffffff;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
}
.bar-container {
    width: 60px;
    height: 5px;
    background: rgba(0,0,0,0.5);
    border-radius: 3px;
    margin-top: 2px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.2);
}
.bar-fill-green { height: 100%; background: #22c55e; }
.bar-fill-yellow { height: 100%; background: #eab308; }
.bar-fill-red { height: 100%; background: #ef4444; }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header("📁 Gestione Rosa")
    uploaded_file = st.file_uploader("Carica file Rosa (.xlsx, .csv)", type=["xlsx", "xls", "csv"])

    if uploaded_file is not None:
        num = app.carica_file(uploaded_file)
        if num > 0:
            st.success(f"Caricati {num} calciatori correttamente!")

    if st.button("🗑️ Svuota Rosa"):
        st.session_state.giocatori = []
        st.rerun()

# INTERFACCIA PRINCIPALE
st.title("⚽ FantAlgoritmo - Formazione Titolare")

if not st.session_state.giocatori:
    st.info("👈 Carica il file della rosa dalla barra laterale per visualizzare il campo.")
else:
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        modulo_scelto = st.selectbox(
            "Modulo:", 
            ["3-4-3", "3-5-2", "4-3-3", "4-4-2", "4-5-1", "5-3-2", "5-4-1"]
        )
    with c2:
        st.markdown(f"<div style='padding-top: 8px;'><span style='color: #93c5fd; font-size: 14px;'>Totale Rosa:</span> <b style='color: #ffffff; font-size: 16px;'>{len(st.session_state.giocatori)}</b></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div style='padding-top: 8px;'><span style='color: #93c5fd; font-size: 14px;'>Indice Rosa:</span> <b style='color: #34d399; font-size: 16px;'>8.6 / 10</b></div>", unsafe_allow_html=True)

    formazione = app.calcola_formazione(modulo_scelto)
    st.markdown("---")

    col_campo, col_panchina = st.columns([3, 2])

    with col_campo:
        st.subheader(f"🏟️ Campo Titolari ({modulo_scelto})")
        
        html_campo = "<div class='campo-reale'>"
        
        def render_player_card(g):
            tit = g.get('titolarita', 85)
            if tit >= 75:
                bar_class = "bar-fill-green"
            elif tit >= 40:
                bar_class = "bar-fill-yellow"
            else:
                bar_class = "bar-fill-red"
                
            return f"""
            <div class='fantalab-player-card'>
                <div class='fl-avatar-container'>
                    <img src='{g['avatar']}' class='fl-avatar-img' />
                </div>
                <div class='fl-player-name'>{g['nome']}</div>
                <div class='bar-container'>
                    <div class='{bar_class}' style='width: {int(tit)}%;'></div>
                </div>
            </div>"""

        # Attacco
        html_campo += "<div class='reparto-line'>"
        for g in formazione["Attacco"]: html_campo += render_player_card(g)
        html_campo += "</div>"

        # Centrocampo
        html_campo += "<div class='reparto-line'>"
        for g in formazione["Centrocampo"]: html_campo += render_player_card(g)
        html_campo += "</div>"

        # Difesa
        html_campo += "<div class='reparto-line'>"
        for g in formazione["Difesa"]: html_campo += render_player_card(g)
        html_campo += "</div>"

        # Portiere
        html_campo += "<div class='reparto-line'>"
        for g in formazione["Portiere"]: html_campo += render_player_card(g)
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
