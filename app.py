import streamlit as st
import pandas as pd

st.set_page_config(page_title="Mio Fanta Algoritmo", page_icon="⚽", layout="centered")

st.title("⚽ Il mio Fanta Algoritmo Personale")
st.write("Inserisci i tuoi giocatori, calcola l'indice di forma e trova la formazione ideale!")

# Sezione per inserire i dati della rosa
st.sidebar.header("Gestione Rosa")
ruolo = st.sidebar.selectbox("Ruolo", ["P", "D", "C", "A"])
nome = st.sidebar.text_input("Nome Giocatore", "Es. De Bruyne")
fmv = st.sidebar.number_input("Fanta Media (FMV)", min_value=0.0, max_value=15.0, value=6.5, step=0.1)
fmv_u5 = st.sidebar.number_input("FMV Ultime 5 (Stato di forma)", min_value=0.0, max_value=15.0, value=6.5, step=0.1)

# Inizializziamo la lista dei giocatori nella memoria della sessione
if 'giocatori' not in st.session_state:
    st.session_state.giocatori = []

if st.sidebar.button("Aggiungi Giocatore"):
    st.session_state.giocatori.append({
        "Ruolo": ruolo,
        "Nome": nome,
        "FMV": fmv,
        "FMV_U5": fmv_u5
    })
    st.sidebar.success(f"Aggiunto {nome}!")

# Mostriamo la rosa attuale
if st.session_state.giocatori:
    df_rosa = pd.DataFrame(st.session_state.giocatori)
    
    # --- L'ALGORITMO DI SCHIERABILITÀ ---
    # Diamo più peso (60%) allo stato di forma recente (FMV_U5) e il 40% alla FMV generale
    df_rosa['Indice Algoritmo'] = (df_rosa['FMV_U5'] * 0.6) + (df_rosa['FMV'] * 0.4)
    
    st.subheader("📋 La tua Rosa e Indice Algoritmo")
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
        
        # Estraiamo i numeri del modulo (es. '3-4-3' -> dif=3, cen=4, att=3)
        num_d = int(modulo[0])
        num_c = int(modulo[2])
        num_a = int(modulo[4])
        
        # Ordiniamo in base all'algoritmo
        p_ord = sorted(p, key=lambda x: (x['FMV_U5']*0.6 + x['FMV']*0.4), reverse=True)
        d_ord = sorted(d, key=lambda x: (x['FMV_U5']*0.6 + x['FMV']*0.4), reverse=True)
        c_ord = sorted(c, key=lambda x: (x['FMV_U5']*0.6 + x['FMV']*0.4), reverse=True)
        a_ord = sorted(a, key=lambda x: (x['FMV_U5']*0.6 + x['FMV']*0.4), reverse=True)
        
        st.write(f"### 🏆 Formazione Titolare ({modulo})")
        if p_ord:
            st.write(f"- **Portiere:** {p_ord[0]['Nome']} (Indice: {p_ord[0]['FMV_U5']*0.6 + p_ord[0]['FMV']*0.4:.2f})")
        else:
            st.warning("Manca almeno 1 Portiere!")
            
        if len(d_ord) >= num_d:
            st.write("**Difensori:**")
            for i in range(num_d):
                st.write(f"- {d_ord[i]['Nome']} (Indice: {d_ord[i]['FMV_U5']*0.6 + d_ord[i]['FMV']*0.4:.2f})")
        else:
            st.warning(f"Hai bisogno di almeno {num_d} difensori nella lista!")
            
        if len(c_ord) >= num_c:
            st.write("**Centrocampisti:**")
            for i in range(num_c):
                st.write(f"- {c_ord[i]['Nome']} (Indice: {c_ord[i]['FMV_U5']*0.6 + c_ord[i]['FMV']*0.4:.2f})")
        else:
            st.warning(f"Hai bisogno di almeno {num_c} centrocampisti nella lista!")
            
        if len(a_ord) >= num_a:
            st.write("**Attaccanti:**")
            for i in range(num_a):
                st.write(f"- {a_ord[i]['Nome']} (Indice: {a_ord[i]['FMV_U5']*0.6 + a_ord[i]['FMV']*0.4:.2f})")
        else:
            st.warning(f"Hai bisogno di almeno {num_a} attaccanti nella lista!")
else:
    st.info("Usa il menu a sinistra per aggiungere i primi giocatori alla tua rosa.")
