<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generatore Formazione - Lega FC</title>
    <style>
        :root {
            --primary-color: #0f172a;
            --accent-color: #10b981;
            --accent-hover: #059669;
            --field-green: #15803d;
            --field-line: rgba(255, 255, 255, 0.4);
            --panel-bg: #1e293b;
            --text-color: #f8fafc;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--primary-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        h1 {
            margin-bottom: 20px;
            font-size: 1.8rem;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--accent-color);
        }

        /* Layout Principale */
        .main-container {
            display: flex;
            gap: 25px;
            max-width: 1200px;
            width: 100%;
            justify-content: center;
            align-items: flex-start;
            flex-wrap: wrap;
        }

        /* Stile Campo da Calcio */
        .football-field {
            width: 450px;
            height: 650px;
            background-color: var(--field-green);
            border: 4px solid #ffffff;
            border-radius: 12px;
            position: relative;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            background-image: 
                linear-gradient(rgba(255,255,255,0.05) 50%, transparent 50%),
                linear-gradient(90deg, rgba(255,255,255,0.05) 50%, transparent 50%);
            background-size: 100% 65px, 45px 100%;
        }

        /* Segninee del campo */
        .field-line-center {
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 2px;
            background-color: var(--field-line);
        }

        .field-circle-center {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90px;
            height: 90px;
            border: 2px solid var(--field-line);
            border-radius: 50%;
        }

        /* Posizioni Giocatori sul Campo */
        .player-node {
            position: absolute;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .player-node:hover {
            transform: translate(-50%, -50%) scale(1.1);
        }

        .player-shirt {
            width: 34px;
            height: 34px;
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            border: 2px solid #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.85rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }

        .player-name-tag {
            background: rgba(0, 0, 0, 0.75);
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-top: 3px;
            white-space: nowrap;
            border: 1px solid rgba(255,255,255,0.2);
        }

        /* Pannello Laterale (Panchina + Pulsante) */
        .sidebar-panel {
            background-color: var(--panel-bg);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            width: 320px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .sidebar-panel h3 {
            margin: 0 0 10px 0;
            font-size: 1.1rem;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 5px;
        }

        /* Panchina a griglia (più colonne per non farla troppo lunga) */
        .bench-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            max-height: 350px;
            overflow-y: auto;
            padding-right: 5px;
        }

        .bench-player {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px;
            border-radius: 6px;
            font-size: 0.85rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .bench-player span.role {
            font-size: 0.7rem;
            color: #94a3b8;
            text-transform: uppercase;
        }

        /* Pulsante Genera Formazione laterale */
        .action-container {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .btn-generate {
            background-color: var(--accent-color);
            color: white;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
        }

        .btn-generate:hover {
            background-color: var(--accent-hover);
        }

        .btn-generate:active {
            transform: scale(0.98);
        }

        .action-hint {
            font-size: 0.75rem;
            color: #94a3b8;
            line-height: 1.3;
        }
    </style>
</head>
<body>

    <h1>Lega FC - Gestione Formazione</h1>

    <div class="main-container">
        <!-- CAMPO DA CALCIO -->
        <div class="football-field">
            <div class="field-line-center"></div>
            <div class="field-circle-center"></div>

            <!-- Esempio Modulo 3-4-3 -->
            <!-- Portiere -->
            <div class="player-node" style="top: 88%; left: 50%;">
                <div class="player-shirt">1</div>
                <div class="player-name-tag">Provedel</div>
            </div>

            <!-- Difensori -->
            <div class="player-node" style="top: 70%; left: 25%;">
                <div class="player-shirt">13</div>
                <div class="player-name-tag">Buongiorno</div>
            </div>
            <div class="player-node" style="top: 70%; left: 50%;">
                <div class="player-shirt">3</div>
                <div class="player-name-tag">Bremer</div>
            </div>
            <div class="player-node" style="top: 70%; left: 75%;">
                <div class="player-shirt">23</div>
                <div class="player-name-tag">Mancini</div>
            </div>

            <!-- Centrocampisti -->
            <div class="player-node" style="top: 45%; left: 20%;">
                <div class="player-shirt">10</div>
                <div class="player-name-tag">Pulisic</div>
            </div>
            <div class="player-node" style="top: 42%; left: 40%;">
                <div class="player-shirt">20</div>
                <div class="player-name-tag">Calhanoglu</div>
            </div>
            <div class="player-node" style="top: 42%; left: 60%;">
                <div class="player-shirt">22</div>
                <div class="player-name-tag">Mkhitaryan</div>
            </div>
            <div class="player-node" style="top: 45%; left: 80%;">
                <div class="player-shirt">7</div>
                <div class="player-name-tag">Koopmeiners</div>
            </div>

            <!-- Attaccanti -->
            <div class="player-node" style="top: 20%; left: 25%;">
                <div class="player-shirt">9</div>
                <div class="player-name-tag">Thuram</div>
            </div>
            <div class="player-node" style="top: 15%; left: 50%;">
                <div class="player-shirt">10</div>
                <div class="player-name-tag">Lautaro</div>
            </div>
            <div class="player-node" style="top: 20%; left: 75%;">
                <div class="player-shirt">70</div>
                <div class="player-name-tag">Lookman</div>
            </div>
        </div>

        <!-- PANCHINA E PULSANTE LATERALE -->
        <div class="sidebar-panel">
            <div>
                <h3>Panchina</h3>
                <div class="bench-grid">
                    <div class="bench-player">
                        <span class="role">POR</span>
                        <strong>Sommer</strong>
                    </div>
                    <div class="bench-player">
                        <span class="role">DIF</span>
                        <strong>Bastoni</strong>
                    </div>
                    <div class="bench-player">
                        <span class="role">DIF</span>
                        <strong>Dimarco</strong>
                    </div>
                    <div class="bench-player">
                        <span class="role">CEN</span>
                        <strong>Barella</strong>
                    </div>
                    <div class="bench-player">
                        <span class="role">CEN</span>
                        <strong>Rabiot</strong>
                    </div>
                    <div class="bench-player">
                        <span class="role">ATT</span>
                        <strong>Zirkzee</strong>
                    </div>
                    <div class="bench-player">
                        <span class="role">ATT</span>
                        <strong>Gudmundsson</strong>
                    </div>
                </div>
            </div>

            <div class="action-container">
                <button class="btn-generate" onclick="generaFormazione()">Genera Formazione</button>
                <div class="action-hint">
                    Clicca per confermare la rosa e inviare i dati ufficiali della giornata di campionato.
                </div>
            </div>
        </div>
    </div>

    <script>
        function generaFormazione() {
            alert("Formazione generata e salvata con successo per la Lega FC!");
        }
    </script>

</body>
</html>
