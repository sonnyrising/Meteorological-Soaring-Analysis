##Import the necessary libraries
import colorsys

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QWidget,
    QDateEdit,
    QComboBox,

)
from PyQt6.QtGui import ( 
    QIcon,
    QPixmap,
    QPalette,
    QColor,
)

from PyQt6.QtCore import (
    Qt,
    QSize,
    QDate,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

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
        
class Image_Button(QPushButton):
    def __init__(self, image_path, subroutine):
        super().__init__()
        self.image_path = image_path
        self.subroutine = subroutine
        self.setIcon(QIcon(self.image_path))
        self.setIconSize(QSize(120,120))
        self.clicked.connect(self.subroutine)
        self.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding,
            QSizePolicy.Policy.MinimumExpanding)
        self.setStyleSheet("background-color: ; border: #95d1ff;")
        
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
        
        ##Use QSS (A form of CSS) to style the title text
        self.setStyleSheet("""color: black;
                           font-size: 42px;
                           font-family: calibri;
                           """)
        
##Same as title but smaller font size
class SubTitle(QLabel):
    
    def __init__(self, text, font_size):
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
        
        ##Use QSS (A form of CSS) to style the title text
        self.setStyleSheet(f"""color: black;
                           font-size: {font_size}px;
                           font-family: calibri;
                           """)
##A class for custom buttons
class Menu_Button(QPushButton):
    
    def __init__(self, text, color, subroutine):
        super().__init__(text)  
        ##Set the button color using QSS
        
        ##Increase the hue of the color passed in by 0.2
        hover_color = increase_hue(color, 0.2)
        
        ##Set the stylesheet of the button using QSS
        self.setStyleSheet(f"""
        QPushButton {{
            color: black;
            background-color: {color}; 
            border: 1px solid black;
            font-size: 24px;
        }}
        QPushButton:hover {{
            background-color: {hover_color};
        }}
        """)
        
        ##The button runs the subroutine passed as an argument
        self.clicked.connect(subroutine)
        
        ##Sets the button to fit the container it was placed in
        self.setSizePolicy(
        QSizePolicy.Policy.MinimumExpanding,
        QSizePolicy.Policy.MinimumExpanding)
        
##!AI WRITTEN CODE STARTS HERE
##Converts the hex value passed to the button class into RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

##Converts the RGB value created by the hex_to_rgb function back into hex
def rgb_to_hex(rgb_color):
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

##Increases the hue of the color passed in by a given increment
def increase_hue(hex_color, increment):
    # Convert hex to RGB
    r, g, b = hex_to_rgb(hex_color)

    # Convert RGB to HSV
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)

    # Increase the hue
    h = (h + increment) % 1.0

    # Convert HSV back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r, g, b = int(r * 255), int(g * 255), int(b * 255)

    # Convert RGB back to hex
    return rgb_to_hex((r, g, b))
##! AI WRITTEN CODE ENDS HERE

class data_options(QWidget):
    def __init__(self, title):
        super().__init__()
        
        ##Create a layout for the data options
        layout = QVBoxLayout()
        layout.setSpacing(0)

        ##Create a widget to contain the inputs for graph A
        graph_widget = QWidget()
        graph_widget.setStyleSheet("background-color: transparent;")
        graph_layout = QVBoxLayout()
        graph_layout.setSpacing(5)
        
        ##Create a subtitle indicating these inputs are for graph A
        graph_title = SubTitle(title, 48)
        graph_title.setMaximumSize(60, 100)
        graph_title.setStyleSheet("background-color: purple;")
        graph_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        ##Create instantiations of each user input widget
        self.start_input = date_input("start")
        self.end_input = date_input("end")
        self.region_input = drop_down_menu("region", "view")
        self.condition_input = drop_down_menu("condition", "view")
        
        #Add each widget to the layout
        graph_layout.addWidget(graph_title)
        graph_layout.addWidget(self.start_input)
        graph_layout.addWidget(self.end_input)
        graph_layout.addWidget(self.region_input)
        graph_layout.addWidget(self.condition_input)

        ##Set the layout for the widget
        self.setLayout(graph_layout)
     
    ##A getter method to retrieve the inputs from the data options widget 
    ##In the form of a dictionary 
    def getInputs(self):
        return {
            "start_date" : self.start_input.getDate(), 
            "end_date" : self.end_input.getDate(), 
            "region" : self.region_input.getOption(), 
            "condition" : self.condition_input.getOption(),
        }

##A custom date input widget which adds the relevant subtitle
class date_input(QWidget):
    def __init__(self, start_end):
        super().__init__()
        
        ##Signal if this date input is for the start or end date
        if start_end == "start":
            title = "Start Date"
        elif start_end == "end":
            title = "End Date"
        else:
            print ("Incorrect start/end parameter")
            
        ##Create a layout to contain the date input
        date_input_layout = QVBoxLayout()
        date_input_layout.setSpacing(10)
        
        subtitle = SubTitle(title, 18)
        subtitle.setMaximumSize(225, 60)
        ##Create a widget for user to enter start date
        self.date_input = QDateEdit(self)
        ##The data starts at 01/01/2010 so don't allow dates before this
        self.date_input.setMinimumDate(QDate(2010, 1, 1))
        ##The data ends at 31/12/2024 so don't allow dates after this
        self.date_input.setMaximumDate(QDate(2024, 12, 31))
        ##Set geometry of the date edit
        self.date_input.setMaximumSize(225,60)
        ##Set the styling of the date input
        self.date_input.setStyleSheet("font-size: 14px;")
        ##Set the format of the date to match SQL Standard
        self.date_input.setDisplayFormat("dd-MM-yyyy")
        
        ##Add the subtitle and date input to the layout
        date_input_layout.addWidget(subtitle)
        date_input_layout.addWidget(self.date_input)
        
        ##Set the layout for the widget
        self.setLayout(date_input_layout)
        
    def getDate(self):
        return self.date_input.date()

##A custom drop down menu widget which adds the relevant subtitle
class drop_down_menu(QWidget):
    def __init__(self, region_condition, view_analyse):
        
        super().__init__()
        
        ##Import the python file storing drop down options
        from Drop_Down_Options import options
        
        ##Create an instance of the options class to take the options from
        options = options()
        
        ##Create a list of regions and their corresponding gliding clubs
        region_glidingClub = []
        ##Iterate through the regions and append the corresponding gliding club to the string
        for i in range(len(options.regions)):
            region_glidingClub.append(options.regions[i] + " - " + options.gliding_clubs[i])
            
        ##Signal whether this drop down if for region or condition
        if region_condition == "region":
            self.title = "Region:"
            drop_down_options = options.regions
        elif region_condition == "condition":
            if view_analyse == "view":
                self.title = "Condition:"
                drop_down_options = options.view_data_conditions
            elif view_analyse == "analyse":
                self.title = "Condition:"
                drop_down_options = options.analyse_data_conditions
            else:
                print("Incorrect view_analyse parameter")
        else:
            print("Incorrect region_condition parameter")
        

        ##Create a layout to contain the drop down menu
        drop_down_layout = QVBoxLayout()
        drop_down_layout.setSpacing(10)
        
        ##Create a subtitle for the drop down menu
        subtitle = SubTitle(self.title, 18)
        subtitle.setMaximumSize(225, 60)
        
        ##Indicate whether this window is for the view data or analyse data window
        if view_analyse == "view":
            if region_condition == "region":
                drop_down_options = region_glidingClub
            else:
                drop_down_options = options.view_data_conditions
        elif view_analyse == "analyse":
            if region_condition == "region":
                drop_down_options = options.regions
            else:
                drop_down_options = options.analyse_data_conditions
        else:
            print("Incorrect view_analyse parameter")
        
        ##Create a drop down menu
        self.drop_down = QComboBox()
        ##Add the options to the drop down menu
        self.drop_down.addItems(drop_down_options)
        ##Set the dimensions of the drop down
        self.drop_down.setMaximumSize(225, 60)
        ##Set the styling of the drop down
        self.drop_down.setStyleSheet("font-size: 14px;")
        
        ##Add the subtitle and drop down menu to the layout
        drop_down_layout.addWidget(subtitle)
        drop_down_layout.addWidget(self.drop_down)
        
        ##Set the layout for the widget
        self.setLayout(drop_down_layout)
        
    def getOption(self):
        return self.drop_down.currentText()
    
class error_message(QDialog):
    def __init__(self, error1, error2):
        super().__init__()
        
        self.setWindowTitle("Error")
        
        layout = QVBoxLayout()
        
        error = QLabel("Error")
        error.setStyleSheet("font-size:20; color:red")
        layout.addWidget(error)
        
        label1 = QLabel(error1)
        layout.addWidget(label1)
        
        label2 = QLabel(error2)
        layout.addWidget(label2)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        self.setLayout(layout)

##A class to contain the graph created by MPL (Matplotlib)
class MplCanvas(FigureCanvasQTAgg):
    ##Set the dimensions of the graph
    def __init__(self, parent = None, width = 6, height = 3.5, dpi = 100):
        ##Create an instance of a figure (graph) with the
        ##Passed dimensions
        fig = Figure(figsize=(width, height), dpi=dpi)
        
        ##Add a subplot
        ##111 represents 1 row, 1 column, 1st subplot
        self.axes = fig.add_subplot(111)
        
        ##Instantiate the FigureCanvas using the figure we created
        super().__init__(fig)
        
        
        
##A class for the inputs for the analyse data window
class analyse_options(QWidget):
    def __init__(self, view_analyse):
        super().__init__()
        
        ##Create a layout for the data options
        layout = QVBoxLayout()
        layout.setSpacing(0)

        ##Create a widget to contain the inputs for graph A
        graph_widget = QWidget()
        graph_widget.setStyleSheet("background-color: transparent;")
        graph_layout = QVBoxLayout()
        graph_layout.setSpacing(5)
        
        
        ##Create instantiations of each user input widget
        self.start_input = date_input("start")
        self.end_input = date_input("end")
        self.region_input = drop_down_menu("region", "analyse")
        self.condition_input = drop_down_menu("condition", "analyse")

        
        #Add each widget to the layout
        graph_layout.addWidget(self.start_input)
        graph_layout.addWidget(self.end_input)
        graph_layout.addWidget(self.region_input)
        graph_layout.addWidget(self.condition_input)

        ##Set the layout for the widget
        self.setLayout(graph_layout)
     
    ##A getter method to retrieve the inputs from the data options widget 
    ##In the form of a dictionary 
    def getInputs(self):
        return {
            "start_date" : self.start_input.getDate(), 
            "end_date" : self.end_input.getDate(), 
            "region" : self.region_input.getOption(), 
            "condition" : self.condition_input.getOption(),
        }

    

        
        
        
    
        
        
        
