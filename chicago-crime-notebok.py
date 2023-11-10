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
# - Block
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
# ### Nun erstellen wir ein Array der Latitude und Longitude Variablen: test

# %%
