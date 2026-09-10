import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(page_title="Gestore Fantacalcio", page_icon="⚽", layout="centered")

st.title("⚽ Gestore Completo Fantacalcio")
st.write("Gestione moduli ufficiali di Lega FC, indici di titolarità e calcolo fantavoto.")

# 1. MODULI UFFICIALI LEGA FANTACALCIO (Classic)
MODULI_LEGA_FC = [
    "3-4-3", 
    "3-5-2", 
    "4-3-3", 
    "4-4-2", 
    "4-5-1", 
    "5-3-2", 
    "5-4-1"
]

# 2. TABELLA BONUS E MALUS STANDARD
TABELLA_MALUS_BONUS = {
    "gol_segnato": +3,
    "assist": +1,
    "rigore_segnato": +3,
    "rigore_parato": +3,
    "rigore_sbagliato": -3,
    "ammonizione": -0.5,
    "espulsione": -1,
    "autogol": -2,
    "gol_subito": -1
}

class GiocatoreFantacalcio:
    def __init__(self, nome, ruolo, indice_titolarita):
        self.nome = nome
        self.ruolo = ruolo  # P, D, C, A
        self.indice_titolarita = indice_titolarita  # Valore da 0 a 100
        self.voto_base = 6.0
        self.eventi = []

    def aggiungi_evento(self, evento):
        if evento in TABELLA_MALUS_BONUS:
            self.eventi.append(evento)

    def calcola_fantavoto(self):
        fantavoto = self.voto_base
        for ev in self.eventi:
            fantavoto += TABELLA_MALUS_BONUS[ev]
        return fantavoto

# --- INTERFACCIA GRAFICA STREAMLIT ---
st.sidebar.header("Impostazioni Formazione")
modulo_scelto = st.sidebar.selectbox("Scegli il Modulo (Lega FC)", MODULI_LEGA_FC)

st.subheader(f"Formazione Analizzata - Modulo: {modulo_scelto}")

# Creazione di una rosa di esempio pre-caricata per la schermata
giocatori_esempio = [
    GiocatoreFantacalcio("Svilar", "P", 95),
    GiocatoreFantacalcio("Dimarco", "D", 90),
    GiocatoreFantacalcio("Buongiorno", "D", 85),
    GiocatoreFantacalcio("Bastoni", "D", 90),
    GiocatoreFantacalcio("Pulisic", "C", 95),
    GiocatoreFantacalcio("Barella", "C", 85),
    GiocatoreFantacalcio("Calhanoglu", "C", 95),
    GiocatoreFantacalcio("McTominay", "C", 80),
    GiocatoreFantacalcio("Koopmeiners", "C", 90),
    GiocatoreFantacalcio("Retegui", "A", 90),
    GiocatoreFantacalcio("Thuram", "A", 90)
]

# Aggiungiamo qualche bonus di test
giocatori_esempio[0].aggiungi_evento("ammonizione")
giocatori_esempio[4].aggiungi_evento("gol_segnato")
giocatori_esempio[4].aggiungi_evento("assist")
giocatori_esempio[9].aggiungi_evento("gol_segnato")

# Filtriamo in base al modulo selezionato (es. 3-5-2 -> 1 P, 3 D, 5 C, 2 A)
pezzi = [int(x) for x in modulo_scelto.split('-')]
richiesti = {"P": 1, "D": pezzi[0], "C": pezzi[1], "A": pezzi[2]}

portieri = [g for g in giocatori_esempio if g.ruolo == "P"][:richiesti["P"]]
difessori = [g for g in giocatori_esempio if g.ruolo == "D"][:richiesti["D"]]
centrocampisti = [g for g in giocatori_esempio if g.ruolo == "C"][:richiesti["C"]]
attaccanti = [g for g in giocatori_esempio if g.ruolo == "A"][:richiesti["A"]]

titolari_schierati = portieri + difessori + centrocampisti + attaccanti

# Mostriamo i dati a schermo con Streamlit
st.markdown("### 📋 Giocatori Titolari Schierati")

titolarita_totale = 0
for g in titolari_schierati:
    f_voto = g.calcola_fantavoto()
    titolarita_totale += g.indice_titolarita
    
    # Mostriamo ogni giocatore dentro una card grafica pulita
    st.markdown(f"""
    - **[{g.ruolo}] {g.nome}** 
      - Indice Titolare: `{g.indice_titolarita}%`
      - Fantavoto Stimato: `{f_voto}`
    """)

media_titolarita = titolarita_totale / len(titolari_schierati)

st.divider()
st.success(f"📈 **Indice di Affidabilità / Titolarità Medio della Formazione:** {media_titolarita:.1f}%")
