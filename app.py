<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>Gestione Formazione Fanta</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #ffffff;
            margin: 0;
            padding: 20px;
            display: flex;
            height: 100vh;
            box-sizing: border-box;
        }
        /* Pannello di sinistra */
        .sidebar {
            width: 300px;
            background: #1e1e1e;
            padding: 20px;
            border-radius: 8px;
            margin-right: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        }
        .sidebar h2 {
            font-size: 1.2rem;
            margin-top: 0;
            color: #00ffcc;
        }
        .sidebar input[type="file"] {
            background: #2c2c2c;
            padding: 10px;
            border: 1px dashed #00ffcc;
            border-radius: 4px;
            color: #fff;
            cursor: pointer;
        }
        /* Campo da calcio stile FantaLab / Leghe FC */
        .field-container {
            flex-grow: 1;
            background: linear-gradient(135deg, #1b4d3e 0%, #0d281e 100%);
            border: 3px solid #ffffff;
            border-radius: 12px;
            position: relative;
            display: flex;
            flex-direction: column;
            justify-content: space-around;
            align-items: center;
            padding: 20px;
            box-shadow: inset 0 0 50px rgba(0,0,0,0.6);
            overflow: hidden;
        }
        /* Linee del campo da calcio */
        .field-container::before {
            content: "";
            position: absolute;
            top: 50%;
            left: 0;
            width: 100%;
            height: 2px;
            background: rgba(255, 255, 255, 0.3);
        }
        .field-row {
            display: flex;
            justify-content: center;
            gap: 30px;
            width: 100%;
            z-index: 2;
        }
        /* Card del Giocatore */
        .player-card {
            background: rgba(0, 0, 0, 0.75);
            border: 1px solid #00ffcc;
            border-radius: 6px;
            padding: 8px 12px;
            text-align: center;
            width: 110px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
            position: relative;
        }
        .player-name {
            font-weight: bold;
            font-size: 0.85rem;
            margin-bottom: 3px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .player-stats {
            font-size: 0.7rem;
            color: #ffcc00;
            margin-bottom: 5px;
        }
        /* Barra di titolarità */
        .titularity-container {
            width: 100%;
            background: #444;
            border-radius: 3px;
            height: 6px;
            overflow: hidden;
            margin-top: 4px;
        }
        .titularity-bar {
            height: 100%;
            border-radius: 3px;
        }
        .bar-green { background-color: #2ecc71; }
        .bar-orange { background-color: #e67e22; }
        
        .titularity-text {
            font-size: 0.65rem;
            margin-top: 2px;
            color: #ddd;
        }
    </style>
</head>
<body>

    <!-- Pannello di Sinistra -->
    <div class="sidebar">
        <h2>Importazione Formazione</h2>
        <label for="file-upload">Carica file formazione:</label>
        <input type="file" id="file-upload" accept=".txt, .csv, .json" onchange="handleFileImport(event)">
        <p style="font-size: 0.8rem; color: #aaa;">Carica il file esportato per popolare automaticamente il campo.</p>
    </div>

    <!-- Campo da Calcio Grafico -->
    <div class="field-container">
        <!-- Portiere -->
        <div class="field-row">
            <div class="player-card">
                <div class="player-name">Provedel</div>
                <div class="player-stats">⚽ 0 🎯 +1</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                <div class="titularity-text">95% (Titolare)</div>
            </div>
        </div>
        <!-- Difensori -->
        <div class="field-row">
            <div class="player-card">
                <div class="player-name">Dimarco</div>
                <div class="player-stats">⚽ +2 🎯 +3</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 90%;"></div></div>
                <div class="titularity-text">90%</div>
            </div>
            <div class="player-card">
                <div class="player-name">Bremer</div>
                <div class="player-stats">⚽ 0 🟨 -0.5</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 98%;"></div></div>
                <div class="titularity-text">98%</div>
            </div>
            <div class="player-card">
                <div class="player-name">Bastoni</div>
                <div class="player-stats">⚽ +1 🎯 +1</div>
                <div class="titularity-container"><div class="titularity-bar bar-orange" style="width: 65%;"></div></div>
                <div class="titularity-text">65% (In dubbio)</div>
            </div>
        </div>
        <!-- Centrocampisti -->
        <div class="field-row">
            <div class="player-card">
                <div class="player-name">Pulisic</div>
                <div class="player-stats">⚽ +4 🎯 +3</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 92%;"></div></div>
                <div class="titularity-text">92%</div>
            </div>
            <div class="player-card">
                <div class="player-name">Koopmeiners</div>
                <div class="player-stats">⚽ +3 🎯 +2</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                <div class="titularity-text">95%</div>
            </div>
            <div class="player-card">
                <div class="player-name">Çalhanoğlu</div>
                <div class="player-stats">⚽ +5 🎯 +4</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 99%;"></div></div>
                <div class="titularity-text">99%</div>
            </div>
        </div>
        <!-- Attaccanti -->
        <div class="field-row">
            <div class="player-card">
                <div class="player-name">Lautaro</div>
                <div class="player-stats">⚽ +8 🎯 +2</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 100%;"></div></div>
                <div class="titularity-text">100%</div>
            </div>
            <div class="player-card">
                <div class="player-name">Thuram</div>
                <div class="player-stats">⚽ +6 🎯 +5</div>
                <div class="titularity-container"><div class="titularity-bar bar-green" style="width: 95%;"></div></div>
                <div class="titularity-text">95%</div>
            </div>
        </div>
    </div>

    <script>
        function handleFileImport(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                const content = e.target.result;
                console.log("File caricato con successo:", file.name);
                alert("File '" + file.name + "' caricato correttamente! (Qui puoi implementare il parsing dei dati per popolare il campo).");
                // Logica di parsing personalizzata per leggere i giocatori dal file...
            };
            reader.readAsText(file);
        }
    </script>
</body>
</html>
