import requests
import ssl
import socket
from datetime import datetime

def controlla_scadenza_ssl(hostname):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                #Estrazione data di scadenza
                scadenza_str = cert['notAfter']
                scadenza_date = datetime.strptime(scadenza_str, '%b %d %H:%M:%S %Y %Z')
                giorni_rimanenti = (scadenza_date - datetime.now()).days
                return giorni_rimanenti
    except:
        return "N/D"

def controlla_url(nome, dati, timeout):
    url = dati["url"]
    keyword = dati["keyword"]
    print(f"DEBUG: sto controllando sito {nome} con url :{url}")
    hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
    try:
        r = requests.get(url, timeout=timeout)
        ms = r.elapsed.total_seconds() * 1000

        redirect = "SI" if r.history else "NO"
        security_header = r.headers.get('X-Frame-Options', 'MANCANTE')
        giorni_ssl = controlla_scadenza_ssl(hostname)
        peso_kb = len(r.content)/1024
        server = r.headers.get('Server', 'Sconosciuto')

        if r.status_code == 200:
            if keyword.lower() in r.text.lower():
                stato_finale = "200"
            else:
                stato_finale = "MISSING KEYWORD"
        else:
            stato_finale = f"HTTP {r.status_code}"
        return {
            "nome" : nome,
            "stato" : stato_finale,
            "tempo" : f"{ms:.0f}ms",
            "peso"  : f"{peso_kb:.1f} KB",
            "server" : server[:15],
            "redirect" : redirect,
            "ssl_days" : giorni_ssl,
            "security" : security_header
        }
    except requests.exceptions.Timeout:
        return{
            "nome" : nome,
            "stato" : "TIMEOUT",
            "tempo" : "N/A",
            "peso"  : "N/A",
            "server" : "N/A",
            "redirect" : "N/A",
            "ssl_days" : "N/A",
            "security" : "N/A"
        }
    except requests.exceptions.ConnectionError:
        return{
            "nome" : nome,
            "stato" : "CONN_ERROR (DNS/OFF)",
            "tempo" : "N/A",
            "peso"  : "N/A",
            "server" : "N/A",
            "redirect" : "N/A",
            "ssl_days" : "N/A",
            "security" : "N/A"
        }

    except Exception as e:
        return{
            "nome" : nome,
            "stato" : f"ERR: {type(e).__name__}",
            "tempo" : "N/A",
            "peso"  : "N/A",
            "server" : "N/A",
            "redirect" : "N/A",
            "ssl_days" : "N/A",
            "security" : "N/A"
        }
    