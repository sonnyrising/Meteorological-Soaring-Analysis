import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
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
        vLayout.addWidget(Color('black'))

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
        
        ##Create a vertical box layout that will hold the title as its first box
        ##and the rest of the window as the second, lower box
        titleLayout = QVBoxLayout()
        
        ##Instantiates the title class, passing in the text as a parameter
        titleLayout.addWidget(Title("Meteorological Soaring Analysis"))
    
        ##Adds the main widget (containing buttons etc) below the title
        titleLayout.addWidget(MainWidget)
        
        ##With the main widget added, the title layout can be considered to be the main
        ##(and only) layout
        mainLayout = titleLayout
        
        ##Set the white top widget (0th index) to take up 10% of the window
        titleLayout.setStretch(0,1)
        ##Therefore the 1st index must take up 90%
        ##?Is this necessary?
        titleLayout.setStretch(1,9)
        
        ##Instantiates a widget to contain the layouts
        WindowWidget = QWidget()
        
        ##Sets the layout of the widget to the layout created
        WindowWidget.setLayout(mainLayout)
        
        ##Ensures the widget containing all of the window is centralised
        self.setCentralWidget(WindowWidget)
        
        
##This class creates a widget filled with a solid color which is passed in as a parameter
class Color(QWidget):
    
    def __init__(self, color):
        super().__init__()
        ##The widget will instantly fill with the background color
        self.setAutoFillBackground(True)
        
        ##Creates an instance of a QPalette
        palette = self.palette()
        
        ##Sets the palette to the passed colour
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        #? Why did putting .ColorRole fix this?
        #TODO: find out what .ColorRole does
        self.setPalette(palette)



#This class creates a widget, containing text that is passed in as a pareameter
##It uses QSS to style as a title
class Title(QLabel):
    
    def __init__(self, text):
        super().__init__()
        
        ##Create a QLable (textbox) holding the title of the window
        ##*This is a form of a widget, like the coloured widgets
        titleLabel = QLabel(text)
        self.setText(text)
        
        ##Set the background color of the QLabel
        self.setAutoFillBackground(True)
        palette = titleLabel.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("white"))
        self.setPalette(palette)
        
        ##Allign the text to the centre of the QLabel
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ##Use QSS (A version of CSS) to style the text
        self.setStyleSheet("color: blue; font-size: 72px")
        
        
        
 

##Instantiate a QtApplication
app = QApplication(sys.argv)

##Set the active window to the main window we have been working with
window = MainWindow()

##Open the window maximised (Windowed FullScreen)
window.showMaximized()

##Run the app
app.exec()
