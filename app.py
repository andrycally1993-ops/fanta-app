import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="FantAlgoritmo - Formazione Titolare", layout="wide")

# Intestazione superiore
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
    # Intestazione del campo
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%); padding: 12px 15px; border-radius: 12px 12px 0 0; border: 2px solid #155724; border-bottom: none; display: flex; align-items: center; color: white;">
            <span style="font-size: 18px; margin-right: 8px;">🏟️</span>
            <h3 style="margin: 0; font-size: 16px; color: white;">Campo Titolari ({modulo_scelto})</h3>
        </div>
    """, unsafe_allow_html=True)

    # Contenitore verde del campo
    st.markdown("""
        <div style="background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%); padding: 20px; border-radius: 0 0 12px 12px; border: 2px solid #155724; border-top: none; margin-bottom: 20px;">
    """, unsafe_allow_html=True)
    
    # ATTACCO
    st.markdown("<p style='text-align: center; color: #a3e635; font-weight: bold; font-size: 11px; margin: 0 0 8px 0; letter-spacing: 1px;'>ATTACCO</p>", unsafe_allow_html=True)
    att1, att2, att3 = st.columns(3)
    
    with att1:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 8px; border-radius: 8px; text-align: center;">
                <div style="font-size: 22px;">👤</div>
                <div style="color: white; font-size: 11px; font-weight: bold;">Tuo Giocatore 1</div>
                <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 4px 0;"></div>
                <div style="color: #4ade80; font-size: 10px; font-weight: bold;">🟢 Titolare</div>
            </div>
        """, unsafe_allow_html=True)
    with att2:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 8px; border-radius: 8px; text-align: center;">
                <div style="font-size: 22px;">👤</div>
                <div style="color: white; font-size: 11px; font-weight: bold;">Tuo Giocatore 2</div>
                <div style="height: 4px; background-color: #f97316; border-radius: 2px; margin: 4px 0;"></div>
                <div style="color: #fb923c; font-size: 10px; font-weight: bold;">🟠 Ballottaggio</div>
            </div>
        """, unsafe_allow_html=True)
    with att3:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 8px; border-radius: 8px; text-align: center;">
                <div style="font-size: 22px;">👤</div>
                <div style="color: white; font-size: 11px; font-weight: bold;">Tuo Giocatore 3</div>
                <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 4px 0;"></div>
                <div style="color: #4ade80; font-size: 10px; font-weight: bold;">🟢 Titolare</div>
            </div>
        """, unsafe_allow_html=True)

    # CENTROCAMPO
    st.markdown("<p style='text-align: center; color: #a3e635; font-weight: bold; font-size: 11px; margin: 20px 0 8px 0; letter-spacing: 1px;'>CENTROCAMPO</p>", unsafe_allow_html=True)
    cc1, cc2, cc3, cc4 = st.columns(4)
    
    with cc1:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 6px; border-radius: 8px; text-align: center;">
                <div style="font-size: 18px;">👤</div>
                <div style="color: white; font-size: 10px; font-weight: bold;">CC 1</div>
                <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                <div style="color: #4ade80; font-size: 9px; font-weight: bold;">🟢 Titolare</div>
            </div>
        """, unsafe_allow_html=True)
    with cc2:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 6px; border-radius: 8px; text-align: center;">
                <div style="font-size: 18px;">👤</div>
                <div style="color: white; font-size: 10px; font-weight: bold;">CC 2</div>
                <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                <div style="color: #4ade80; font-size: 9px; font-weight: bold;">🟢 Titolare</div>
            </div>
        """, unsafe_allow_html=True)
    with cc3:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 6px; border-radius: 8px; text-align: center;">
                <div style="font-size: 18px;">👤</div>
                <div style="color: white; font-size: 10px; font-weight: bold;">CC 3</div>
                <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                <div style="color: #4ade80; font-size: 9px; font-weight: bold;">🟢 Titolare</div>
            </div>
        """, unsafe_allow_html=True)
    with cc4:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 6px; border-radius: 8px; text-align: center;">
                <div style="font-size: 18px;">👤</div>
                <div style="color: white; font-size: 10px; font-weight: bold;">CC 4</div>
                <div style="height: 4px; background-color: #f97316; border-radius: 2px; margin: 3px 0;"></div>
                <div style="color: #fb923c; font-size: 9px; font-weight: bold;">🟠 Ballottaggio</div>
            </div>
        """, unsafe_allow_html=True)

    # DIFESA
    st.markdown("<p style='text-align: center; color: #a3e635; font-weight: bold; font-size: 11px; margin: 20px 0 8px 0; letter-spacing: 1px;'>DIFESA</p>", unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    
    with d1:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 6px; border-radius: 8px; text-align: center;">
                <div style="font-size: 18px;">👤</div>
                <div style="color: white; font-size: 10px; font-weight: bold;">DC 1</div>
                <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                <div style="color: #4ade80; font-size: 9px; font-weight: bold;">🟢 Titolare</div>
            </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 6px; border-radius: 8px; text-align: center;">
                <div style="font-size: 18px;">👤</div>
                <div style="color: white; font-size: 10px; font-weight: bold;">DC 2</div>
                <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                <div style="color: #4ade80; font-size: 9px; font-weight: bold;">🟢 Titolare</div>
            </div>
        """, unsafe_allow_html=True)
    with d3:
        st.markdown("""
            <div style="background: rgba(0,0,0,0.5); padding: 6px; border-radius: 8px; text-align: center;">
                <div style="font-size: 18px;">👤</div>
                <div style="color: white; font-size: 10px; font-weight: bold;">DC 3</div>
                <div style="height: 4px; background-color: #f97316; border-radius: 2px; margin: 3px 0;"></div>
                <div style="color: #fb923c; font-size: 9px; font-weight: bold;">🟠 Ballottaggio</div>
            </div>
        """, unsafe_allow_html=True)

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
        ("Riserva 1 (P)", "6.17", "+10%"),
        ("Riserva 2 (D)", "6.33", "+10%"),
        ("Riserva 3 (D)", "6.17", "+10%"),
        ("Riserva 4 (D)", "6.00", "+5%"),
        ("Riserva 5 (C)", "6.25", "+15%"),
        ("Riserva 6 (C)", "6.00", "+5%")
    ]
    
    for nome, fm, bonus in panchina_giocatori:
        st.markdown(f"""
            <div style="font-size: 12px; padding: 5px 0; border-bottom: 1px solid #f8fafc; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #334155; font-weight: 500;">🔹 {nome}</span>
                <span style="color: #64748b; font-size: 11px;">FM: <b>{fm}</b> | <span style="color: #16a34a; font-weight: bold;">Bonus: {bonus}</span></span>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
