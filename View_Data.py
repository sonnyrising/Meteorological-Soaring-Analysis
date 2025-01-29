import sys

##Import classes from my own custom UI Elements
from Custom_UI_Elements import (
    Menu_Button,
    Image_Button,
    Conf_Dialogue,
    Title,
)

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)
from PyQt6.QtGui import QIcon

class View_Data_Window(QMainWindow):

    def __init__(self):
        ##Inherits from QMainWindow, the window class from the PyQt library
        super().__init__()

        self.setWindowTitle("Meteorological Soaring Analysis")
        self.setWindowIcon(QIcon("logo.png"))
        
        ##Instantiate both layouts as a widget
        MainWidget = QWidget()
        
        ##Create a vertical box layout that will hold the title as its first box
        ##and the rest of the window as the second, lower box
        titleLayout = QVBoxLayout()
        
        # Create a container widget for the title and logo
        title_logo_container = QWidget()
        
        ##Set the container to be blue
        title_logo_container.setStyleSheet("background-color: #95d1ff;")
        
        # Create a horizontal layout for the title and logo
        title_logo_layout = QHBoxLayout()
        title_logo_layout.setContentsMargins(5,5,5,5)
        title_logo_layout.setSpacing(0)
        
        # Set the layout for the container
        title_logo_container.setLayout(title_logo_layout)
        
        ##Instantiates the title class, passing in the text as a parameter
        title_logo_layout.addWidget(Title("Meteorological Soaring Analysis"))
        
        ##Instantiates the image button class, passing in the image path and the subroutine to run
        logo_button = Image_Button("logo.png", self.test)
        # Limit the logo size
        logo_button.setFixedSize(45, 30)
        title_logo_layout.addWidget(logo_button)
        
        # Set the title to take up 10% of the window width
        title_logo_layout.setStretch(0, 1)
        # Set the logo to take up 90% of the window width
        title_logo_layout.setStretch(1, 9)
        
         ##Set the maximum height of the title and logo container
        title_logo_container.setMaximumHeight(50)
    
        ##Create a vertical box layout that will hold the title as its first box
        ##and the rest of the window as the second, lower box
        topLayout = QVBoxLayout()
        
        # Create a container widget for the title and logo
        top_container = QWidget()
        
        ##Set the container to be blue
        top_container.setStyleSheet("background-color: #95d1ff;")
        
        # Create a horizontal layout for the title and logo
        topLayout = QVBoxLayout()
        topLayout.setContentsMargins(5,5,5,5)
        topLayout.setSpacing(0)
        
        titleLayout.addLayout(topLayout)
        
        topLayout.addWidget(title_logo_container)
        
        subtitle = Title("View Data")
        subtitle.setMaximumHeight(50)
        topLayout.addWidget(subtitle)
        
        
        
        
        
        # Add the main widget (containing buttons etc) below the title
        titleLayout.addWidget(QLabel("Main content here"))
        
        # Set the layout for the main widget
        MainWidget.setLayout(titleLayout)
        
        # Set the main widget as the central widget of the main window
        self.setCentralWidget(MainWidget)

    def test(self):
        print("Test")

# ##Instantiate a QtApplication
# app = QApplication(sys.argv)
# ##Set the active window to the main window we have been working with
# window = View_Data_Window()
# ##Open the window maximized (Windowed FullScreen)
# window.showMaximized()
# ##Run the application
# sys.exit(app.exec())