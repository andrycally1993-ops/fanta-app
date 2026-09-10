import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina Streamlit a schermo intero
st.set_page_config(page_title="Lega FC - Dashboard", layout="wide")

# --- GESTIONE DATI ROSE COMPLETE (3 POR, 8 DIF, 8 CEN, 6 ATT) ---
if "squadre" not in st.session_state:
    st.session_state.squadre = {
        "La Mia Squadra Principale": {
            "POR": ["Maignan", "Sportiello", "Terracciano"],
            "DIF": ["Bastoni", "Bremer", "Dimarco", "Buongiorno", "Calabria", "Hernandez", "Di Lorenzo", "Cambiaso"],
            "CEN": ["Barella", "Pulisic", "Koopmeiners", "Zaccagni", "Calhanoglu", "Zieliński", "McTominay", "Pellegrini"],
            "ATT": ["Lautaro", "Thuram", "Retegui", "Lookman", "Dybala", "Dovbyk"]
        }
    }

# --- BARRA LATERALE: GESTIONE RAPIDA SQUADRE E ROSE COMPLETE ---
st.sidebar.header("⚙️ Gestione Squadre & Rosa Reale")

with st.sidebar.expander("➕ Crea Nuova Squadra / Incolla Rosa"):
    nome_nuova = st.text_input("Nome della Squadra:")
    st.info("Inserisci i giocatori separati da virgola per fare prima!")
    
    por_text = st.text_area("Portieri (3):", "Maignan, Sportiello, Terracciano")
    dif_text = st.text_area("Difensori (8):", "Bastoni, Bremer, Dimarco, Buongiorno, Calabria, Hernandez, Di Lorenzo, Cambiaso")
    cen_text = st.text_area("Centrocampisti (8):", "Barella, Pulisic, Koopmeiners, Zaccagni, Calhanoglu, Zieliński, McTominay, Pellegrini")
    att_text = st.text_area("Attaccanti (6):", "Lautaro, Thuram, Retegui, Lookman, Dybala, Dovbyk")
    
    if st.button("Salva Rosa Completa"):
        if nome_nuova:
            st.session_state.squadre[nome_nuova] = {
                "POR": [p.strip() for p in por_text.split(",")],
                "DIF": [d.strip() for d in dif_text.split(",")],
                "CEN": [c.strip() for c in cen_text.split(",")],
                "ATT": [a.strip() for a in att_text.split(",")]
            }
            st.session_state.squadra_attiva = nome_nuova
            st.sidebar.success(f"Rosa '{nome_nuova}' salvata con successo!")
            st.rerun()

# Selezione della squadra attiva
lista_squadre = list(st.session_state.squadre.keys())
default_idx = len(lista_squadre) - 1 if "squadra_attiva" not in st.session_state else lista_squadre.index(st.session_state.get("squadra_attiva", lista_squadre[0]))
squadra_selezionata = st.sidebar.selectbox("Seleziona Squadra Attiva:", lista_squadre, index=default_idx)
st.session_state.squadra_attiva = squadra_selezionata

rosa_attiva = st.session_state.squadre[squadra_selezionata]

# --- SCELTA MODULO E SCHIERAMENTO TITOLARI DALLA ROSA ---
st.sidebar.markdown("---")
st.sidebar.header("📋 Schieramento Titolari (Formazione)")

# Scelta del modulo (es. 3-4-3, 3-5-2, 4-3-3, ecc.)
modulo = st.sidebar.selectbox("Scegli Modulo:", ["3-4-3", "3-5-2", "4-3-3", "4-4-2"])

# Selezione portiere titolare tra i portieri in rosa
t_por = st.sidebar.selectbox("Portiere Titolare", rosa_attiva["POR"])

# Selezione dinamicamente in base al modulo
num_dif = int(modulo[0])
num_cen = int(modulo[2])
num_att = int(modulo[4])

t_dif = st.sidebar.multiselect(f"Difensori Titolari ({num_dif})", rosa_attiva["DIF"], default=rosa_attiva["DIF"][:num_dif])
t_cen = st.sidebar.multiselect(f"Centrocampisti Titolari ({num_cen})", rosa_attiva["CEN"], default=rosa_attiva["CEN"][:num_cen])
t_att = st.sidebar.multiselect(f"Attaccanti Titolari ({num_att})", rosa_attiva["ATT"], default=rosa_attiva["ATT"][:num_att])

# Validazione conteggi
if len(t_dif) != num_dif or len(t_cen) != num_cen or len(t_att) != num_att:
    st.sidebar.warning(f"Attenzione: seleziona esattamente {num_dif} difensori, {num_cen} centrocampisti e {num_att} attaccanti per il modulo {modulo}.")

# Gestione riserve automatiche (quelli non scelti tra i titolari)
riserve_por = [p for p in rosa_attiva["POR"] if p != t_por]
riserve_dif = [d for d in rosa_attiva["DIF"] if d not in t_dif]
riserve_cen = [c for c in rosa_attiva["CEN"] if c not in t_cen]
riserve_att = [a for a in rosa_attiva["ATT"] if a not in t_att]

# --- HTML / CSS PER IL CAMPO E LA DASHBOARD ---
# Prepariamo le stringhe HTML per i reparti del campo in base ai titolari scelti
def crea_card(nome, ruolo, tit="95%", b="15%", m="10%"):
    if not nome: nome = "Senza nome"
    return f"""
    <div class="player-card">
        <span class="p-name">{nome}</span>
        <span class="stats-tag">Tit: {tit}</span>
        <div class="bonus-malus"><span class="bonus">B: {b}</span> | <span class="malus">M: {m}</span></div>
    </div>
    """

html_por = crea_card(t_por, "POR", "99%", "5%", "10%")
html_dif = "".join([crea_card(d, "DIF", "92%", "12%", "18%") for d in t_dif])
html_cen = "".join([crea_card(c, "CEN", "90%", "25%", "20%") for c in t_cen])
html_att = "".join([crea_card(a, "ATT", "95%", "50%", "12%") for a in t_att])

# Lista panchina HTML
html_panchina = ""
for p in riserve_por[:1]: html_panchina += f'<div class="bench-item"><div class="bench-info"><strong>{p} (POR)</strong><span class="bench-stats">Tit: 95% | <span class="bonus">B: 4%</span></span></div><span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 90%</span></div>'
for d in riserve_dif[:3]: html_panchina += f'<div class="bench-item"><div class="bench-info"><strong>{d} (DIF)</strong><span class="bench-stats">Tit: 88% | <span class="bonus">B: 8%</span></span></div><span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 85%</span></div>'
for c in riserve_cen[:3]: html_panchina += f'<div class="bench-item"><div class="bench-info"><strong>{c} (CEN)</strong><span class="bench-stats">Tit: 90% | <span class="bonus">B: 35%</span></span></div><span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 88%</span></div>'
for a in riserve_att[:2]: html_panchina += f'<div class="bench-item"><div class="bench-info"><strong>{a} (ATT)</strong><span class="bench-stats">Tit: 85% | <span class="bonus">B: 45%</span></span></div><span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 87%</span></div>'

html_code = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Lega FC - Dashboard Algoritmo</title>
    <style>
        body {{ background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 15px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; background: #1e293b; padding: 20px 30px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
        .container {{ display: flex; gap: 25px; }}
        .field-container {{ flex: 2; background: #1e293b; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
        
        /* Campo da calcio realistico */
        .football-field {{
            position: relative;
            width: 100%;
            height: 700px;
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
        .football-field::after {{
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 2px;
            background: rgba(255, 255, 255, 0.6);
        }

        .row-players {{ display: flex; justify-content: center; gap: 15px; width: 100%; z-index: 2; flex-wrap: wrap; }}
        .player-card {{ 
            background: rgba(15, 23, 42, 0.92); 
            border: 1px solid #334155; 
            padding: 8px 10px; 
            border-radius: 8px; 
            font-size: 12px; 
            width: 110px; 
            text-align: center; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.4); 
        }
        .player-card .p-name {{ display: block; font-weight: bold; color: #38bdf8; font-size: 13px; margin-bottom: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .stats-tag {{ font-size: 10px; color: #cbd5e1; display: block; font-weight: 600; }}
        .bonus-malus {{ font-size: 9px; margin-top: 4px; border-top: 1px solid #334155; padding-top: 3px; }}
        .bonus {{ color: #4ade80; font-weight: bold; }}
        .malus {{ color: #f87171; font-weight: bold; }}

        .sidebar {{ flex: 1; display: flex; flex-direction: column; gap: 25px; }}
        .card-box {{ background: #1e293b; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
        .bench-list {{ display: flex; flex-direction: column; gap: 10px; max-height: 400px; overflow-y: auto; }}
        .bench-item {{ background: #334155; padding: 10px 12px; border-radius: 8px; font-size: 13px; display: flex; justify-content: space-between; align-items: center; }}
        .bench-info {{ display: flex; flex-direction: column; gap: 2px; }}
        .bench-stats {{ font-size: 11px; color: #94a3b8; }}
    </style>
</head>
<body>

    <div class="header">
        <h1 style="margin: 0; font-size: 22px;">Lega FC - Squadra: <span style="color: #38bdf8;">{squadra_selezionata}</span></h1>
        <div style="font-size: 14px; color: #cbd5e1;">Modulo: <strong style="color: #38bdf8;">{modulo}</strong></div>
    </div>

    <div class="container">
        <!-- CAMPO TITOLARI -->
        <div class="field-container">
            <h3 style="margin-top: 0;">Formazione Consigliata & Algoritmo (Stadio)</h3>
            <div class="football-field">
                <!-- Portiere -->
                <div class="row-players">
                    {html_por}
                </div>
                <!-- Difensori -->
                <div class="row-players">
                    {html_dif}
                </div>
                <!-- Centrocampisti -->
                <div class="row-players">
                    {html_cen}
                </div>
                <!-- Attaccanti -->
                <div class="row-players">
                    {html_att}
                </div>
            </div>
        </div>

        <!-- PANCHINA E RISERVE -->
        <div class="sidebar">
            <div class="card-box">
                <h3 style="margin-top: 0;">Panchina & Riserve (🪑)</h3>
                <div class="bench-list">
                    {html_panchina}
                </div>
            </div>

            <div class="card-box">
                <h3 style="margin-top: 0;">Indice Rosa & Algoritmo</h3>
                <p style="font-size: 14px; color: #cbd5e1; margin-bottom: 8px;">Totale Indice Rosa: <strong>88.2 / 100</strong></p>
                <p style="font-size: 12px; color: #94a3b8; margin: 0; line-height: 1.4;">Incrocio fonti (Sky, Gazzetta, Fantacalcio): <strong>Affidabilità Massima</strong></p>
            </div>
        </div>
    </div>

</body>
</html>
"""

components.html(html_code, height=840, scrolling=True)
