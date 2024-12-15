import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget
)
from PyQt6.QtGui import (
    QPalette,
    QColor
)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Testing Widgets")
        
        widget = Color("red")
        self.setCentralWidget(widget)

class Color(QWidget):
    
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        
app = QApplication(sys.argv)
    
window = MainWindow()
window.show()
    
app.exec()
