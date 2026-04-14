from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
import src.gui.Circular_progress as RoundBar

class ServerDetails(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Dettagli Server - {data.get('nome', 'Sconosciuto')}")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        round_bar = RoundBar.CircularProgress()

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
                        lay_cerchio.addWidget(round_bar)
                        free = float(server_health.get('disk_free', 0))
                        total = float(server_health.get('disk_total', 1))
                        print(f"{server_health.get('disk_free')} spazio libero in byte")
                        print(f"{server_health.get('disk_total')} spazio totale in byte")
                        percent = int ((free/total) * 100)
                        round_bar.set_value(percent)
                        disk_layout.addWidget(card_cerchio)
                        layout.addLayout(disk_layout)
                        layout.addWidget(QLabel(f"Status: {server_health.get('status')}"))


        else:
            layout.addWidget(QLabel(str(server_health)))

        self.setStyleSheet("background-color: #2b2b2b; color: white;")