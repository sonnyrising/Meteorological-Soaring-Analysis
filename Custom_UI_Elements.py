##Import the necessary libraries
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QWidget
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
)

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
                           font-size: 64px;
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
            font-size: 36px;
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