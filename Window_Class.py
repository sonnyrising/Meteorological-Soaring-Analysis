##To reduce memory load, each widget is imported seperately
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

##Import the logo class
from Logo_Class import Clickable_Image

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
        
        # Create a clickable image instance (logo)
        self.logo = Clickable_Image("logo.png", self.quit_to_menu)
        
        # Layout to display the clickable image
        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        self.setLayout(layout)
        
        
    def quit_to_menu(self):
        ##TODO: Subroutine to quit to main menu
        print("Quitting to menu")
        
    
