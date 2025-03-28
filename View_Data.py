import sys

from datetime import(
    datetime,
    timedelta,
)

import numpy as np

##Used to query the database
import sqlite3

##Import classes from my own custom UI Elements
from Custom_UI_Elements import (
    Menu_Button,
    Image_Button,
    Conf_Dialogue,
    Title,
    SubTitle,
    data_options,
    error_message,
    MplCanvas,
)

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
)

from PyQt6.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates

from Drop_Down_Options import options

##Mehtods to retrieve data from database /api and input validation
from MSA_Utils import (
    Retrieve_Data,
    input_validation,
)

class View_Data_Window(QMainWindow):

    def __init__(self):
        ##Inherits from QMainWindow, the window class from the PyQt library
        super().__init__()
        
        self.normalised = True

        self.setWindowTitle("Meteorological Soaring Analysis")
        self.setWindowIcon(QIcon("logo.png"))
        
        ##Instantiate both layouts as a widget
        main_widget = QWidget()
        
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
        
        ##Create a layout for the whole window and add the title bar
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_bar)
        
        ##Create a layout for the lower part of the window below the title
        main_contents_layout = QHBoxLayout()
        
        left_third_layout = QVBoxLayout()
        
        ##Add the user inputs for each graph
        self.data_options_A = data_options("Line A:")
        self.line_B_checkbox = QCheckBox('Plot Second Line', self)
        self.data_options_B = data_options("Line B:")
        left_third_layout.addWidget(self.data_options_A)
        left_third_layout.addWidget(self.line_B_checkbox)
        left_third_layout.addWidget(self.data_options_B)
        
        ##Add a button to create the graph
        plot_button = Menu_Button(
            text = 'Plot Graph',
            color = '#7ED941',
            subroutine = self.plot_graph
        )
        
        ##Add a button to export the graph
        self.export_button = Menu_Button(
            text = 'Export Graph',
            color = '#7ED941',
            subroutine = self.export_graph
        )

        ##Set the maximum size of the plot and export button
        plot_button.setMaximumSize(150, 25)
        self.export_button.setMaximumSize(150, 25)
        
        ##Create a layout to hold the buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(plot_button)
        button_layout.addWidget(self.export_button)

        ##Add to the input layout
        left_third_layout.addLayout(button_layout)
        
        ##Hide the export button if there is no graph to export
        self.export_button.hide()
        
        ##Add the user inputs held on the left of the screen
        main_contents_layout.addLayout(left_third_layout)
        
        
        ##Create the maptlotlib FigureCanvas object,
        ##which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        ##Plot a line graph to test
        self.sc.axes.plot([12, 45, 106, 15, 24], [10,1,20,3,40])
        ##Hide the graph until it is plotted with user selected data
        self.sc.hide()

        ##Add the canvas to the main window layout
        main_contents_layout.addWidget(self.sc)
        main_layout.addLayout(main_contents_layout)
                     
        ##Set the layout for the main widget
        main_widget.setLayout(main_layout)
        
        ##Set the main widget as the central widget of the main window
        self.setCentralWidget(main_widget)

    def logo_clicked(self):
        ##Create a dialogue box for quit to main menu confirmation
        ##Parameter 1 is the window title
        ##Parameter 2 is the statement in the dialogue box
        quit_dialogue = Conf_Dialogue("Quit to Menu",
                                     "Are you sure you want to quit to the Main Menu?"
                                )
        if quit_dialogue.exec():
            ##If the user clicks yes in the dialogue box, the application will quit
            import Main_Menu
            self.main_window = Main_Menu.main_window()
            self.main_window.showMaximized()
            self.close()
        else:
            ##If the user clicks cancel in the dialogue box, the application will continue running
            print("Cancel")
            
    def test(self):
        print("Test")
        
    def export_graph(self):
        self.sc.figure.savefig("graph.png")
            
    def plot_graph(self):
        ##Display the export button
        self.export_button.show()
        
        lineB = False
        ##Check if the user wishes to plot a second line
        if self.line_B_checkbox.isChecked():
            lineB = True
        else:
            lineB = False
        
        ##Use the getter method from the data options to retrieve user inputs
        ##A dictionary is returned with the keys being the input type
        inputsA = self.data_options_A.getInputs()
        inputsB = self.data_options_B.getInputs()
        
        ##Extracts start and end dates from the dictionary
        if lineB:
            start_dates = [inputsA['start_date'], inputsB['start_date']]
            end_dates = [inputsA['end_date'], inputsB['end_date']]
        else:
            start_dates = [inputsA["start_date"]]
            end_dates = [inputsA["end_date"]]
        
        ##Create an instance of the data validation class for inputs A
        validateA = input_validation(start_dates[0], end_dates[0])
        if lineB:
            ##Create an instance of the data validation class for inputs B
            validateB = input_validation(start_dates[1], end_dates[1])
        
        #Only plot the graph if the date inputs are valid
        if validateA.validate_date() != True or (lineB and validateB.validate_date() != True):
            return(False)
        
        ##Create an instance of data retrieval
        retriever = Retrieve_Data(
            data_options_A = self.data_options_A,
            data_options_B = self.data_options_B,
            view_data = True
            )
        
        self.flight_data = [
            "Distance (km)",
            "Speed (kph)",
            "Completed",
            "Speed Points",
            "Height Points",
            "Distance Points",
            "Bonus Points",
            "Total Score",
        ]
        
        self.weather_data = [
            'Temperature (Celcius)',
            'Humidity (%)',
            'Dew Point (Celcius)',
            'Precipitation (mm)',
            'Wind Speed (kph)'
            ]
        
        ## Initialize pointsA and pointsB to None
        pointsA = None
        pointsB = None
        
        ##Call the correct subroutine based on if the user has requested weather or flight data
        ##If the user has selected line B retrieve the data for both A and B
        if lineB:
            ##If the condition is flight data then an sql query is needed
            if inputsA['condition'] in self.flight_data:
                print("flight")
                pointsA = retriever.retrieve_flights('A') 
            ##If the condition is weather data then an API request is needed  
            elif inputsA['condition'] in self.weather_data:
                print("weather")
                pointsA = retriever.retrieve_weather('A')
            
            ##Repeat for line B
            if inputsB['condition'] in self.flight_data:
                pointsB = retriever.retrieve_flights('B')
            elif inputsB['condition'] in self.weather_data:
                pointsB = retriever.retrieve_weather('B')
        
        ##If the user only wants line A don't retrieve data for line B
        else:
            if inputsA['condition'] in self.flight_data:
                pointsA = retriever.retrieve_flights('A') 
                print("flight")  
            elif inputsA['condition'] in self.weather_data:
                pointsA = retriever.retrieve_weather('A')
                print("weather")
            else:
                print(f"Condition: {inputsA['condition']}")
                print("Condition invalid")
                
        ## Ensure pointsA and pointsB have been retrieved
        if pointsA is None:
            print("Error: No data retrieved for Line A")
            return False
        ##Only check for line B if it is needed
        if lineB and pointsB is None:
            print("Error: No data retrieved for Line B")
            return False
        
        
        ##Convert the values for A into a numpy array
        ##Convert dates from DD-MM-YYYY to YYYY-MM-DD
        ##To support the matplotlib date format
        datesA = [mdates.date2num(datetime.strptime(row[0], "%Y-%m-%d")) for row in pointsA]
        ##Convert to numpy array
        datesA_numpy = np.array(datesA)
        ##Convert values to floats
        valuesA = [float(row[1]) for row in pointsA]
        ##Find the range of dates
        date_rangeA = datesA_numpy.max() - datesA_numpy.min()
        
        ##Only convert and plot inputsB if the uer wants to plot them
        if lineB:
            ##Convert dates from DD-MM-YYYY to YYYY-MM-DD
            ##To support the matplotlib date format
            datesB = [mdates.date2num(datetime.strptime(row[0], "%Y-%m-%d")) for row in pointsB]
            ##Convert to numpy array to get range
            datesB_numpy = np.array(datesA)
            ##Find the range of dates
            date_rangeB = datesB_numpy.max() - datesB_numpy.min()
            ##Convert values to floats
            valuesB = [float(row[1]) for row in pointsB]
            
            
        ##If the 2 conditions are dissimiar they must be normalised
        if lineB:
            self.normalised = True
            if (inputsA["condition"] != inputsB["condition"]):
                normalised_data = retriever.normaliseData(
                    valuesA=pointsA,
                    valuesB=pointsB,
                    inputsA=inputsA,
                    inputsB=inputsB
                )
                # Update valuesA for all its data points
                for i in range(len(normalised_data[0])):
                    valuesA[i] = normalised_data[0][i][1]
                
                # Update valuesB for all its data points
                for i in range(len(normalised_data[1])):
                    valuesB[i] = normalised_data[1][i][1]
                    
                    
                    
            else:
                # When conditions are the same, no normalization is needed.
                pass
                
            
            
        ##Clear previous plots
        self.sc.axes.clear()
        
        ##Plot the graph
        self.sc.axes.plot(datesA, valuesA, label='Line A', color = '#17becf' )
        ##Only plot lineB if the user has selected
        if lineB:
            self.sc.axes.plot(datesB, valuesB, label='Line B', alpha = 0.5, color = 'red')
            
        ## Convert date range to timedelta to be able to locate days
        date_rangeA = timedelta(days=(datesA[-1] - datesA[0]))
        if lineB:
            date_rangeB = timedelta(days=(datesB[-1] - datesB[0]))
            
        # The largest date range should be used
        if lineB and date_rangeB > date_rangeA:
            date_range = date_rangeB
        else:
            date_range = date_rangeA

        ##Set the axis label based on the date range
        ##If there are less than 2 months show each day
        if date_range.days <= 60:
            self.sc.axes.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
            self.sc.axes.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ##If there are less than 2 years show each month
        elif date_range.days <= 730:
            self.sc.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
            self.sc.axes.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        ##If there is more than 2 years show each year
        else:
            self.sc.axes.xaxis.set_major_locator(mdates.YearLocator())
            self.sc.axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
            
        ##Rotate the axis label by 45 degrees
        self.sc.axes.set_xticklabels(self.sc.axes.get_xticklabels(), rotation=45, ha='right')
        ##Reduce size
        self.sc.axes.tick_params(axis='x', which='major', labelsize=10)
        
        ## Adjust the bottom margin to ensure the labels are visible
        self.sc.figure.subplots_adjust(bottom=0.2)
        
        ##Add a label to the axis
        if lineB:
            self.sc.axes.set_xlabel(
                inputsA['condition'] +' - ' +'(' + inputsA['region'] + ')' +
                ' / ' +
                inputsB['condition'] +' - ' + '(' + inputsB['region'] + ')'
            )
            
            ##Set the legend
            self.sc.axes.legend([
                inputsA['condition'] +' - ' + '(' + inputsA['region'] + ')',
                inputsB['condition'] +' - ' + '(' + inputsB['region'] + ')'
            ]
            )
            
        else:
            self.sc.axes.set_xlabel(
                inputsA['condition'] +' - ' + '(' + inputsA['region'] + ')'
            )
            
            ##Set the legend
            self.sc.axes.legend([
                inputsA['condition'] +' - ' + '(' + inputsA['region'] + ')'
            ]
            )
        
        ##Set the y axis label if data has been normalised
        if self.normalised:
            self.sc.axes.set_ylabel(
                'Normalised Values (%)'
            )
            
        
        self.sc.show()
        self.sc.draw()
         
# ##Instantiate a QtApplication
# app = QApplication(sys.argv)
# ##Set the active window to an instance of this class
# view_data_window = View_Data_Window()
# ##Open the window maximized (Windowed FullScreen)
# view_data_window.showMaximized()
# ##Run the application
# sys.exit(app.exec())