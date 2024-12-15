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
        hLayout = QHBoxLayout()
        vLayout = QVBoxLayout()
        
        ##Create the left box
        hLayout.addWidget(Color('red'))
        
        ##Create a vertical box layout within the left box
        hLayout.addLayout( vLayout )
        
        ##Add widgets to the vertical box
        #vLayout.addWidget('green')
        # vLayout.addWidget('purple')
        # vLayout.addWidget('pink')
        
        ##Create the right box
        hLayout.addWidget(Color('blue'))
        
        ##Instantiate a single widget and set the layout to the
        ##layout just created
        ##*(Effectively instiates what was just defined)
        widget = QWidget()
        widget.setLayout(hLayout)
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
