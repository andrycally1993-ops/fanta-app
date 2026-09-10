import streamlit as st

# Configurazione della pagina
st.set_page_config(page_title="FantAlgoritmo - Formazione Titolare", layout="wide")

# Intestazione dell'app
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; background-color: #f8f9fa; padding: 10px 20px; border-radius: 8px; border-bottom: 3px solid #2e7d32;">
        <h2 style="margin: 0; color: #1e293b;">⚽ FantAlgoritmo - Formazione Titolare</h2>
        <div>
            <span style="background-color: #e2e8f0; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; margin-right: 10px; color: #334155;">Totale Rosa: 25</span>
            <span style="background-color: #dcfce7; color: #166534; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 14px;">Indice Rosa: 8.6 / 10</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# Filtri: Rosa e Modulo di gioco
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    st.selectbox("Seleziona la rosa da visualizzare:", ["la beneamata ma non troppo"])
with col_f2:
    modulo_scelto = st.selectbox("Cambia Modulo:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2", "3-4-2-1"])

# Layout principale: Campo Titolari (Sinistra) e Panchina (Destra)
col_campo, col_panchina = st.columns([2, 1])

with col_campo:
    # Sezione Campo da Calcio con stili e dinamica del modulo
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%); padding: 20px; border-radius: 12px; border: 2px solid #155724; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; margin-bottom: 15px; color: white;">
                <span style="font-size: 20px; margin-right: 8px;">🏟️</span>
                <h3 style="margin: 0; font-size: 18px; color: white;">Campo Titolari ({modulo_scelto})</h3>
            </div>
            
            <!-- Attacco -->
            <div style="display: flex; justify-content: center; gap: 15px; margin-bottom: 20px;">
                <div style="background: rgba(0,0,0,0.5); padding: 8px 12px; border-radius: 8px; text-align: center; width: 95px;">
                    <div style="font-size: 24px;">👤</div>
                    <div style="color: white; font-size: 12px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Kvaratskhelia</div>
                    <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 4px 0;"></div>
                    <div style="color: #4ade80; font-size: 11px; font-weight: bold;">+85%</div>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 8px 12px; border-radius: 8px; text-align: center; width: 95px;">
                    <div style="font-size: 24px;">👤</div>
                    <div style="color: white; font-size: 12px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Esposito F.P.</div>
                    <div style="height: 4px; background-color: #f97316; border-radius: 2px; margin: 4px 0;"></div>
                    <div style="color: #fb923c; font-size: 11px; font-weight: bold;">+65%</div>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 8px 12px; border-radius: 8px; text-align: center; width: 95px;">
                    <div style="font-size: 24px;">👤</div>
                    <div style="color: white; font-size: 12px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Kean</div>
                    <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 4px 0;"></div>
                    <div style="color: #4ade80; font-size: 11px; font-weight: bold;">+80%</div>
                </div>
            </div>

            <!-- Centrocampo -->
            <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 20px;">
                <div style="background: rgba(0,0,0,0.5); padding: 6px 8px; border-radius: 8px; text-align: center; width: 85px;">
                    <div style="font-size: 20px;">👤</div>
                    <div style="color: white; font-size: 11px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Bastoni</div>
                    <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                    <div style="color: #4ade80; font-size: 10px; font-weight: bold;">+70%</div>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 6px 8px; border-radius: 8px; text-align: center; width: 85px;">
                    <div style="font-size: 20px;">👤</div>
                    <div style="color: white; font-size: 11px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Mkhitaryan</div>
                    <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                    <div style="color: #4ade80; font-size: 10px; font-weight: bold;">+75%</div>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 6px 8px; border-radius: 8px; text-align: center; width: 85px;">
                    <div style="font-size: 20px;">👤</div>
                    <div style="color: white; font-size: 11px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Barella</div>
                    <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                    <div style="color: #4ade80; font-size: 10px; font-weight: bold;">+90%</div>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 6px 8px; border-radius: 8px; text-align: center; width: 85px;">
                    <div style="font-size: 20px;">👤</div>
                    <div style="color: white; font-size: 11px; font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">Koopmeiners</div>
                    <div style="height: 4px; background-color: #f97316; border-radius: 2px; margin: 3px 0;"></div>
                    <div style="color: #fb923c; font-size: 10px; font-weight: bold;">+60%</div>
                </div>
            </div>

            <!-- Difesa -->
            <div style="display: flex; justify-content: center; gap: 15px;">
                <div style="background: rgba(0,0,0,0.5); padding: 6px 10px; border-radius: 8px; text-align: center; width: 90px;">
                    <div style="font-size: 20px;">👤</div>
                    <div style="color: white; font-size: 11px; font-weight: bold;">Di Lorenzo</div>
                    <div style="height: 4px; background-color: #ef4444; border-radius: 2px; margin: 3px 0;"></div>
                    <div style="color: #f87171; font-size: 10px; font-weight: bold;">+30%</div>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 6px 10px; border-radius: 8px; text-align: center; width: 90px;">
                    <div style="font-size: 20px;">👤</div>
                    <div style="color: white; font-size: 11px; font-weight: bold;">Bremer</div>
                    <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                    <div style="color: #4ade80; font-size: 10px; font-weight: bold;">+82%</div>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 6px 10px; border-radius: 8px; text-align: center; width: 90px;">
                    <div style="font-size: 20px;">👤</div>
                    <div style="color: white; font-size: 11px; font-weight: bold;">Buongiorno</div>
                    <div style="height: 4px; background-color: #22c55e; border-radius: 2px; margin: 3px 0;"></div>
                    <div style="color: #4ade80; font-size: 10px; font-weight: bold;">+88%</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_panchina:
    # Sezione Panchina con icona della sedia in legno (🪑)
    st.markdown("""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; margin-bottom: 12px; border-bottom: 2px solid #f1f5f9; padding-bottom: 8px;">
                <span style="font-size: 20px; margin-right: 8px;">🪑</span>
                <h3 style="margin: 0; font-size: 16px; color: #1e293b;">Panchina & Riserve</h3>
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
            <div style="font-size: 13px; padding: 6px 0; border-bottom: 1px solid #f8fafc; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #334155; font-weight: 500;">🔹 {nome}</span>
                <span style="color: #64748b; font-size: 12px;">FM: <b>{fm}</b> | <span style="color: #16a34a; font-weight: bold;">Bonus: {bonus}</span></span>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

# Link rapidi alle probabili formazioni in basso
st.markdown("---")
st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #64748b;">
        🔗 <b>Fonti Probabili Formazioni:</b> 
        <a href="https://www.gazzetta.it" target="_blank" style="color: #2563eb; text-decoration: none; margin: 0 5px;">Gazzetta</a> | 
        <a href="https://sport.sky.it" target="_blank" style="color: #2563eb; text-decoration: none; margin: 0 5px;">Sky Sport</a> | 
        <a href="https://www.fantacalcio.it" target="_blank" style="color: #2563eb; text-decoration: none; margin: 0 5px;">Fantacalcio.it</a>
    </div>
""", unsafe_allow_html=True)
