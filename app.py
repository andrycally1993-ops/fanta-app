import pandas as pd
import streamlit as st

# Configurazione della pagina
st.set_page_config(
    page_title="Algo Fantacalcio - Analisi", layout="wide", page_icon="⚽"
)

# --- SIDEBAR: Informazioni & Fonti ---
with st.sidebar:
  st.header("⚙️ Informazioni & Fonti")
  st.markdown("### 🤖 Motore Algoritmico")
  st.markdown(
      "Analisi combinata di flussi dati da testate giornalistiche, stime"
      " di titolarità in tempo reale, indice di pericolosità offensiva e"
      " propensione ai malus."
  )

  st.markdown("### 📊 Fonti Aggregate")
  st.markdown(
      "- Gazzetta dello Sport & Corriere\n- Sky Sport & Tuttosport\n- Algoritmi"
      " Probabili Formazioni Pro\n- Expected Stats (xG / xA match)"
  )

  st.markdown("### 📈 Stato Analisi Giornata")
  st.success("Sincronizzazione ultimata")
  st.info("Modelli predittivi attivi")

# --- TOP BAR: Carica Leghe, Lega Attiva, Moduli e Metriche ---
col_up, col_liga, col_mod, col_stat1, col_stat2 = st.columns(
    [1.5, 1.2, 1.2, 1, 1]
)

with col_up:
  uploaded_file = st.file_uploader(
      "Carica Leghe CSV", type=["csv"], help="200MB per file - CSV"
  )

# Gestione caricamento CSV leghe e rosa
df_leghe = None
if uploaded_file is not None:
  try:
    df_leghe = pd.read_csv(uploaded_file)
    st.success("CSV caricato con successo!")
  except Exception as e:
    st.error(f"Errore nella lettura del CSV: {e}")

with col_liga:
  # Gestione squadre salvate / aggiunte multiple
  if "squadre_salvate" not in st.session_state:
    st.session_state.squadre_salvate = [
        "forza_stelle_la_beneamata",
        "altra_squadra_fanta",
    ]

  lega_selezionata = st.selectbox(
      "Lega Attiva", st.session_state.squadre_salvate
  )

  # Input per aggiungere una nuova squadra salvata
  nuova_squadra = st.text_input(
      "Aggiungi nuova squadra", placeholder="Nome squadra..."
  )
  if st.button("➕ Aggiungi Squadra"):
    if nuova_squadra and nuova_squadra not in st.session_state.squadre_salvate:
      st.session_state.squadre_salvate.append(nuova_squadra)
      st.rerun()

with col_mod:
  moduli_fc = [
      "3-4-3",
      "3-5-2",
      "4-3-3",
      "4-4-2",
      "4-2-3-1",
      "5-3-2",
      "5-4-1",
  ]
  modulo_selezionato = st.selectbox("Moduli LegheFC", moduli_fc)

with col_stat1:
  st.metric(label="TOTALE GIOCATORI", value="25")

with col_stat2:
  st.metric(label="INDICE ROSA REALE", value="6.0")

st.markdown("---")

# --- SEZIONE CENTRALE: Formazione e Salvataggio ---
st.text("Nome Formazione da salvare")
nome_formazione_default = f"Formazione {lega_selezionata}-mia-non-troppo_rosa_2026-09-10_{modulo_selezionato}"
col_nome, col_btn = st.columns([3, 1])
with col_nome:
  nome_formazione = st.text_input("Formazione", value=nome_formazione_default, label_visibility="collapsed")
with col_btn:
  if st.button("💾 Aggiungi / Salva Formazione"):
    st.success("Formazione salvata con successo!")

st.markdown("---")

# --- LAYOUT CAMPO / TITOLARI E PANCHINA ---
col_titolari, col_panchina = st.columns([2, 1])

with col_titolari:
  st.subheader("4ª Giornata - Titolari")
  # Filtri di ricerca sopra il campo
  f_col1, f_col2 = st.columns(2)
  with f_col1:
    st.selectbox("Filtro Ruolo", ["Tutti", "POR", "DIF", "CEN", "ATT"], key="filtro_ruolo_titolari", label_visibility="collapsed")
  with f_col2:
    st.text_input("Cerca giocatore...", key="cerca_titolari", label_visibility="collapsed")

  # Box visivo della struttura titolari (mantenuto come nel tuo layout)
  st.markdown(
      """
      <div style="background-color: #f8f9fa; padding: 30px; border-radius: 10px; text-align: center; border: 1px dashed #ccc; min-height: 350px;">
          <p style="color: #666; font-weight: bold;">[ Struttura Campo Titolari - Modulo: %s ]</p>
      </div>
      """ % modulo_selezionato,
      unsafe_allow_html=True,
  )

with col_panchina:
  st.subheader("Panchina & Riserve")
  
  # Visualizzazione schede panchina pulite (senza codice grezzo HTML visibile)
  panchinari = [
      {"ruolo": "POR", "nome": "Sommer", "voto": "5,9 F.FA", "stat": "Tit: 99% | 40/43"},
      {"ruolo": "DIF", "nome": "Dimarco", "voto": "6,2 F.FA", "stat": "Tit: 98% | 41/43"},
      {"ruolo": "DIF", "nome": "Pavard", "voto": "5,7 F.FA", "stat": "Tit: 75% | 35/43"},
      {"ruolo": "CEN", "nome": "Rabiot", "voto": "6,0 F.FA", "stat": "Tit: 90% | 38/43"},
      {"ruolo": "CEN", "nome": "Koopmeiners", "voto": "6,3 F.FA", "stat": "Tit: 99% | 42/43"},
      {"ruolo": "ATT", "nome": "Zirkzee", "voto": "6,2 F.FA", "stat": "Tit: 92% | 39/43"}
  ]

  for p in panchinari:
    st.markdown(
        f"""
        <div style="background-color: #2b2b2b; color: white; padding: 10px; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 10px; background: #444; padding: 2px 5px; border-radius: 4px;">{p['ruolo']}</span><br>
                <b>{p['nome']}</b>
            </div>
            <div style="text-align: right;">
                <span style="color: #4cd137; font-size: 12px; font-weight: bold;">{p['voto']}</span><br>
                <span style="font-size: 9px; color: #aaa;">{p['stat']}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# --- SEZIONE CONSIGLI E GENERAZIONE ---
col_gen, col_info = st.columns([1, 2])
with col_gen:
  if st.button("💡 Genera Formazione Ufficiale", type="primary", use_container_width=True):
    st.balloons()

with col_info:
  with st.expander("Perché schierare questi?"):
    st.markdown(
        """
        - **Dettaglio Metriche Giornate**: Percentuale derivata dall'incrocio delle ultime 4 giocate.
        - **Probabilità Bonus (V/S)**: Stima basata su Expected Goals (xG) e calci piazzati.
        - **Probabilità Malus**: Indice di rischio ammonizioni/espulsioni basato sull'arbitro e sui falli subiti/commessi.
        """
    )
