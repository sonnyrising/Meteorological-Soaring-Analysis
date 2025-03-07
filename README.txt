Note:
This readme was written with help from DeepSeek AI with the prompt:
"Please write a .README for this software, use the attached python files and word document" - I had attached each python file from the program as well the main project document.

Overview:
The Meteorological Soaring Analysis (MSA) software is a Python-based application designed to analyze and visualize meteorological and flight data. It provides tools for plotting graphs, analyzing trends, and exporting results. The software is built using the PyQt6 library for the graphical user interface (GUI) and integrates with Matplotlib for data visualization. It also interacts with a SQLite database and the Open-Meteo API to retrieve historical weather and flight data.

Features:
Data Visualization: Plot graphs for flight and weather data, including temperature, humidity, wind speed, and more.

Data Analysis: Perform regression analysis to find lines of best fit and calculate statistical measures like R² and RMSE.

Customizable Inputs: Users can select specific regions, date ranges, and conditions to analyze.

Export Functionality: Export graphs as image files for further use.

User-Friendly Interface: Intuitive GUI with custom buttons, dropdown menus, and date pickers.

Data Normalization: Normalize dissimilar data sets for comparative analysis.


Prerequisites:
Python 3.x
Required Python libraries: PyQt6, matplotlib, numpy, pandas, scipy, openmeteo_requests, requests_cache, retry_requests, sqlite3


Goals:
The goal of this project is to use a combination of historical meteorological data and information about cross-country soaring flights in the UK to determine the optimal conditions for a successful soaring day and to predict when these conditions are most likely to occur. The project aims to provide glider pilots with a tool that not only forecasts weather conditions but also educates them on the meteorological factors that contribute to good soaring days. By analyzing historical data, the software will help pilots understand the relationship between weather patterns and flight performance, ultimately improving their ability to plan and execute cross-country flights safely and efficiently.


Understanding Gliding and Cross-Country Soaring:
Gliding is a sport where pilots fly unpowered aircraft known as gliders or sailplanes. Unlike powered aircraft, gliders rely on natural forces such as thermals, ridge lift, and wave lift to stay airborne. Cross-country soaring involves flying long distances across the country, using these natural forces to gain altitude and extend flight duration. Pilots must carefully plan their routes, taking into account weather conditions, wind patterns, and thermal activity to maximize their flight distance and speed.

Thermals and Soaring
Thermals are columns of rising warm air that form when the sun heats the ground unevenly. As the warm air rises, it cools, and if it contains enough moisture, it can form cumulus clouds. Glider pilots use these thermals to gain altitude by circling within the rising air. Once they reach a sufficient height, they can glide to the next thermal, repeating the process to stay airborne for hours and cover significant distances.

Cross-Country Flying
In cross-country flying, pilots set tasks based on the day's weather conditions. These tasks involve flying to specific turnpoints and returning to the starting point or landing at a different airfield. The goal is to complete the task as quickly as possible, often competing against other pilots. Successful cross-country flights require a deep understanding of meteorology, as pilots must predict where thermals will form and how wind patterns will affect their flight.

The Role of Weather in Gliding
Weather plays a crucial role in gliding. Factors such as temperature, wind speed and direction, humidity, and atmospheric stability all influence the formation of thermals and the overall conditions for soaring. Pilots must be able to interpret weather forecasts and make informed decisions about when and where to fly. This project aims to bridge the gap between raw meteorological data and practical, actionable insights for glider pilots.


Project Achievements:
This project will provide glider pilots with a comprehensive tool that combines historical weather data with flight performance data to identify the optimal conditions for soaring. The software will allow pilots to:

Analyze Historical Data: By comparing historical weather data with flight performance data, the software will identify trends and patterns that lead to successful soaring days. Pilots will be able to see how different weather conditions, such as wind speed, temperature, and humidity, affect flight performance.

Educate Pilots: The software will educate pilots on the meteorological factors that contribute to good soaring conditions. By understanding these factors, pilots can make more informed decisions and improve their flying skills.

Visualize Data: The software will present data in an easy-to-understand visual format, using graphs and charts to show the relationship between weather conditions and flight performance. This will help pilots quickly interpret the data and apply it to their flight planning.

Customizable Analysis: Pilots will be able to customize the analysis by selecting specific weather conditions and time periods. This flexibility allows pilots to focus on the factors most relevant to their flying style and local conditions.


Conclusion:
This project aims to enhance the safety, efficiency, and enjoyment of gliding by providing pilots with a powerful tool for weather analysis and flight planning. By combining historical data with advanced computational methods, the software will offer insights that were previously only available through years of experience. Whether you are a novice pilot or an experienced competitor, this tool will help you make the most of every soaring day.


Usage:
Main Menu:
View Data: Opens a window to plot and analyze flight and weather data.

Run Analysis: Opens a window to perform regression analysis on selected data.

Info: Displays information about the software.

Quit: Exits the application.

View Data Window:
Line A: Select the region, date range, and condition for the first data set.

Line B (Optional): Select the region, date range, and condition for the second data set.

Plot Graph: Plots the selected data on a graph.

Export Graph: Exports the plotted graph as an image file.

Analyse Data Window:
Inputs: Select the region, date range, and condition for analysis.

Plot Graph: Plots the data and performs regression analysis to display lines of best fit.

Export Graph: Exports the plotted graph as an image file.


File Structure:
Analyse_Data.py: Contains the code for the analysis window.

Custom_UI_Elements.py: Defines custom UI elements like buttons, dropdowns, and dialogs.

Differentiation file.py: Contains mathematical functions for differentiation (currently incomplete).

Drop_Down_Options.py: Defines options for dropdown menus.

entry_point.py: The main entry point for the application.

lookup_tables.py: Contains lookup tables for converting UI labels to database fields.

Main_Menu.py: Contains the code for the main menu window.

Maths_Functions.py: Contains mathematical functions for regression and optimization.

MSA_Utils.py: Contains utility functions for data retrieval and validation.

View_Data.py: Contains the code for the data viewing window.

MSA2.db: The flight database containing info about flights on each day


Dependencies:
PyQt6: For the graphical user interface.

Matplotlib: For plotting graphs.

NumPy: For numerical computations.

Pandas: For data manipulation.

Scipy: For optimization and statistical functions.

Open-Meteo API: For retrieving historical weather data.

SQLite3: For querying the flight database.