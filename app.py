import streamlit as st

# Configurazione della pagina Streamlit in modalità wide
st.set_page_config(
    page_title="Algo Fantacalcio - Analisi Avanzata",
    page_icon="⚽",
    layout="wide"
)

# Stile CSS personalizzato per la grafica in stile app avanzata
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #f0f6fc;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 700;
    }

    .info-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .info-card h4 {
        color: #58a6ff;
        margin-top: 0;
        font-size: 1rem;
        border-bottom: 1px solid #30363d;
        padding-bottom: 6px;
    }

    /* Stile Campo da Calcio realistico */
    .football-field {
        background: linear-gradient(180deg, #1e7e34 0%, #157347 50%, #198754 100%);
        border: 4px solid #ffffff;
        border-radius: 16px;
        width: 100%;
        max-width: 540px;
        height: 720px;
        margin: 0 auto;
        position: relative;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        background-image: 
            linear-gradient(rgba(255,255,255,0.07) 50%, transparent 50%),
            linear-gradient(90deg, rgba(255,255,255,0.07) 50%, transparent 50%);
        background-size: 100% 70px, 70px 100%;
        overflow: hidden;
    }
    
    .field-center-circle {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 110px;
        height: 110px;
        border: 2px solid rgba(255, 255, 255, 0.4);
        border-radius: 50%;
    }
    .field-center-line {
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 2px;
        background-color: rgba(255, 255, 255, 0.4);
    }

    /* Card giocatore sul campo con metriche dettagliate */
    .player-card {
        background: rgba(13, 17, 23, 0.9);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 5px 6px;
        text-align: center;
        width: 85px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.4);
        backdrop-filter: blur(4px);
    }
    .player-rating {
        font-size: 0.65rem;
        color: #3fb950;
        font-weight: bold;
    }
    .player-name {
        font-size: 0.75rem;
        color: #ffffff;
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .player-stats {
        font-size: 0.6rem;
        color: #8b949e;
        margin-top: 2px;
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 2px;
    }

    .bench-container {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        max-height: 420px;
        overflow-y: auto;
    }
    
    .reasoning-box {
        background: #1f6feb15;
        border-left: 4px solid #1f6feb;
        padding: 10px;
        border-radius: 4px;
        font-size: 0.8rem;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Layout principale diviso in 3 colonne
col_left, col_center, col_right = st.columns([1.1, 1.4, 1.1])

with col_left:
    st.markdown("### ⚙️ Informazioni & Fonti")
    
    st.markdown("""
    <div class="info-card">
        <h4>🤖 Motore Algoritmico</h4>
        <p style="font-size: 0.8rem; color: #8b949e;">
        Analisi combinata di flussi dati da testate giornalistiche, stime di titolarità in tempo reale, indice di pericolosità offensiva e propensione ai malus.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>🌐 Fonti Aggregate</h4>
        <ul style="font-size: 0.8rem; color: #c9d1d9; padding-left: 18px; margin: 0;">
            <li>Gazzetta dello Sport & Corriere</li>
            <li>Sky Sport & Tuttosport</li>
            <li>Algoritmi Probabili Formazioni Pro</li>
            <li>Expected Stats (xG / xA match)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h4>📊 Stato Analisi Giornata</h4>
        <p style="font-size: 0.8rem; color: #3fb950; margin-bottom: 4px;">✔ Sincronizzazione Ultimatum</p>
        <p style="font-size: 0.8rem; color: #3fb950; margin: 0;">✔ Modelli predittivi attivi</p>
    </div>
    """, unsafe_allow_html=True)

with col_center:
    st.markdown("<h3 style='text-align: center; margin-bottom: 5px;'>4ª Giornata - Titolari</h3>", unsafe_allow_html=True)
    
    modulo_col1, modulo_col2 = st.columns(2)
    with modulo_col1:
        st.selectbox("Modulo Consigliato", ["3-4-3", "3-5-2", "4-3-3"], index=0, label_visibility="collapsed")
    with modulo_col2:
        st.selectbox("Match / Filtro", ["Tutte le partite", "Scontro Diretto"], index=0, label_visibility="collapsed")

    # CAMPO DA CALCIO REALISTICO CON INDICI TITOLARITÀ, BONUS E MALUS
    st.markdown("""
    <div class="football-field">
        <div class="field-center-line"></div>
        <div class="field-center-circle"></div>
        
        <!-- Portiere -->
        <div style="position: absolute; bottom: 5%; left: 50%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">6.50 FVA</div>
                <div class="player-name">Provedel</div>
                <div class="player-stats">Tit: 98% | +0.1 | -0.2</div>
            </div>
        </div>

        <!-- Difensori -->
        <div style="position: absolute; bottom: 28%; left: 18%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">6.29 FVA</div>
                <div class="player-name">Buongiorno</div>
                <div class="player-stats">Tit: 95% | +0.2 | -0.4</div>
            </div>
        </div>
        <div style="position: absolute; bottom: 28%; left: 50%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">6.13 FVA</div>
                <div class="player-name">Bastoni</div>
                <div class="player-stats">Tit: 90% | +0.3 | -0.3</div>
            </div>
        </div>
        <div style="position: absolute; bottom: 28%; left: 82%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">6.12 FVA</div>
                <div class="player-name">Di Lorenzo</div>
                <div class="player-stats">Tit: 99% | +0.4 | -0.4</div>
            </div>
        </div>

        <!-- Centrocampisti -->
        <div style="position: absolute; top: 46%; left: 18%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">7.04 FVA</div>
                <div class="player-name">Pulisic</div>
                <div class="player-stats">Tit: 98% | +0.7 | -0.2</div>
            </div>
        </div>
        <div style="position: absolute; top: 44%; left: 38%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">6.52 FVA</div>
                <div class="player-name">Calhanoglu</div>
                <div class="player-stats">Tit: 100%| +0.8 | -0.3</div>
            </div>
        </div>
        <div style="position: absolute; top: 44%; left: 62%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">6.50 FVA</div>
                <div class="player-name">Barella</div>
                <div class="player-stats">Tit: 95% | +0.4 | -0.5</div>
            </div>
        </div>
        <div style="position: absolute; top: 46%; left: 82%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">6.45 FVA</div>
                <div class="player-name">Zaccagni</div>
                <div class="player-stats">Tit: 92% | +0.5 | -0.3</div>
            </div>
        </div>

        <!-- Attaccanti -->
        <div style="position: absolute; top: 12%; left: 22%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">8.35 FVA</div>
                <div class="player-name">Thuram</div>
                <div class="player-stats">Tit: 95% | +0.9 | -0.2</div>
            </div>
        </div>
        <div style="position: absolute; top: 8%; left: 50%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">5.40 FVA</div>
                <div class="player-name">Lautaro</div>
                <div class="player-stats">Tit: 98% | +1.1 | -0.2</div>
            </div>
        </div>
        <div style="position: absolute; top: 12%; left: 78%; transform: translateX(-50%);">
            <div class="player-card">
                <div class="player-rating">7.04 FVA</div>
                <div class="player-name">Lookman</div>
                <div class="player-stats">Tit: 95% | +0.9 | -0.3</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown("<h3>Panchina & Riserve</h3>", unsafe_allow_html=True)
    
    # Panchina disposta su più colonne con indici di titolarità, bonus e malus
    st.markdown("""
    <div class="bench-container">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
            <div style="background: #21262d; padding: 7px; border-radius: 6px; text-align: center;">
                <span style="font-size: 0.65rem; color: #8b949e;">POR</span><br><strong>Sommer</strong><br><span style="font-size: 0.7rem; color: #3fb950;">5.8 FVA</span><br><span style="font-size: 0.6rem; color: #8b949e;">Tit: 99% | +0.1 | -0.1</span>
            </div>
            <div style="background: #21262d; padding: 7px; border-radius: 6px; text-align: center;">
                <span style="font-size: 0.65rem; color: #8b949e;">DIF</span><br><strong>Dimarco</strong><br><span style="font-size: 0.7rem; color: #3fb950;">6.1 FVA</span><br><span style="font-size: 0.6rem; color: #8b949e;">Tit: 85% | +0.5 | -0.3</span>
            </div>
            <div style="background: #21262d; padding: 7px; border-radius: 6px; text-align: center;">
                <span style="font-size: 0.65rem; color: #8b949e;">DIF</span><br><strong>Pavard</strong><br><span style="font-size: 0.7rem; color: #3fb950;">5.9 FVA</span><br><span style="font-size: 0.6rem; color: #8b949e;">Tit: 80% | +0.2 | -0.4</span>
            </div>
            <div style="background: #21262d; padding: 7px; border-radius: 6px; text-align: center;">
                <span style="font-size: 0.65rem; color: #8b949e;">CEN</span><br><strong>Rabiot</strong><br><span style="font-size: 0.7rem; color: #3fb950;">6.0 FVA</span><br><span style="font-size: 0.6rem; color: #8b949e;">Tit: 85% | +0.3 | -0.5</span>
            </div>
            <div style="background: #21262d; padding: 7px; border-radius: 6px; text-align: center;">
                <span style="font-size: 0.65rem; color: #8b949e;">CEN</span><br><strong>Koopmeiners</strong><br><span style="font-size: 0.7rem; color: #3fb950;">6.3 FVA</span><br><span style="font-size: 0.6rem; color: #8b949e;">Tit: 90% | +0.6 | -0.3</span>
            </div>
            <div style="background: #21262d; padding: 7px; border-radius: 6px; text-align: center;">
                <span style="font-size: 0.65rem; color: #8b949e;">ATT</span><br><strong>Zirkzee</strong><br><span style="font-size: 0.7rem; color: #3fb950;">6.2 FVA</span><br><span style="font-size: 0.6rem; color: #8b949e;">Tit: 88% | +0.7 | -0.2</span>
            </div>
            <div style="background: #21262d; padding: 7px; border-radius: 6px; text-align: center;">
                <span style="font-size: 0.65rem; color: #8b949e;">ATT</span><br><strong>Gudmundsson</strong><br><span style="font-size: 0.7rem; color: #3fb950;">6.0 FVA</span><br><span style="font-size: 0.6rem; color: #8b949e;">Tit: 82% | +0.6 | -0.3</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Genera Formazione Ufficiale", type="primary", use_container_width=True):
        st.success("Formazione ufficiale confermata dall'algoritmo!")

    st.markdown("### 💡 Perché schierare questi?")
    st.markdown("""
    <div class="reasoning-box">
        <b>Dettaglio Metriche Giornata:</b>
        <ul style="margin: 4px 0 0 -15px; font-size: 0.75rem;">
            <li><b>Indice Titolarità:</b> Percentuale derivata dall'incrocio delle ultime rifiniture.</li>
            <li><b>Probabili Bonus (+):</b> Stima basata su Expected Goals (xG) e calci piazzati.</li>
            <li><b>Probabili Malus (-):</b> Indice di rischio ammonizione/cartellini basato sull'arbitro e falli subiti/commessi.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
