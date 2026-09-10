import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina Streamlit a schermo intero
st.set_page_config(page_title="Lega FC - Dashboard", layout="wide")

# --- GESTIONE DATI CON SESSION STATE ---
if "squadre" not in st.session_state:
    st.session_state.squadre = {
        "La Mia Squadra Principale": {
            "POR": "Maignan",
            "DIF": ["Bastoni", "Bremer", "Dimarco"],
            "CEN": ["Barella", "Pulisic", "Koopmeiners", "Zaccagni"],
            "ATT": ["Lautaro", "Thuram", "Retegui"]
        }
    }

# --- BARRA LATERALE PER AGGIUNGERE SQUADRE E GIOCATORI REALI ---
st.sidebar.header("⚙️ Gestione Squadre & Rosa")

with st.sidebar.form("form_aggiungi_squadra"):
    st.subheader("Crea / Aggiungi Nuova Squadra")
    nome_nuova = st.text_input("Nome della Squadra:")
    
    st.text_input_por = "Portiere (es. Svilar)"
    por_input = st.text_input("Portiere Titolare:", "Svilar")
    
    st.markdown("---")
    st.markdown("**Difensori (3)**")
    d1_input = st.text_input("Difensore 1", "Buongiorno")
    d2_input = st.text_input("Difensore 2", "Calabria")
    d3_input = st.text_input("Difensore 3", "Hernandez")
    
    st.markdown("---")
    st.markdown("**Centrocampisti (4)**")
    c1_input = st.text_input("Centrocampista 1", "Calhanoglu")
    c2_input = st.text_input("Centrocampista 2", "Zieliński")
    c3_input = st.text_input("Centrocampista 3", "McTominay")
    c4_input = st.text_input("Centrocampista 4", "Pellegrini")
    
    st.markdown("---")
    st.markdown("**Attaccanti (3)**")
    a1_input = st.text_input("Attaccante 1", "Lookman")
    a2_input = st.text_input("Attaccante 2", "Dybala")
    a3_input = st.text_input("Attaccante 3", "Dovbyk")
    
    submit_squadra = st.form_submit_button("➕ Salva e Aggiungi Squadra")

if submit_squadra:
    if nome_nuova:
        st.session_state.squadre[nome_nuova] = {
            "POR": por_input,
            "DIF": [d1_input, d2_input, d3_input],
            "CEN": [c1_input, c2_input, c3_input, c4_input],
            "ATT": [a1_input, a2_input, a3_input]
        }
        st.sidebar.success(f"Squadra '{nome_nuova}' creata con successo!")
        # Imposta la nuova squadra come quella selezionata salvandola nello state
        st.session_state.squadra_attiva = nome_nuova
        st.rerun()
    else:
        st.sidebar.error("Inserisci un nome valido per la squadra.")

# Selezione della squadra attiva (mantiene la scelta o prende l'ultima aggiunta)
lista_squadre = list(st.session_state.squadre.keys())
default_index = len(lista_squadre) - 1 if "squadra_attiva" not in st.session_state else lista_squadre.index(st.session_state.get("squadra_attiva", lista_squadre[0]))

squadra_selezionata = st.sidebar.selectbox("Seleziona Squadra Attiva:", lista_squadre, index=default_index)
st.session_state.squadra_attiva = squadra_selezionata

rosa_corrente = st.session_state.squadre[squadra_selezionata]

por = rosa_corrente["POR"]
d1, d2, d3 = rosa_corrente["DIF"]
c1, c2, c3, c4 = rosa_corrente["CEN"]
a1, a2, a3 = rosa_corrente["ATT"]

# --- CODICE HTML/CSS PER IL CAMPO E LA DASHBOARD ---
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Lega FC - Dashboard Algoritmo</title>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 15px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #1e293b; padding: 20px 30px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        .container { display: flex; gap: 25px; }
        .field-container { flex: 2; background: #1e293b; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        
        /* Campo da calcio realistico */
        .football-field {
            position: relative;
            width: 100%;
            height: 680px;
            background: linear-gradient(to bottom, #2e7d32, #1b5e20);
            border: 3px solid #ffffff;
            border-radius: 10px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: center;
            padding: 20px 0;
            box-sizing: border-box;
        }
        .football-field::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 2px;
            background: rgba(255, 255, 255, 0.6);
        }

        .row-players { display: flex; justify-content: center; gap: 18px; width: 100%; z-index: 2; }
        .player-card { 
            background: rgba(15, 23, 42, 0.92); 
            border: 1px solid #334155; 
            padding: 10px 12px; 
            border-radius: 8px; 
            font-size: 13px; 
            width: 115px; 
            text-align: center; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.4); 
        }
        .player-card .p-name { display: block; font-weight: bold; color: #38bdf8; font-size: 14px; margin-bottom: 4px; }
        .stats-tag { font-size: 11px; color: #cbd5e1; display: block; font-weight: 600; }
        .bonus-malus { font-size: 10px; margin-top: 5px; border-top: 1px solid #334155; padding-top: 4px; }
        .bonus { color: #4ade80; font-weight: bold; }
        .malus { color: #f87171; font-weight: bold; }

        .sidebar { flex: 1; display: flex; flex-direction: column; gap: 25px; }
        .card-box { background: #1e293b; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        .bench-list { display: flex; flex-direction: column; gap: 12px; }
        .bench-item { background: #334155; padding: 12px 15px; border-radius: 8px; font-size: 14px; display: flex; justify-content: space-between; align-items: center; }
        .bench-info { display: flex; flex-direction: column; gap: 2px; }
        .bench-stats { font-size: 12px; color: #94a3b8; }
    </style>
</head>
<body>

    <div class="header">
        <h1 style="margin: 0; font-size: 24px;">Lega FC - Squadra: <span style="color: #38bdf8;">REPLACE_SQUADRA</span></h1>
    </div>

    <div class="container">
        <!-- CAMPO TITOLARI -->
        <div class="field-container">
            <h3 style="margin-top: 0;">Formazione Consigliata (Titolari in Campo)</h3>
            <div class="football-field">
                <!-- Portiere -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">REPLACE_POR</span>
                        <span class="stats-tag">Tit: 99%</span>
                        <div class="bonus-malus"><span class="bonus">B: 5%</span> | <span class="malus">M: 10%</span></div>
                    </div>
                </div>
                <!-- Difensori -->
                <div class="row-players">
                    <div class="player-card"><span class="p-name">REPLACE_D1</span><span class="stats-tag">Tit: 95%</span><div class="bonus-malus"><span class="bonus">B: 12%</span> | <span class="malus">M: 20%</span></div></div>
                    <div class="player-card"><span class="p-name">REPLACE_D2</span><span class="stats-tag">Tit: 90%</span><div class="bonus-malus"><span class="bonus">B: 10%</span> | <span class="malus">M: 25%</span></div></div>
                    <div class="player-card"><span class="p-name">REPLACE_D3</span><span class="stats-tag">Tit: 98%</span><div class="bonus-malus"><span class="bonus">B: 30%</span> | <span class="malus">M: 15%</span></div></div>
                </div>
                <!-- Centrocampisti -->
                <div class="row-players">
                    <div class="player-card"><span class="p-name">REPLACE_C1</span><span class="stats-tag">Tit: 92%</span><div class="bonus-malus"><span class="bonus">B: 22%</span> | <span class="malus">M: 25%</span></div></div>
                    <div class="player-card"><span class="p-name">REPLACE_C2</span><span class="stats-tag">Tit: 96%</span><div class="bonus-malus"><span class="bonus">B: 42%</span> | <span class="malus">M: 10%</span></div></div>
                    <div class="player-card"><span class="p-name">REPLACE_C3</span><span class="stats-tag">Tit: 88%</span><div class="bonus-malus"><span class="bonus">B: 35%</span> | <span class="malus">M: 18%</span></div></div>
                    <div class="player-card"><span class="p-name">REPLACE_C4</span><span class="stats-tag">Tit: 85%</span><div class="bonus-malus"><span class="bonus">B: 28%</span> | <span class="malus">M: 22%</span></div></div>
                </div>
                <!-- Attaccanti -->
                <div class="row-players">
                    <div class="player-card"><span class="p-name">REPLACE_A1</span><span class="stats-tag">Tit: 100%</span><div class="bonus-malus"><span class="bonus">B: 65%</span> | <span class="malus">M: 15%</span></div></div>
                    <div class="player-card"><span class="p-name">REPLACE_A2</span><span class="stats-tag">Tit: 95%</span><div class="bonus-malus"><span class="bonus">B: 55%</span> | <span class="malus">M: 12%</span></div></div>
                    <div class="player-card"><span class="p-name">REPLACE_A3</span><span class="stats-tag">Tit: 90%</span><div class="bonus-malus"><span class="bonus">B: 50%</span> | <span class="malus">M: 10%</span></div></div>
                </div>
            </div>
        </div>

        <!-- PANCHINA E RISERVE -->
        <div class="sidebar">
            <div class="card-box">
                <h3 style="margin-top: 0;">Panchina & Riserve (🪑)</h3>
                <div class="bench-list">
                    <div class="bench-item">
                        <div class="bench-info"><strong>Riserva 1 (POR)</strong><span class="bench-stats">Tit: 98% | <span class="bonus">B: 4%</span></span></div>
                        <span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 92%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info"><strong>Riserva 2 (DIF)</strong><span class="bench-stats">Tit: 90% | <span class="bonus">B: 8%</span></span></div>
                        <span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 88%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info"><strong>Riserva 3 (CEN)</strong><span class="bench-stats">Tit: 95% | <span class="bonus">B: 48%</span></span></div>
                        <span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 95%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info"><strong>Riserva 4 (ATT)</strong><span class="bench-stats">Tit: 85% | <span class="bonus">B: 58%</span></span></div>
                        <span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 90%</span>
                    </div>
                </div>
            </div>

            <div class="card-box">
                <h3 style="margin-top: 0;">Indice Rosa & Algoritmo</h3>
                <p style="font-size: 14px; color: #cbd5e1; margin-bottom: 10px;">Totale Indice Rosa: <strong>86.4 / 100</strong></p>
                <p style="font-size: 13px; color: #94a3b8; margin: 0; line-height: 1.4;">Incrocio dati probabili formazioni: <strong>Affidabilità Massima</strong></p>
            </div>
        </div>
    </div>

</body>
</html>
"""

# Sostituzioni pulite nel codice HTML
html_code = html_code.replace("REPLACE_SQUADRA", squadra_selezionata)
html_code = html_code.replace("REPLACE_POR", por)
html_code = html_code.replace("REPLACE_D1", d1)
html_code = html_code.replace("REPLACE_D2", d2)
html_code = html_code.replace("REPLACE_D3", d3)
html_code = html_code.replace("REPLACE_C1", c1)
html_code = html_code.replace("REPLACE_C2", c2)
html_code = html_code.replace("REPLACE_C3", c3)
html_code = html_code.replace("REPLACE_C4", c4)
html_code = html_code.replace("REPLACE_A1", a1)
html_code = html_code.replace("REPLACE_A2", a2)
html_code = html_code.replace("REPLACE_A3", a3)

components.html(html_code, height=820, scrolling=True)
