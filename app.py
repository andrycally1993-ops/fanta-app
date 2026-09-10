import streamlit as st
import csv
import io

class FantAlgoritmoV3_2:
    def __init__(self, nome_squadra):
        self.nome_squadra = nome_squadra
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

        # Formula Algoritmo v3.2
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
        
        # Evitiamo duplicati con lo stesso nome
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
            return ["Aggiungi prima qualche giocatore per ricevere consigli sugli scambi!"]

        medie_reparti = {}
        for r, nome_r in [('P', 'Porta'), ('D', 'Difesa'), ('C', 'Centrocampo'), ('A', 'Attacco')]:
            giocatori_reparto = [g["fanta_media"] for g in lista if g["ruolo"] == r]
            medie_reparti[nome_r] = sum(giocatori_reparto) / len(giocatori_reparto) if giocatori_reparto else 0

        if medie_reparti:
            reparto_debole = min(medie_reparti, key=medie_reparti.get)
            consigli.append(f"🎯 **Squilibrio di Rosa**: Il tuo reparto meno performante è la **{reparto_debole}** (Media: {round(medie_reparti[reparto_debole], 2)}). Cerca un rinforzo mirato.")

        for g in lista:
            if g["titolarita"] < 0.65 and g["valore_mercato"] > 25:
                consigli.append(f"🔄 **Cessione Consigliata**: **{g['nome']} ({g['ruolo']})** ha un valore alto ({g['valore_mercato']}) ma titolarità critica ({int(g['titolarita']*100)}%). Monetizzalo.")
            elif g["fanta_media"] < 6.0 and g["ruolo"] in ['C', 'A'] and g["indice_partita"] > 3:
                consigli.append(f"⚠️ **Valuta il Taglio/Scambio**: **{g['nome']}** sta faticando (Fanta-media {g['fanta_media']}). Usalo come esubero.")

        return consigli


# ==========================================
# INTERFACCIA GRAFICA STREAMLIT
# ==========================================
st.title("⚽ FantAlgoritmo v3.2 - Gestione Rosa & Scambi")

manager = FantAlgoritmoV3_2("Mia Squadra")

# Sidebar per la gestione dell'inserimento
st.sidebar.header("⚙️ Gestione Rosa")
modalita = st.sidebar.radio("Scegli come inserire i giocatori:", ["Inserimento Manuale (Tasto)", "Importa da CSV / Testo"])

if modalita == "Inserimento Manuale (Tasto)":
    st.sidebar.subheader("Aggiungi Giocatore a Mano")
    with st.sidebar.form("form_giocatore"):
        nome_i = st.text_input("Nome Giocatore")
        ruolo_i = st.selectbox("Ruolo", ["P", "D", "C", "A"])
        fanta_m_i = st.number_input("Fanta Media", min_value=0.0, max_value=15.0, value=6.5, step=0.1)
        diff_i = st.slider("Difficoltà Partita (1-5)", 1, 5, 2)
        titol_i = st.slider("Titolarità (0.0 - 1.0)", 0.0, 1.0, 0.9, 0.05)
        bm_i = st.number_input("Bonus/Malus Score (+/-)", value=0.0, step=0.5)
        val_i = st.number_input("Valore di Mercato / Crediti", min_value=1, value=15, step=1)
        
        submit_btn = st.form_submit_button("➕ Aggiungi alla Rosa")
        if submit_btn and nome_i:
            successo = manager.aggiungi_giocatore(nome_i, ruolo_i, fanta_m_i, diff_i, titol_i, bm_i, val_i)
            if successo:
                st.sidebar.success(f"Aggiunto {nome_i}!")
            else:
                st.sidebar.error("Giocatore già esistente o dati non validi.")

else:
    st.sidebar.subheader("Importa Lista")
    testo_csv = st.sidebar.text_area("Incolla qui i dati CSV (Nome,Ruolo,FantaMedia,Diff,Titol,BonusMalus,Valore)", 
                                     value="Lautaro,A,8.4,1,0.95,3.5,120\nPulisic,C,7.6,1,0.90,2.0,75\nDimarco,D,7.1,1,0.95,1.2,50")
    if st.sidebar.button("📥 Carica Dati"):
        f = io.StringIO(testo_csv)
        reader = csv.reader(f)
        count = 0
        for riga in reader:
            if len(riga) >= 7:
                if manager.aggiungi_giocatore(riga[0], riga[1], riga[2], riga[3], riga[4], riga[5], riga[6]):
                    count += 1
        st.sidebar.success(encji := f"Importati {count} giocatori!")

# Pulsante per resettare la rosa
if st.sidebar.button("🗑️ Svuota Rosa"):
    st.session_state.giocatori = []
    st.sidebar.warning("Rosa svuotata.")

# --- CORPO PRINCIPALE DELL'APP ---
st.subheader("📋 La tua Rosa Attuale")
if not st.session_state.giocatori:
    st.info("La rosa è vuota. Usa il menu a sinistra per aggiungere i giocatori a mano o tramite importazione!")
else:
    # Mostriamo la tabella dei giocatori
    st.write(f"Giocatori totali in rosa: **{len(st.session_state.giocatori)}**")
    
    # Scelta del modulo per la formazione
    st.markdown("---")
    st.subheader("🤖 Elaborazione Automatica")
    modulo_scelto = st.selectbox("Seleziona il modulo tattico:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])
    
    if st.button("⚡ Calcola Formazione e Consigli Scambi"):
        formazione = manager.calcola_formazione_automatica(modulo_scelto)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### ⚽ Formazione Titolare ({modulo_scelto})")
            for reparto, giocatori in formazione.items():
                if reparto != "Panchina":
                    st.markdown(f"**{reparto}:**")
                    for g in giocatori:
                        st.write(f"- **{g['nome']}** | Score: `{g['score']}` (FM: {g['fanta_media']} | Titol: {int(g['titolarita']*100)}%)")
            
            st.markdown("### 🏃‍♂️ Panchina Consigliata")
            for g in formazione["Panchina"]:
                st.write(f"- {g['nome']} ({g['ruolo']}) | Score: `{g['score']}`")

        with col2:
            st.markdown("### 🔄 Consigli Scambi (Algoritmo v3.2)")
            consigli = manager.genera_consigli_scambi()
            for consiglio in consigli:
                st.warning(consiglio)
