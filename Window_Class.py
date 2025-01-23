##To reduce memory load, each widget is imported seperately
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

##Define the Window class
class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    ##Defining Attributes
        ##Window title
        self.title = 'Meteorological Soaring Analysis'
        self.setWindowTitle(self.title)
        
        ##Window dimensions
        ##Gets the window dimensions using the .geometry method of the application
        resolution = QApplication.primaryScreen().geometry() ##an object with attributes x, y, width and height
        self.height = resolution.height()
        self.width = resolution.width()
        
        ##Tuples to hold containers
        self.left_third = ()
        self.right_thirds = ()
        
        ##Tuple to hold buttons
        self.buttons = ()
        
        
    def quit_to_menu(self):
        ##TODO: Subroutine to quit to main menu
        print("Quitting to menu")
        
        
    
