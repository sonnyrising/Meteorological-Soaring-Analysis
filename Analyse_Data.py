import sys

##Import classes from my own custom UI Elements
from Custom_UI_Elements import (
    Menu_Button,
    Image_Button,
    Conf_Dialogue,
    Title,
    SubTitle,
    analyse_options,
    MplCanvas,
)

##PyQt Widgets
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

##PyQt GUI Element (used for images)
from PyQt6.QtGui import QIcon

##Used to plot graphs with matplotlib
from matplotlib.ticker import MaxNLocator

##Integrates matplotlib with PyQt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

##Mehtods to retrieve data from database /api and input validation
from MSA_Utils import (
    Retrieve_Data,
    input_validation,
)
##Mathematical functions from my own custom class
from Maths_Functions import (
    Maths_Functions
)

##Used for some data manipulation
import pandas as pd

class Analyse_Data_Window(QMainWindow):

    def __init__(self):
        ##Inherits from QMainWindow, the window class from the PyQt library
        super().__init__()

        self.setWindowTitle("Meteorological Soaring Analysis")
        self.setWindowIcon(QIcon("logo.png"))
        
        ##Instantiate both layouts as a widget
        main_widget = QWidget()
        
        ##Creates the title bar using the custom title class
        title_bar = Title("Meterological Soaring Analysis")
        title_bar.setMaximumHeight(60)
        
        ##Creates the subtitle bar using the custom subtitle class
        ##Slightly smaller than the title bar
        subtitle_bar = SubTitle("Analyse Data", 36)
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
        self.data_options = analyse_options("analyse")
        left_third_layout.addWidget(self.data_options)

        
        ##Add a button to create the graph
        plot_button = Menu_Button(
            text = 'Plot Graph',
            color = '#7ED941',
            subroutine = self.plot_graph
        )

        ##Set the maximum size of the plot button
        plot_button.setMaximumSize(200, 30)
        
        ##Create a layout to hold all of the inputs
        left_third_layout.addWidget(plot_button)
        
        ##Add the user inputs held on the left of the screen
        main_contents_layout.addLayout(left_third_layout)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot([12, 45, 106, 15, 24], [10,1,20,3,40])
        self.sc.hide()

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
          
    def get_data(self):
        ##Use the getter method from the data options to retrieve user inputs
        ##A dictionary is returned with the keys being the input type
        self.inputsA = self.data_options.getInputs()
        
        ##Extracts start and end dates from the dictionary
        start_dates = [self.inputsA["start_date"]]
        end_dates = [self.inputsA["end_date"]]
        
        ##Create an instance of the data validation class for inputs A
        validateA = input_validation(start_dates[0], end_dates[0])
        
        #Only plot the graph if the date inputs are valid
        if validateA.validate_date() != True:
            return(False)
            self.validation = "failed"
            print(self.validation)
        else:
            self.validation = "passed"
            print(self.validation)
        
        ##Create an instance of data retrieval to access the user selected condition
        retriever = Retrieve_Data(
            data_options_A = self.data_options,
            data_options_B = None,
            view_data = False
            )
        
        print(self.data_options.getInputs())
        
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
        
        ## Initialize pointsA to None
        points = None
        
        ##Use the data retrieval class to access the weather data
        ##THis returns an array of tuples containing the date and value
        points = retriever.retrieve_weather('A')
        print("weather")
        print(f"Points A accessed \n Length: {len(points)}")
        
        ##Convert the array of tuples into a dictionary
        points = {date: value for date, value in points}
        
        
        ##Ensure the points have been retrieved
        if points is None:
            print("Error: No data retrieved for Line A")
            return False
        
        ##Access the users inputs
        start_date = self.data_options.getInputs()['start_date']
        end_date = self.data_options.getInputs()['end_date']
        region = self.data_options.getInputs()['region']
        
        ##Create a class that holds the inputs for the score retrieval
        class score_retrieval:
            def __init__(self, start_date, end_date, region):
                self.score_retrieval_dict = {
                    'start_date': start_date,
                    'end_date': end_date,
                    'region': region,
                    'condition': 'Total Score'
                }
            
            def getInputs(self):
                return self.score_retrieval_dict
            
        ##Create an instance of the score retrieval class
        score_retrieval_instance = score_retrieval(start_date, end_date, region)
            
        ##Create a new retriever object to access the score
        ##using the new dictionary
        score_retriever = Retrieve_Data(
            data_options_A = score_retrieval_instance,
            data_options_B = None,
            view_data = False
        )
        
        ##Retrieve the score using the retriever object
        ##This returns an array of tuples with the date and score
        score = score_retriever.retrieve_flights('A')
        print(f"Score accessed \n Length: {len(score)}")
        
        ##Convert the array of tuples into a dictionary
        score = {date: value for date, value in score}
        
        ##Convert the score and condition dictionary to a pandas dataframe
        points_df = pd.DataFrame(list(points.items()), columns=["date", "points"])
        score_df = pd.DataFrame(list(score.items()), columns=["date", "score"])
        
        
        ##Merge the two dataframes on the date
        ##Merging on 'date' to get only matching entries
        ##This ensures that every value datapoint has a corresponding score
        merged_df = pd.merge(points_df, score_df, on="date", how="inner")
        
        ##Check the dataframe isn't 0
        ##To prevent division by 0
        if merged_df.empty:
            print("Merged DF Empty")
            return False
        
        
        ##Sort the merged dataframe by the condition
        merged_df = merged_df.sort_values(by="points")
        
        ##Convert columns to numeric values, if they aren't already
        merged_df['points'] = pd.to_numeric(merged_df['points'], errors='coerce')
        merged_df['score'] = pd.to_numeric(merged_df['score'], errors='coerce')

        ##Drop any rows where the conversion failed
        merged_df = merged_df.dropna()
        
        x_values = merged_df['points']
        y_values = merged_df['score']
        
        return (x_values, y_values, merged_df)

    def plot_graph(self):
        ##Use the get_data method to retrieve the data
        retrieved_data = self.get_data()
        if self.get_data() == False:
            print("Validation Failed")
            return(False)
        
        ##Access the data points from the retrieved data array
        self.x_values = retrieved_data[0]
        y_values = retrieved_data[1]
        merged_df = retrieved_data[2]
        
        ##An instance of the maths_functions class
        functioner = Maths_Functions()
        
        ##Use the regression method to calculate the line of best fit
        regression_results = functioner.regression(merged_df, self.x_values, y_values)
        
        ##Retrieve the equations for each line of best fit
        equation_r_squared = regression_results['r_squared'][1]
        equation_rmse = regression_results['rmse'][1]
        equation_fit_rating = regression_results['fit_rating'][1]
        
        ##Check if all measures of fit are equal
        if equation_r_squared == equation_rmse == equation_fit_rating:
            print("All equations are equal")
            self.equation = equation_fit_rating
            
        ##Else choose the equation with the highest fit rating
        else:
            self.equation = equation_fit_rating
        
        
        ##Clear previous plots
        self.sc.axes.clear()
        
        ##Plot the points as a scatter graph with reduced opacity
        self.sc.axes.scatter(
            merged_df['points'],
            merged_df['score'],
            label = self.inputsA['condition'],
            color='blue',
            alpha=0.5      
        )
        
        ##Plot a line of best fit using the data points used to create the line of best fit with r^2
        self.sc.axes.plot(
            regression_results['x_values'],
            regression_results['r_squared'][0],
            label='R Squared',
            color='blue',
            linewidth=2
        )
        
        ##Plot a line of best fit using the data points used to create the line of best fit with rmse
        self.sc.axes.plot(
            regression_results['x_values'],
            regression_results['rmse'][0],
            label='RMSE',
            color='pink',
            linewidth=2
        )
        
        ##Plot a line of best fit using the data points used to create the line of best fit with rmse
        self.sc.axes.plot(
            regression_results['x_values'],
            regression_results['fit_rating'][0],
            label='Fit Rating',
            color='red',
            linewidth=2
        )

            
        ##Rotate the x axis label by 45 degrees
        self.sc.axes.set_xticklabels(self.sc.axes.get_xticklabels(), rotation=45, ha='right')
        
        ##Reduce size
        self.sc.axes.tick_params(axis='x', which='major', labelsize=10)
        
        ##Control the number of ticks on the y-axis
        self.sc.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        ##Set the y axis label
        self.sc.axes.set_ylabel('Total Score')
        
        ##Adjust the bottom margin to ensure the labels are visible
        self.sc.figure.subplots_adjust(bottom=0.2)
        

        ##Set the x axis label
        self.sc.axes.set_xlabel(
            self.inputsA['condition'] +' - ' + '(' + self.inputsA['region'] + ')'
        )
        
        ##Set the legend
        self.sc.axes.legend([
            self.inputsA['condition'] +' - ' + '(' + self.inputsA['region'] + ')'
        ]
            )
            
        ##Make the graph visible
        self.sc.show()
        
        ##Draw the graph
        self.sc.draw()
        
        
    def calculate_info(self):
        ##An instance of the maths_functions class
        functioner = Maths_Functions()
        
        ##Use the maths functions to find the minimum and maximum values
        ##Using both optimisation and differentiation
        
        ##Calculate the minimum and maximum values using optimisation
        minimum_opt = functioner.max_and_min_opt(self.equation)[0]
        maximum_opt = functioner.max_and_min_opt(self.equation)[1]
        print(f"Minimum Value from Optimisation: {minimum_opt.fun} at x {minimum_opt.x}")
        print(f"Maximum Value from Optimisation: {-maximum_opt.fun} at x {maximum_opt.x}")
        
        ##Calculate the minimum and maximum values using differentiation
        minimum_diff= functioner.max_and_min_diff(self.equation)[0]
        maximum_diff = functioner.max_and_min_diff(self.equation)[1]
         
##Instantiate a QtApplication
app = QApplication(sys.argv)
##Set the active window to an instance of this class
view_data_window = Analyse_Data_Window()
##Open the window maximized (Windowed FullScreen)
view_data_window.showMaximized()
##Ensures the app closes properly
sys.exit(app.exec())