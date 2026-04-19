# Modeling Atmospheric Drivers Affecting Air Quality in the South Bay

## Project Overview
This repository contains a data processing and statistical analysis pipeline designed to identify the environmental and atmospheric drivers of poor air quality in the Coronado and Imperial Beach areas of San Diego. By integrating hyper-local community sensor data with regional meteorological and hydrological records, this project provides a "Citizen Science" validation of air quality trends.

The project supports local forecasting efforts to help the community anticipate and mitigate the impact of hazardous air quality events.

## Data Sources
The analysis integrates four primary data streams:
* **Air Quality:** PM2.5 and VOC data from the **PurpleAir** sensor network.
* **Weather:** Hourly measurements (temperature, humidity, wind, and pressure) sourced from **Open-Meteo** (Imperial Beach Ream Field NAS station).
* **Hydrology:** Hourly river flow data for the Tijuana River at the International Boundary, maintained by the **IBWC**.
* **Tide & Oceanography:** Water level and temperature data from **NOAA**.

## Features & Analysis
The included Python script performs the following operations:
1.  **Data Integration:** Merges disparate CSV datasets into a unified time-series dataframe based on local timestamps.
2.  **Correlation Analysis:** Generates a heatmap to visualize linear relationships between PM2.5 levels and environmental variables like wind speed, humidity, and river flow.
3.  **ANOVA (Analysis of Variance):** Statistically tests the impact of categorical variables, specifically wind direction, on air quality levels.
4.  **PCA (Principal Component Analysis):** Reduces dimensionality to identify the primary "loadings" or contributors to air quality variance, such as the relationship between the nocturnal inversion and stagnant winds.

## Scientific Context
This project builds upon research from the **Scripps Institution of Oceanography** and **SDSU**, which links water quality in the Tijuana River to air quality via aerosolization. Key drivers investigated include:
* **The Nocturnal Inversion:** Air cooling at night trapping gases near the ground.
* **South-Easterly Wind Effect:** Localized wind patterns that transport pollutants into residential areas.
* **Aerosolization:** High humidity and turbulent river flow contributing to the formation of fine particulate matter.

## Contributing Organizations
This work is intended to benefit local advocacy and research groups, including:
* Emerald Keepers 
* Environmental Health Coalition 
* San Diego County Air Pollution Control District (SDAPCD) 
* Surfrider San Diego 

## Author
**Jessica Smith**
California Naturalist Stewardship Project, Spring 2026 
