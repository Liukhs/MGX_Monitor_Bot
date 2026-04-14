from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QFrame, QWidget
from PySide6.QtCore import Qt
import src.gui.Circular_progress as RoundBar

class ServerDetails(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Dettagli Server - {data.get('nome', 'Sconosciuto')}")
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)

        round_bar = RoundBar.CircularProgress()
        tech_frame = QFrame()
        tech_frame.setStyleSheet("""
            QFrame {
                background-color: #333; 
                border-radius: 10px; 
                padding: 10px;
            }
            QLabel { 
                background: transparent; 
                font-family: 'Segoe UI';
            }
        """)
        tech_layout = QVBoxLayout(tech_frame)
        layout.addWidget(QLabel("Dettagli Server Health:"))

        server_health = data.get('server_health', {})
        if isinstance(server_health, dict):
            if 'Error' in server_health:
                layout.addWidget(QLabel(f"Errore health: {server_health['Error']}"))
            else:
                for key, value in server_health.items():
                    if key == 'db_status':
                        db_row = QWidget()
                        row_lay = QHBoxLayout(db_row)
                        row_lay.setContentsMargins(10, 5, 10, 5)
                        db_row.setStyleSheet("border-radius: 10px;")
                        db_val = server_health.get('db_status', 'not checked')#Il DB ancora non viene interrogato per questo sarà sempre not checked
                        db_color = "#22c55e" if "OK" in db_val else "#eab308"
                        db_lbl = QLabel("DATABASE:")
                        lbl_value = QLabel(f"{db_val}")
                        db_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 5px; padding: 5px 2px 5px 2px;")
                        lbl_value.setStyleSheet(f"color: {db_color}; font-size: 12px; margin-top: 5px; padding: 5px 2px 5px 2px;")
                        row_lay.addWidget(db_lbl)
                        row_lay.addStretch()
                        row_lay.addWidget(lbl_value)
                        tech_layout.addWidget(db_row)
                    elif key == 'php_version':
                        php_row = QWidget()
                        row_layout = QHBoxLayout(php_row)
                        row_layout.setContentsMargins(10,5,10,5)
                        php_row.setStyleSheet("border-radius: 10px;")

                        php_val = server_health.get('php_version', 'N/D')
                        php_lbl = QLabel("PHP VERSION:")
                        lbl_version = QLabel(f"{php_val}")
                        php_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 5px; padding: 5px 2px 5px 2px;")
                        lbl_version.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 5px; padding: 5px 2px 5px 2px;")
                        row_layout.addWidget(php_lbl)
                        row_layout.addStretch()
                        row_layout.addWidget(lbl_version)
                        tech_layout.addWidget(php_row)
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
                        status_row = QWidget()
                        status_layout = QHBoxLayout(status_row)
                        status_layout.setContentsMargins(10,5,10,5)
                        status_row.setStyleSheet("border-radius: 10px;")
                        
                        status_val = server_health.get('status')
                        status_lbl = QLabel("STATUS:")
                        lbl_val = QLabel(f"{status_val}")
                        status_color =  "#22c55e" if "OK" in status_val else "#eab308"
                        status_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 5px; padding: 5px 2px 5px 2px;")
                        lbl_val.setStyleSheet(f"color: {status_color}; font-size: 12px; margin-top: 5px; padding: 5px 2px 5px 2px;")
                        status_layout.addWidget(status_lbl)
                        status_layout.addStretch()
                        status_layout.addWidget(lbl_val)
                        tech_layout.addWidget(status_row)


        else:
            layout.addWidget(QLabel(str(server_health)))
        layout.addWidget(tech_frame)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")