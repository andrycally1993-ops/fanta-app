import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="FantAlgoritmo - Formazione Titolare", layout="wide")

# Intestazione dell'app
st.title("⚽ FantAlgoritmo - Formazione Titolare")

# Filtri superiori e gestione rosa
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    st.selectbox("Seleziona la rosa da visualizzare:", ["la beneamata ma non troppo"])
with col_f2:
    st.info("**Totale Rosa:** 25  |  **Indice Rosa:** 8.6 / 10")

st.markdown("---")

# Layout principale: Campo Titolare (Sinistra) e Panchina & Riserve (Destra)
col_campo, col_panchina = st.columns([2, 1])

with col_campo:
    st.subheader("Campo Titolari (3-4-3)")
    
    # Contenitore grafico del campo da calcio
    st.markdown("""
        <style>
        .campo-container {
            background-color: #2e7d32;
            padding: 20px;
            border-radius: 15px;
            border: 3px solid #ffffff;
            color: white;
            text-align: center;
        }
        . giocatore-card {
            background: rgba(0, 0, 0, 0.4);
            padding: 10px;
            border-radius: 10px;
            display: inline-block;
            margin: 5px;
            width: 90px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Simulazione visiva dei reparti sul campo con le linee di stato e percentuali
    # Linea Verde = Titolare sicuro, Arancione = Ballottaggio, Rossa = Panchina/Infortunato
    st.markdown("""
    <div style="background-color: #2e7d32; padding: 20px; border-radius: 12px; text-align: center;">
        <p style="font-weight: bold; color: white; margin-bottom: 15px;">Titolari in Campo (3-4-3)</p>
        
        <div style="margin-bottom: 10px;">
            <span style="display:inline-block; margin: 0 10px; background:rgba(0,0,0,0.5); padding:8px; border-radius:8px;">
                👤 <b>Kvaratskhelia</b><br><hr style="margin:2px 0; border-color:green;">+85%<br><a href="https://www.gazzetta.it" target="_blank" style="font-size:10px; color:#add8e6;">Prob. Formazione</a>
            </span>
        </div>
        <div style="margin-bottom: 10px;">
            <span style="display:inline-block; margin: 0 5px; background:rgba(0,0,0,0.5); padding:8px; border-radius:8px;">
                👤 <b>Esposito F.P.</b><br><hr style="margin:2px 0; border-color:orange;">+65%
            </span>
            <span style="display:inline-block; margin: 0 5px; background:rgba(0,0,0,0.5); padding:8px; border-radius:8px;">
                👤 <b>Kean</b><br><hr style="margin:2px 0; border-color:green;">+80%
            </span>
        </div>
        <div style="margin-bottom: 10px;">
            <span style="display:inline-block; margin: 0 3px; background:rgba(0,0,0,0.5); padding:6px; border-radius:8px; font-size:12px;">👤 Bastoni<br><hr style="margin:2px 0; border-color:green;">+70%</span>
            <span style="display:inline-block; margin: 0 3px; background:rgba(0,0,0,0.5); padding:6px; border-radius:8px; font-size:12px;">👤 Mkhitaryan<br><hr style="margin:2px 0; border-color:green;">+75%</span>
            <span style="display:inline-block; margin: 0 3px; background:rgba(0,0,0,0.5); padding:6px; border-radius:8px; font-size:12px;">👤 Barella<br><hr style="margin:2px 0; border-color:green;">+90%</span>
            <span style="display:inline-block; margin: 0 3px; background:rgba(0,0,0,0.5); padding:6px; border-radius:8px; font-size:12px;">👤 Koopmeiners<br><hr style="margin:2px 0; border-color:orange;">+60%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_panchina:
    st.subheader("Panchina & Riserve")
    
    # Lista dettagliata della panchina con fantamedia, voto e bonus
    panchina_list = [
        "Martinez Jo. (P) - FM: 6.17 | Bonus: +10%",
        "Doekhi (D) - FM: 6.33 | Bonus: +10%",
        "Scalvini (D) - FM: 6.17 | Bonus: +10%",
        "Bastoni S. (D) - FM: 6.0 | Bonus: +5%",
        "Akinsanmiro (C) - FM: 6.25 | Bonus: +15%",
        "Jones C. (C) - FM: 6.0 | Bonus: +5%"
    ]
    
    for giocatore in panchina_list:
        st.markdown(f"- {giocatore}")

# Footer o link rapidi ai siti di probabile formazione
st.markdown("---")
st.markdown("🔗 **Link Utili Probabili Formazioni:** [Gazzetta dello Sport](https://www.gazzetta.it) | [Sky Sport](https://sport.sky.it) | [Fantacalcio.it](https://www.fantacalcio.it)")
