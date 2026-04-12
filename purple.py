import requests
import os
from dotenv import load_dotenv
import pandas as pd
import json
from datetime import datetime


def get_key():
    load_dotenv()
    key = os.getenv('purple_key')

    if not key:
        print("API Key not found. Check your .env file for 'purple_key'.")
    else:
        print('API key retrieved successfully.')

    return key

def get_data(start_time, end_time, sensor_id, fields):
    url = f"https://api.purpleair.com/v1/sensors/{sensor_id}/history"
    api_key = get_key()
    headers = {
        "X-API-Key": api_key}
    params = {
        "start_timestamp": start_time,
        "end_timestamp": end_time,
        "average": 60,
        "fields": fields
    }

    response = requests.get(url, headers=headers, params=params)
    sensor_data = response.json()

    print("Data keys:", sensor_data.keys())
    if 'data' in sensor_data and len(sensor_data['data']) > 0:
        print("\nSample Data Row (First Entry):")
        print(json.dumps(sensor_data['data'][0], indent=4))

    return sensor_data

def get_dataframe(json_data):
    if 'data' in json_data and len(json_data['data']) > 0:
        df = pd.DataFrame(json_data['data'], columns=json_data['fields'])

        # Convert UTC unix timestamps to local datetime
        df['time_stamp'] = pd.to_datetime(df['time_stamp'], unit='s', utc=True)
        df['time_stamp_local'] = df['time_stamp'].dt.tz_convert('America/Los_Angeles')
        df['time_stamp_local'] = df['time_stamp_local'].dt.strftime('%Y-%m-%d %H:%M:%S')
        del df['time_stamp']
        time_col = 'time_stamp_local'
        col_data = df.pop(time_col)
        df.insert(0, time_col, col_data)

        #Average both channels
        df['pm2.5_avg'] = df[['pm2.5_atm_a', 'pm2.5_atm_b']].mean(axis=1)

        # Calculate the percent difference of measurements from both channels
        df['rpd'] = 1 - (abs(df['pm2.5_atm_a'] - df['pm2.5_atm_b']) / df['pm2.5_avg'])

        # Keep rows where the difference in readings between a and b sensors is < 20%
        df = df[df['rpd'] >= .80]

        #Apply epa correction
        df['pm2.5_epa_a'] = (0.524 * df['pm2.5_atm_a']) - (0.0862 * df['humidity']) + 5.75
        df['pm2.5_epa_b'] = (0.524 * df['pm2.5_atm_b']) - (0.0862 * df['humidity']) + 5.75

        #Get the average across both sensor channels
        df['pm2.5_epa_avg'] = df[['pm2.5_epa_a', 'pm2.5_epa_b']].mean(axis=1)

        #results = df[['time_stamp_local', 'pm2.5_avg']]

        return df
    else:
        print("No data found for this sensor in the specified time range.")

        return None

def merge_csv_files(folder_path):
    """
    Reads all .csv files from a folder and merges them into one DataFrame.
    Removes duplicate rows after concatenation.
    """
    # Get all files in the folder
    all_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

    # read each file into a list of DataFrames
    df_list = [pd.read_csv(file) for file in all_files]

    # Concatenate all DataFrames in the list
    combined_df = pd.concat(df_list, ignore_index=True)

    # Remove duplicate rows
    cleaned_df = combined_df.drop_duplicates()

    return cleaned_df



fields = "pm2.5_atm_a,pm2.5_atm_b,humidity, pm2.5_atm, pm1.0_atm, pm10.0_atm, voc"
#sensor_index = 161215 #Coronado Cayes 32.5751/-117.1352
#sensor_index = 82281 #Mathewson Park 32.6543/-117.179
#sensor_index = 188113 #IB 32.5751/-117.1352

#sensor_list = ['161215', '82281', '188113']
sensor_list = ['188113']
start_date = pd.Timestamp("2024-04-01")
end_date = pd.Timestamp("2026-04-01")
dates = pd.date_range(start=start_date, end=end_date, freq='180D').tolist()
if dates[-1] < end_date:
    dates.append(end_date)

time_windows = [(int(dates[i].timestamp()), int(dates[i+1].timestamp())) for i in range(len(dates)-1)]
print(time_windows)


for sensor_index in sensor_list:
    print(f"Getting data for sensor {sensor_index} . . . ")
    for start, end in time_windows:
        try:
            data = get_data(start_time=start, end_time=end, sensor_id=sensor_index, fields=fields)
            purple_df = get_dataframe(data)
            if purple_df is None:
                print(f"No data found for sensor {sensor_index} in the window ending {end}.")
                break
            purple_df['SensorID'] = sensor_index
            purple_df.to_csv(f"purple_data\purple_data_{sensor_index}_{start}.csv", index=False)
            print(f"File saved.")

        except Exception as e:
            print(e)
            break


print("Merging files . . .")
df = merge_csv_files('./purple_data')
print(df.head())
df.to_csv(f"purple_data.csv", index=False)
print("Saved purple_data.csv")
