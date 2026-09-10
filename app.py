import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina Streamlit a schermo intero
st.set_page_config(page_title="Lega FC - Dashboard", layout="wide")

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Lega FC - Gestione Multi-Squadra & Algoritmo</title>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 15px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #1e293b; padding: 20px 30px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        .team-selector select { background: #0f172a; color: #38bdf8; border: 1px solid #334155; padding: 10px 15px; border-radius: 8px; font-weight: bold; font-size: 14px; cursor: pointer; }
        .container { display: flex; gap: 25px; }
        .field-container { flex: 2; background: #1e293b; padding: 25px; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        
        /* Campo da calcio realistico e più alto/largo */
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
        /* Linea di metà campo */
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
        
        /* Card dei giocatori più grandi e leggibili */
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
        <h1 style="margin: 0; font-size: 24px;">Lega FC - Dashboard Algoritmo</h1>
        <div class="team-selector">
            <label for="teamSelect">Squadra: </label>
            <select id="teamSelect">
                <option value="1">La Tua Squadra Principale</option>
                <option value="2">Seconda Squadra</option>
                <option value="3">Terza Squadra</option>
            </select>
        </div>
    </div>

    <div class="container">
        <!-- CAMPO TITOLARI (STADIO) -->
        <div class="field-container">
            <h3 style="margin-top: 0;">Formazione Consigliata (Titolari in Campo)</h3>
            <div class="football-field">
                <!-- Portiere -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">Tuo Portiere</span>
                        <span class="stats-tag">Tit: 99%</span>
                        <div class="bonus-malus"><span class="bonus">B: 5%</span> | <span class="malus">M: 10%</span></div>
                    </div>
                </div>
                <!-- Difensori (3) -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">Difensore 1</span>
                        <span class="stats-tag">Tit: 95%</span>
                        <div class="bonus-malus"><span class="bonus">B: 12%</span> | <span class="malus">M: 20%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Difensore 2</span>
                        <span class="stats-tag">Tit: 90%</span>
                        <div class="bonus-malus"><span class="bonus">B: 10%</span> | <span class="malus">M: 25%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Difensore 3</span>
                        <span class="stats-tag">Tit: 98%</span>
                        <div class="bonus-malus"><span class="bonus">B: 30%</span> | <span class="malus">M: 15%</span></div>
                    </div>
                </div>
                <!-- Centrocampisti (4) -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">Cento 1</span>
                        <span class="stats-tag">Tit: 92%</span>
                        <div class="bonus-malus"><span class="bonus">B: 22%</span> | <span class="malus">M: 25%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Cento 2</span>
                        <span class="stats-tag">Tit: 96%</span>
                        <div class="bonus-malus"><span class="bonus">B: 42%</span> | <span class="malus">M: 10%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Cento 3</span>
                        <span class="stats-tag">Tit: 88%</span>
                        <div class="bonus-malus"><span class="bonus">B: 35%</span> | <span class="malus">M: 18%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Cento 4</span>
                        <span class="stats-tag">Tit: 85%</span>
                        <div class="bonus-malus"><span class="bonus">B: 28%</span> | <span class="malus">M: 22%</span></div>
                    </div>
                </div>
                <!-- Attaccanti (3) -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">Attaccante 1</span>
                        <span class="stats-tag">Tit: 100%</span>
                        <div class="bonus-malus"><span class="bonus">B: 65%</span> | <span class="malus">M: 15%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Attaccante 2</span>
                        <span class="stats-tag">Tit: 95%</span>
                        <div class="bonus-malus"><span class="bonus">B: 55%</span> | <span class="malus">M: 12%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Attaccante 3</span>
                        <span class="stats-tag">Tit: 90%</span>
                        <div class="bonus-malus"><span class="bonus">B: 50%</span> | <span class="malus">M: 10%</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- PANCHINA E RISERVE (SEDIA) -->
        <div class="sidebar">
            <div class="card-box">
                <h3 style="margin-top: 0;">Panchina & Riserve (🪑)</h3>
                <div class="bench-list">
                    <div class="bench-item">
                        <div class="bench-info">
                            <strong style="font-size: 15px;">Riserva 1 (POR)</strong>
                            <span class="bench-stats">Tit: 98% | <span class="bonus">B: 4%</span></span>
                        </div>
                        <span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 92%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info">
                            <strong style="font-size: 15px;">Riserva 2 (DIF)</strong>
                            <span class="bench-stats">Tit: 90% | <span class="bonus">B: 8%</span></span>
                        </div>
                        <span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 88%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info">
                            <strong style="font-size: 15px;">Riserva 3 (CEN)</strong>
                            <span class="bench-stats">Tit: 95% | <span class="bonus">B: 48%</span></span>
                        </div>
                        <span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 95%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info">
                            <strong style="font-size: 15px;">Riserva 4 (ATT)</strong>
                            <span class="bench-stats">Tit: 85% | <span class="bonus">B: 58%</span></span>
                        </div>
                        <span style="color: #38bdf8; font-weight: bold; font-size: 13px;">Alg: 90%</span>
                    </div>
                </div>
            </div>

            <div class="card-box">
                <h3 style="margin-top: 0;">Indice Rosa & Algoritmo</h3>
                <p style="font-size: 14px; color: #cbd5e1; margin-bottom: 10px;">Totale Indice Rosa: <strong>86.4 / 100</strong></p>
                <p style="font-size: 13px; color: #94a3b8; margin: 0; line-height: 1.4;">Incrocio dati probabili formazioni (Sky, Gazzetta, Corsport, Fantacalcio): <strong>Affidabilità Massima</strong></p>
            </div>
        </div>
    </div>

</body>
</html>
"""

components.html(html_code, height=820, scrolling=True)
