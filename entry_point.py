##Import each class from the other files
from Main_Menu import main_window

##Import libraries necessary to run the program
import sys
from PyQt6.QtWidgets import (
    QApplication
)

##Create an instance of the main window
main_window = main_window()

##Show the main window fullscreen
main_window.showMaximized()

##Initilaise the PyQT application
app = QApplication(sys.argv) 

##Ensures the app closes properly
sys.exit(app.exec())