import requests
import json
import pandas as pd

# --- CONFIGURATION ---
# https://www.ncdc.noaa.gov/cdo-web/token
API_TOKEN = 'AcWsKCHzUZtwiRcOLtbkeOkxbIkRhmGH'

# https://www.ncdc.noaa.gov/cdo-web/datatools/selectlocation
LOCATION_ID = 'CITY:US060030' #SD
STATION_ID = 'GHCND:USW00093115' #IB

# Dates must be in YYYY-MM-DD format
START_DATE = '2026-01-01'
END_DATE = '2026-01-02'



def results_to_dataframe(api_response):

    if not api_response or 'results' not in api_response:
        return pd.DataFrame()

    # Flatten the JSON results
    df = pd.json_normalize(api_response['results'])
    # Convert date strings to actual datetime objects
    df['date'] = pd.to_datetime(df['date'])
    # Split the 'attributes' column into 4 distinct flag columns
    #df[['m_flag', 'q_flag', 'day_flag', 's_flag']] = df['attributes'].str.split(',', expand=True)

    del df['attributes']

    return df


def check_datasets(token, identifier):

    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/datasets"
    headers = {'token': token}
    params = {}

    print(f'Checking {identifier}.')
    # Logic to determine if the ID is a Station or a Location
    if identifier.startswith('GHCND:') or identifier.startswith('COOP:'):
        params['stationid'] = identifier
    else:
        params['locationid'] = identifier

    try:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            #print(json.dumps(response.json(), indent=2))
            print("\n--- Summary of Available Datasets ---")
            for dataset in response.json()['results']:
                print(f"ID: {dataset['id']:10} | Name: {dataset['name']:30} | Min Date: {dataset['mindate']}| Max Date: {dataset['maxdate']}")

            return response.json()

        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"Connection error: {e}")
        return None


def get_historic_weather_by_station(token, dataset_id, station_id, start_date, end_date):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    #base_url = 'https://www.ncei.noaa.gov/cdo-web/api/v2/datasets?datatypeid=TOBS'

    headers = {
        'token': token
    }

    params = {
        'datasetid': dataset_id,
        #'locationid': location_id,
        'stationid': station_id,
        'startdate': start_date,
        'enddate': end_date,
        'limit': 100,  # Max allowed per request IS 1000
        'units': 'standard'  # Use 'metric' for Celsius/mm
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)

        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            if not data:
                print("No data found for the specified parameters.")
                return None
            print(f"Successfully retrieved {len(data['results'])} records.")
            # Print the first record
            print(json.dumps(data['results'][0], indent=2))
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_historic_weather_by_location(token, dataset_id, location_id, start_date, end_date):
    base_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"

    headers = {
        'token': token
    }

    params = {
        'locationid': location_id,
        'datasetid': dataset_id,
        'startdate': start_date,
        'enddate': end_date,
        'limit': 100,  # Max allowed per request IS 1000
        'units': 'standard'  # Use 'metric' for Celsius/mm
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)

        # Check for successful response
        if response.status_code == 200:
            data = response.json()
            if not data:
                print("No data found for the specified parameters.")
                return None
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#station_info = check_datasets(API_TOKEN, STATION_ID)
#location_info = check_datasets(API_TOKEN, LOCATION_ID)



d_id = 'GHCND'
#d_id ='NEXRAD2'
#d_id ='NEXRAD3'

location_data = get_historic_weather_by_location(API_TOKEN,  dataset_id = d_id, location_id = LOCATION_ID, start_date= START_DATE,end_date= END_DATE)
station_data = get_historic_weather_by_station(token= API_TOKEN, dataset_id = 'GHCND', station_id = STATION_ID, start_date = START_DATE,end_date = END_DATE)

print(json.dumps(location_data['results'], indent=2))
print(json.dumps(station_data['results'], indent=2))


# Convert to DataFrames
df_location = results_to_dataframe(location_data)
df_station = results_to_dataframe(station_data)

# Display the results
print("Location Dataframe (San Diego):")
print(df_location.head())

print("\nStation Dataframe (Imperial Beach):")
print(df_station.head())