<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Lega FC - Gestione Multi-Squadra & Algoritmo</title>
    <style>
        body { background-color: #0f172a; color: #f8fafc; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; }
        .header { display: flex; justify-content: space-between; align-items: center; background: #1e293b; padding: 15px 25px; border-radius: 12px; margin-bottom: 20px; }
        .team-selector select { background: #0f172a; color: #38bdf8; border: 1px solid #334155; padding: 8px 12px; border-radius: 6px; font-weight: bold; cursor: pointer; }
        .container { display: flex; gap: 20px; }
        .field-container { flex: 2; background: #1e293b; padding: 20px; border-radius: 12px; text-align: center; }
        
        /* Campo da calcio realistico */
        .football-field {
            position: relative;
            width: 100%;
            height: 580px;
            background: linear-gradient(to bottom, #2e7d32, #1b5e20);
            border: 3px solid #ffffff;
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: center;
            padding: 15px 0;
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

        .row-players { display: flex; justify-content: center; gap: 12px; width: 100%; z-index: 2; }
        .player-card { background: rgba(15, 23, 42, 0.9); border: 1px solid #334155; padding: 6px 8px; border-radius: 6px; font-size: 11px; width: 95px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .player-card .p-name { display: block; font-weight: bold; color: #38bdf8; font-size: 12px; margin-bottom: 2px; }
        .stats-tag { font-size: 9px; color: #cbd5e1; display: block; }
        .bonus-malus { font-size: 9px; margin-top: 3px; border-top: 1px solid #334155; padding-top: 2px; }
        .bonus { color: #4ade80; }
        .malus { color: #f87171; }

        .sidebar { flex: 1; display: flex; flex-direction: column; gap: 20px; }
        .card-box { background: #1e293b; padding: 15px; border-radius: 12px; }
        .bench-list { display: flex; flex-direction: column; gap: 8px; }
        .bench-item { background: #334155; padding: 8px 12px; border-radius: 6px; font-size: 12px; display: flex; justify-content: space-between; align-items: center; }
        .bench-info { display: flex; flex-direction: column; }
        .bench-stats { font-size: 10px; color: #94a3b8; }
    </style>
</head>
<body>

    <div class="header">
        <h1>Lega FC - Dashboard Algoritmo</h1>
        <div class="team-selector">
            <label for="teamSelect">Squadra: </label>
            <select id="teamSelect">
                <option value="1">FC Dinamo (La tua Rosa)</option>
                <option value="2">Real Maraviglia (Rosa 2)</option>
                <option value="3">Atletico Borgo (Rosa 3)</option>
            </select>
        </div>
    </div>

    <div class="container">
        <!-- CAMPO TITOLARI (STADIO) -->
        <div class="field-container">
            <h3>Formazione Consigliata (Titolari)</h3>
            <div class="football-field">
                <!-- Portiere -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">Maignan</span>
                        <span class="stats-tag">Tit: 99%</span>
                        <div class="bonus-malus"><span class="bonus">B: 5%</span> | <span class="malus">M: 10%</span></div>
                    </div>
                </div>
                <!-- Difensori (3) -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">Bastoni</span>
                        <span class="stats-tag">Tit: 95%</span>
                        <div class="bonus-malus"><span class="bonus">B: 12%</span> | <span class="malus">M: 20%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Bremer</span>
                        <span class="stats-tag">Tit: 90%</span>
                        <div class="bonus-malus"><span class="bonus">B: 10%</span> | <span class="malus">M: 25%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Dimarco</span>
                        <span class="stats-tag">Tit: 98%</span>
                        <div class="bonus-malus"><span class="bonus">B: 30%</span> | <span class="malus">M: 15%</span></div>
                    </div>
                </div>
                <!-- Centrocampisti (4) -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">Barella</span>
                        <span class="stats-tag">Tit: 92%</span>
                        <div class="bonus-malus"><span class="bonus">B: 22%</span> | <span class="malus">M: 25%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Pulisic</span>
                        <span class="stats-tag">Tit: 96%</span>
                        <div class="bonus-malus"><span class="bonus">B: 42%</span> | <span class="malus">M: 10%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Koopmeiners</span>
                        <span class="stats-tag">Tit: 88%</span>
                        <div class="bonus-malus"><span class="bonus">B: 35%</span> | <span class="malus">M: 18%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Zaccagni</span>
                        <span class="stats-tag">Tit: 85%</span>
                        <div class="bonus-malus"><span class="bonus">B: 28%</span> | <span class="malus">M: 22%</span></div>
                    </div>
                </div>
                <!-- Attaccanti (3) -->
                <div class="row-players">
                    <div class="player-card">
                        <span class="p-name">Lautaro</span>
                        <span class="stats-tag">Tit: 100%</span>
                        <div class="bonus-malus"><span class="bonus">B: 65%</span> | <span class="malus">M: 15%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Thuram</span>
                        <span class="stats-tag">Tit: 95%</span>
                        <div class="bonus-malus"><span class="bonus">B: 55%</span> | <span class="malus">M: 12%</span></div>
                    </div>
                    <div class="player-card">
                        <span class="p-name">Retegui</span>
                        <span class="stats-tag">Tit: 90%</span>
                        <div class="bonus-malus"><span class="bonus">B: 50%</span> | <span class="malus">M: 10%</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- PANCHINA E RISERVE (SEDIA) -->
        <div class="sidebar">
            <div class="card-box">
                <h3>Panchina (Riserve 🪑)</h3>
                <div class="bench-list">
                    <div class="bench-item">
                        <div class="bench-info">
                            <strong>Svilar (POR)</strong>
                            <span class="bench-stats">Tit: 98% | <span class="bonus">B: 4%</span></span>
                        </div>
                        <span style="color: #38bdf8; font-size: 11px;">Alg: 92%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info">
                            <strong>Buongiorno (DIF)</strong>
                            <span class="bench-stats">Tit: 90% | <span class="bonus">B: 8%</span></span>
                        </div>
                        <span style="color: #38bdf8; font-size: 11px;">Alg: 88%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info">
                            <strong>Calhanoglu (CEN)</strong>
                            <span class="bench-stats">Tit: 95% | <span class="bonus">B: 48%</span></span>
                        </div>
                        <span style="color: #38bdf8; font-size: 11px;">Alg: 95%</span>
                    </div>
                    <div class="bench-item">
                        <div class="bench-info">
                            <strong>Lookman (ATT)</strong>
                            <span class="bench-stats">Tit: 85% | <span class="bonus">B: 58%</span></span>
                        </div>
                        <span style="color: #38bdf8; font-size: 11px;">Alg: 90%</span>
                    </div>
                </div>
            </div>

            <div class="card-box">
                <h3>Indice Rosa & Algoritmo</h3>
                <p style="font-size: 12px; color: #94a3b8; margin-bottom: 8px;">Totale Indice Rosa: <strong>86.4 / 100</strong></p>
                <p style="font-size: 12px; color: #94a3b8; margin: 0;">Incrocio dati probabili formazioni (Sky, Gazzetta, Corsport, Fantacalcio): <strong>Affidabilità Massima</strong></p>
            </div>
        </div>
    </div>

</body>
</html>
