import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt6.QtGui import QPixmap, QMouseEvent

class Clickable_Image(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Load and display the image
        self.pixmap = QPixmap(image_path)
        self.setPixmap(self.pixmap)
        # Ensures the image scales to the widget size
        self.setScaledContents(True) 
        
        #Function to call when image is clicked)
        self.subroutine = subroutine
        ##TODO: Subroutine to quit to main menu
    
    def on_click(self, event: QMouseEvent): ##Called when the image is clicked
        print("Image Clicked")
        if self.subroutine: ##Prevents an error if no subroutine is provided
            self.subroutine()  # Calls the provided subroutine

        

# Step 3: Run the PyQt6 application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())