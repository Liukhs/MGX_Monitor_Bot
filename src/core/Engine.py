from PySide6.QtCore import QObject, Signal
import src.core.Config as Config
import src.core.Checker as Checker

class WorkerSignals(QObject):
    log_signal = Signal(str)
    progress_signal = Signal(float)
    status_signal = Signal(str, str)
    finished_signal = Signal(list)
    segnale_risultato = Signal(dict)

def funzione_bot(signals):
        signals.log_signal.emit("Inizio lavoro di monitoraggio...")
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
        if errori: notifier.invia_messaggio("⚠️ Errori rilevati!")
        