import sys
from PySide6.QtWidgets import QApplication
from src.gui.Main_window import BotApp
from src.gui.Styles import MAIN_STYLE

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(MAIN_STYLE)
    win = BotApp()
    win.show()
    sys.exit(app.exec())