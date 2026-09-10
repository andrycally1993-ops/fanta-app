import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="FantAlgoritmo - Formazione Titolare", layout="wide")

# Intestazione superiore pulita con componenti nativi
col_title_1, col_title_2 = st.columns([3, 2])
with col_title_1:
    st.subheader("⚽ FantAlgoritmo - Formazione Titolare")
with col_title_2:
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.metric(label="Totale Rosa", value="25")
    with c_m2:
        st.metric(label="Indice Rosa", value="8.6 / 10")

st.markdown("---")

# Filtri superiori: Rosa e Modulo
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    st.selectbox("Seleziona la rosa da visualizzare:", ["la beneamata ma non troppo"])
with col_f2:
    modulo_scelto = st.selectbox("Cambia Modulo:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])

# Layout principale: Campo Titolari (Sinistra) e Panchina (Destra)
col_campo, col_panchina = st.columns([2, 1])

with col_campo:
    st.markdown(f"### 🏟️ Campo Titolari ({modulo_scelto})")
    
    # Contenitore stile campo da gioco
    with st.container(border=True):
        st.markdown("**ATTACCO**")
        att_cols = st.columns(3)
        attaccanti = [
            ("Kvaratskhelia", "+85%", "https://img.leghe.fc-parma.com/player/default.png"), 
            ("Esposito F.P.", "+65%", "https://img.leghe.fc-parma.com/player/default.png"), 
            ("Kean", "+80%", "https://img.leghe.fc-parma.com/player/default.png")
        ]
        for i, (nome, bonus, foto) in enumerate(attaccanti):
            with att_cols[i]:
                st.image(foto, width=50) # Qui puoi inserire l'URL reale della foto del giocatore
                st.text(nome)
                st.caption(f"Indice: {bonus}")

        st.markdown("---")
        st.markdown("**CENTROCAMPO**")
        c_cols = st.columns(4)
        centrocampisti = [
            ("Bastoni", "+70%"), ("Mkhitaryan", "+75%"), 
            ("Barella", "+90%"), ("Koopmeiners", "+60%")
        ]
        for i, (nome, bonus) in enumerate(centrocampisti):
            with c_cols[i]:
                st.text(nome)
                st.caption(f"Indice: {bonus}")

        st.markdown("---")
        st.markdown("**DIFESA**")
        d_cols = st.columns(3)
        difensori = [
            ("Di Lorenzo", "+30%"), ("Bremer", "+82%"), ("Buongiorno", "+88%")
        ]
        for i, (nome, bonus) in enumerate(difensori):
            with d_cols[i]:
                st.text(nome)
                st.caption(f"Indice: {bonus}")

with col_panchina:
    # Se
