##Numpy for mathematical functions
import numpy as np

##SkLearn used to calculate r^2 values for line of best fit
from sklearn.metrics import r2_score

from scipy.optimize import (
    minimize_scalar,
    fsolve
)


class Maths_Functions:
    def __init__(self):
        pass
        
    def regression(self, merged_df, x_values, y_values):
        
        ##First quartile (low 25%)
        Q1 = x_values.quantile(0.25)
        ##Third quartile (top 25%)
        Q3 = x_values.quantile(0.75)
        ##Interquartile range
        IQR = Q3 - Q1

        ##Define outlier limits
        lower_bound = Q1 - (0.75 * IQR)
        upper_bound = Q3 + (0.75 * IQR)
        print(f"Lower bound: {lower_bound}")
        print(f"Upper bound: {upper_bound}")

        ##Remove outliers
        filtered_df = merged_df[(x_values >= lower_bound) & (x_values <= upper_bound)]
        
        ##Calculate the percentage of data removed
        percentage_removed = (1 - len(filtered_df) / len(merged_df)) * 100
        print(f"Percentage of data removed: {percentage_removed:.2f}%")

        x_values = filtered_df['points']
        y_values = filtered_df['score']
        self.x_min = x_values.min()
        self.x_max = x_values.max()
        self.x_range = filtered_df['points'].max() - filtered_df['points'].min()
        
        ##Iterate hrough degrees of polynomial to find the best fit
        ##Iterate from 1 to 5
        r_squared_values = {}
        rmse_values = {}
        fit_rating_values = {}
        for i in range(1, 10):
            ##Calculate the equation of the line using the polyfit method of numpy
            coefficients = np.polyfit(x_values, y_values, i)
            poly = np.poly1d(coefficients)
            y_fit = poly(x_values)
            
            ##Calculate the R² value
            r_squared = r2_score(y_values, y_fit)
            print(f"Degree: {i}")
            print(f"R²: {r_squared}")
            
            ##Calculate difference between predicted y and observed y
            errors = y_values - y_fit
            ##Calculate the root mean square of the error
            rmse = np.sqrt(np.mean(errors ** 2))
            print(f"RMSE: {rmse}")
            
            ##Calculate the r^2 as a percentage where 100% is best
            r_squared_percent = (r_squared) * 100
            
            ##Calculate the normalised rmse (NRMSE) by dividing by the range of y values
            y_values_range = y_values.max() - y_values.min()
            nrmse = rmse / y_values_range
            ##Convert nrmse to a percentage
            nrmse_percent = (1-nrmse) * 100

            print(f"R² Percent: {r_squared_percent}%")
            print(f"NRMSE Percent: {nrmse_percent}%")
            
            ##Create a measure of how well the line of best fit fits the data
            ##Using both RMSE and R²
            ##With a weighting towards RMSE
            fit_rating = (0.7*r_squared_percent) + (nrmse_percent)
            print()
            print(f"Degree: {i}")
            print(f"Fit Rating: {fit_rating}")
            print()
            
            ##Add the r^2 value to a dictionary with the degree of polynomial as the key
            r_squared_values[i] = r_squared
            rmse_values[i] = rmse
            fit_rating_values[i] = fit_rating
        
        ##Choose the best fitting degree of polynomial
        best_fit_rmse = min(rmse_values, key=rmse_values.get)
        print(f"Best rmse: {best_fit_rmse}")
        best_fit_r_squared = max(r_squared_values, key=r_squared_values.get)
        print(f"Best r^2: {best_fit_r_squared}")
        best_fit_rating = max(fit_rating_values, key=fit_rating_values.get)
        print(f"Best fit rating: {best_fit_rating}")
        

        ##Calculate the line of best fit using the best fitting degree of polynomial
        ##Calculated using root mean square error
        coefficients_rmse = np.polyfit(x_values, y_values, best_fit_rmse)
        y_fit_rmse = np.poly1d(coefficients)(x_values)
        equation_rmse = np.poly1d(coefficients)
        
        ##Calculate the line of best fit using the best fitting degree of polynomial
        ##Calculated using r^2
        coefficients_r_squared = np.polyfit(x_values, y_values, best_fit_r_squared)
        y_fit_r_squared = np.poly1d(coefficients)(x_values)
        equation_r_squared = np.poly1d(coefficients)
        
        ##Calculate the line of best fit using the best fitting degree of polynomial
        ##Calculated using the fit rating
        coefficients_fit_rating = np.polyfit(x_values, y_values, best_fit_rating)
        y_fit_fit_rating = np.poly1d(coefficients)(x_values)
        equation_fit_rating = np.poly1d(coefficients)
        
        ## Ensure x_values and y_fit have the same length
        if len(x_values) != len(y_fit):
            print("Error: x_values and y_fit have different lengths")
            return False
        
        ##Create a dictionary containing the values for each line of best fit
        lines_of_best_fit ={
            'x_values' : x_values,
            'r_squared' : (y_fit_r_squared, equation_r_squared),
            'rmse' : (y_fit_rmse, equation_rmse),
            'fit_rating' : (y_fit_fit_rating, equation_fit_rating)
        }
        
        return (lines_of_best_fit)
    
    
    ##Convert the numpy equation object to a string
    def numpy_to_strings(self):
        self.equation = str(self.equation_numpy)
    
    
    ##Differentiate the equation
    def differentiate(self, equation):
        ##Use the deriv() function of the numpy object to differentiate the equation
        differentiated_equation = equation.deriv()
        
        return differentiated_equation
    
    ##Calculate maximum and minimum values
    def max_and_min_diff(self, equation):
        ##First derivative
        first_derivative = self.differentiate(equation)

        ##Second derivative
        second_derivative = self.differentiate(first_derivative)

        ##Find critical points by solving the first derivative equal to zero
        critical_points = fsolve(first_derivative, np.linspace(-10, 10, 100))

        ##Remove duplicates by rounding to a reasonable precision
        critical_points = np.unique(np.round(critical_points, decimals=8))

        ##Evaluate the second derivative at each critical point
        maxima = []
        minima = []
        for point in critical_points:
            second_derivative_at_point = second_derivative(point)
            if second_derivative_at_point < 0:
                maxima.append((point, equation(point)))
            elif second_derivative_at_point > 0:
                minima.append((point, equation(point)))
            else:
                print(f"Point {point} is a point of inflection")
                
        ##Return results
        if len(maxima) == 0:
            print("No maximums found")
        if len(minima) == 0:
            print("No minimums found")
        for point, value in maxima:
            print(f"Maximum at x = {point}, value = {value}")
        for point, value in minima:
            print(f"Minimum at x = {point}, value = {value}")
            
        return maxima, minima
    
    ##Find maximum and minimum values using Numerical Optimisation
    def max_and_min_opt(self, equation):
        
        ##Define the function to be minimised
        def f(x):
            return equation(x)
        
        ##Calculate the minimum value within a range
        minimum = minimize_scalar(
            f,
            bounds = (self.x_min, self.x_max),
            method = 'bounded')
        
        ##Calculate the maximum value within th range of the line of best fit
        ##By minimising the negative of the equation
        maximum = minimize_scalar(
            lambda x: -f(x),
            bounds = (self.x_min, self.x_max),
            method = 'bounded')
        
        
        return minimum, maximum
        
        

    