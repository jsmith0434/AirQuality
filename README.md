# Modeling Atmospheric Drivers Affecting Air Quality in the South Bay

## Project Overview
This repository contains a data processing and statistical analysis pipeline designed to identify the environmental and atmospheric drivers of poor air quality in the Coronado and Imperial Beach areas of San Diego [cite: 124, 127, 129]. By integrating hyper-local community sensor data with regional meteorological and hydrological records, this project provides a "Citizen Science" validation of air quality trends [cite: 67].

The project supports local forecasting efforts to help the community anticipate and mitigate the impact of hazardous air quality events [cite: 132, 134].

## Data Sources
The analysis integrates four primary data streams:
* **Air Quality:** PM2.5 and VOC data from the **PurpleAir** sensor network [cite: 74, 80].
* **Weather:** Hourly measurements (temperature, humidity, wind, and pressure) sourced from **Open-Meteo** (Imperial Beach Ream Field NAS station) [cite: 72, 73].
* **Hydrology:** Hourly river flow data for the Tijuana River at the International Boundary, maintained by the **IBWC** [cite: 81, 82].
* **Tide & Oceanography:** Water level and temperature data from **NOAA** [cite: 70, 71].

## Features & Analysis
The included Python script performs the following operations:
1.  **Data Integration:** Merges disparate CSV datasets into a unified time-series dataframe based on local timestamps.
2.  **Correlation Analysis:** Generates a heatmap to visualize linear relationships between PM2.5 levels and environmental variables like wind speed, humidity, and river flow.
3.  **ANOVA (Analysis of Variance):** Statistically tests the impact of categorical variables, specifically wind direction, on air quality levels [cite: 141].
4.  **PCA (Principal Component Analysis):** Reduces dimensionality to identify the primary "loadings" or contributors to air quality variance, such as the relationship between the nocturnal inversion and stagnant winds [cite: 55, 141].

## Scientific Context
This project builds upon research from the **Scripps Institution of Oceanography** and **SDSU**, which links water quality in the Tijuana River to air quality via aerosolization [cite: 43, 44, 48]. Key drivers investigated include:
* **The Nocturnal Inversion:** Air cooling at night trapping gases near the ground [cite: 55].
* **South-Easterly Wind Effect:** Localized wind patterns that transport pollutants into residential areas [cite: 56].
* **Aerosolization:** High humidity and turbulent river flow contributing to the formation of fine particulate matter [cite: 57, 98].

## Contributing Organizations
This work is intended to benefit local advocacy and research groups, including:
* Emerald Keepers [cite: 144]
* Environmental Health Coalition [cite: 145]
* San Diego County Air Pollution Control District (SDAPCD) [cite: 146]
* Surfrider San Diego [cite: 148]

## Author
**Jessica Smith**
California Naturalist Stewardship Project, Spring 2026 [cite: 113, 114]
