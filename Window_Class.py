##To reduce memory load, each widget is imported seperately
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
)

##Define the Window class
class Window(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ##Set the window title
        self.__title = 'Meteorological Soaring Analysis'
        self.setWindowTitle(self.__title)
        
        self.button_count = 0
        self.label = QLabel('Click the button')
        
        button = QPushButton('Button')
        button.clicked.connect(self.button_clicked)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        layout.addWidget(button)
        layout.addWidget(self.label)
        
        self.show()
        
    def button_clicked(self,label):
        label = self.label
        print('clicked')
        self.button_count += 1
        text = 'Button Clicked ' + str(self.button_count) + ' times'
        label.setText(text)
        