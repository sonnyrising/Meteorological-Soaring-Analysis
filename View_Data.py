import sys
from PyQt6.QtWidgets import(
    QApplication,
    QMainWindow,
    QWidget,
)
from PyQt6.QtGui import QIcon
class View_Data_Window(QMainWindow):

    def __init__(self):
        ##Inherits from QMainWindow, the window class from the PyQt library
        super().__init__()

        self.setWindowTitle("Meteorological Soaring Analysis")
        self.setWindowIcon(QIcon("logo.png"))
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

def run_app():
    ##Instantiate a QtApplication
    app = QApplication(sys.argv)
    ##Set the active window to the main window we have been working with
    window = MainWindow()
    #Open the window maximised (Windowed FullScreen)
    window.showMaximized()