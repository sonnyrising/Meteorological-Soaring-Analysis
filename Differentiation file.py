import numpy as np

class Maths_Functions:
    def __init__(self, equation):
        self.equation = equation
    
    def format_equation(self):
        ##Remove the spaces
        self.equation = self.equation.replace(" ", "")
        
        ##Split the string into a list of terms
        ##Add a unique character to the end of each term
        ##to be able to split the string
        self.equation = self.equation.replace("x", "xi")
        ##Split the string by unique character
        self.equation = self.equation.split("i")
        
        print(f"Split Equation: {self.equation}")
        return(self.equation)
        

    
functioner = Maths_Functions()
functioner.format_equation()