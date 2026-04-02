<div align="center">
    <h1>🤖 MYXMONITOR</h1>
    <p><b>Advanced Desktop Website Monitoring Tool</b></p>
    <p>Una dashboard professionale in Python per il monitoraggio real-time di performance, sicurezza e integrità dei siti web.</p>

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-yellow.svg)
![UI](https://img.shields.io/badge/UI-PySide6-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
</div>

---

## 🚀 Panoramica
**MyxMonitor** è un'applicazione desktop (GUI) progettata per gestire il monitoraggio di una flotta di siti web da un'unica console centralizzata. Sviluppata in Python con PySide6, l'app fornisce un'analisi tecnica profonda che va oltre il semplice controllo "online/offline".

### ⚡ Funzionalità Chiave
* **Analisi Multi-Sito:** Scansione simultanea di tutti i domini configurati tramite multithreading per non bloccare l'interfaccia.
* **Performance Check:** Monitoraggio di HTTP Status, TTFB (Time To First Byte) e Peso della pagina.
* **Security Suite:** Controllo automatico della scadenza dei certificati **SSL** e verifica degli header di sicurezza (**X-Frame-Options**).
* **Content Verification:** Ricerca di una "Keyword" specifica nella pagina per prevenire falsi positivi (es. pagine bianche con status 200).
* **Console Log Real-time:** Interfaccia animata con log tecnici dettagliati e colorati durante la scansione.
* **Reportistica Automatica:** Esportazione dei risultati e rotazione dei log giornalieri nella cartella `Logs/` (auto-cleaning dopo 7 giorni).

---

## 🛠️ Requisiti Tecnici
L'applicazione richiede **Python 3.10+**. 

### Librerie necessarie:
* `PySide6` (Interfaccia Grafica)
* `requests` (Gestione chiamate HTTP)
* `python-dotenv` (Gestione configurazione .env)
* Moduli standard: `ssl`, `socket`, `threading`, `datetime`, `os`

---

## 📦 Installazione e Setup

### 1. Clonazione della Repository
```bash
git clone [https://github.com/tuo-username/MyxMonitor.git](https://github.com/tuo-username/MyxMonitor.git)
cd MyxMonitor
```

### 2. Installazione Dipendenze
Si consiglia l'uso di un ambiente virtuale:
```bash
python -m venv venv
# Attivazione (Windows)
venv\Scripts\activate
# Installazione
pip install PySide6 requests python-dotenv
```

### 3. Configurazione Dati (.env)
Crea un file `.env` nella cartella principale del progetto:
```env
CLIENTE_A_URL=[https://sito-uno.it](https://sito-uno.it)
CLIENTE_A_KEY=ParolaDaCercareNelCodice

CLIENTE_B_URL=[https://sito-due.com](https://sito-due.com)
CLIENTE_B_KEY=AltraParolaChiave
```
*Nota: La KEY serve a confermare che il sito stia servendo i contenuti corretti e non una pagina di errore generica.*

---

## 🖥️ Funzionamento
Per avviare l'applicazione, eseguire il file principale:

```bash
python Main.py
```

### Workflow di scansione:
1. **Inizializzazione:** All'avvio, l'app carica la configurazione dal file `.env`.
2. **Esecuzione:** Cliccando su "Esegui Operazione", viene lanciato un Thread dedicato che interroga i server senza freezare la GUI.
3. **Feedback UI:** La barra di progresso si aggiorna fluidamente tramite animazioni `QPropertyAnimation`, mentre la console stampa i dettagli tecnici di ogni sito (SSL days, Server type, Redirect).
4. **Finalizzazione:** Al termine, i dati vengono aggregati in una tabella riassuntiva con badge colorati per una lettura immediata delle criticità.

---

## 📂 Struttura del Progetto
| Percorso | Scopo |
| :--- | :--- |
| `Main.py` | Entry point e inizializzazione App |
| `src/core/Engine.py` | Gestione segnali (Signals) e logica thread |
| `src/core/Checker.py` | Analisi tecnica degli URL (SSL, Header, HTTP) |
| `src/gui/Main_window.py` | Gestione layout, console e tabella risultati |
| `src/gui/Styles.py` | Definizione dello stile grafico (QSS) |
| `Logs/` | Output dei report giornalieri in formato TXT |

---

<div align="center">
    <sub>Sviluppato per il monitoraggio professionale di infrastrutture web.</sub>
</div>