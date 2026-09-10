import csv
import io

class FantAlgoritmoV3_1:
    def __init__(self, nome_squadra):
        self.nome_squadra = nome_squadra
        self.giocatori = []

    def aggiungi_giocatore(self, nome, ruolo, fanta_media, indice_partita, titolarita, bonus_malus_score, valore_mercato):
        """Aggiunge manualmente un singolo giocatore."""
        score_schierabilita = ((fanta_media + bonus_malus_score) * titolarita) - (indice_partita * 0.3)
        
        giocatore = {
            "nome": nome,
            "ruolo": ruolo.upper(),
            "fanta_media": float(fanta_media),
            "indice_partita": int(indice_partita),
            "titolarita": float(titolarita),
            "bonus_malus_score": float(bonus_malus_score),
            "valore_mercato": int(valore_mercato),
            "score": round(score_schierabilita, 2)
        }
        self.giocatori.append(giocatore)

    def importa_da_csv(self, file_path_o_stringa, e_stringa=False):
        """
        IMPORTA LA ROSA DA UN FILE CSV (o stringa CSV).
        Il formato delle colonne deve essere:
        Nome,Ruolo,FantaMedia,IndicePartita,Titolarita,BonusMalus,ValoreMercato
        Esempio riga: Lautaro,A,8.4,1,0.95,3.5,120
        """
        if e_stringa:
            f = io.StringIO(file_path_o_stringa)
            reader = csv.reader(f)
        else:
            try:
                f = open(file_path_o_stringa, mode='r', encoding='utf-8')
                reader = csv.reader(f)
            except FileNotFoundError:
                print(f"⚠️ File '{file_path_o_stringa}' non trovato. Impossibile importare.")
                return

        count = 0
        for riga in reader:
            # Salta righe vuote o l'intestazione
            if not riga or riga[0].lower() in ['nome', 'giocatore']:
                continue
            if len(riga) >= 7:
                self.aggiungi_giocatore(
                    nome=riga[0].strip(),
                    ruolo=riga[1].strip(),
                    fanta_media=riga[2],
                    indice_partita=riga[3],
                    titolarita=riga[4],
                    bonus_malus_score=riga[5],
                    valore_mercato=riga[6]
                )
                count += 1
        
        print(f"✅ Importati con successo {count} giocatori dalla rosa!\n")
        if not e_stringa:
            f.close()

    def calcola_formazione_automatica(self, modulo="3-4-3"):
        """Seleziona automaticamente l'undici titolare e la panchina."""
        portieri = sorted([g for g in self.giocatori if g["ruolo"] == 'P'], key=lambda x: x["score"], reverse=True)
        difensori = sorted([g for g in self.giocatori if g["ruolo"] == 'D'], key=lambda x: x["score"], reverse=True)
        centrocampisti = sorted([g for g in self.giocatori if g["ruolo"] == 'C'], key=lambda x: x["score"], reverse=True)
        attaccanti = sorted([g for g in self.giocatori if g["ruolo"] == 'A'], key=lambda x: x["score"], reverse=True)

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
        """Genera suggerimenti intelligenti sugli scambi in base alla rosa."""
        consigli = []
        
        medie_reparti = {}
        for r, nome_r in [('P', 'Porta'), ('D', 'Difesa'), ('C', 'Centrocampo'), ('A', 'Attacco')]:
            giocatori_reparto = [g["fanta_media"] for g in self.giocatori if g["ruolo"] == r]
            medie_reparti[nome_r] = sum(giocatori_reparto) / len(giocatori_reparto) if giocatori_reparto else 0

        if medie_reparti:
            reparto_debole = min(medie_reparti, key=medie_reparti.get)
            consigli.append(f"🎯 **Squilibrio di Rosa**: Il tuo reparto meno performante è la **{reparto_debole}** (Media voto: {round(medie_reparti[reparto_debole], 2)}). Cerca un rinforzo mirato qui.")

        for g in self.giocatori:
            if g["titolarita"] < 0.65 and g["valore_mercato"] > 25:
                consigli.append(f"🔄 **Cessione Consigliata**: **{g['nome']} ({g['ruolo']})** ha un valore alto ({g['valore_mercato']}) ma titolarità critica ({int(g['titolarita']*100)}%). Monetizzalo.")
            elif g["fanta_media"] < 6.0 and g["ruolo"] in ['C', 'A'] and g["indice_partita"] > 3:
                consigli.append(f"⚠️ **Valuta il Taglio/Scambio**: **{g['nome']}** sta faticando (Fanta-media {g['fanta_media']}). Usalo come esubero in uno scambio.")

        return consigli

# ==========================================
# ESEMPIO DI UTILIZZO CON IMPORT CSV
# ==========================================
if __name__ == "__main__":
    mia_squadra = FantAlgoritmoV3_1("FC Algoritmo Pro")

    # SIMULAZIONE DELL'IMPORT DELLA ROSA (es. copiato da un file CSV o esportato da Leghe FC)
    # Formato: Nome, Ruolo, FantaMedia, DifficoltàPartita(1-5), Titolarità(0-1), BonusMalus, ValoreMercato
    dati_csv_simulati = """Nome,Ruolo,FantaMedia,DifficoltàPartita,Titolarità,BonusMalus,ValoreMercato
Maignan,P,6.3,1,0.95,0.5,35
Sportiello,P,6.0,1,0.10,0.0,5
Bastoni,D,6.6,2,0.90,0.4,28
Dimarco,D,7.1,1,0.95,1.2,50
Buongiorno,D,6.4,2,0.90,0.2,25
Gatti,D,6.2,4,0.70,-0.2,15
Pulisic,C,7.6,1,0.90,2.0,75
Koopmeiners,C,7.3,2,0.95,1.5,80
Colpani,C,6.5,3,0.80,0.5,25
Zaccagni,C,6.8,2,0.85,0.8,40
Lautaro,A,8.4,1,0.95,3.5,120
Thuram,A,8.0,2,0.90,3.0,110
Orsolini,A,7.0,4,0.75,1.0,35"""

    # Eseguiamo l'importazione automatica dalla stringa (puoi sostituire con il percorso del file es: 'rosa.csv')
    mia_squadra.importa_da_csv(dati_csv_simulati, e_stringa=True)

    # 1. Calcolo Formazione Automatica (es. Modulo 3-4-3)
    modulo_scelto = "3-4-3"
    formazione_ideale = mia_squadra.calcola_formazione_automatica(modulo_scelto)
    
    print(f"==================================================")
    print(f" 📋 FORMAZIONE CONSIGLIATA - MODULO: {modulo_scelto}")
    print(f"==================================================")
    for reparto, giocatori in formazione_ideale.items():
        print(f"\n🔹 **{reparto}**:")
        for g in giocatori:
            print(f"   - {g['nome']} | Score: {g['score']} (FantaM: {g['fanta_media']} | B/M: {g['bonus_malus_score']} | Titol.: {int(g['titolarita']*100)}%)")

    print(f"\n==================================================")
    print(f" 🔄 CONSIGLI SCAMBI AUTOMATICI (VERSIONE 3.1)")
    print(f"==================================================")
    for consiglio in mia_squadra.genera_consigli_scambi():
        print(f"* {consiglio}\n")
