class lookup_tables:
    def __init__(self):
        ##A lookup table to convert the text that is shown
        ##for a condition into the field name from the db
        self.conditionLookup = {
            'Temperature (Celcius)': 'Temperature',
            'Humidity (%)': 'Humidity',
            'Dew Point (Celcius)': 'Dew Point',
            'Precipitation (mm)': 'Precipitation',
            'Wind Speed (kph)': 'WindSpeed',
            "Distance (km)": "Scoring Distance (km)",
            "Speed (kph)": "Speed (kph)",
            "Completed": "Completed",
            "Speed Points": "VPoints",
            "Height Points": "HPoints",
            "Distance Points": "DPoints",
            "Bonus Points": "BPoints",
            "Total Score": "Total Score",
            'Temperature (Celcius)' : 'temperature_2m',
            'Humidity (%)' : 'relative_humidity_2m',
            'Dew Point (Celcius)' : 'dew_point_2m',
            'Precipitation (mm)' : 'precipitation',
            'Wind Speed (kph)' : 'wind_speed_10m',
        }
        
        ##A lookup table to convert region to its longitude and latitude
        self.region_lookup = {
            "East Anglia": [1.115, 52.423],  # Tibenham, Norfolk
            "East Midlands": [-0.698, 52.876],  # Saltby, Lincolnshire
            "North Wales": [-3.418, 53.183],  # Denbigh, Wales
            "North West": [-3.145, 51.979],  # Talgarth, Wales
            "Scotland": [-2.774, 57.050],   # Aboyne GC, Aboyne
            "South East": [0.876, 51.227],  # Kent Gliding Club, Challock, Kent
            "South Wales": [-4.151, 50.553],  # Dartmoor, Devon
            "South West": [-2.808, 52.497],  # Long Mynd, Church Stretton, Shropshire
            "West Midlands": [-3.134, 54.602],  # Keswick, Lake District
        }
        
