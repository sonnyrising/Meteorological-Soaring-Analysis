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
        
        self.setWindowTitle('Testing Widgets')
        
        ##Create a layout using the QHBoxLayout
        ##This places widgets horizontally
        layout = QHBoxLayout()
        
        ##Add 2 widgets to the layout
        layout.addWidget(Color('red'))
        layout.addWidget(Color('blue'))
        
        ##Instantiate a single widget and set the layout to the
        ##layout just created
        ##*(Effectively instiates what was just defined)
        widget = QWidget()
        widget.setLayout(layout)
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
