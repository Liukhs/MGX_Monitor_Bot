from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QFrame
from PySide6.QtCore import Qt

class ServerDetails(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Dettagli Server - {data.get('nome', 'Sconosciuto')}")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Dettagli Server Health:"))

        server_health = data.get('server_health', {})
        if isinstance(server_health, dict):
            if 'Error' in server_health:
                layout.addWidget(QLabel(f"Errore health: {server_health['Error']}"))
            else:
                for key, value in server_health.items():
                    if key == 'db_status':
                        layout.addWidget(QLabel(f"DB Status: {value}"))
                    elif key == 'php_version':
                        layout.addWidget(QLabel(f"PHP Version: {value}"))
                    elif key == 'disk_total':
                        GB = 1024 ** 3
                        self.bar = QProgressBar()
                        disk_layout = QHBoxLayout()
                        card_libero = QFrame()
                        card_libero.setFixedSize(160, 160)
                        card_libero.setStyleSheet("background-color: #333; border-radius: 15px;")
                        lay_libero = QVBoxLayout(card_libero)
                        lay_libero.setAlignment(Qt.AlignCenter)
                        lbl_titolo = QLabel("LIBERO")
                        lbl_titolo.setStyleSheet("color: #94a3b8; font-size: 10px; font-weight: bold;")
                        lbl_valore = QLabel(f"{round(server_health.get('disk_free')/GB)}GB")
                        lbl_valore.setAlignment(Qt.AlignCenter)
                        lbl_valore.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
                        lay_libero.addWidget(lbl_titolo)
                        lay_libero.addWidget(lbl_valore)
                        disk_layout.addWidget(card_libero)
                        card_cerchio = QFrame()
                        card_cerchio.setFixedSize(160, 160)
                        card_cerchio.setStyleSheet("background-color: #333; border-radius: 15px;")
                        lay_cerchio = QVBoxLayout(card_cerchio)
                        lay_cerchio.setAlignment(Qt.AlignCenter)
                        disk_layout.addWidget(card_cerchio)
                        layout.addLayout(disk_layout)
                        percent = int (server_health.get('disk_free') / server_health.get('disk_total') * 100)
                        if percent > 50 :
                            self.bar.setStyleSheet(f"""
                            QProgressBar {{
                                border: 2px solid #444;       /* Bordo esterno */
                                border-radius: 8px;           /* Arrotondamento contenitore */
                                background-color: #1e1e1e;    /* Colore dello SFONDO della barra */
                                text-align: center;           /* Posizione del testo % */
                                color: white;                 /* Colore del testo % */
                                font-weight: bold;
                                height: 20px;
                            }}

                            QProgressBar::chunk {{  
                                background-color: #22c55e; /* Colore della BARRA effettiva */
                                border-radius: 6px;              /* Arrotondamento barra interna */
                                margin: 2px;                     /* Piccolo stacco dai bordi */
                            }}
                        """)
                        elif percent > 20:
                            self.bar.setStyleSheet(f"""
                            QProgressBar {{
                                border: 2px solid #444;       /* Bordo esterno */
                                border-radius: 8px;           /* Arrotondamento contenitore */
                                background-color: #1e1e1e;    /* Colore dello SFONDO della barra */
                                text-align: center;           /* Posizione del testo % */
                                color: white;                 /* Colore del testo % */
                                font-weight: bold;
                                height: 20px;
                            }}

                            QProgressBar::chunk {{  
                                background-color: #eab308; /* Colore della BARRA effettiva */
                                border-radius: 6px;              /* Arrotondamento barra interna */
                                margin: 2px;                     /* Piccolo stacco dai bordi */
                            }}
                        """)
                        else:
                            self.bar.setStyleSheet(f"""
                            QProgressBar {{
                                border: 2px solid #444;       /* Bordo esterno */
                                border-radius: 8px;           /* Arrotondamento contenitore */
                                background-color: #1e1e1e;    /* Colore dello SFONDO della barra */
                                text-align: center;           /* Posizione del testo % */
                                color: white;                 /* Colore del testo % */
                                font-weight: bold;
                                height: 20px;
                            }}

                            QProgressBar::chunk {{  
                                background-color: #ef4444; /* Colore della BARRA effettiva */
                                border-radius: 6px;              /* Arrotondamento barra interna */
                                margin: 2px;                     /* Piccolo stacco dai bordi */
                            }}
                        """)
                        
                        
                        
                        self.bar.setValue(percent)
                        layout.addWidget(QLabel(f"Spazio libero: {round(server_health.get('disk_free')/GB)}GB"))
                        layout.addWidget(self.bar)
                        layout.addWidget(QLabel(f"Spazio totale: {round(server_health.get('disk_total')/GB)}GB"))
                        layout.addWidget(QLabel(f"Status: {server_health.get('status')}"))


        else:
            layout.addWidget(QLabel(str(server_health)))

        self.setStyleSheet("background-color: #2b2b2b; color: white;")