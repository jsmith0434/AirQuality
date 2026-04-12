import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

#pip install openmeteo-requests
#pip install requests-cache retry-requests numpy pandas

def get_data(start, end):

	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	#
	url = "https://archive-api.open-meteo.com/v1/archive"
	params = {
		"latitude": 32.5745,
		"longitude": -117.127,
		"start_date": start,
		"end_date": end,
		"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "rain", "wind_speed_10m", "wind_direction_10m", "pressure_msl", "cloud_cover", "cloud_cover_low"],
		"temperature_unit": "fahrenheit",
		"precipitation_unit": "inch",
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation: {response.Elevation()} m asl")
	print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
	hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
	hourly_rain = hourly.Variables(3).ValuesAsNumpy()
	hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
	hourly_wind_direction_10m = hourly.Variables(5).ValuesAsNumpy()
	hourly_pressure_msl = hourly.Variables(6).ValuesAsNumpy()
	hourly_cloud_cover = hourly.Variables(7).ValuesAsNumpy()
	hourly_cloud_cover_low = hourly.Variables(8).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
		end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = hourly.Interval()),
		inclusive = "left"
	)}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["dew_point_2m"] = hourly_dew_point_2m
	hourly_data["rain"] = hourly_rain
	hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
	hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
	hourly_data["pressure_msl"] = hourly_pressure_msl
	hourly_data["cloud_cover"] = hourly_cloud_cover
	hourly_data["cloud_cover_low"] = hourly_cloud_cover_low

	return hourly_data


def get_dataframe(dataset):

	weather_df = pd.DataFrame(data=dataset)
	weather_df['date'] = pd.to_datetime(weather_df['date'], unit='s', utc=True)
	weather_df['datetime_local'] = weather_df['date'].dt.tz_convert('America/Los_Angeles')
	weather_df['datetime_local'] = weather_df['datetime_local'].dt.strftime('%Y-%m-%d %H:%M:%S')
	del weather_df['date']
	weather_df = weather_df[['datetime_local'] + [col for col in weather_df.columns if col != 'datetime_local']]

	return weather_df


start_date = "2024-04-01"
end_date = "2026-04-01"
data = get_data(start_date, end_date)
weather = get_dataframe(data)
print("\nHourly data\n", weather)
weather.to_csv('weather.csv', index = False, header = True)
print('Weather data saved.')