import sys

##Import classes from my own custom UI Elements
from Custom_UI_Elements import (
    Menu_Button,
    Image_Button,
    Conf_Dialogue,
    Title,
)
    
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
)
from PyQt6.QtGui import (
    QIcon,

)

class MainWindow(QMainWindow):

    def __init__(self):
        ##Inherits from QMainWindow, the window class from the PyQt library
        super().__init__()

        self.setWindowTitle("Meteorological Soaring Analysis")
        self.setWindowIcon(QIcon("logo.png"))    
        
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
                                      subroutine = self.view_data))
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
        ##The close button is initially hidden, as the info is not yet shown
        if self.info_shown == False:
            self.closeButton.hide()
        else:
            self.closeButton.show()

        ##Set the "button" area of the window (0th index) to take up 30% of the horizontal window space
        hLayout.setStretch(0, 2)
        ##Therefore set the 1st index area of the window to take up 70% of the horizontal window space
        hLayout.setStretch(1,8)
        
        ##Instantiate both layouts as a widget
        MainWidget = QWidget()
        MainWidget.setLayout(hLayout)
        
        ##Create a vertical box layout that will hold the title as its first box
        ##and the rest of the window as the second, lower box
        titleLayout = QVBoxLayout()
        
        # Create a container widget for the title and logo
        title_logo_container = QWidget()
        ##Set the container to be blue
        title_logo_container.setStyleSheet("background-color: #95d1ff;")
        
        ##Create a horizontal layout for the title and logo
        title_logo_layout = QHBoxLayout()
        title_logo_layout.setContentsMargins(5,5,5,5)
        title_logo_layout.setSpacing(0)
        
        ##Set the layout of the container to the horizontal layout
        title_logo_container.setLayout(title_logo_layout)
        
        ##Instantiates the title class, passing in the text as a parameter
        title_logo_layout.addWidget(Title("Meteorological Soaring Analysis"))
        
        ##Instantiates the image button class, passing in the image path and the subroutine to run
        logo_button = Image_Button("logo.png", self.test)
        # Limit the logo size
        logo_button.setFixedSize(140, 100)
        title_logo_layout.addWidget(logo_button)
        
        ##Set the title to take up 90% of the window
        title_logo_layout.setStretch(0,9)
        ##Set the logo to take up 10% of the window
        title_logo_layout.setStretch(1,1)
        
        ##Set the maximum height of the title and logo container
        title_logo_container.setMaximumHeight(100)
        
        ##Add the title and logo to the top of the window
        titleLayout.addWidget(title_logo_container)
        
        ##Adds the main widget (containing buttons etc) below the title
        titleLayout.addWidget(MainWidget)        
        ##With the main widget added, the title layout can be considered to be the main
        ##(and only) layout
        mainLayout = titleLayout
        
        ##Set the top widget (0th index) to take up 10% of the window
        titleLayout.setStretch(0,1)
        ##Therefore the 1st index must take up 90%
        titleLayout.setStretch(1,29)
        
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
        self.info_shown = False
        
    def view_data(self):
        import View_Data
        self.view_data_window = View_Data.View_Data_Window()
        self.view_data_window.showMaximized()
        self.close()
        
        
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
        info_doc = open('README.txt','r')
        self.info_widget.setText(info_doc.read())
        self.closeButton.show()
        self.info_shown = True
        info_doc.close()
        

##Instantiate a QtApplication
app = QApplication(sys.argv)

##Set the active window to the main window we have been working with
window = MainWindow()

##Open the window maximised (Windowed FullScreen)
window.showMaximized()

##Run the app
app.exec()
