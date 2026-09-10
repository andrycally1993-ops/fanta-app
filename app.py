import streamlit as st
import csv
import io

class FantAlgoritmoV3_4:
    def __init__(self):
        if 'giocatori' not in st.session_state:
            st.session_state.giocatori = []

    def aggiungi_giocatore(self, nome, ruolo, fanta_media, indice_partita, titolarita, bonus_malus_score, valore_mercato):
        try:
            f_media = float(str(fanta_media).strip().replace(',', '.')) if fanta_media else 6.5
            i_partita = int(float(str(indice_partita).strip().replace(',', '.'))) if indice_partita else 2
            titol = float(str(titolarita).strip().replace(',', '.')) if titolarita else 0.85
            b_malus = float(str(bonus_malus_score).strip().replace(',', '.')) if bonus_malus_score else 0.0
            v_mercato = int(float(str(valore_mercato).strip().replace(',', '.'))) if valore_mercato else 10
        except (ValueError, TypeError):
            return False

        # Algoritmo di schierabilità
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
            return ["Carica la rosa per sbloccare i consigli scambi!"]

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
                consigli.append(f"⚠️ **Da Tagliare/Scambiare**: **{g['nome']}** sta rendendo poco (Fanta-media {g['fanta_media']}). Valuta la cessione.")

        return consigli

# ==========================================
# INTERFACCIA STREAMLIT
# ==========================================
st.title("⚽ FantAlgoritmo v3.4 - Smart Manager")

app = FantAlgoritmoV3_4()

st.sidebar.header("📁 Carica la tua Rosa")
uploaded_file = st.sidebar.file_uploader("Scegli file CSV di Leghe FC", type=["csv"])

if uploaded_file is not None:
    try:
        stringa_dati = uploaded_file.getvalue().decode("utf-8", errors="ignore")
        f = io.StringIO(stringa_dati)
        
        # Legge il separatore (virgola o punto e virgola)
        sample = f.read(2048)
        f.seek(0)
        delimiter = ';' if ';' in sample else ','
        
        reader = csv.reader(f, delimiter=delimiter)
        righe = list(reader)
        
        count = 0
        if righe:
            # Cerca di capire dove sono le colonne analizzando la prima riga (intestazione)
            header = [str(h).strip().lower() for h in righe[0]]
            
            # Indici di default basati sulla struttura tipica di Leghe FC
            idx_nome = 0
            idx_ruolo = 1
            idx_fm = -1
            idx_val = -1
            
            for i, h in enumerate(header):
                if 'nome' in h or 'giocatore' in h:
                    idx_nome = i
                elif 'ruolo' in h:
                    idx_ruolo = i
                elif 'fanta' in h or 'media' in h or 'fm' in h:
                    idx_fm = i
                elif 'quotazione' in h or 'valore' in h or 'qt' in h:
                    idx_val = i

            # Processa le righe saltando l'intestazione
            for riga in righe[1:]:
                if not riga or len(riga) < 2:
                    continue
                
                try:
                    nome = riga[idx_nome] if idx_nome < len(riga) else riga[0]
                    ruolo = riga[idx_val] if False else (riga[idx_ruolo] if idx_ruolo < len(riga) else "C")
                    
                    # Pulisce il ruolo se contiene sigle strane (es. 'A*' -> 'A')
                    ruolo = ''.join([c for c in ruolo if c.upper() in ['P', 'D', 'C', 'A']])
                    if not ruolo: 
                        ruolo = "C"

                    fanta_media = 6.5
                    if idx_fm != -1 and idx_fm < len(riga):
                        try:
                            fanta_media = float(riga[idx_fm].replace(',', '.'))
                        except:
                            pass

                    valore_mercato = 15
                    if idx_val != -1 and idx_val < len(riga):
                        try:
                            valore_mercato = int(float(riga[idx_val].replace(',', '.')))
                        except:
                            pass

                    if app.aggiungi_giocatore(nome, ruolo, fanta_media, indice_partita=2, titolarita=0.85, bonus_malus_score=0.0, valore_mercato=valore_mercato):
                        count += 1
                except:
                    continue
                    
        if count > 0:
            st.sidebar.success(f"Caricati con successo {count} giocatori!")
        else:
            st.sidebar.warning("Impossibile leggere i campi. Verifica il file.")
            
    except Exception as e:
        st.sidebar.error(f"Errore: {e}")

if st.sidebar.button("🗑️ Svuota Rosa"):
    st.session_state.giocatori = []
    st.sidebar.warning("Rosa azzerata.")

# CORPO PRINCIPALE
st.subheader("📋 Stato Attuale Rosa")
if not st.session_state.giocatori:
    st.info("👈 Carica il file CSV della tua squadra per iniziare.")
else:
    st.write(f"Giocatori totali caricati: **{len(st.session_state.giocatori)}**")
    
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
