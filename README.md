<div align="center">
    <h1>🤖 Site Monitoring Bot</h1>
    <p>Un bot python leggero e sicuro per monitorare i siti web dei clienti e ricevere notifiche istantanee su Telegram.</p>

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Build](https://img.shields.io/badge/status-active-success.svg)
</div>

---

## 🛠️ Requisiti Professionali
* **Python 3.8+**
* **Librerie:** `python-dotenv`, `requests`, `os`, `ssl`, `socket`, `datetime`
* **Telegram:** Un bot creato tramite [@BotFather](https://t.me/botfather)

---

## 🚀 Configurazione Rapida

### 1. Preparazione dell'ambiente
Clona il progetto ed installa le dipendenze:

```bash
git clone [https://github.com/tuo-username/nome-repo.git](https://github.com/tuo-username/nome-repo.git)
cd nome-repo
pip install -r requirements.txt
```
### 2. Architettura di Configurazione
Il progetto è strutturato per garantire la massima sicurezza, separando il codice dai dati sensibili dei clienti e delle chiavi API.

#### 1. Il file .env
Il Bot si basa sull'utilizzo di un file .env per contenere i suoi dati "segreti". Ovviamente **non caricato su GitHub**. Il file deve essere caricato nella cartella principale del progetto con questo formato:
```env
TELEGRAM_TOKEN=123456789:ABCDEF...
CHAT_ID=987654321
CLIENTE_A_URL=[https://sito-cliente-a.it](https://sito-cliente-a.it)
CLIENTE_B_URL=[https://sito-cliente-b.com](https://sito-cliente-b.com)
CLIENTE_A_KEY=CLIENTE_A
CLIENTE_B_KEY=CLIENTE_B
```
#### 2. Il file Config.py
Questo file viene utilizzato per leggere i dati dei clienti dal file .env sopraccitato e a renderli disponibili al bot in modo organizzato
```python
import os
from dotenv import load_dotenv
load_dotenv()
clienti = {
    "clienteA" : {"url": os.getenv("CLIENTE_A_URL"), "keyword": os.getenv("CLIENTE_A_KEY")},
    "clienteB" : {"url": os.getenv("CLIENTE_B_URL"), "keyword": os.getenv("CLIENTE_B_KEY")}
}
```
#### 3. Il file notifier.py
Questo file viene utilizzato per la configurazione e l'invio dei messaggi tramite il bot di telegram precedentemente creato
```python
import requests
import os
from dotenv import load_dotenv 

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
```

---
### 3. File da creare
#### .env
Come spiegato nella sezione precedente il file di configurazione e il file environment vanno creati per ogni nuovo bot.
```env
TELEGRAM_API = telegramAPI
CHAT_ID = chatid

CLIENTE_URL = urldelsitodelcliente
CLIENTE_KEY = chiavecliente
```
Il parametro CLIENTE_KEY deve essere una parola da cercare all'interno della prima pagina che si apre del sito, viene utilizzato nel caso in cui alla richiesta HTTP la risposta sia 200 ma la pagina, per qualche problema, sia bianca
#### Config.py
Come spiegato in precedenza il file config dovrà contenere tutti gli url delle pagine da visitare assieme alla parola chiave da cercare nella pagina cercata
```python
import os
from dotenv import load_dotenv
load_dotenv()
clienti = {
    "cliente" : {"url": os.getenv("CLIENTE_URL"), "keyword": os.getenv("CLIENTE_KEY")}
}
```
---
### 4. Funzionamento
Il bot può essere lasciato in perenne esecuzione, lui è configurato per eseguire una scansione ogni due ore, con possibilità di aumentare, diminuire o togliere direttamente l'esecuzione automatica.
All'interno del progetto è presente la cartella Logs, cartella che conterrà i report completi scritti dal bot dopo ogni esecuzione.
I file dei report vengono divisi in base al giorno(uno al giorno) e quelli più vecchi di 7 giorni vengono cancellati automaticamente.
Il bot verifica il funzionamento del sito, il ttfb(Time To First Bite), il peso della pagina, la tipologia di server, se sono presenti redirect, quanti giorni prima della scadenza del certificato SSL e l'header security.
La notifica su telegram viene inviata solo se un sito non è più online o se al certificato SSL mancano <10 giorni alla scadenza. 

---
### 5. Struttura File
| File | Scopo | Visibilità |
| :---: | :---: | :---: |
| Main.py | Logica principale e ciclo di controllo | ✅ Pubblico |
| Config.py | Gestione e mappatura dei clienti | ✅ Pubblico |
| Notifier.py | Modulo invio notifiche telegram | ✅ Pubblico |
| Logger.py | Scrittura dei report del bot | ✅ Pubblico |
| .env | Token e URL privati | ❌ PRIVATO |
| Checker.py | Effettivo controllo delle pagine | ✅ Pubblico |