import sys

##Import classes from my own custom UI Elements
from Custom_UI_Elements import (
    Menu_Button,
    Image_Button,
    Conf_Dialogue,
    Title,
    SubTitle,
    data_options
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
        
        ##Creates the title bar using the custom title class
        title_bar = Title("Meterological Soaring Analysis")
        title_bar.setMaximumHeight(60)
        
        ##Creates the subtitle bar using the custom subtitle class
        ##Slightly smaller than the title bar
        subtitle_bar = SubTitle("View Data", 36)
        subtitle_bar.setMaximumHeight(30)
        
        ##Creates a blue background to hold the title and subtitle
        title_widget = QWidget()
        title_widget.setStyleSheet("background-color: #95d1ff;")
        
        title_layout = QVBoxLayout()
        title_layout.addWidget(title_bar)
        title_layout.addWidget(subtitle_bar)
        
        title_widget.setLayout(title_layout)
        
        ##Set a maximum height for the title and subtitle widget
        title_widget.setMaximumHeight(100)
        
        ##Creates a background for the title and subtitle and logo
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #95d1ff;")
        
        top_layout = QHBoxLayout()
    
        ##Creates a logo button using the custom image button class
        logo_button = Image_Button("logo.png", self.logo_clicked)
        logo_button.setFixedSize(145, 90)
        
        ##Adds the subtitle and title bar to the logo as a horizontal layout
        top_layout.addWidget(title_widget)
        top_layout.addWidget(logo_button)
        
        top_bar.setLayout(top_layout)
        
        top_bar.setMaximumHeight(100)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_bar)
        
        ##Add the user inputs for each graph
        self.data_options_A = data_options("Line A:")
        self.data_options_B = data_options("Line B:")
        main_layout.addWidget(self.data_options_A)
        main_layout.addWidget(self.data_options_B)
        
        ##Add a button to create the graph
        plot_button = Menu_Button(
            text = 'Plot Graph',
            color = '#7ED941',
            subroutine = self.plot_graph
        )

        plot_button.setMaximumSize(200, 30)
        main_layout.addWidget(plot_button)
        
        main_layout.setStretch(0,1)
        main_layout.setStretch(1,12)
        main_layout.setStretch(2,2)
        main_layout.setSpacing(5)
        
        ##Set the layout for the main widget
        MainWidget.setLayout(main_layout)
        
        ##Set the main widget as the central widget of the main window
        self.setCentralWidget(MainWidget)

    def logo_clicked(self):
        ##Create a dialogue box for quit to main menu confirmation
        ##Parameter 1 is the window title
        ##Parameter 2 is the statement in the dialogue box
        quitDialogue = Conf_Dialogue("Quit to Menu",
                                     "Are you sure you want to quit to the Main Menu?"
                                )
        if quitDialogue.exec():
            ##If the user clicks yes in the dialogue box, the application will quit
            import Main_Menu
            self.mainWindow = Main_Menu.MainWindow()
            self.mainWindow.showMaximized()
            self.close()
        else:
            ##If the user clicks cancel in the dialogue box, the application will continue running
            print("Cancel")
            
    def test(self):
        print("Test")
    
    ##Subroutine called when the plot graph button is clicked
    def plot_graph(self):
        
        ##Use the getter method from the data options to retrieve user inputs
        ##A dictionary is returned with the keys being the input type
        inputsA = self.data_options_A.getInputs()
        inputsB = self.data_options_A.getInputs()
        
        ##Extracts start and end dates from the dictionary
        start_dates = [inputsA['start_date'], inputsB['start_date']]
        end_dates = [inputsA['end_date'], inputsB['end_date']]
        
        ##Create an instance of input validation to the current inputs
        ##Repeated twice to check graph A and B
        for i in range (0,1):
            input_validation = inputValidation(start_dates[i], end_dates[i])
            if input_validation.validateDate() == True:
                print("Validated")
            elif input_validation.validateDate() == "end_date before start_date":
                print("end_date before start_date")
                if i == 0:
                    print("Error graph A")
                else:
                    print("Error graph B")
            elif input_validation.validateDate() == "start_date = end_date":
                print ("start_date = end_date")
                if i == 0:
                    print("Error graph A")
                else:
                    print("Error graph B")
            else:
                print("Error")
        
        
##A class to handle validating user inputs  
class inputValidation:
    def __init__(self,start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
    
    def validateDate(self):
        ##Due to the QDateEdit widget, the date is already in the correct format
        ##Minimum and maximum dates are set by the QDateEdit widget so dont need to be validated
        
        ##Check if dates are in the correct order
        ##ie cant end before it starts
        if self.start_date  < self.end_date:
            return(True)
        
        ##Check if the start date is before the end date
        elif self.start_date > self.end_date:
            ##Return an appropriate error message to trigger a popup
            return "end_date before start_date"
        
        ##Check if the start date is the same as the end date
        else:
            return "start_date = end_date"
        

        
        


##Instantiate a QtApplication
app = QApplication(sys.argv)
##Set the active window to the main window we have been working with
window = View_Data_Window()
##Open the window maximized (Windowed FullScreen)
window.showMaximized()
##Run the application
sys.exit(app.exec())