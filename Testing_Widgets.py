import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtGui import (
    QPalette,
    QColor
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        layout1.setContentsMargins(0,0,0,0)
        layout1.setSpacing(10)

        layout2.addWidget(Color('red'))
        layout2.addWidget(Color('yellow'))
        layout2.addWidget(Color('purple'))

        layout1.addLayout( layout2 )

        layout1.addWidget(Color('green'))
        

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)
        
        

class Color(QWidget):
    
    def __init__(self, color):
        super().__init__()
        ##The widget will instantly fill with the background color
        self.setAutoFillBackground(True)
        
        ##Creates an instance of a QPalette
        palette = self.palette()
        
        ##Sets the palette to the passed color
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        #TODO: find out what .ColorRole does
        self.setPalette(palette)
        
app = QApplication(sys.argv)
    
window = MainWindow()
window.show()
    
app.exec()
