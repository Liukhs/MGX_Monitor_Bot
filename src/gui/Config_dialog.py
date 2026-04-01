import os
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QScrollArea, 
                               QWidget, QFrame, QLineEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt
from dotenv import load_dotenv

class ConfigDialog(QDialog):
    """Finestra Toplevel per la configurazione dei siti"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurazione siti")
        self.resize(800, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #ffffff; color: black;")
        
        layout = QVBoxLayout(self)
        
        # Area lista (Scrollable)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.lista_layout = QVBoxLayout(self.scroll_content)
        self.lista_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.scroll_content)
        layout.addWidget(self.scroll)
        
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
            w.setStyleSheet("background: #333; border: 1px solid #555; padding: 5px;")
            
        layout.addWidget(add_frame)
        self.aggiorna_lista_config()

    def aggiorna_lista_config(self):
        load_dotenv(override=True)
        # Pulisce layout
        for i in reversed(range(self.lista_layout.count())): 
            self.lista_layout.itemAt(i).widget().setParent(None)
            
        for chiave, valore in os.environ.items():
            if chiave.endswith("_URL"):
                nome_base = chiave.replace("_URL", "")
                url = valore
                keyword = os.getenv(f"{nome_base}_KEY", "-")
                
                item_label = QLabel(f"CLIENTE: {nome_base}  |  URL: {url}  |  KEY: {keyword}")
                item_label.setStyleSheet("border-bottom: 1px solid #333; padding: 5px;")
                self.lista_layout.addWidget(item_label)

    def aggiungi_nuovo_sito(self):
        with open(".env", "a") as f:
            nome = self.entry_nome.text().upper()
            url = self.entry_url.text()
            key = self.entry_key.text()
            f.write(f'\n{nome}_URL = "{url}"\n{nome}_KEY = "{key}"')
        self.aggiorna_lista_config()