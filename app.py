import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="FantAlgoritmo - Formazione Titolare", layout="wide")

# Intestazione superiore pulita
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #f8f9fa; padding: 12px 20px; border-radius: 8px; border-bottom: 3px solid #2e7d32;">
        <h2 style="margin: 0; color: #1e293b; font-size: 20px;">⚽ FantAlgoritmo - Formazione Titolare</h2>
        <div>
            <span style="background-color: #e2e8f0; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 13px; margin-right: 10px; color: #334155;">Totale Rosa: 25</span>
            <span style="background-color: #dcfce7; color: #166534; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 13px;">Indice Rosa: 8.6 / 10</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# Filtri superiori: Rosa e Modulo
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    st.selectbox("Seleziona la rosa da visualizzare:", ["la beneamata ma non troppo"])
with col_f2:
    modulo_scelto = st.selectbox("Cambia Modulo:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])

# Layout principale a due colonne: Campo (Sinistra) e Panchina (Destra)
col_campo, col_panchina = st.columns([2, 1])

with col_campo:
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%); padding: 15px; border-radius: 12px 12px 0 0; border: 2px solid #155724; border-bottom: none;">
            <div style="display: flex; align-items: center; color: white;">
                <span style="font-size: 18px; margin-right: 8px;">🏟️</span>
                <h3 style="margin: 0; font-size: 16px; color: white;">Campo Titolari ({modulo_scelto})</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Contenitore del campo con sfondo verde uniforme
    with st.container():
        st.markdown("""
            <div style="background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%); padding: 15px; border-radius: 0 0 12px 12px; border: 2px solid #155724; border-top: none; margin-bottom: 20px;">
        """, unsafe_allow_html=True)
        
        # Attacco
        st.markdown("<p style='text-align: center; color: #a3e635; font-weight: bold; font-size: 12px; margin: 0 0 5px 0;'>ATTACCO</p>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label="Kvaratskhelia", value="+85%", delta="Titolare")
        with c2:
            st.metric(label="Esposito F.P.", value="+65%", delta="Ballottaggio")
        with c3:
            st.metric(label="Kean", value="+80%", delta="Titolare")

        # Centrocampo
        st.markdown("<p style='text-align: center; color: #a3e635; font-weight: bold; font-size: 12px; margin: 15px 0 5px 0;'>CENTROCAMPO</p>", unsafe_allow_html=True)
        cc1, cc2, cc3, cc4 = st.columns(4)
        with cc1:
            st.metric(label="Bastoni", value="+70%", delta="OK")
        with cc2:
            st.metric(label="Mkhitaryan", value="+75%", delta="OK")
        with cc3:
            st.metric(label="Barella", value="+90%", delta="Top")
        with cc4:
            st.metric(label="Koopmeiners", value="+60%", delta="Dubbio")

        # Difesa
        st.markdown("<p style='text-align: center; color: #a3e635; font-weight: bold; font-size: 12px; margin: 15px 0 5px 0;'>DIFESA</p>", unsafe_allow_html=True)
        d1, d2, d3 = st.columns(3)
        with d1:
            st.metric(label="Di Lorenzo", value="+30%", delta="A rischio")
        with d2:
            st.metric(label="Bremer", value="+82%", delta="Top")
        with d3:
            st.metric(label="Buongiorno", value="+88%", delta="Top")
            
        st.markdown("</div>", unsafe_allow_html=True)

with col_panchina:
    # Sezione Panchina con icona della sedia in legno (🪑)
    st.markdown("""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; margin-bottom: 12px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px;">
                <span style="font-size: 18px; margin-right: 8px;">🪑</span>
                <h3 style="margin: 0; font-size: 15px; color: #1e293b;">Panchina & Riserve</h3>
            </div>
    """, unsafe_allow_html=True)
    
    panchina_giocatori = [
        ("Martinez Jo. (P)", "6.17", "+10%"),
        ("Doekhi (D)", "6.33", "+10%"),
        ("Scalvini (D)", "6.17", "+10%"),
        ("Bastoni S. (D)", "6.00", "+5%"),
        ("Akinsanmiro (C)", "6.25", "+15%"),
        ("Jones C. (C)", "6.00", "+5%")
    ]
    
    for nome, fm, bonus in panchina_giocatori:
        st.markdown(f"""
            <div style="font-size: 12px; padding: 6px 0; border-bottom: 1px solid #f8fafc; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #334155; font-weight: 500;">🔹 {nome}</span>
                <span style="color: #64748b; font-size: 11px;">FM: <b>{fm}</b> | <span style="color: #16a34a; font-weight: bold;">Bonus: {bonus}</span></span>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Link rapidi alle fonti in basso
st.markdown("---")
st.markdown("""
    <div style="text-align: center; font-size: 13px; color: #64748b;">
        🔗 <b>Fonti Probabili Formazioni:</b> 
        <a href="https://www.gazzetta.it" target="_blank" style="color: #2563eb; text-decoration: none; margin: 0 5px;">Gazzetta</a> | 
        <a href="https://sport.sky.it" target="_blank" style="color: #2563eb; text-decoration: none; margin: 0 5px;">Sky Sport</a> | 
        <a href="https://www.fantacalcio.it" target="_blank" style="color: #2563eb; text-decoration: none; margin: 0 5px;">Fantacalcio.it</a>
    </div>
""", unsafe_allow_html=True)
