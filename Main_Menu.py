import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QScrollArea,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
    
    
)
from PyQt6.QtGui import (
    QPalette,
    QColor,
    
)



class MainWindow(QMainWindow):

    def __init__(self):
        ##Inherits from QMainWindow, the window class from the PyQt library
        super().__init__()

        self.setWindowTitle("Meteorological Soaring Analysis")    
        
        ##Horizontal layout            
        hLayout = QHBoxLayout()
        ##Vertical Layout
        vLayout = QVBoxLayout()

        ##Sets spacing and margins for the horizontal widget
        hLayout.setContentsMargins(0,0,0,0)
        hLayout.setSpacing(10)

        ##Adds each coloured widget to the vertical widget
        ##* The second layout must be fully defined before it is adde to the first layout
        vLayout.addWidget(Menu_Button(text = 'View Data',
                                      color = '#7ED941',
                                      subroutine = self.test))
        vLayout.addWidget(Menu_Button(text = 'Run Analysis',
                                      color = '#7ED941',
                                      subroutine = self.test))
        vLayout.addWidget(Menu_Button(text = 'Info',
                                      color = '#7ED941',
                                      subroutine = self.show_info))
        vLayout.addWidget(Menu_Button(text = 'Quit',
                                      color = '#7ED941',
                                      subroutine = self.quit))
        
        ##Sets each button to have the same stretch factor
        ##i.e. each button will have the same size and fill the layout
        vLayout.setStretch(0,1)
        vLayout.setStretch(1,1)
        vLayout.setStretch(2,1)
        vLayout.setStretch(3,1)
        
        
        ##Adds the vertical layout as a widget to the horizontal layout
        hLayout.addLayout( vLayout )
        
        ##Initially, the info window is not displayed, so the close button is not needed
        self.info_shown = False

        ##Create the widget to display info
        self.info_widget = QLabel()
        
        ##Set the font size of the text in the info scroll area
        ##Using inline styling with QSS
        self.info_widget.setStyleSheet("font-size: 24px")
        
        ##Set the text to allign to the centre of the label
        self.info_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ##Allow the label to expand vertically
        ##(By default, widgets can only expand horizontally)
        self.info_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        ##Wordwrap allows lines to be cut and added to another line below
        ##This prevents lines from spilling over the window
        self.info_widget.setWordWrap(True)

        ##Create a scroll area attached to the info label
        ##This allows the text to be scrolled with either the scrollbar created or the scroll wheel
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.info_widget)
        self.scroll_area.setWidgetResizable(True)
        
        ##Create a button to close the info box
        self.closeButton = QPushButton("Close Info")
        self.closeButton.clicked.connect(self.close_info)
        
        ##Adds the scroll area (and the info label) to the layout
        hLayout.addWidget(self.scroll_area)
        hLayout.addWidget(self.closeButton)
        if self.info_shown == False:
            self.closeButton.hide()
        else:
            self.closeButton.show()

        ##Set the "button" area of the window (0th index) to take up 30% of the horizontal window space
        hLayout.setStretch(0, 3)
        ##Therefore set the 1st index area of the window to take up 70% of the horizontal window space
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
        titleLayout.setStretch(1,9)
        
        ##Instantiates a widget to contain the layouts
        WindowWidget = QWidget()
        
        ##Sets the layout of the widget to the layout created
        WindowWidget.setLayout(mainLayout)
        
        ##Ensures the widget containing all of the window is centralised
        self.setCentralWidget(WindowWidget)
    
    ##Used to test the buttons are working
    def test(self):
        print("Button Clicked")
    
    ##Fills the scroll area with an empty string
    ##Giving the effect that it has been closed
    def close_info(self):
        self.info_widget.setText("")
        self.closeButton.hide()
        
    def quit(self):
        ##Create a dialogue box for quit confirmation
        ##Parameter 1 is the window title
        ##Parameter 2 is the statement in the dialogue box
        quitDialogue = Conf_Dialogue("Quit",
                                     "Are you sure you want to quit?"
                                )
        if quitDialogue.exec():
            ##If the user clicks yes in the dialogue box, the application will quit
            QApplication.quit()
        else:
            ##If the user clicks cancel in the dialogue box, the application will continue running
            print("Cancel")
        
    ##Reads the info from the relevant text file and displays it in the info widget     
    def show_info(self):
        info_doc = open('main_menu_info.txt','r')
        self.info_widget.setText(info_doc.read())
        self.closeButton.show()
        self.info_shown = True
        info_doc.close()
        
        
        
##This class creates a widget filled with a solid color which is passed in as a parameter
class Color(QWidget):
    
    def __init__(self, color):
        super().__init__()
        ##The widget will instantly fill with the background color
        self.setAutoFillBackground(True)
        
        ##Creates an instance of a QPalette
        ##This is used for setting the fill color of the widget
        palette = self.palette()
        
        ##Sets the palette to the passed colour
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)



##This class creates a widget, containing text that is passed in as a pareameter
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
        palette.setColor(QPalette.ColorRole.Window, QColor(149, 209, 255))
        self.setPalette(palette)
        
        ##Allign the text to the centre of the QLabel
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ##Use QSS (A form of CSS) to style the text
        self.setStyleSheet("""color: black;
                           font-size: 64px;
                           font-family: calibri;
                           """)

##A class for custom buttons
class Menu_Button(QPushButton):
    
    def __init__(self, text, color, subroutine):
        super().__init__(text)
        
        ##Set the button color using QSS
        self.setStyleSheet(f"background-color: {color}; font-size: 36px; color: black")
        
        ##The button runs the subroutine passed as an argument
        self.clicked.connect(subroutine)
        
        ##Sets the button to fit the container it was placed in
        self.setSizePolicy(
        QSizePolicy.Policy.MinimumExpanding,
        QSizePolicy.Policy.MinimumExpanding)

##A class to create a confirmation dialogue
class Conf_Dialogue(QDialog):
    def __init__(self, title, statement):
        super().__init__()
        self.title = title
        self.statement = statement

        
        ##Set the title of the window to the parameter passed in
        self.setWindowTitle(self.title)
        
        ##Create the buttons (the pipe (|) indicates an OR)
        buttons = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.Cancel
        
        ##Instantiate the button box
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        ##Create the layout for the dialogue box
        layout = QVBoxLayout()
        message = QLabel(self.statement)
        layout.addWidget(message)
        layout.addWidget(self.button_box)
        self.setLayout(layout)
        
        
        
 

##Instantiate a QtApplication
app = QApplication(sys.argv)

##Set the active window to the main window we have been working with
window = MainWindow()

##Open the window maximised (Windowed FullScreen)
window.showMaximized()

##Run the app
app.exec()
