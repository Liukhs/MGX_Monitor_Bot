import os
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QScrollArea, 
                               QWidget, QFrame, QLineEdit, QPushButton, QLabel, 
                               QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
                               QStyledItemDelegate, QStyle, QCheckBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from dotenv import load_dotenv, set_key

class ConfigDialog(QDialog):
    """Finestra Toplevel per la configurazione dei siti"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #ffffff; color: black;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        self.btn_back = QPushButton("⬅ Torna indietro")
        self.btn_back.setStyleSheet("padding: 8px; font-weight: bold;")

        lbl_titolo = QLabel("CONFIGURAZIONE SISTEMA")
        lbl_titolo.setStyleSheet("font-size: 18px; font-weight: bold; color: #333;")

        header_layout.addWidget(self.btn_back)
        header_layout.addStretch()
        header_layout.addWidget(lbl_titolo)
        main_layout.addLayout(header_layout)

        config_options = QHBoxLayout()
        timeout_layout = QVBoxLayout()
        rescan_layout = QVBoxLayout()
        timeout_lbl = QLabel("TimeOut")
        rescan_lbl = QLabel("Temporized Scan")
        self.timeout_entry = QLineEdit()
        timeout_btn = QPushButton("SALVA")
        rescan_entry = QLineEdit()
        rescan_btn = QPushButton("SALVA")
        rescan_toggle = QCheckBox()
        config_options.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.timeout_entry.setFixedWidth(50)
        rescan_entry.setFixedWidth(50)
        timeout_btn.setFixedWidth(80)
        rescan_btn.setFixedWidth(80)
        rescan_entry.setEnabled(False)
        rescan_btn.setEnabled(False)
        self.riempi_da_env(self.timeout_entry)
        timeout_btn.clicked.connect(self.cambia_timeout)
        timeout_layout.addWidget(timeout_lbl)
        timeout_btn_entry = QHBoxLayout()
        timeout_btn_entry.addWidget(self.timeout_entry)
        timeout_btn_entry.addWidget(timeout_btn)
        timeout_layout.addLayout(timeout_btn_entry)
        config_options.addLayout(timeout_layout)
        
        
        rescan_btn_entry = QHBoxLayout()
        rescan_title_check = QHBoxLayout()
        rescan_title_check.addWidget(rescan_lbl)
        rescan_title_check.addWidget(rescan_toggle)
        rescan_layout.addLayout(rescan_title_check)
        rescan_btn_entry.addWidget(rescan_entry)
        rescan_btn_entry.addWidget(rescan_btn)
        rescan_layout.addLayout(rescan_btn_entry)
        rescan_title_check.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
       
        config_options.addLayout(rescan_layout)
        config_options.setAlignment(timeout_layout, Qt.AlignTop)
        config_options.setAlignment(rescan_layout, Qt.AlignTop)
        main_layout.addLayout(config_options)
        timeout_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        rescan_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")
        


        
        # Area lista (Scrollable)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll_content = QWidget()
        self.lista_layout = QVBoxLayout(self.scroll_content)
        self.lista_layout.setAlignment(Qt.AlignTop)
        #self.scroll.setWidget(self.scroll_content)
        #main_layout.addWidget(self.scroll)
        self.tab = QTableWidget()
        self.tab.setColumnCount(3)
        self.tab.setHorizontalHeaderLabels(["CLIENTE", "URL", "KEYWORD"])
        header = self.tab.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tab.verticalHeader().setDefaultSectionSize(40)
        self.tab.setMouseTracking(True)
        
        self.tab.setShowGrid(False)
        self.tab.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab.setItemDelegate(HoverDelegate(self.tab))
        self.tab.setFocusPolicy(Qt.NoFocus)
        main_layout.addWidget(self.tab)
        
        
        
        # Frame Aggiungi
        add_frame = QFrame()
        add_layout = QHBoxLayout(add_frame)
        self.entry_nome = QLineEdit(); self.entry_nome.setPlaceholderText("NOME")
        self.entry_url = QLineEdit(); self.entry_url.setPlaceholderText("URL")
        self.entry_key = QLineEdit(); self.entry_key.setPlaceholderText("KEYWORD")
        btn_salva = QPushButton("SALVA")
        btn_salva.clicked.connect(self.aggiungi_nuovo_sito)
        
        for w in [self.entry_nome, self.entry_url, self.entry_key, btn_salva]:
            add_layout.addWidget(w)
            w.setStyleSheet("background: #ffffff; border: 1px solid #555; padding: 8px;")
        btn_salva.setStyleSheet("background: green; border: 1px solid #555; padding 8px")
            
        main_layout.addWidget(add_frame)
        self.aggiorna_lista_config()

    def aggiorna_lista_config(self):
        load_dotenv(override=True)
        

        self.tab.setRowCount(0)

        row_index = 0
        
        # Pulisce layout
        for i in reversed(range(self.lista_layout.count())): 
            self.lista_layout.itemAt(i).widget().setParent(None)
            
        for chiave, valore in os.environ.items():
            if chiave.endswith("_URL"):
                nome_base = chiave.replace("_URL", "")
                url = valore
                keyword = os.getenv(f"{nome_base}_KEY", "-")

                self.tab.insertRow(row_index)
                
                
                self.tab.setItem(row_index, 0, QTableWidgetItem(nome_base))
                self.tab.setItem(row_index, 1, QTableWidgetItem(url))
                self.tab.setItem(row_index, 2, QTableWidgetItem(keyword))

                row_index += 1
        
        

    def aggiungi_nuovo_sito(self):
        with open(".env", "a") as f:
            nome = self.entry_nome.text().upper()
            url = self.entry_url.text()
            key = self.entry_key.text()
            f.write(f'\n{nome}_URL = "{url}"\n{nome}_KEY = "{key}"')
        self.aggiorna_lista_config()

    def disegna_tabella(self):
        tab_headers = ["NOME", "URL", "KEYWORD"]
        tab = QTableWidget()
        tab.setColumnCount(len(tab_headers))
        tab.setHorizontalHeaderLabels(tab_headers)

        tab.setRowCount(0)
    
    def riempi_da_env(self, timeoutEntry):
        load_dotenv()
        for chiave, valore in os.environ.items():
            if chiave == "TIMEOUT":
                timeoutEntry.setText(valore)
    
    def cambia_timeout(self):
        timeout = self.timeout_entry.text().strip()
        set_key(".env", "TIMEOUT", timeout)
        os.environ["TIMEOUT"] = timeout

                

class HoverDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # Se il mouse è sopra la riga (State_MouseOver)
        if option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, QColor(240, 240, 240)) # Grigio hover
        
        # Se la riga è selezionata
        elif option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor(0, 120, 215)) # Blu selezione
            option.palette.setColor(QPalette.HighlightedText, QColor("white"))
        
        # Rimuove il rettangolo tratteggiato (il "brutto contorno")
        option.state &= ~QStyle.State_HasFocus
        
        # Disegna il testo normale sopra lo sfondo che abbiamo creato
        super().paint(painter, option, index)
