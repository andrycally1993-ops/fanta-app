import streamlit as st
import csv
import io

# Configurazione pagina per sfruttare tutto lo spazio (stile app professionale)
st.set_page_config(page_title="FantAlgoritmo Pro", page_icon="⚽", layout="wide")

class FantAlgoritmoPro:
    def __init__(self):
        if 'giocatori' not in st.session_state:
            st.session_state.giocatori = []

    def aggiungi_giocatore(self, nome, ruolo, fanta_media, valore_mercato):
        try:
            f_media = float(str(fanta_media).strip().replace(',', '.')) if fanta_media else 6.5
            v_mercato = int(float(str(valore_mercato).strip().replace(',', '.'))) if valore_mercato else 10
        except (ValueError, TypeError):
            f_media = 6.5
            v_mercato = 10

        # Parametri standard per calcolo score
        indice_partita = 2
        titolarita = 0.85
        bonus_malus = 0.0

        score_schierabilita = ((f_media + bonus_malus) * titolarita) - (indice_partita * 0.3)
        
        giocatore = {
            "nome": str(nome).strip(),
            "ruolo": str(ruolo).strip().upper(),
            "fanta_media": f_media,
            "valore_mercato": v_mercato,
            "score": round(score_schierabilita, 2)
        }
        
        if not any(g['nome'].lower() == giocatore['nome'].lower() for g in st.session_state.giocatori):
            st.session_state.giocatori.append(giocatore)
            return True
        return False

    def calcola_formazione(self, modulo="3-4-3"):
        lista = st.session_state.giocatori
        portieri = sorted([g for g in lista if g["ruolo"] == 'P'], key=lambda x: x["score"], reverse=True)
        difensori = sorted([g for g in lista if g["ruolo"] == 'D'], key=lambda x: x["score"], reverse=True)
        centrocampisti = sorted([g for g in lista if g["ruolo"] == 'C'], key=lambda x: x["score"], reverse=True)
        attaccanti = sorted([g for g in lista if g["ruolo"] == 'A'], key=lambda x: x["score"], reverse=True)

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
            return ["Carica la tua rosa per ricevere consigli mirati."]
        
        for g in lista:
            if g["fanta_media"] < 6.0 and g["ruolo"] in ['C', 'A']:
                consigli.append(f"⚠️ **Attenzione a {g['nome']} ({g['ruolo']})**: Fanta-media bassa ({g['fanta_media']}). Valuta uno scambio.")
            elif g["valore_mercato"] > 30 and g["fanta_media"] < 6.5:
                consigli.append(f"🔄 **Opportunità Scambio**: {g['nome']} ha un'alta quotazione ({g['valore_mercato']}) ma rendimento altalenante. Ottimo da cedere.")
        
        if not consigli:
            consigli.append("✅ La tua rosa è ben bilanciata al momento!")
        return consigli

app = FantAlgoritmoPro()

# ==========================================
# INTERFACCIA GRAFICA STILE APPLICAZIONE
# ==========================================
st.title("⚽ FantAlgoritmo - Live Manager")
st.markdown("Gestione automatica della formazione e consigli intelligenti per la tua rosa.")

# Sidebar per il caricamento file
with st.sidebar:
    st.header("📁 Gestione Rosa")
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
                # Trova indici intestazione intelligenti
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
                        
                        # Cerca il ruolo corretto (P, D, C, A)
                        ruolo = "C"
                        for item in riga:
                            item_clean = str(item).strip().upper()
                            if item_clean in ['P', 'D', 'C', 'A'] or item_clean in ['P*', 'D*', 'C*', 'A*']:
                                ruolo = item_clean.replace('*', '')
                                break
                        if idx_ruolo < len(riga) and str(riga[idx_ruolo]).strip().upper().replace('*','') in ['P', 'D', 'C', 'A']:
                            ruolo = str(riga[idx_ruolo]).strip().upper().replace('*','')

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
                st.success(f"Caricati {count} giocatori correttamente!")
            else:
                st.warning("Verifica il formato del file CSV.")
        except Exception as e:
            st.error(f"Errore: {e}")

    if st.button("🗑️ Svuota Rosa"):
        st.session_state.giocatori = []
        st.rerun()

# CORPO PRINCIPALE
if not st.session_state.giocatori:
    st.info("👋 **Benvenuto!** Carica il file CSV della tua squadra dal pannello a sinistra per visualizzare subito la formazione ottimizzata.")
else:
    # Sezione Modulo interattivo (Aggiornamento in tempo reale senza bottoni)
    col_mod1, col_mod2 = st.columns([2, 4])
    with col_mod1:
        modulo_scelto = st.selectbox("🎯 Modulo Tattico:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])
    with col_mod2:
        st.write(f"📊 **Giocatori in rosa:** {len(st.session_state.giocatori)}")

    formazione = app.calcola_formazione(modulo_scelto)

    st.markdown("---")
    
    # Layout Grafico a Colonne (Simulazione Campo / Reparti Ordinati)
    col_campo, col_mercato = st.columns([3, 2])

    with col_campo:
        st.subheader(f"📋 Formazione Titolare ({modulo_scelto})")
        
        for reparto, giocatori in formazione.items():
            if reparto != "Panchina":
                with st.container(border=True):
                    st.markdown(f"**🟢 {reparto}**")
                    if giocatori:
                        for g in giocatori:
                            st.markdown(f"- **{g['nome']}** | ⚽ Fanta-Media: `{g['fanta_media']}` | 📈 Score: `{g['score']}`")
                    else:
                        st.write("*(Nessun giocatore disponibile per questo reparto)*")

        with st.container(border=True):
            st.markdown("**🪑 Panchina Consigliata**")
            if formazione["Panchina"]:
                for g in formazione["Panchina"]:
                    st.markdown(f"- {g['nome']} ({g['ruolo']}) | Score: `{g['score']}`")
            else:
                st.write("*(Panchina vuota)*")

    with col_mercato:
        st.subheader("💡 Consigli & Scambi")
        with st.container(border=True):
            for consiglio in app.genera_scambi():
                st.markdown(consiglio)
