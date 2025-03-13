class options():
    def __init__(self):     
        self.regions = [
                'East Anglia',
                'East Midlands',
                'North West',
                'Scotland',
                'South East',
                'South Wales',
                'South West',
                'West Midlands'
            ]
        
        self.gliding_clubs = [
            "Kent GC",
            "Saltby",
            "Borders GC",
            "Aboyne GC",
            "Tibenham",
            "Talgarth",
            "Dartmoor GC",
            "Long Mynd",
        ]
        
        self.conditions = [
            "Rain (mm)",
            "Wind Speed (kts)",
            "Wind Direction (degrees)",
            "Distance (km)",
            "Speed (kph)",
            "Speed Points",
            "Height Points",
            "Distance Points",
            "Total Score",
            
        ]
        
        ##A lookup table to convert the text that is shown
        ##for a condition into the field name from the db
        self.conditionLookup = {
            "Distance (km)" : "Scoring Distance",
            "Speed (kph)" : "Speed (kph)",
            "Completed" : "Completed",
            "Speed Points" : "Vpoints",
            "Height Points" : "Hpoints",
            "Distance Points" : "Dpoints",
            "Bonus Points" : "BPoints",
            "Total Score" : "Total Score",
            
        }