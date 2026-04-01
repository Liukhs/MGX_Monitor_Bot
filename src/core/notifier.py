import requests
import os
from dotenv import load_dotenv 

#caricamento delle variabili dal file
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def invia_messaggio(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id" : CHAT_ID, "text" : testo}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Errore invio Telegram: {e}")