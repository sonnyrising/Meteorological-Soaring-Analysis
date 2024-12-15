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

        self.setWindowTitle("Widget Testing")      
        
        ##Horizontal layout            
        hLayout = QHBoxLayout()
        ##Vertical Layout
        vLayout = QVBoxLayout()

        ##Sets spacing and margins for the horizontal widget
        hLayout.setContentsMargins(0,0,0,0)
        hLayout.setSpacing(10)

        ##Adds each coloured widget to the vertical widget
        ##* The second layout must be fully defined before it is adde to the first layout
        vLayout.addWidget(Color('red'))
        vLayout.addWidget(Color('yellow'))
        vLayout.addWidget(Color('purple'))

        ##Adds the vertical layout as a widget to the horizontal layout
        #?Does this instantiate the second layout?
        hLayout.addLayout( vLayout )

        ##Adds a second widget the same size as the vertical layout to the horizontal layout
        hLayout.addWidget(Color('green'))

        ##Set the "button" area of the window (0th index) to take up 30% of the horizontal window space
        hLayout.setStretch(0, 3)
        ##Therefore set the 1st index area of the window to take up 70% of the horizontal window space
        ##?Is this necessary?
        hLayout.setStretch(1,7)
        
        ##Instantiate both layouts as a widget
        MainWidget = QWidget()
        MainWidget.setLayout(hLayout)
        
        titleLayout = QVBoxLayout()
        titleLayout.addWidget(Color('white'))
        titleLayout.addWidget(MainWidget)
        
        ##Set the white top widget (0th index) to take up 10% of the window
        titleLayout.setStretch(0,1)
        ##Therefore the 1st index must take up 90%
        ##?Is this necessary?
        titleLayout.setStretch(1,9)
        WindowWidget = QWidget()
        WindowWidget.setLayout(titleLayout)
        
        self.setCentralWidget(WindowWidget)
        
        

class Color(QWidget):
    
    def __init__(self, color):
        super().__init__()
        ##The widget will instantly fill with the background color
        self.setAutoFillBackground(True)
        
        ##Creates an instance of a QPalette
        palette = self.palette()
        
        ##Sets the palette to the passed color
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        #? Why did putting .ColorRole fix this?
        #TODO: find out what .ColorRole does
        self.setPalette(palette)
        
app = QApplication(sys.argv)
    
window = MainWindow()
window.show()
    
app.exec()
