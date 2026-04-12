import pandas as pd
from functools import reduce
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from statsmodels.formula.api import ols
import numpy as np


def get_dataframe():
    #River flow data
    df_river_flow = pd.read_csv('TJRFlow.csv')
    df_river_flow['time_stamp_local'] = pd.to_datetime(df_river_flow['End of Interval (UTC-08:00)']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df_river_flow.rename(columns={'Average (m^3/s)': 'flow_rate'}, inplace=True)
    df_river_flow.drop(columns=['Start of Interval (UTC-08:00)', 'End of Interval (UTC-08:00)'], errors='ignore', inplace=True)
    df_river_flow = df_river_flow[['time_stamp_local', 'flow_rate']].copy()

    #weather data
    df_weather = pd.read_csv('weather.csv')
    df_weather.rename(columns={'datetime_local':'time_stamp_local'}, inplace=True)
    wd = df_weather['wind_direction_10m']
    conditions = [
        (wd >= 337.5) | (wd < 22.5),
        (wd >= 22.5) & (wd < 67.5),
        (wd >= 67.5) & (wd < 112.5),
        (wd >= 112.5) & (wd < 157.5),
        (wd >= 157.5) & (wd < 202.5),
        (wd >= 202.5) & (wd < 247.5),
        (wd >= 247.5) & (wd < 292.5),
        (wd >= 292.5) & (wd < 337.5)
    ]
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    df_weather['wind_direction_category'] = np.select(conditions, directions, default=None)
    df_weather['wind_direction_category'] = df_weather['wind_direction_category'].replace('N_2', 'N')

    #tide data
    df_tides = pd.read_csv('noaa_data.csv')
    df_tides.rename(columns={'date_time': 'time_stamp_local'}, inplace=True)

    #purple sensor data
    df_air = pd.read_csv('purple_data.csv')
    df_air['time_stamp_local'] = pd.to_datetime(df_air['time_stamp_local'], format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
    df_air = df_air[['time_stamp_local', 'pm2.5_epa_avg', 'pm2.5_avg', 'pm2.5_atm', 'pm1.0_atm', 'pm10.0_atm', 'voc', 'SensorID']].copy()

    # Merge data
    dfs = [df_air, df_weather, df_tides, df_river_flow]
    df = reduce(lambda left, right: pd.merge(left, right, on='time_stamp_local', how='outer'), dfs)
    df['air_pressure_value'] = df['air_pressure_value'].fillna(df['pressure_msl'])
    df.drop(columns=['pressure_msl'], errors='ignore', inplace=True)

    return df

def check_correlation(df):
    ###Correlation
    correlation_matrix = df.corr(numeric_only=True)
    pm25_correlations = correlation_matrix.loc['pm2.5_avg']
    print(pm25_correlations.sort_values(ascending=False))

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    plt.show()

def run_anova(df, cat_col):
    df_clean = df.dropna(subset=['pm2.5_avg', cat_col])
    model = ols(f'Q("pm2.5_avg") ~ Q("{cat_col}")', data=df_clean).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)

    summary = df_clean.groupby(cat_col, observed=True)['pm2.5_avg'].agg(['mean'])
    print('Mean PM2.5 values for each wind direction:')
    print(summary.sort_values('mean', ascending=False))
    #print(df['pm2.5_avg'].describe())

def run_pca(df):
    pca_cols = [
        'temperature_2m',
        'relative_humidity_2m',
        'dew_point_2m',
        'rain',
        'wind_speed_10m',
        'wind_direction_10m',
        'cloud_cover',
        'cloud_cover_low',
        'air_pressure_value',
        'hourly_height_value',
        'water_temperature_value',
        'flow_rate'
    ]

    data = df[pca_cols].dropna()
    scaled_data = StandardScaler().fit_transform(data)

    pca = PCA(n_components=3) # creates a PCA object with n number of components
    pca.fit(scaled_data) # fits the model on the data
    loadings = pd.DataFrame(pca.components_.T, columns=['PC1', 'PC2', 'PC3'], index=pca_cols)
    print(loadings)

    # Print the grouped relationships
    for pc in loadings.columns:
        print(f"\n{pc} Top Contributors:")
        top_contributors = loadings[pc].abs().sort_values(ascending=False).head(4)
        for var, val in top_contributors.items():
            print(f" - {var}: {loadings.at[var, pc]:.3f}")

df = get_dataframe()
print(df.head())

check_correlation(df)
run_anova(df, 'wind_direction_category')