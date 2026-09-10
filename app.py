import streamlit as st
import csv
import io

# Configurazione pagina a tutto schermo
st.set_page_config(page_title="FantAlgoritmo Pro - Ultimate", page_icon="⚽", layout="wide")

class FantAlgoritmoPro:
    def __init__(self):
        if 'giocatori' not in st.session_state:
            st.session_state.giocatori = []

    def aggiungi_giocatore(self, nome, ruolo, fanta_media, valore_mercato, presenze_stimate=0.9):
        try:
            f_media = float(str(fanta_media).strip().replace(',', '.')) if fanta_media else 6.5
            v_mercato = int(float(str(valore_mercato).strip().replace(',', '.'))) if valore_mercato else 10
        except (ValueError, TypeError):
            f_media = 6.5
            v_mercato = 10

        nome_lower = str(nome).lower()
        
        fattore_titolarita = presenze_stimate
        if "provedel" in nome_lower:
            fattore_titolarita = 0.4  # Gestione portiere panchinaro
        elif "vicario" in nome_lower:
            fattore_titolarita = 0.99 # Gestione portiere titolare fisso

        score_affidabilita = (f_media * 0.7) + (fattore_titolarita * 3.0)
        
        giocatore = {
            "nome": str(nome).strip(),
            "ruolo": str(ruolo).strip().upper(),
            "fanta_media": f_media,
            "valore_mercato": v_mercato,
            "titolarita": fattore_titolarita,
            "score": round(score_affidabilita, 2)
        }
        
        if not any(g['nome'].lower() == giocatore['nome'].lower() for g in st.session_state.giocatori):
            st.session_state.giocatori.append(giocatore)
            return True
        return False

    def calcola_formazione(self, modulo="3-4-3"):
        lista = st.session_state.giocatori
        
        # Sicurezza sui dizionari esistenti senza chiave titolarita
        for g in lista:
            if "titolarita" not in g:
                g["titolarita"] = 0.9

        portieri = sorted([g for g in lista if g["ruolo"] == 'P'], key=lambda x: (x.get("titolarita", 0.9), x["fanta_media"]), reverse=True)
        difensori = sorted([g for g in lista if g["ruolo"] == 'D'], key=lambda x: (x.get("titolarita", 0.9), x["fanta_media"]), reverse=True)
        centrocampisti = sorted([g for g in lista if g["ruolo"] == 'C'], key=lambda x: (x.get("titolarita", 0.9), x["fanta_media"]), reverse=True)
        attaccanti = sorted([g for g in lista if g["ruolo"] == 'A'], key=lambda x: (x.get("titolarita", 0.9), x["fanta_media"]), reverse=True)

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

    def genera_scambi(self):
        consigli = []
        lista = st.session_state.giocatori
        if not lista:
            return ["Carica la rosa per sbloccare i consigli."]
        for g in lista:
            if g["fanta_media"] < 6.0 and g["ruolo"] in ['C', 'A']:
                consigli.append(f"⚠️ **{g['nome']} ({g['ruolo']})**: Rendimento basso (FM {g['fanta_media']}). **Valuta cessione / scambio.**")
        if not consigli:
            consigli.append("✅ Rosa in salute e ottimizzata!")
        return consigli

app = FantAlgoritmoPro()

# ==========================================
# STYLING GRAFICA MODERNA (STILE APP PRO)
# ==========================================
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #ffffff;
}
.campo-pro {
    background: linear-gradient(180deg, #1e3a1e 0%, #112611 100%);
    border: 3px solid rgba(255, 255, 255, 0.2);
    border-radius: 20px;
    padding: 30px 10px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 560px;
    background-image: 
        linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
    background-size: 100% 100%;
}
.campo-pro::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 5%;
    width: 90%;
    height: 2px;
    background: rgba(255, 255, 255, 0.2);
}
.reparto-row {
    display: flex;
    justify-content: center;
    gap: 18px;
    z-index: 2;
    margin: 6px 0;
    flex-wrap: wrap;
}
.player-badge {
    background: rgba(30, 41, 59, 0.9);
    border: 2px solid #38bdf8;
    border-radius: 12px;
    padding: 8px 10px;
    text-align: center;
    width: 115px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.4);
}
.player-avatar {
    width: 38px;
    height: 38px;
    background: #475569;
    border-radius: 50%;
    margin: 0 auto 5px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    border: 1px solid #94a3b8;
}
.player-name-pro {
    font-weight: 700;
    font-size: 12px;
    color: #f8fafc;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.player-sub {
    font-size: 9px;
    color: #38bdf8;
    margin-top: 2px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR: GESTIONE ROSA
with st.sidebar:
    st.header("📁 Caricamento Rosa")
    uploaded_file = st.file_uploader("Carica file CSV Leghe FC", type=["csv"])

    if uploaded_file is not None:
        try:
            stringa_dati = uploaded_file.getvalue().decode("utf-8", errors="ignore")
            f = io.StringIO(stringa_dati)
            sample = f.read(2048)
            f.seek(0)
            delimiter = ';' if ';' in sample else ','
            
            reader = csv.reader(f, delimiter=delimiter)
            righe = list(reader)
            count = 0
            
            if righe:
                header = [str(h).strip().lower() for h in righe[0]]
                idx_nome, idx_ruolo, idx_fm, idx_val = 0, 1, -1, -1
                
                for i, h in enumerate(header):
                    if 'nome' in h or 'giocatore' in h: idx_nome = i
                    elif 'ruolo' in h: idx_ruolo = i
                    elif 'fanta' in h or 'media' in h or 'fm' in h: idx_fm = i
                    elif 'quotazione' in h or 'valore' in h or 'qt' in h: idx_val = i

                for riga in righe[1:]:
                    if not riga or len(riga) < 2: continue
                    try:
                        nome = riga[idx_nome] if idx_nome < len(riga) else riga[0]
                        
                        ruolo = "C"
                        for item in riga:
                            item_clean = str(item).strip().upper().replace('*','')
                            if item_clean in ['P', 'D', 'C', 'A']:
                                ruolo = item_clean
                                break
                        if idx_ruolo < len(riga):
                            r_cand = str(riga[idx_ruolo]).strip().upper().replace('*','')
                            if r_cand in ['P', 'D', 'C', 'A']: ruolo = r_cand

                        fanta_media = 6.5
                        if idx_fm != -1 and idx_fm < len(riga):
                            try: fanta_media = float(str(riga[idx_fm]).replace(',', '.'))
                            except: pass

                        valore_mercato = 15
                        if idx_val != -1 and idx_val < len(riga):
                            try: valore_mercato = int(float(str(riga[idx_val]).replace(',', '.')))
                            except: pass

                        if app.aggiungi_giocatore(nome, ruolo, fanta_media, valore_mercato):
                            count += 1
                    except:
                        continue
                        
            if count > 0:
                st.success(f"Caricati {count} giocatori con successo!")
            else:
                st.warning("Controlla il formato del file CSV.")
        except Exception as e:
            st.error(f"Errore: {e}")

    if st.button("🗑️ Svuota Rosa"):
        st.session_state.giocatori = []
        st.rerun()

# CORPO PRINCIPALE
st.title("⚽ FantAlgoritmo Pro - Campo Live")

if not st.session_state.giocatori:
    st.info("👈 Carica il file CSV della tua rosa dal menu laterale per generare la formazione sul campo grafico.")
else:
    col_m1, col_m2 = st.columns([2, 4])
    with col_m1:
        modulo_scelto = st.selectbox("🎯 Modulo Tattico:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])
    with col_m2:
        st.write(f"📊 **Rosa Totale:** {len(st.session_state.giocatori)} Calciatori")

    formazione = app.calcola_formazione(modulo_scelto)
    st.markdown("---")

    col_campo, col_lato = st.columns([3, 2])

    with col_campo:
        st.subheader(f"🏟️ Formazione Titolare ({modulo_scelto})")
        
        html_campo = "<div class='campo-pro'>"
        
        # 1. Attacco
        html_campo += "<div class='reparto-row'>"
        for g in formazione["Attacco"]:
            html_campo += f"""
            <div class='player-badge'>
                <div class='player-avatar'>⚽</div>
                <div class='player-name-pro'>{g['nome']}</div>
                <div class='player-sub'>A • FM {g['fanta_media']}</div>
            </div>"""
        html_campo += "</div>"

        # 2. Centrocampo
        html_campo += "<div class='reparto-row'>"
        for g in formazione["Centrocampo"]:
            html_campo += f"""
            <div class='player-badge'>
                <div class='player-avatar'>⚽</div>
                <div class='player-name-pro'>{g['nome']}</div>
                <div class='player-sub'>C • FM {g['fanta_media']}</div>
            </div>"""
        html_campo += "</div>"

        # 3. Difesa
        html_campo += "<div class='reparto-row'>"
        for g in formazione["Difesa"]:
            html_campo += f"""
            <div class='player-badge'>
                <div class='player-avatar'>🛡️</div>
                <div class='player-name-pro'>{g['nome']}</div>
                <div class='player-sub'>D • FM {g['fanta_media']}</div>
            </div>"""
        html_campo += "</div>"

        # 4. Portiere
        html_campo += "<div class='reparto-row'>"
        for g in formazione["Portiere"]:
            html_campo += f"""
            <div class='player-badge' style='border-color: #facc15;'>
                <div class='player-avatar'>🧤</div>
                <div class='player-name-pro'>{g['nome']}</div>
                <div class='player-sub' style='color: #facc15;'>P • FM {g['fanta_media']}</div>
            </div>"""
        html_campo += "</div>"

        html_campo += "</div>"
        
        st.markdown(html_campo, unsafe_allow_html=True)

        # PANCHINA
        with st.container(border=True):
            st.markdown("### 🪑 Panchina Consigliata")
            if formazione["Panchina"]:
                panchina_testo = " • ".join([f"**{g['nome']}** ({g['ruolo']} - FM: {g['fanta_media']})" for g in formazione["Panchina"]])
                st.markdown(panchina_testo)
            else:
                st.write("Panchina vuota.")

    with col_lato:
        st.subheader("💡 Consigli & Scambi")
        with st.container(border=True):
            for consiglio in app.genera_scambi():
                st.markdown(consiglio)
