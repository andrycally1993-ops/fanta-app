import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mio Fanta Algoritmo", page_icon="⚽", layout="centered")

st.title("⚽ Il mio Fanta Algoritmo Avanzato")
st.write("Gestione rosa, indice di forma, ballottaggi e calcolo avanzato della formazione!")

# Sezione per inserire i dati della rosa con bonus e ballottaggio
st.sidebar.header("Gestione Rosa & Parametri")
ruolo = st.sidebar.selectbox("Ruolo", ["P", "D", "C", "A"])
nome = st.sidebar.text_input("Nome Giocatore", "Es. Immobile")
fmv = st.sidebar.number_input("Fanta Media (FMV)", min_value=0.0, max_value=15.0, value=6.5, step=0.1)
fmv_u5 = st.sidebar.number_input("FMV Ultime 5 (Stato di forma)", min_value=0.0, max_value=15.0, value=6.5, step=0.1)

# Nuovi parametri avanzati
st.sidebar.subheader("⚖️ Fattori Extra")
ballottaggio = st.sidebar.slider("Probabilità di Titolarità (%)", min_value=0, max_value=100, value=80, step=5)
bonus_malus_previsti = st.sidebar.number_input("Bonus/Malus Previsto (es. +3 rigore, -0.5 amm.)", min_value=-5.0, max_value=10.0, value=0.0, step=0.5)

# Inizializziamo la lista dei giocatori nella memoria della sessione
if 'giocatori' not in st.session_state:
    st.session_state.giocatori = []

if st.sidebar.button("Aggiungi Giocatore"):
    st.session_state.giocatori.append({
        "Ruolo": ruolo,
        "Nome": nome,
        "FMV": fmv,
        "FMV_U5": fmv_u5,
        "Ballottaggio": ballottaggio,
        "BonusExtra": bonus_malus_previsti
    })
    st.sidebar.success(f"Aggiunto {nome}!")

# Mostriamo la rosa attuale e calcoliamo l'algoritmo avanzato
if st.session_state.giocatori:
    df_rosa = pd.DataFrame(st.session_state.giocatori)
    
    # --- L'ALGORITMO AVANZATO ---
    # Formula: 50% Ultime 5, 30% FMV generale, 10% Bonus stimati, 10% Rapportato alla probabilità di ballottaggio
    forma_base = (df_rosa['FMV_U5'] * 0.5) + (df_rosa['FMV'] * 0.3) + df_rosa['BonusExtra'] * 0.2
    fattore_presenza = df_rosa['Ballottaggio'] / 100.0
    
    df_rosa['Indice Algoritmo'] = forma_base * fattore_presenza
    
    st.subheader("📋 La tua Rosa e Indice Algoritmo Avanzato")
    st.dataframe(df_rosa.sort_values(by="Indice Algoritmo", ascending=False), use_container_width=True)
    
    if st.button("Svuota Rosa"):
        st.session_state.giocatori = []
        st.rerun()

    # --- CONSIGLIO FORMAZIONE ---
    st.subheader("🤖 Consigliere Formazione Automatica")
    modulo = st.selectbox("Scegli il Modulo", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])
    
    if st.button("Genera Formazione Ideale"):
        p = [g for g in st.session_state.giocatori if g['Ruolo'] == 'P']
        d = [g for g in st.session_state.giocatori if g['Ruolo'] == 'D']
        c = [g for g in st.session_state.giocatori if g['Ruolo'] == 'C']
        a = [g for g in st.session_state.giocatori if g['Ruolo'] == 'A']
        
        num_d = int(modulo[0])
        num_c = int(modulo[2])
        num_a = int(modulo[4])
        
        # Funzione di ordinamento basata sul nuovo indice
        def calcola_score(g):
            base = (g['FMV_U5'] * 0.5) + (g['FMV'] * 0.3) + g['BonusExtra'] * 0.2
            return base * (g['Ballottaggio'] / 100.0)

        p_ord = sorted(p, key=calcola_score, reverse=True)
        d_ord = sorted(d, key=calcola_score, reverse=True)
        c_ord = sorted(c, key=calcola_score, reverse=True)
        a_ord = sorted(a, key=calcola_score, reverse=True)
        
        st.write(f"### 🏆 Formazione Titolare Consigliata ({modulo})")
        
        if p_ord:
            st.write(f"- **Portiere:** {p_ord[0]['Nome']} (Indice: {calcola_score(p_ord[0]):.2f} - Ballottaggio: {p_ord[0]['Ballottaggio']}%)")
        else:
            st.warning("Manca almeno 1 Portiere!")
            
        if len(d_ord) >= num_d:
            st.write("**Difensori:**")
            for i in range(num_d):
                st.write(f"- {d_ord[i]['Nome']} (Indice: {calcola_score(d_ord[i]):.2f} - Ballottaggio: {d_ord[i]['Ballottaggio']}%)")
        else:
            st.warning(f"Hai bisogno di almeno {num_d} difensori nella lista!")
            
        if len(c_ord) >= num_c:
            st.write("**Centrocampisti:**")
            for i in range(num_c):
                st.write(f"- {c_ord[i]['Nome']} (Indice: {calcola_score(c_ord[i]):.2f} - Ballottaggio: {c_ord[i]['Ballottaggio']}%)")
        else:
            st.warning(f"Hai bisogno di almeno {num_c} centrocampisti nella lista!")
            
        if len(a_ord) >= num_a:
            st.write("**Attaccanti:**")
            for i in range(num_a):
                st.write(f"- {a_ord[i]['Nome']} (Indice: {calcola_score(a_ord[i]):.2f} - Ballottaggio: {a_ord[i]['Ballottaggio']}%)")
        else:
            st.warning(f"Hai bisogno di almeno {num_a} attaccanti nella lista!")
else:
    st.info("Usa il menu a sinistra per aggiungere i primi giocatori alla tua rosa inserendo anche i ballottaggi e i bonus stimati.")
