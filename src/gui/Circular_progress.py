from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QFont
from PySide6.QtCore import Qt, QRect

class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0 #Quello che sarà il valore della barra piena
        self.color = QColor("#3b82f6")
        self.setFixedSize(120, 120)
    
    #Questa funzione permette di settare il valore a cui dovrà essere riempito il cerchio, lo assegna e lo ridisegna
    def set_value(self, value):
        self.value = value
        if value > 50 :
            color_hex="#22c55e"
        elif value > 20:
            color_hex="#eab308"
        else :
            color_hex="#ef4444"
        self.color = QColor(color_hex)
        self.update()

    def paintEvent(self, event):

        width = self.width()
        height = self.height()
        thickness = 10
        margin = 10
        rect = QRect(margin, margin, width - margin*2, height - margin*2)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #Disegniamo lo sfondo del cerchio
        pen_bg = QPen(QColor("#1e1e1e"))
        pen_bg.setWidth(thickness)
        pen_bg.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_bg)
        painter.drawArc(rect, 0, 360 * 16)
        #Disegniamo l'arco del progresso
        pen_progress = QPen(self.color)
        pen_progress.setWidth(thickness)
        pen_progress.setCapStyle(Qt.RoundCap)
        painter.setPen(pen_progress)
        
        start_angle = 90 * 16
        span_angle = -int((self.value/100)* 360 * 16)
        painter.drawArc(rect, start_angle, span_angle)
        #Testo centrale
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Segoe UI", 12, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, f"{self.value}%")
        painter.end()
        