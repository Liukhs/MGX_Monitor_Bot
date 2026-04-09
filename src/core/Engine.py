from PySide6.QtCore import QObject, Signal, QTime
import src.core.Config as Config
import src.core.Checker as Checker
import time

class WorkerSignals(QObject):
    log_signal = Signal(str)
    progress_signal = Signal(float)
    status_signal = Signal(str, str)
    finished_signal = Signal(list)
    segnale_risultato = Signal(dict)

def funzione_bot(signals):
        while(True):
            signals.log_signal.emit("Inizio lavoro di monitoraggio...")
            print("[DEBUG] - inizio scansione")
            
            Config.carica_configurazione()
            report_attuale = []
            errori = []
            totale = len(Config.clienti)
            
            if totale == 0:
                signals.log_signal.emit("Nessun sito da controllare.")
                
                return

            for i, (nome, dati) in enumerate(Config.clienti.items(), 1):
                stato = Checker.controlla_url(nome, dati, Config.TIMEOUT)
                report_attuale.append(stato)
                signals.segnale_risultato.emit(stato)
                signals.log_signal.emit(f"Sto controllando {nome} all'indirizzo {dati['url']}")
                
                signals.progress_signal.emit(i / totale)
                if stato["stato"] != "200": errori.append(f"{nome}: {stato['stato']}")
            
            signals.finished_signal.emit(report_attuale)
            signals.status_signal.emit("● SCANSIONE COMPLETATA", "#2ecc71")
            if errori: print("Errori rilevati")
            if not Config.is_temporized:
                break
            time.sleep(int(Config.timer_intervallo) * 60)
        

def temporized_scan(self, secondi):
    self.timer_intervallo = secondi
    self.isTemporized = True

        