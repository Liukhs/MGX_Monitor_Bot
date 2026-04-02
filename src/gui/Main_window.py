import datetime
import threading
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QLabel, QFrame, QScrollArea, 
                               QProgressBar, QTableWidget, QTableWidgetItem, QHeaderView, QStackedWidget)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QGuiApplication

# I TUOI MODULI
from src.gui.Styles import MAIN_STYLE
from src.gui.Config_dialog import ConfigDialog
from src.core.Engine import WorkerSignals, funzione_bot # Importiamo i tuoi nomi
import src.core.Config as Config
import src.core.Logger as Logger
import assets_rc
from .Config_dialog import ConfigDialog

class BotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        screen = QGuiApplication.primaryScreen()
        rect = screen.availableGeometry()
        width = rect.width()
        height = rect.height()
        self.report_attuale = []
        self.headers = ["SITO", "STATO", "TEMPO", "PESO", "SERVER", "REDIRECT", "SSL", "SECURITY"]
        self.setWindowTitle("MyxMonitor - v1.0")
        self.resize(1200, 800)

        
        self.signals = WorkerSignals()
        self.signals.log_signal.connect(self.log)
        self.signals.progress_signal.connect(self.progress_bar_update)
        self.signals.status_signal.connect(self.update_status)
        self.signals.finished_signal.connect(self.renderizza_tabella)
        self.signals.segnale_risultato.connect(self.scrivi_log_sito)

        self.setup_ui()
        
        Config.carica_configurazione()
        self.log("Sistema pronto. Inserisci i dati o avvia la scansione")

    def setup_ui(self):
        stacked_widget = QStackedWidget()
        self.setCentralWidget(stacked_widget)
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(24)

        #PAGINE DA AGGIUNGERE
        self.page_config = ConfigDialog()

        # HEADER
        self.header_frame = QFrame()
        self.header_frame.setObjectName("HeaderFrame")
        h_layout = QHBoxLayout(self.header_frame)
        app_icon = QPixmap("assets/icons/app_icon.png")
        
        v_titles = QVBoxLayout()
        h_title = QHBoxLayout()
        self.label_nome = QLabel("MYXMONITOR")
        self.label_icon = QLabel()
        self.label_icon.setPixmap(app_icon)
        self.label_nome.setObjectName("MainTitle")
        self.label_stato = QLabel("Sistema di monitoraggio siti . V1.0")
        self.label_stato.setObjectName("SubTitle")
        self.label_icon.setFixedSize(48, 48)
        self.label_icon.setPixmap(app_icon.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_icon.setScaledContents(True)
        h_title.addWidget(self.label_icon)
        h_title.addWidget(self.label_nome)
        v_titles.addLayout(h_title)
        v_titles.addWidget(self.label_stato)
        self.btn_avvia = QPushButton("AVVIA SCANSIONE")
        self.btn_avvia.setObjectName("StartButton")
        self.btn_avvia.clicked.connect(self.avvio_sicuro)
        self.btn_avvia.setToolTip("Avvia la scansione dei siti")
        h_layout.addLayout(v_titles)
        h_layout.addStretch()
        h_layout.addWidget(self.btn_avvia)
        main_layout.addWidget(self.header_frame)

        # TOOLS
        tools_layout = QHBoxLayout()
        tools_layout.setContentsMargins(20, 0, 20, 0)
        self.btn_config = QPushButton("⚙️ Configurazione")
        self.btn_config.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        self.btn_config.setToolTip("Accedi alla configurazione dei siti")
        self.btn_export = QPushButton("📄 Esporta Report TXT")
        self.btn_export.clicked.connect(self.verify_export)
        self.btn_export.setToolTip("Stampa i risultati in un file .txt")
        tools_layout.addWidget(self.btn_config)
        tools_layout.addWidget(self.btn_export)
        tools_layout.addStretch()
        main_layout.addLayout(tools_layout)
        self.page_config.btn_back.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))

        # LOG CONTAINER
        log_wrapper = QFrame()
        log_wrapper.setContentsMargins(0, 0, 0, 0)
        log_wrapper.setLineWidth(0)
        log_wrapper.setFrameShape(QFrame.NoFrame)
        wrapper_layout = QVBoxLayout(log_wrapper)
        wrapper_layout.setSpacing(0)
        self.log_header = QFrame(); self.log_header.setObjectName("LogHeader")
        self.log_header.setFixedHeight(40)
        lh_layout = QHBoxLayout(self.log_header)
        lbl_log_header = QLabel(">_ Log di sistema - Console di monitoraggio")
        lbl_log_header.setObjectName("LogLabel")
        lh_layout.addWidget(lbl_log_header)
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("LogArea")
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; padding: 0; margin: 0; }")
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("margin: 0; padding: 0;")
        self.console_layout = QVBoxLayout(self.scroll_content)
        self.console_layout.setContentsMargins(0, 0, 0, 0)
        self.console_layout.setSpacing(0)
        self.console_layout.setAlignment(Qt.AlignTop)
        self.console_content_widget = QWidget() # Per piallare il bianco
        self.scroll_area.setWidget(self.scroll_content)
        self.status_footer = QFrame(); self.status_footer.setObjectName("StatusFooter")
        sf_layout = QHBoxLayout(self.status_footer)
        self.lbl_footer_left = QLabel("Pronto")
        self.lbl_footer_right = QLabel("Log totali: 0")
        sf_layout.addWidget(self.lbl_footer_left); sf_layout.addStretch(); sf_layout.addWidget(self.lbl_footer_right)
        wrapper_layout.addWidget(self.log_header)
        wrapper_layout.addWidget(self.scroll_area)
        wrapper_layout.addWidget(self.status_footer)
        main_layout.addWidget(log_wrapper)

        # PROGRESS
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(8)
        self.progress_bar.setTextVisible(False)
        self.lbl_progress_left = QLabel("Avanzamento scansione")
        self.lbl_progress_right = QLabel("0%")
        p_container = QWidget();
        p_layout = QVBoxLayout(p_container)
        ho_layout = QHBoxLayout()
        ho_layout.addWidget(self.lbl_progress_left)
        ho_layout.addStretch()
        ho_layout.addWidget(self.lbl_progress_right)
        p_container.setObjectName("ProgressLayout")
        p_container.setContentsMargins(20, 22, 20, 22)
        p_layout.setContentsMargins(0, 0, 0, 0); 
        p_layout.addLayout(ho_layout)
        p_layout.addWidget(self.progress_bar)
        main_layout.addWidget(p_container)
        stacked_widget.addWidget(central)
        stacked_widget.addWidget(self.page_config)

    def log(self, msg):
        lbl = QLabel(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")
        lbl.setStyleSheet("color: white; font-family: 'Consolas'; background: transparent;")
        self.console_layout.addWidget(lbl)
        QTimer.singleShot(10, lambda: self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum()))

    def update_status(self, txt, col):
        self.label_stato.setText(txt)
        self.label_stato.setStyleSheet(f"color: {col};")

    def progress_bar_update(self, val):
        # 'val' arriva come float (0.0 a 1.0), lo portiamo a 0-100
        target_value = int(val * 100)
    
       # Se l'animazione esiste già, la fermiamo per non accavallare i movimenti
        if hasattr(self, "anim_bar"):
            self.anim_bar.stop()
    
        # Creiamo l'animazione sulla proprietà "value" della progress_bar
        self.anim_bar = QPropertyAnimation(self.progress_bar, b"value")
        self.anim_bar.setDuration(400)  # Millisecondi di durata del movimento
        self.anim_bar.setStartValue(self.progress_bar.value())
        self.anim_bar.setEndValue(target_value)
        self.lbl_progress_right.setText(f"{target_value}%")
    
        # QEasingCurve.OutQuad rende il movimento fluido all'inizio e morbido alla fine
        self.anim_bar.setEasingCurve(QEasingCurve.OutQuad)
    
        self.anim_bar.start()

    def avvio_sicuro(self):
        self.btn_avvia.setEnabled(False)
        for i in reversed(range(self.console_layout.count())): 
            self.console_layout.itemAt(i).widget().setParent(None)
        
        # Lanciamo la funzione_bot che ora sta nell'engine, passandogli i segnali
        threading.Thread(target=funzione_bot, args=(self.signals,), daemon=True).start()
        
        # Riabilita il bottone quando ha finito (collegato al segnale finished)
        self.signals.finished_signal.connect(lambda: self.btn_avvia.setEnabled(True))

    def renderizza_tabella(self, risultati):
        self.report_attuale = risultati
        
        # Pulizia layout
        for i in reversed(range(self.console_layout.count())): 
            widget = self.console_layout.itemAt(i).widget()
            if widget: widget.setParent(None)

        tab = QTableWidget()
        tab.setColumnCount(len(self.headers))
        tab.setRowCount(len(risultati))

        headers_icone = ["🌐 SITO", "✅ STATO", "🕒 TEMPO", "💾 PESO", "🗄 SERVER", "🔗 REDIRECT", "🛡 SSL", "⚠️ SECURITY"]
        tab.setHorizontalHeaderLabels(headers_icone)
        tab.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tab.verticalHeader().setDefaultSectionSize(50) 
        tab.verticalHeader().setVisible(False)
        tab.setShowGrid(False)
        tab.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        tab.viewport().setStyleSheet("background-color: white;")

        for i, r in enumerate(risultati):
            # --- COLONNA 0: NOME (Testo Bold) ---
            nome_item = QTableWidgetItem(str(r.get('nome', '-')))
            
            # Creiamo un oggetto font basato su quello della tabella
            nuovo_font = tab.font() 
            nuovo_font.setBold(True) # Impostiamo il grassetto
            
            nome_item.setFont(nuovo_font) # Ora passiamo il font, non un booleano!
            tab.setItem(i, 0, nome_item)

            # --- COLONNA 1: STATO (Badge Verde/Rosso) ---
            stato_val = str(r.get('stato', '-'))
            if stato_val == "200":
                badge_stato = self.crea_badge("● 200", "#dcfce7", "#166534")
            else:
                badge_stato = self.crea_badge(f"● {stato_val}", "#fee2e2", "#991b1b")
            tab.setCellWidget(i, 1, badge_stato)

            # --- COLONNA 2 & 3: TEMPO e PESO (Testo semplice) ---
            tab.setItem(i, 2, QTableWidgetItem(str(r.get('tempo', '-'))))
            tab.setItem(i, 3, QTableWidgetItem(str(r.get('peso', '-'))))

            # --- COLONNA 4: SERVER (Badge Azzurro) ---
            srv = r.get('server', 'N/D')
            badge_srv = self.crea_badge(srv.upper(), "#dbeafe", "#1e40af")
            tab.setCellWidget(i, 4, badge_srv)

            # --- COLONNA 5: REDIRECT ---
            tab.setItem(i, 5, QTableWidgetItem(str(r.get('redirect', 'NO'))))

            # --- COLONNA 6: SSL (Badge Grigio/Icona) ---
            ssl_val = str(r.get('ssl_days', '-'))
            badge_ssl = self.crea_badge(f"🛡 {ssl_val}", "#f1f5f9", "#475569")
            tab.setCellWidget(i, 6, badge_ssl)

            # --- COLONNA 7: SECURITY (Badge Arancio/Verde) ---
            sec = r.get('security', 'MANCANTE')
            if sec == "SAMEORIGIN":
                badge_sec = self.crea_badge("SAMEORIGIN", "#dcfce7", "#166534")
            else:
                badge_sec = self.crea_badge("MANCANTE", "#ffedd5", "#9a3412")
            tab.setCellWidget(i, 7, badge_sec)

        self.console_layout.addWidget(tab)
        self.lbl_footer_left.setText(f"Siti analizzati: {len(risultati)}")


    def verify_export(self):
        if not self.report_attuale: return
        Logger.scrivi_report(self.report_attuale)

    def crea_badge(self, testo, colore_bg, colore_testo):
        lbl = QLabel(testo)
        lbl.setAlignment(Qt.AlignCenter)
        # Il segreto è il border-radius per fare la pillola
        lbl.setStyleSheet(f"""
            background-color: {colore_bg};
            color: {colore_testo};
            border-radius: 12px;
            font-weight: bold;
            font-size: 11px;
        """)
        # Incapsuliamo in un widget per centrarlo nella cella
        container = QWidget()
        lay = QHBoxLayout(container)
        lay.addWidget(lbl)
        lay.setContentsMargins(0,0,0,0)
        return container
    def scrivi_log_sito(self, dati_risultato):
            C_BIANCO = "#ffffff"
            C_VERDE = "#2ECC71"
            C_GIALLO = "#F1C40F"
            C_ROSSO = "#E74C3C"
            C_GRIGIO = "#7F8C8D"

            head = f"<span style='color:{C_BIANCO};'>[#] Monitoraggio: </span>"\
                    f"<b style='color:{C_VERDE};'>{dati_risultato['nome']}</b>"
            self.aggiungi_riga_console(head)

            colore_stato = C_ROSSO
            if dati_risultato['stato'] == "200":
                colore_stato = C_VERDE
            elif "MISSING" in dati_risultato['stato']:
                colore_stato = C_GIALLO
            
            try:
                giorni = int(dati_risultato['ssl_days'])
                if giorni >= 30 :
                    colore_ssl = C_VERDE
                elif giorni > 10 and giorni < 30:
                    colore_ssl = C_GIALLO
                else:
                    colore_ssl = C_ROSSO
                valore_ssl = f"{giorni}"
            except:
                colore_ssl = C_ROSSO
                valore_ssl = dati_risultato['ssl_days']

            righe = [
                ("Risposta HTTP", dati_risultato['stato'], colore_stato),
                ("Latenza", dati_risultato['tempo'], C_BIANCO),
                ("Peso Pagina", dati_risultato['peso'], C_BIANCO),
                ("Server Info", dati_risultato['server'], C_GRIGIO),
                ("Certificato SSL", valore_ssl, colore_ssl)
            ]

            for etichetta, valore, colore in righe:
                testo = f"<span style='color:{C_BIANCO};'>  ├ {etichetta}: </span>" \
                        f"<b style='color:{colore};'>{valore}</b>"
                self.aggiungi_riga_console(testo)

            self.aggiungi_riga_console("<br>")

    def aggiungi_riga_console(self, messaggio_html):
        label = QLabel(messaggio_html)
        label.setStyleSheet("font-family: 'Consolas', 'Courier New'; font-size: 13px; margin-left: 15px;")
        self.console_layout.insertWidget(self.console_layout.count(), label)
