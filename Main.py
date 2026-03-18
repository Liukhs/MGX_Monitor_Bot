import Config
import Checker
import time
import Logger
import os
import notifier

cartella = "logs"
if os.path.exists(cartella):
    for f in os.listdir(cartella):
        percorso = os.path.join(cartella, f)
        if os.stat(percorso).st_mtime < time.time() - 7 * 86400:
            os.remove(percorso)
while(True):


    report_attuale = []
    errori_rilevati = []
    print("avvio del bot, procedendo alla scansione...")

    print(f"--- Avvio monitoraggio delle ore {time.ctime()}")

    for nome, dati in Config.clienti.items():
        stato = Checker.controlla_url(nome, dati, Config.TIMEOUT)
        report_attuale.append(stato)
    
        if stato["stato"] != "200":
            errori_rilevati.append(f"{nome}: {stato['stato']}")
        elif isinstance(stato["ssl_days"], int) and stato["ssl_days"] < 10:
            errori_rilevati.append(f"{nome}: SSL in scadenza tra {stato['ssl_days']} giorni!")

    Logger.scrivi_report(report_attuale)

    if errori_rilevati:
        messaggio = "⚠️ *PROBLEMI RILEVATI!*\n\n" + "\n".join(errori_rilevati)
        notifier.invia_messaggio(messaggio)
        print("NOTIFICA INVIATA!")
    else:
        print("Tutto regolare")
    print("Lavoro finito - controllare report_siti.txt")

    print("Sleeping for 2 hours")
    time.sleep(7200)