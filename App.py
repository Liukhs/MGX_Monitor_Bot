import customtkinter as ctk
from CTkToolTip import *
import threading
import time
import Config
import Logger
import notifier
import Checker
import Tips
import Styles

class BotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.report_attuale = []
        self.title("MyxMonitor - v1.0")
        self.geometry("1000x600")
        

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- RIGA 0
        self.header_frame = ctk.CTkFrame(self, **Styles.STYLE_HEADER)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.label_nome = ctk.CTkLabel(self.header_frame, **Styles.STYLE_TITLE, text="MYXMONITOR")
        self.label_nome.grid(row=0, column=0, sticky="w", padx=20, pady=10)
        
        

        self.btn_avvia = ctk.CTkButton(self.header_frame, **Styles.STYLE_BTN_AVVIA, text="Esegui Operazione",  command=self.avvio_sicuro)
        self.btn_avvia.grid(row=0, column=1, sticky="e", padx=20, pady=10)
        tip_btn_avvia = CTkToolTip(self.btn_avvia, "Avvia la scansione dei siti")
        

        # --- RIGA 1
        self.tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tools_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=15)

        self.btn_config = ctk.CTkButton(self.tools_frame, **Styles.STYLE_BTN_CONFIG, text="⚙️ Configurazione", command=self.apri_config)
        self.btn_config.grid(row=1, column=0, padx=(0, 10))
        tip_btn_config = CTkToolTip(self.btn_config, "Accedi alla configurazione dei siti")
        self.btn_export = ctk.CTkButton(self.tools_frame, **Styles.STYLE_BTN_CONFIG, text="📄 Esporta Report TXT", command=self.verify_export)
        self.btn_export.grid(row=1, column=1, padx=(0, 10))
        tip_btn_export = CTkToolTip(self.btn_export, "Stampa i risultati in un file .txt")
        # --- RIGA 2
        self.area_log = ctk.CTkScrollableFrame(self,fg_color="#2b2b2b", border_width=2, corner_radius=0)
        self.area_log.grid(row="2", column="0", sticky="nsew", padx=20, pady=(0, 15))
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate")
        self.progress_bar.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
        self.progress_bar.configure(progress_color=self.progress_bar.cget("fg_color"))

        self.headers = ["SITO", "STATO", "TEMPO", "PESO", "SERVER", "REDIRECT", "SSL", "SECURITY"]

        Config.carica_configurazione()

        self.log("Sistema pronto. Inserisci i dati o avvia la scansione")

    def apri_config(self):
        if hasattr(self, "finestra_config") and self.finestra_config.winfo_exists():
            self.finestra_config.focus()
            return

        self.finestra_config = ctk.CTkToplevel(self)
        self.finestra_config.title("Configurazione siti")
        self.finestra_config.geometry("800x600")
        
        # Forza la finestra sopra le altre
        self.finestra_config.attributes("-topmost", True)
        
        # Configurazione layout della finestra secondaria
        self.finestra_config.grid_columnconfigure(0, weight=1)
        self.finestra_config.grid_rowconfigure(0, weight=1) # Frame lista
        self.finestra_config.grid_rowconfigure(1, weight=0) # Frame inserimento

        # --- FRAME LISTA (Sopra)
        self.frame_lista = ctk.CTkScrollableFrame(self.finestra_config, label_text="Siti nel file .env")
        self.frame_lista.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_lista.grid_columnconfigure((0, 1, 2), weight=1)

        # --- FRAME AGGIUNGI (Sotto)
        self.frame_add = ctk.CTkFrame(self.finestra_config)
        self.frame_add.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.entry_nome = ctk.CTkEntry(self.frame_add, placeholder_text="NOME (es: MYGLADIX)")
        self.entry_nome.grid(row=0, column=0, padx=10, pady=10)
        
        self.entry_url = ctk.CTkEntry(self.frame_add, placeholder_text="URL (https://...)")
        self.entry_url.grid(row=0, column=1, padx=10, pady=10)
        
        self.entry_key = ctk.CTkEntry(self.frame_add, placeholder_text="KEYWORD")
        self.entry_key.grid(row=0, column=2, padx=10, pady=10)

        self.btn_salva = ctk.CTkButton(self.frame_add, text="SALVA NEL .ENV", command=self.aggiungi_nuovo_sito)
        self.btn_salva.grid(row=0, column=3, padx=10, pady=10)

        # Carica i dati dal .env
        self.aggiorna_lista_config()

    def aggiorna_lista_config(self):
        
        import os
        from dotenv import load_dotenv
        # override=True è fondamentale per leggere le modifiche appena fatte
        load_dotenv(override=True)

        # Pulisce i vecchi widget nel frame
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        # Header colonne
        headers = ["CLIENTE", "URL", "KEYWORD"]
        for j, h in enumerate(headers):
            lbl = ctk.CTkLabel(self.frame_lista, text=h, font=("Arial", 12, "bold"), text_color="#555555")
            lbl.grid(row=0, column=j, padx=10, pady=5, sticky="w")

        # Legge l'ambiente e filtra le chiavi
        riga = 1
        # Usiamo os.environ per scansionare tutto il .env caricato
        for chiave, valore in os.environ.items():
            if chiave.endswith("_URL"):
                nome_base = chiave.replace("_URL", "")
                url = valore
                keyword = os.getenv(f"{nome_base}_KEY", "-")

                # Crea le label nella mini-tabella
                ctk.CTkLabel(self.frame_lista, text=nome_base).grid(row=riga, column=0, padx=10, pady=2, sticky="w")
                ctk.CTkLabel(self.frame_lista, text=url, text_color="#1f538d").grid(row=riga, column=1, padx=10, pady=2, sticky="w")
                ctk.CTkLabel(self.frame_lista, text=keyword).grid(row=riga, column=2, padx=10, pady=2, sticky="w")
                riga += 1
    
    def aggiungi_nuovo_sito(self):
        
        with open(".env", "a") as f:
            nome = self.entry_nome.get().upper()
            url = self.entry_url.get()
            key = self.entry_key.get()
            f.write(f'\n{nome}_URL = "{url}"')
            f.write(f'\n{nome}_KEY = "{key}"')
        self.aggiorna_lista_config()
    
    def log(self, messaggio):
        """Funzione per scrivere nell'area di testo dell'app"""
        label = ctk.CTkLabel(self.area_log, text=messaggio, font=("Consolas", 12), anchor="w", text_color="#ffffff")
        label.grid(sticky="ew", padx=10, pady=1)

        self.area_log.update_idletasks()
        self.area_log._parent_canvas.yview_moveto(1.0)

    def avvio_sicuro(self):
        self.btn_avvia.configure(state="disabled")
        thread = threading.Thread(target=self.funzione_bot, daemon=True)
        thread.start()
    
    def funzione_bot(self):
        self.log(f"Inizio lavoro di monitoraggio")
        self.progress_bar.configure(progress_color="#1f538d")

        Config.carica_configurazione()
        self.report_attuale = []
        errori_rilevati = []
        self.log("--- Avvio del bot, procedendo alla scansione...")

        self.log(f"--- Avvio monitoraggio delle ore {time.ctime()}")

        totale_siti = len(Config.clienti)
        if totale_siti == 0:
            self.log("Nessun sito da controllare.")
            self.btn_avvia.configure(state="normal")
            return
        self.progress_bar.set(0)
        counter = 0
        for nome, dati in Config.clienti.items():
            stato = Checker.controlla_url(nome, dati, Config.TIMEOUT)
            self.report_attuale.append(stato)
            counter += 1
            progress_value = counter/totale_siti
            self.progress_bar.set(progress_value)
            self.log(f"Verificando il sito {nome} all'indirizzo: {dati['url']} - {time.ctime()}")
    
            if stato["stato"] != "200":
                errori_rilevati.append(f"{nome}: {stato['stato']}")
            elif isinstance(stato["ssl_days"], int) and stato["ssl_days"] < 10:
                errori_rilevati.append(f"{nome}: SSL in scadenza tra {stato['ssl_days']} giorni!")

        
        try:
            self.renderizza_tabella(self.report_attuale)

        except Exception as e:
            self.log(f"Errore nella scrittura del report: {e}")
        finally:
            # Riabilita il bottone
            self.btn_avvia.configure(state="normal", text="AVVIA SCANSIONE")
        if errori_rilevati:
            messaggio = "⚠️ *PROBLEMI RILEVATI!*\n\n" + "\n".join(errori_rilevati)
            notifier.invia_messaggio(messaggio)
            
        self.log("Scansione terminata")

    def renderizza_tabella(self, risultati):
        # Pulisce tutto quello che c'è nel frame (log vecchi o tabelle vecchie)
        for widget in self.area_log.winfo_children():
            widget.destroy()
        
        self.area_log.grid_columnconfigure(0, weight=1)
        self.area_log.grid_rowconfigure(0, weight=1)

        buffer_tabella = ctk.CTkFrame(self.area_log, fg_color="transparent")
        buffer_tabella.grid(row=0, column=0, sticky="nsew")

        for col in range(len(self.headers)):
            buffer_tabella.grid_columnconfigure(col, weight=1)
        
        # Header (Intestazioni)
        for j, h in enumerate(self.headers):
            header_cell = ctk.CTkLabel(buffer_tabella, text=h, font=("Segoe UI", 12, "bold"), 
                                      fg_color="#1f538d", text_color="white", padx=10, pady=5)
            header_cell.grid(row=0, column=j, sticky="nsew", padx=1, pady=1)
            tip = self.scegli_tip(h)
            tip_header_cell = CTkToolTip(header_cell, f"{tip}")

        # Dati (Righe)
        for i, r in enumerate(risultati, start=1):
            bg_color = "#333333" if i % 2 == 0 else "#2b2b2b"
            
            dati_riga = [
                r.get('nome', '-'), r.get('stato', '-'), r.get('tempo', '-'), 
                r.get('peso', '-'), r.get('server', '-'), r.get('redirect', '-'), 
                r.get('ssl_days', '-'), r.get('security', '-')
            ]

            for j, valore in enumerate(dati_riga):
                testo_colore = "white"
                # Formattazione condizionale: STATO rosso se non è 200
                if j == 1 and str(valore) != "200": 
                    testo_colore = "#ff6666"

                cella = ctk.CTkLabel(buffer_tabella, **Styles.STYLE_BADGE_OK, text=str(valore) )
                cella.grid(row=i, column=j, sticky="nsew", padx=1, pady=1)
        buffer_tabella.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()

    def verify_export(self):
        if not self.report_attuale:
            self.log("Non esistono report da esportare al momento")
            return
        Logger.scrivi_report(self.report_attuale)

    def scegli_tip(self, header):
        for nome, dati in Tips.tips.items():
            if nome == header:
                return dati
            
if __name__ == "__main__":
    app = BotApp()
    app.mainloop()