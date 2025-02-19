import sys

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
    QLabel,
    QCheckBox,
)

from PyQt6.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.dates as mdates

from Drop_Down_Options import options
from lookup_tables import lookup_tables

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
        self.line_B_checkbox = QCheckBox('Plot Second Line', self)
        self.data_options_B = data_options("Line B:")
        left_third_layout.addWidget(self.data_options_A)
        left_third_layout.addWidget(self.line_B_checkbox)
        left_third_layout.addWidget(self.line_B_checkbox)
        left_third_layout.addWidget(self.data_options_B)
        
        ##Add a button to create the graph
        plot_button = Menu_Button(
            text = 'Plot Graph',
            color = '#7ED941',
            subroutine = self.validate_data
        )

        ##Set the maximum size of the plot button
        plot_button.setMaximumSize(200, 30)
        
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
        

        
        
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot([12, 45, 106, 15, 24], [10,1,20,3,40])

        main_contents_layout.addWidget(sc)
        
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
            
    def export_graph(self):
        self.sc.figure.savefig('Saved Graph.png')

            
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
        
        ##If the validation class returns True, the input is valid
        if validation_result_A == True:
            ##Set passed to true
            validation_passed = True
        elif validation_result_A == "end_date before start_date":
            ##The end date is before the start date
            ##Create a popup to inform the user
            popup = error_message("Error in Line A", "End Date before Start Date")
            popup.exec()
            validation_passed = False
        elif validation_result_A == "start_date = end_date":
            ##The end date is equal to the start date
            ##Create a popup to inform the user
            popup = error_message("Error in Line A", "Start Date equal to End Date")
            popup.exec()
            validation_passed = False
        
        ##Create an instance of input validation to the current inputs for line B
        input_validation_B = inputValidation(start_dates[1], end_dates[1])
        validation_result_B = input_validation_B.validateDate()

        if validation_result_B == True:
            ##Set passed to true
            validation_passed = True
        elif validation_result_B == "end_date before start_date":
            ##The end date is before the start date
            ##Create a popup to inform the user
            popup = error_message("Error in Line B", "End Date before Start Date")
            popup.exec()
            validation_passed = False
        elif validation_result_B == "start_date = end_date":
            ##The end date is equal to the start date
            ##Create a popup to inform the user
            print ("start_date = end_date")
            popup = error_message("Error in Line B", "End Date equal to Start Date")
            popup.exec()
            validaton_passed = False
        
        
        ##Validation has been passed, return true
        if validation_passed == True:
            return True
            
            
    def plot_graph(self):
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
        
        ##Only plot the graph if the inputs are valid
        if self.validate_data(start_dates, end_dates) != True:
            return(False)
        
        ##Create an instance of data retrieval
        retriever = Retrieve_Data(self.data_options_A, self.data_options_B)
        
        flight_data = [
            "Distance (km)",
            "Speed (kph)",
            "Completed",
            "Speed Points",
            "Height Points",
            "Distance Points",
            "Bonus Points",
            "Total Score",
        ]
        
        weather_data = [
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
        if lineB:
            if inputsA['condition'] in flight_data:
                print("flight")
                pointsA = retriever.retrieve_flights('A')   
            elif inputsA['condition'] in weather_data:
                print("weather")
                pointsA = retriever.retrieve_weather('A')
            
            if inputsB['condition'] in flight_data:
                pointsB = retriever.retrieve_flights('B')
            elif inputsB['condition'] in weather_data:
                pointsB = retriever.retrieve_weather('B')
                
        else:
            if inputsA['condition'] in flight_data:
                pointsA = retriever.retrieve_flights('A') 
                print("flight")  
            elif inputsA['condition'] in weather_data:
                pointsA = retriever.retrieve_weather('A')
                print("weather")
            else:
                print(f"Condition: {inputsA['condition']}")
                print("Condition invalid")
                
        ## Ensure pointsA and pointsB are not None
        if pointsA is None:
            print("Error: No data retrieved for Line A")
            return False
        
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

            
            
        ##Clear previous plots
        self.sc.axes.clear()
        
        ##Plot the graph
        self.sc.axes.plot(datesA, valuesA, label='Line A')
        ##Only plot lineB if the user has selected
        if lineB:
            self.sc.axes.plot(datesB, valuesB, label='Line B')
            
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
        
        
        self.sc.show()
        self.sc.draw()
        
        
##A class to handle validating user inputs  
class inputValidation:
    def __init__(self, Pstart_date, Pend_date):
        self.start_date = Pstart_date
        self.end_date = Pend_date
    
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

##A class to handle retrieving data from the flights database
##and weather API
class Retrieve_Data:
    def __init__(self):
        self.inputsA = self.data_options_A.getInputs()
        self.inputsB = self.data_options_B.getInputs()
        
    ##Retrieve the data from the flight database
    def retrieve_flights(self, A_or_B):
        ##Retrieve data with the parameters from the correct input
        if A_or_B == 'A':
            inputs = self.inputsA
        elif A_or_B == 'B':
            inputs = self.inputsB
        else:
            return False
        
        start_date = inputs['start_date'].toString("yyyy-MM-dd")
        end_date = inputs['end_date'].toString("yyyy-MM-dd")
        condition = inputs['condition']
        region = inputs['region']
        
        ##Use the lookup table in lookup_tables to convert the
        ##Drop Down titles into field headings
        lookupObject = lookup_tables()
        condition = lookupObject.conditionLookup[condition]
        
        ##Create an SQL query to retrieve this data from the db
        query = (f'''SELECT Date, [{condition}]
                    FROM flights
                    WHERE Region = '{region}' 
                    AND DateConverted BETWEEN '{start_date}' 
                    AND '{end_date}'
                    ORDER BY DateConverted ASC
                    ''')            
    
        ##Open the database temporarily ensuring it is closed when finished with
        with sqlite3.connect('MSA.db', timeout=30) as conn:
            ##Create an instance of cursor
            cursor = conn.cursor()
            ##Execute the query defined earlier
            cursor.execute(query)
            ##Fetch the data returned
            rows = cursor.fetchall()

            return rows
        
    ##A subroutine to retrieve historic weather data
    ##from the open-meteo API
    def retrieve_weather(self, A_or_B):
        ##Import the necessary libraries for the API
        import openmeteo_requests
        import requests_cache
        import pandas as pd
        from retry_requests import retry    
        
        ## Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        ##Retrieve data with the parameters from the correct input
        if A_or_B == 'A':
            inputs = self.inputsA
        elif A_or_B == 'B':
            inputs = self.inputsB
        else:
            return False
        
        start_date = inputs['start_date'].toString("yyyy-MM-dd")
        end_date = inputs['end_date'].toString("yyyy-MM-dd")
        condition = inputs['condition']
        region = inputs['region']
        
        
        ##Create an instance of lookup_tables
        lookupObject = lookup_tables()
        
        ##Get the coordinates of the users region
        regionCoord = lookupObject.region_lookup[region]
        
        ##Get the API request for the user's condition
        APIcondition = lookupObject.conditionLookup[condition]

        ##Set the URL of the API
        url = "https://archive-api.open-meteo.com/v1/archive"
        
        ##Set the parameters for the request
        params = {
            "latitude" : regionCoord[1],
            "longitude" : regionCoord[0],
            "start_date" : start_date,
            "end_date" : end_date,
            "hourly": APIcondition
        }
        
        responses = openmeteo.weather_api(url, params=params)

        # Process first location. Add a for-loop for multiple locations or weather models
        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()   
        condition = hourly.Variables(0).ValuesAsNumpy()               
        
        hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
            )
        }

        hourly_data["condition"] = condition

        hourly_dataframe = pd.DataFrame(data = hourly_data)
        
        averages = self.dailyAverage(hourly_dataframe)
        
        return averages
        
        
        
    ##Find daily average temp
    ##(Between 10:00 and 17:00)
    def dailyAverage(self, hourly_dataframe):
        averages = []
        ##Iterate through each day
        for i in range(0, len(hourly_dataframe), 24):
            sum = 0
            ##Iterate through each hour between 10:00 and 17:00
            for j in range(10, 18):
                ##Sum the values for each hour
                sum += hourly_dataframe.loc[i + j, "condition"]
                ##Convert the date to a string
                date_str = hourly_dataframe.loc[i, "date"].strftime("%Y-%m-%d")
                ##Add the date and average to an array
                averages.append([date_str, sum / 8])
            
            
        return(averages)
            
                
            

                
                
            
 
            
        
        

        
    
        

        
        


##Instantiate a QtApplication
app = QApplication(sys.argv)
##Set the active window to the main window we have been working with
window = View_Data_Window()
##Open the window maximized (Windowed FullScreen)
window.showMaximized()
##Run the application
sys.exit(app.exec())