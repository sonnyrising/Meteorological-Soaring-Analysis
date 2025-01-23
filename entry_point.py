##Import each class from the other files
from Main_Menu import MainWindow

##Import libraries necessary to run the program
import sys
from PyQt6.QtWidgets import (
    QApplication
)

##Initilaise the PyQT application
app = QApplication(sys.argv) 

##Keeps the app responsive, listening for user inputs
##Ensures the app closes properly
sys.exit(app.exec())