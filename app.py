# ==========================================
# GESTORE COMPLETO FANTACALCIO (MODULI + BONUS/MALUS + TITOLARITÀ)
# ==========================================

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
        self.indice_titolarita = indice_titolarita  # Valore da 0 a 100 (es. 90 = titolarissimo)
        self.voto_base = 6.0
        self.eventi = [] # Lista di eventi registrati (es. ["gol_segnato", "ammonizione"])

    def aggiungi_evento(self, evento):
        if evento in TABELLA_MALUS_BONUS:
            self.eventi.append(evento)

    def calcola_fantavoto(self):
        """Calcola il fantavoto partendo dal voto base, aggiungendo bonus e malus."""
        fantavoto = self.voto_base
        for ev in self.eventi:
            fantavoto += TABELLA_MALUS_BONUS[ev]
        return fantavoto


class GestoreFantacalcioCompleto:
    def __init__(self):
        self.rosa = []

    def aggiungi_giocatore(self, giocatore):
        self.rosa.append(giocatore)

    def valida_modulo(self, modulo):
        """Verifica se il modulo rientra tra quelli ufficiali di Lega FC."""
        if modulo not in MODULI_LEGA_FC:
            return False, f"Modulo '{modulo}' non valido per Leghe FC."
        return True, f"Modulo '{modulo}' valido."

    def analizza_formazione(self, modulo_schierato, titolari_schierati):
        """
        Analizza la formazione inserita controllando il modulo, 
        la titolarità media e calcolando i potenziali bonus/malus.
        """
        is_valido, msg = self.valida_modulo(modulo_schierato)
        if not is_valido:
            print(msg)
            return False

        print(f"--- ANALISI FORMAZIONE CON MODULO: {modulo_schierato} ---")
        
        # Controllo reparti dal modulo (es. 3-4-3 -> Dif:3, Cen:4, Att:3)
        pezzi = [int(x) for x in modulo_schierato.split('-')]
        richiesti = {"P": 1, "D": pezzi[0], "C": pezzi[1], "A": pezzi[2]}
        
        # Conteggio ruoli schierati
        conteggio = {"P": 0, "D": 0, "C": 0, "A": 0}
        for g in titolari_schierati:
            if g.ruolo in conteggio:
                conteggio[g.ruolo] += 1

        # Verifica rispondenza numerica
        if conteggio["P"] != richiesti["P"] or conteggio["D"] != richiesti["D"] or conteggio["C"] != richiesti["C"] or conteggio["A"] != richiesti["A"]:
            print("⚠️ ERRORE: I giocatori schierati non corrispondono al modulo scelto!")
            print(f"Richiesti -> Portieri: {richiesti['P']}, Difessori: {richiesti['D']}, Centrocampisti: {richiesti['C']}, Attaccanti: {richiesti['A']}")
            print(f"Schierati -> Portieri: {conteggio['P']}, Difessori: {conteggio['D']}, Centrocampisti: {conteggio['C']}, Attaccanti: {conteggio['A']}")
            return False

        # Analisi indici di titolarità e fantavoti
        titolarita_totale = 0
        for g in titolari_schierati:
            f_voto = g.calcola_fantavoto()
            titolarita_totale += g.indice_titolarita
            print(f"[{g.ruolo}] {g.nome} | Indice Titolare: {g.indice_titolarita}% | Fantavoto stimato: {f_voto}")

        media_titolarita = titolarita_totale / len(titolari_schierati)
        print(f"\n📈 Indice di Affidabilità/Titolarità Medio della Formazione: {media_titolarita:.1f}%\n")
        return True


# ==========================================
# ESEMPIO PRATICO DI UTILIZZO
# ==========================================
if __name__ == "__main__":
    gestore = GestoreFantacalcioCompleto()

    # Creazione di alcuni giocatori con relativo indice di titolarità (0-100)
    p1 = GiocatoreFantacalcio("Svilar", "P", 95)
    d1 = GiocatoreFantacalcio("Dimarco", "D", 90)
    d2 = GiocatoreFantacalcio("Buongiorno", "D", 85)
    d3 = GiocatoreFantacalcio("Bastoni", "D", 90)
    c1 = GiocatoreFantacalcio("Pulisic", "C", 95)
    c2 = GiocatoreFantacalcio("Barella", "C", 85)
    c3 = GiocatoreFantacalcio("Calhanoglu", "C", 95)
    c4 = GiocatoreFantacalcio("McTominay", "C", 80)
    a1 = GiocatoreFantacalcio("Retegui", "A", 90)
    a2 = GiocatoreFantacalcio("Thuram", "A", 90)

    # Simuliamo qualche bonus/malus per la giornata
    p1.aggiungi_evento("ammonizione")  # -0.5
    c1.aggiungi_evento("gol_segnato")  # +3
    c1.aggiungi_evento("assist")       # +1
    a1.aggiungi_evento("gol_segnato")  # +3

    # Mettiamo in campo un 3-4-2 (3 difensori, 4 centrocampisti, 2 attaccanti + 1 portiere = 10 titolari + portiere)
    formazione_titolare = [p1, d1, d2, d3, c1, c2, c3, c4, a1, a2]

    # Eseguiamo il test con il modulo ufficiale 3-4-2-1 oppure 3-5-2 correggendo il numero di giocatori
    # Facciamo l'esempio con il 3-5-2 (1 Portiere, 3 Difessori, 5 Centrocampisti, 2 Attaccanti)
    c5 = GiocatoreFantacalcio("Koopmeiners", "C", 90)
    formazione_352_titolare = [p1, d1, d2, d3, c1, c2, c3, c4, c5, a1, a2]

    # Testiamo la validazione e l'analisi
    gestore.analizza_formazione("3-5-2", formazione_352_titolare)
