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