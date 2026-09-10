import streamlit as st
import csv
io_module = __import__('io')

class FantAlgoritmoV3_3:
    def __init__(self):
        if 'giocatori' not in st.session_state:
            st.session_state.giocatori = []

    def aggiungi_giocatore(self, nome, ruolo, fanta_media, indice_partita, titolarita, bonus_malus_score, valore_mercato):
        try:
            f_media = float(str(fanta_media).strip())
            i_partita = int(str(indice_partita).strip())
            titol = float(str(titolarita).strip())
            b_malus = float(str(bonus_malus_score).strip())
            v_mercato = int(str(valore_mercato).strip())
        except (ValueError, TypeError):
            return False

        # Algoritmo di schierabilità v3.3
        score_schierabilita = ((f_media + b_malus) * titol) - (i_partita * 0.3)
        
        giocatore = {
            "nome": str(nome).strip(),
            "ruolo": str(ruolo).strip().upper(),
            "fanta_media": f_media,
            "indice_partita": i_partita,
            "titolarita": titol,
            "bonus_malus_score": b_malus,
            "valore_mercato": v_mercato,
            "score": round(score_schierabilita, 2)
        }
        
        # Evita duplicati
        if not any(g['nome'].lower() == giocatore['nome'].lower() for g in st.session_state.giocatori):
            st.session_state.giocatori.append(giocatore)
            return True
        return False

    def calcola_formazione_automatica(self, modulo="3-4-3"):
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

    def genera_consigli_scambi(self):
        consigli = []
        lista = st.session_state.giocatori
        if not lista:
            return ["Carica la tua rosa per sbloccare i consigli sugli scambi!"]

        medie_reparti = {}
        for r, nome_r in [('P', 'Porta'), ('D', 'Difesa'), ('C', 'Centrocampo'), ('A', 'Attacco')]:
            giocatori_reparto = [g["fanta_media"] for g in lista if g["ruolo"] == r]
            medie_reparti[nome_r] = sum(giocatori_reparto) / len(giocatori_reparto) if giocatori_reparto else 0

        if medie_reparti:
            reparto_debole = min(medie_reparti, key=medie_reparti.get)
            consigli.append(f"🎯 **Reparto Critico**: Il tuo reparto con la media più bassa è la **{reparto_debole}** ({round(medie_reparti[reparto_debole], 2)}). Cerca un rinforzo urgente tramite scambio.")

        for g in lista:
            if g["titolarita"] < 0.65 and g["valore_mercato"] > 25:
                consigli.append(f"🔄 **Scambio in Uscita**: **{g['nome']} ({g['ruolo']})** ha un valore alto ({g['valore_mercato']}) ma titolarità bassa ({int(g['titolarita']*100)}%). Usalo per uno scambio vantaggioso.")
            elif g["fanta_media"] < 6.0 and g["ruolo"] in ['C', 'A'] and g["indice_partita"] > 3:
                consigli.append(f"⚠️ **Da Tagliare/Scambiare**: **{g['nome']}** sta rendendo poco (Fanta-media {g['fanta_media']}) e ha una partita difficile. Valuta la cessione.")

        return consigli

# ==========================================
# INTERFACCIA STREAMLIT
# ==========================================
st.title("⚽ FantAlgoritmo v3.3 - Smart Manager")

app = FantAlgoritmoV3_3()

st.sidebar.header("📁 Carica la tua Rosa")
st.sidebar.write("Carica il file CSV della tua squadra con un click:")

# TASTO UFFICIALE DI UPLOAD FILE
uploaded_file = st.sidebar.file_uploader("Scegli file CSV", type=["csv"])

if uploaded_file is not None:
    try:
        stringa_dati = uploaded_file.getvalue().decode("utf-8")
        f = io_module.StringIO(stringa_dati)
        reader = csv.reader(f)
        count = 0
        for riga in reader:
            if not riga or riga[0].lower() in ['nome', 'giocatore']:
                continue
            if len(riga) >= 7:
                if app.aggiungi_giocatore(riga[0], riga[1], riga[2], riga[3], riga[4], riga[5], riga[6]):
                    count += 1
        st.sidebar.success(f"Caricati con successo {count} giocatori!")
    except Exception as e:
        st.sidebar.error(f"Errore nella lettura del file: {e}")

if st.sidebar.button("🗑️ Svuota Rosa"):
    st.session_state.giocatori = []
    st.sidebar.warning("Rosa azzerata.")

# CORPO PRINCIPALE
st.subheader("📋 Stato Attuale Rosa")
if not st.session_state.giocatori:
    st.info("👈 Usa il pannello a sinistra per caricare il file della tua rosa tramite il tasto di upload.")
else:
    st.write(Giocatori in rosa := f"Giocatori totali caricati: **{len(st.session_state.giocatori)}**")
    
    st.markdown("---")
    st.subheader("🤖 Motore di Calcolo")
    modulo_scelto = st.selectbox("Seleziona il Modulo Tattico:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])
    
    if st.button("🚀 Genera Formazione Ideale & Scambi"):
        formazione = app.calcola_formazione_automatica(modulo_scelto)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### 📋 Formazione Titolare ({modulo_scelto})")
            for reparto, giocatori in formazione.items():
                if reparto != "Panchina":
                    st.markdown(f"**{reparto}:**")
                    for g in giocatori:
                        st.write(f"- **{g['nome']}** | Score: `{g['score']}` (FM: {g['fanta_media']} | Titol: {int(g['titolarita']*100)}%)")
            
            st.markdown("### 🪑 Panchina Consigliata")
            for g in formazione["Panchina"]:
                st.write(f"- {g['nome']} ({g['ruolo']}) | Score: `{g['score']}`")

        with col2:
            st.markdown("### 🔄 Consigli Scambi Consigliati")
            for consiglio in app.genera_consigli_scambi():
                st.warning(consiglio)
