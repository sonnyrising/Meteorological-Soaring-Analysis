# Meteorological Soaring Analysis (MSA)

A Python-based desktop application that analyzes and visualizes historical meteorological data alongside cross-country soaring flight logs. By applying data science techniques to flight records and Open-Meteo API data, this tool helps glider pilots identify the exact weather patterns that lead to optimal soaring conditions.

---

## Tech Stack

*   **GUI Framework:** PyQt6
*   **Data Science & Math:** Pandas, NumPy, SciPy
*   **Data Visualization:** Matplotlib
*   **Database & APIs:** SQLite3, Open-Meteo REST API

---

## Key Features

*   **Statistical Analysis:** Performs regression analysis to find lines of best fit, calculating statistical measures like R² and RMSE.
*   **Data Normalization:** Normalizes dissimilar datasets (e.g., weather metrics vs. flight performance) for accurate comparative analysis.
*   **Interactive Visualization:** Generates customizable graphs for temperature, humidity, wind speed, and flight data.
*   **Custom Filtering:** Filter analysis by specific regions, date ranges, and meteorological conditions.
*   **Export Functionality:** Export generated plots as image files for flight planning and sharing.

---

## Domain Context: Bridging Data and Aviation
*Cross-country gliding relies entirely on natural atmospheric forces—specifically thermals (rising columns of warm air)—to stay airborne and cover large distances. Predicting these conditions requires interpreting complex meteorological variables.*

This software solves a real problem in the competitive gliding community: bridging the gap between raw meteorological data and practical, actionable insights. By mathematically correlating historical UK flight databases with weather data, it determines the ingredients of a successful soaring day, allowing pilots to plan safer, faster, and more efficient flights.

---

## Installation & Setup

### 1. Prerequisites
Ensure you have Python 3.x installed on your machine.

### 2. Clone and Install Dependencies
```bash
git clone [https://github.com/your-username/msa-software.git](https://github.com/your-username/msa-software.git)
cd msa-software
pip install PyQt6 matplotlib numpy pandas scipy openmeteo_requests requests_cache retry_requests
```

### 3. Run the Application
```bash
python entry_point.py
```

---

## Usage Guide

Upon launching, the **Main Menu** provides access to the core modules:

*   **View Data:** Select regions, date ranges, and conditions (Line A & optional Line B) to plot historical weather against flight data. 
*   **Run Analysis:** Automatically perform regression analysis on selected conditions and plot the lines of best fit.
*   **Export:** Save any generated graph directly to your local machine as an image file.

---

## Project Architecture

*   `entry_point.py` — The main application launcher.
*   `Main_Menu.py`, `View_Data.py`, `Analyse_Data.py` — Core UI window controllers.
*   `Custom_UI_Elements.py`, `Drop_Down_Options.py` — Reusable PyQt6 interface components.
*   `Maths_Functions.py` — Core logic for regression and statistical optimization.
*   `MSA_Utils.py` — Utility functions for Open-Meteo API requests and data validation.
*   `lookup_tables.py` — Maps UI labels to SQLite database fields.
*   `MSA2.db` — Local SQLite database containing historical flight records.
