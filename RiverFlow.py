import pandas as pd

#https://waterdata.ibwc.gov/AQWebportal/Data/Export
df = pd.read_csv('TJRFlow.csv')
summary_stats = df.describe()

# 4. Display the results
print("--- Data Overview ---")
print(df.head())
print("\n--- Summary Statistics ---")
print(summary_stats)