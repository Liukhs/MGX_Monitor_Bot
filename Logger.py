import os
from datetime import datetime

def scrivi_report(risultati):
    """
    Riceve una lista di risultati e li riscrive su file .txt
    """
    cartella_logs = "logs"

    if not os.path.exists(cartella_logs):
        os.makedirs(cartella_logs)
    
    data_oggi = datetime.now().strftime("%Y_%m_%d")
    percorso_file = os.path.join(cartella_logs, f"report_{data_oggi}.txt")
    orario = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    with open(percorso_file, "a", encoding="utf-8") as file:
        file.write(f"\n{'='*80}\n")
        file.write(f"REPORT MONITORAGGIO SITI - {orario}")
        file.write(f"\n{'='*80}\n")
        #Intestazione della tabella
        header = f"{'SITO':<20} | {'STATO':<20} | {'TEMPO': <10} | {'PESO':<10} | {'SERVER':<15} | {'REDIRECT':<15} | {'SSL':<10} | {'SECURITY':<10}"
        separatore = "-" * len(header)
        file.write(separatore + "\n")
        file.write(header + "\n")
        file.write(separatore + "\n")

        #Righe della tabella

        for r in risultati:
            riga = f"{r['nome']:<20} | {r['stato']:<20} | {r['tempo']:<10} | {r['peso']: <10} | {r['server']:<15} | {r['redirect']: <15} | {r['ssl_days']: <10} | {r['security']:<10}"
            file.write(riga+ "\n")
        
        file.write(separatore + "\n")

def scrivi_report_app(risultati, app_instance):
    cartella_log = "logs"

    if not os.path.exists(cartella_log):
        os.makedirs(cartella_log)
    
    data_oggi = datetime.now().strftime("%d_%m_%Y")
    percorso_file = os.path.join(cartella_log, f"Report_{data_oggi}.txt")
    orario = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    #app_instance.area_log.delete("1.0", "end")

    doppia_barra = "="*80
    titolo = f"REPORT MONITORAGGIO SITI - {orario}"

    header = f"{'SITO':<20} | {'STATO':<20} | {'TEMPO': <10} | {'PESO':<10} | {'SERVER':<15} | {'REDIRECT':<15} | {'SSL':<10} | {'SECURITY':<10}"
    separatore = "-" * len(header)

    with open(percorso_file, "a", encoding="utf-8") as file:
        def scrivi_doppio(testo):
            file.write(testo + "\n")
            app_instance.log(testo)

        file.write(f"\n{doppia_barra}\n")
        scrivi_doppio(doppia_barra)
        scrivi_doppio(titolo)
        scrivi_doppio(doppia_barra)
        scrivi_doppio(separatore)
        scrivi_doppio(header)
        scrivi_doppio(separatore)

        for r in risultati:
            riga = f"{r['nome']:<20} | {r['stato']:<20} | {r['tempo']:<10} | {r['peso']: <10} | {r['server']:<15} | {r['redirect']: <15} | {r['ssl_days']: <10} | {r['security']:<10}"
            scrivi_doppio(riga)
        
        scrivi_doppio(separatore)

        msg_fine = f"Scansione completata. Report salvato in: {percorso_file}"
        scrivi_doppio(msg_fine)
