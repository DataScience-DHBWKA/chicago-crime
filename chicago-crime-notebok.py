# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium as fo

# %%
chicago_crime_data = pd.read_csv('C:\\Users\\zbv\\Documents\\chicago-crime-dataset\\Crimes_-_2001_to_Present_20231110.csv')

# %%
print('chicago_crime_data hat',chicago_crime_data.shape[1],'spalten und',chicago_crime_data.shape[0],'zeilen.' )

# %%
chicago_crime_data.head()

# %% [markdown]
# ## Input Variable:
# - Case Number
# ## Output Variablen:
# - Block test
# - Primary Type
# - Description

# %%
print('Fast alle Variablen sind Nominal skaliert')
print('Die Variablen Arrest und Domestic sind Ordinal')

# %%
chicago_crime_data.info()

# %%
null_daten_count = chicago_crime_data.isnull().sum()
print(null_daten_count)

# %%
pd.set_option('display.float_format', '{:.2f}'.format)
chicago_crime_data.describe()

# %%
chicago_crime_data_numeric = chicago_crime_data.select_dtypes(include=[float, int])

# %%
correlation_matrix = chicago_crime_data_numeric.corr()

# %%
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Kreuzkorrelation der numerischen Spalten')
plt.show()

# %% [markdown]
# ### Karte von Chicago mit Heatmap
#  - Wir beginnen indem wir ein Folium Kartenobjekt von Chicago erstellen
#  - Tutorial: https://wellsr.com/python/plotting-geographical-heatmaps-with-python-folium-module/

# %%
map_obj = f.Map(location = [41.88194, -87.62778], zoom_start = 10)

map_obj

# %%
map_obj.save(r"C:\Users\zbv\Documents\chicago-crime\folium_map.html")

# %% [markdown]
# Nun erstellen wir ein Array der Latitude und Longitude Variablen. Daraus können wir dann eine Heatmap erstellen, in der alle in der Öffentlichkeit im Jahr 2019 passierten Verbrechen gezeigt werden. Mit der Zoom Funktion können auch einzelne Blöcke und Straßen mit deren Verbrechen gezeigt werden.

# %%
<<<<<<< Updated upstream
=======
lat_long = nur2019[['Latitude', 'Longitude']].values.tolist()
HeatMap(lat_long, 0.3).add_to(map_obj)
map_obj

# %% [markdown]
# Um eine lesbare Auswertung herzustellen, nehmen wir die Summe der Anzahl von Verbrechen und gruppieren diese nach den jeweiligen Arealen (Im Datensatz als "Block" gespeichert, z.B. "074XX N ROGERS AVE")

# %%
# Summe der Verbrechen gruppiert nach Blöcken
crimes_pro_block = data_cleaned['Block'].value_counts()
# crimes_pro_block = crimes_pro_block[crimes_pro_block > 1]
# Balkendiagramm erstellen
top10_crimes_pro_block = crimes_pro_block[crimes_pro_block > 1].nlargest(10)
top10_crimes_pro_block.plot(kind='bar', color='skyblue')
plt.xlabel('Block')
plt.ylabel('Number of Crimes')
plt.title('Number of Crimes in Each Block')
plt.show()

# %% [markdown]
# Hier werden die 10 Areale gezeigt, die in denen am meisten Verbrechen seit 2001 geschehen sind. Wir haben nun somit die Anzahl an Verbrechen pro Areal gesammelt
#
# Um diese Daten auf einer Heatmap anzuzeigen, müssen wir nun noch die Koordinaten der jeweiligen Areale zur Liste hinzufügen. Dazu nehmen wir den Durschnitt der 'Latitude' und 'Longitude' Variablen jedes Verbrechens, das in einem Areal passiert ist. Diese Durchschnittskoordinaten können wir dann als Mittelpunkt des Areals ansehen:

# %%
block_crime_stats = data_cleaned.groupby('Block').agg({
    'Block': 'count',
    'Latitude': 'mean',
    'Longitude': 'mean'
}).rename(columns={'Block': 'Anzahl Verbrechen'}).reset_index()
block_crime_stats['Normalized Crime Count'] = block_crime_stats['Anzahl Verbrechen'] / 5000

# %%
print(block_crime_stats['Anzahl Verbrechen'].nlargest(5))

# %%
map1 = fl.Map(location = [41.88194, -87.62778], zoom_start = 10)
map1.save("folium_map1.html")
lats_longs1 = block_crime_stats[['Latitude', 'Longitude', 'Normalized Crime Count']].values.tolist()
HeatMap(lats_longs1).add_to(map1)
map1

# %%
# Assuming you have block_crime_stats DataFrame with 'Latitude', 'Longitude', and 'Normalized Crime Count' columns

# Define the size of the grid squares (in degrees)
grid_size_degrees = 0.0009  # Assuming 100x100 meters, you might need to adjust this based on your exact requirements

# Calculate the number of grid squares in latitude and longitude
lat_bins = np.arange(data_cleaned['Latitude'].min(), data_cleaned['Latitude'].max(), grid_size_degrees)
lon_bins = np.arange(data_cleaned['Longitude'].min(), data_cleaned['Longitude'].max(), grid_size_degrees)

# Create a new DataFrame with grid square coordinates
grid_df = pd.DataFrame(np.array(np.meshgrid(lat_bins, lon_bins)).T.reshape(-1, 2), columns=['Grid Lat', 'Grid Lon'])

# Initialize a column to store the number of crimes in each square
grid_df['Crime Count'] = 0

# Iterate through each crime and increment the count in the corresponding grid square
for _, crime in data_cleaned.iterrows():
    lat_idx = np.digitize(crime['Latitude'], lat_bins) - 1
    lon_idx = np.digitize(crime['Longitude'], lon_bins) - 1
    grid_df.loc[(grid_df['Grid Lat'] == lat_bins[lat_idx]) & (grid_df['Grid Lon'] == lon_bins[lon_idx]), 'Crime Count'] += 1

# Display the resulting DataFrame
print(grid_df)

# BUG: Dauert ewig weil das eine Verbrechen ja sonstwo ist, deswegen fängt er dort an. Deshalb muss man das aus dem Datensatz rauslöschen

# %%
>>>>>>> Stashed changes
