##Used to query the database
import sqlite3

##Converts text in drop down menu to database / api headings
from lookup_tables import lookup_tables

##Used to ensure dates are in correct format for matplotlib
from datetime import(
    datetime,
)

from Custom_UI_Elements import (
    error_message
)

##A class to handle validating user inputs  
class input_validation:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
    
    def validate_date(self):
        ##Due to the QDateEdit widget, the date is already in the correct format
        ##Minimum and maximum dates are set by the QDateEdit widget so dont need to be validated
        
        ##Check if dates are in the correct order
        ##ie cant end before it starts
        if self.start_date  < self.end_date:
            return(True)
        
        ##Check if the start date is before the end date
        elif self.start_date > self.end_date:
            ##Trigger a popup
            popup = error_message("Error in Date Input", "End Date before Start Date")
            popup.exec()
            ##Return an appropriate error message
            return "end_date before start_date"
        
        ##Check if the start date is the same as the end date
        else:
            ##Trigger a popup
            popup = error_message("Error in Date Input", "End Date equal to Start Date")
            popup.exec()
            ##Return an appropriate error message
            return "start_date = end_date"

##A class to handle retrieving data from the flights database
##and weather API
class Retrieve_Data:
    def __init__(self, data_options_A, data_options_B, view_data):
        ##Retrieve user inputs from the inputs widet
        self.inputsA = data_options_A.getInputs()
        ##Only retrieve inputs from the second line if it is needed
        if view_data:
            self.inputsB = data_options_B.getInputs()

        ##Arrays to check whether a condition is for flight or weather
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
        
    ##Retrieve the data from the flight database
    def retrieve_flights(self, A_or_B):
        ##Retrieve data with the parameters from the correct input
        if A_or_B == 'A':
            inputs = self.inputsA
        elif A_or_B == 'B':
            inputs = self.inputsB
        else:
            return False
        
        ##Convert dates from QDates to strings in the correct format
        start_date = inputs['start_date'].toString("yyyy-MM-dd")
        end_date = inputs['end_date'].toString("yyyy-MM-dd")
        
        condition = inputs['condition']
        region = inputs['region']
        
        ##Use the lookup table in lookup_tables to convert the
        ##Drop Down titles into field headings
        lookupObject = lookup_tables()
        condition = lookupObject.conditionLookup[condition]
        
        ##Create an SQL query to retrieve this data from the db
        ##Retrieve the average value of each day
        query = (f'''SELECT DateConverted, AVG([{condition}]) 
                FROM flights
                WHERE Region = '{region}' 
                AND DateConverted BETWEEN '{start_date}' 
                AND '{end_date}'
                GROUP BY DateConverted
                ORDER BY DateConverted ASC
                ''')      
        
        print(f"Making query \n query: {query}")      
    
        ##Open the database temporarily ensuring it is closed when finished with
        with sqlite3.connect('MSA.db', timeout=30) as conn:
            ##Create an instance of cursor
            cursor = conn.cursor()
            ##Execute the query defined earlier
            cursor.execute(query)
            ##Fetch the data returned
            rows = cursor.fetchall()
            
            ## Convert the date format from dd-mm-yyyy to yyyy-mm-dd
            formatted_rows = []
            ##Iterate through the query result
            for row in rows:
                #Use the datetime module to convert each row to YYYY-MM-DD
                date = datetime.strptime(row[0], "%d-%m-%Y").strftime("%Y-%m-%d")
                ##Add the formated rows to the new array
                formatted_rows.append((date, row[1]))
                
            print(f"Data Accessed \n length: {len(formatted_rows)}")

            ##Return the sql query result with correctly formated dates
            return formatted_rows
        
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
        
        ##Access user inputs
        ##Convert dates from QDates to strings in the correct format
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
        
        ##Make the api request
        responses = openmeteo.weather_api(url, params=params)

        ##Only one response is returned as only one request is made
        response = responses[0]
        
        ##Print information about the data for debugging
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        ##All returned data is hourly (rather than daily)
        ##So we only need to access the hourly attribute
        hourly = response.Hourly()
        ##Convert to a numpy array
        condition = hourly.Variables(0).ValuesAsNumpy()               
        
        ##Create a dictionary with the time for each datapoint
        hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
            )
        }

        ##Add the values of the requested condition to the dictionary
        hourly_data["condition"] = condition
        print(f"Hourly Data Accessed \n length: {len(hourly_data['condition'])}")

        ##Convert the dictionary to a pandas dataframe
        ##The df is more human readable for debugging
        hourly_dataframe = pd.DataFrame(data = hourly_data)
        
        ##Convert hourly data into daily averages
        averages = self.dailyAverage(hourly_dataframe)
        print(f"Averages found \n length: {len(averages)}")
        
        ##Return these averages
        return averages
        
        
        
    ##Find daily average temp from hourly data
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
                ##*(Must be in YYYY-MM-DD format to support plot_graph)
                date_str = hourly_dataframe.loc[i, "date"].strftime("%Y-%m-%d")
            ##Add the date and average to an array
            averages.append([date_str, sum / 8])
            
        ##Return the array in a format supported by the plot_graph subroutine
        return(averages)
    
    
    ##When plotting 2 dissimilar conditions data must be normalised
    def normaliseData(self, valuesA, valuesB, inputsA, inputsB):
        ##Find ranges for both inputs
        if inputsA["condition"] in self.flight_data:
            ##If the condition is flight data the database must be queried
            conditionA_range = self.find_range_sql(inputsA)
        else:
            ##If the condition is weather data an API request is needed
            conditionA_range = self.find_range_api(inputsA)
        
        ##Repeat for condition B
        if inputsB["condition"] in self.flight_data:
            conditionB_range = self.find_range_sql(inputsB)
        else:
            conditionB_range = self.find_range_api(inputsB)
            
            
            
                    
        ##For each data point, convert it to a percentage of that condition's range
        ##Use error checking since some values from the db may return Null
        ##Iterate through the values
        for i in range(len(valuesA)):
            ##If no error is produced
            try:
                ##Convert tuple to list so it can be changed
                valuesA[i] = list(valuesA[i])
                ##Convert the data point to a percentage of its range
                valuesA[i][1] = (float(valuesA[i][1]) / conditionA_range) * 100
                
            ##If an error is produced (Null value in db)
            except ValueError as e:
                ##Print for debugging
                print(f"Skipping invalid data point in valuesA: {valuesA[i]} - {e}")
                ##Continue with the program
                continue
        
        ##Repeat for valuesB
        for i in range(len(valuesB)):
            try:
                valuesB[i] = list(valuesB[i])  # Convert tuple to list
                valuesB[i][1] = (float(valuesB[i][1]) / conditionB_range) * 100
            except ValueError as e:
                print(f"Skipping invalid data point in valuesB: {valuesB[i]} - {e}")
                continue
        
        ##Return the normalised values as a tuple
        values = (valuesA, valuesB)
        return values
            
    ##Find the maximum rage of a condition in the db
    def find_range_sql(self, inputs):
        condition = inputs["condition"]
        ##Convert to the column heading used in the db
        lookup_object = lookup_tables()
        condition = lookup_object.conditionLookup[condition]

        ##SQL Query to find the range of values for that condition for the whole country from 2010 to 2024
        query = (f'''SELECT
                    MAX(CAST("{condition}" AS REAL)) AS max_value, 
                    MIN(CAST("{condition}" AS REAL)) AS min_value
                    FROM flights
                    WHERE DateConverted BETWEEN '2010-01-01' AND '2024-12-31';''')
        
        ##Print query for debugging
        print(f"Executing query: {query}")
        
        ##Open the database temporarily ensuring it is closed when finished with
        with sqlite3.connect('MSA.db', timeout=30) as conn:
            ##Create an instance of cursor
            cursor = conn.cursor()
            ##Execute the query defined earlier
            cursor.execute(query)
            ##Fetch the data returned
            row = cursor.fetchone()
            
        ##Must return None if either row is None
        ##Contuining with a None value will lead to division by 0
        if row is None or row[0] is None or row[1] is None:
            ##Print for debugging
            print("Error: No data found ")
            return None
        
        ##Set the max and minimum values
        maxValue = row[0]
        minValue = row[1]

        ##Calculate range
        range_value = maxValue - minValue

        ##Must return None if range is 0
        ##To prevent division by 0 error
        if range_value == 0:
            print("Error: Range = 0")
            return None
        else:
            ##If the range isn't 0 it can be returned
            return range_value
            
            
    def find_range_api(self, inputs):
        ##Import the necessary libraries for the API
        import openmeteo_requests
        import requests_cache
        import pandas as pd
        from retry_requests import retry    
        
        ## Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)
        
        condition = inputs["condition"]
        region = inputs["region"]
        ##Convert to the column heading used in the db using the lookup table
        lookupObject = lookup_tables()
        condition = lookupObject.conditionLookup[condition]
        
        ##Get the coordinates of the users region using the lookup table
        regionCoord = lookupObject.region_lookup[region]

        ##Set the URL of the API
        url = "https://archive-api.open-meteo.com/v1/archive"
        
        ##Set the parameters for the request
        params = {
            "latitude" : regionCoord[1],
            "longitude" : regionCoord[0],
            "start_date" : "2010-01-01",
            "end_date" : "2024-12-31",
            "hourly": condition
        }
        
                ##Make the api request
        responses = openmeteo.weather_api(url, params=params)

        ##Only one response is returned as only one request is made
        response = responses[0]
        
        ##Print information about the data for debugging
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        ##All returned data is hourly (rather than daily)
        ##So we only need to access the hourly attribute
        hourly = response.Hourly()
        ##Convert to a numpy array
        condition = hourly.Variables(0).ValuesAsNumpy()               
        
        ##Create a dictionary with the time for each datapoint
        hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
            )
        }

        ##Add the values of the requested condition to the dictionary
        hourly_data["condition"] = condition

        ##Convert the dictionary to a pandas dataframe
        ##Pandas allows us to use .max() and .min()
        hourly_dataframe = pd.DataFrame(data = hourly_data)        

        #Find the lowest and highest value of the condition
        min_value = hourly_dataframe["condition"].min()
        max_value = hourly_dataframe["condition"].max()
        
        ##Find the range
        condition_range = max_value - min_value
        
        ##If the range isn't 0 return the range
        if condition_range != 0:     
            return condition_range
        ##If the range is 0 return None to prevent division by 0
        else:
            print("Error: API range = 0")
            return None
            