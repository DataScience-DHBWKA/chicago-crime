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
import folium as fl
from folium.plugins import HeatMap

# %%
chicago_crime_data = pd.read_csv('crimes-chicago-dataset.csv')

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

# %% [markdown]
# # 1.x Data Cleaning
#  Die meisten Datensätze sind nicht vollständig. Die fehlenden Stellen können z.B. entweder fehlender Sorgfalt beim Füllen des Datensatzes von Menschen geschuldet sein, oder manche Daten sind einfach nicht verfügbar. 
#  - mit isnull().sum() können wir die Anzahl von fehlenden Daten(NaN) jeder Spalte auslesen:

# %%
null_daten_count = chicago_crime_data.isnull().sum() #zählt Anzahl an NaN Werten pro Spalte
null_stellen_count = null_daten_count.sum() #zählt Anzahl an Daten die insgesamt fehlen
daten_stellen_Insg = chicago_crime_data.shape[0]*chicago_crime_data.shape[1] #zur Darstellung mit print 
prozent_fehlend = round(100 * null_stellen_count / daten_stellen_Insg, 2)

print("Insgesamt fehlen " + str(null_stellen_count) + " von " + str(daten_stellen_Insg) + " (" + str(prozent_fehlend) + "%) Daten")
print("Pro Spalte fehlen: ")
print(null_daten_count)

# %% [markdown]
# Fehlende Werte (NaN) im Datensatz können manche Auswertungen erschweren oder sogar unmöglich machen. Unser Datensatz hat 7,9 Millionen Reihen, deshalb können wir ohne Probleme Reihen mit NaN löschen, ohne die Statistische Relevanz der Auswertung zu verlieren. Deshalb löschen wir mit .dropna() alle Reihen aus unserem Dataset, die mindestens ein NaN haben: 

# %%
data_cleaned = chicago_crime_data.dropna(ignore_index='true')

# %% [markdown]
# Nun sollten im neuen Dataframe data_cleaned 0 Reihen vorhanden sein, die mindestens ein NaN enthalten:

# %%
#Berechnung der Anzahl von Feldern ohne Wert
null_stellen_count = data_cleaned.isnull().sum().sum() #zählt Anzahl an Daten die insgesamt fehlen
daten_stellen_Insg = data_cleaned.shape[0]*data_cleaned.shape[1] #zur Darstellung mit print 
prozent_fehlend = round(100 * null_stellen_count / daten_stellen_Insg, 2)

print("Nun fehlen " + str(null_stellen_count) + " von " + str(daten_stellen_Insg) + " (" + str(prozent_fehlend) + "%) Daten")

#Berechnung der Anzahl an Reihen gesamt, die ohne Wert waren
prozent_reihen_uebrig = round(100 * data_cleaned.shape[0] / chicago_crime_data.shape[0], 2)

print("Der Datensatz hat nach dem Data Cleaning noch " + str(data_cleaned.shape[0]) + "/" + str(chicago_crime_data.shape[0]) + " (" + str(prozent_reihen_uebrig) + "%) Reihen")

# %% [markdown]
# *Die Anzahl an Datenfeldern ist dabei mehr als 1 Prozent gesunken, da pro fehlender Wert die gesamte Reihe an Daten (22 Datenfelder) gelöscht wird, nicht nur das fehlende Datenfeld*
#
# ### Auschließung von häusliche Verbrechen
# Da wir mit unserer Auswertung herausfinden wollen, wo ein Urlaubstrip nach Chicago am wichtigsten ist, können wir alle Verbrechen aus dem Datensatz herausfiltern, die in der Öffentlichkeit geschehen sind. Häusliche Verbrechen betreffen uns als Urlauber eher nicht.

# %%
crimes_public = data_cleaned.loc[data_cleaned['Domestic'] == False]

#Prozent Berechnung der Übrigen Reihen nach Ausschluss von häuslichen Verbrechen
prozent_reihen_uebrig = round(100 * crimes_public.shape[0] / data_cleaned.shape[0], 2)
print("Der Datensatz hat nach Ausschließung der häuslichen Verbrechen noch " + str(crimes_public.shape[0]) + "/" + str(data_cleaned.shape[0]) + "(" + str(prozent_reihen_uebrig) + "%) Reihen vom gecleaned Datensatz übrig")
data_cleaned = crimes_public

# %% [markdown]
# ### Begrenzung auf ein Jahr
# In manchen Auswertungen wollen wir nur ein bestimmtes Jahr beachten. Um das ressourcenintensive Erstellen eines Dataframes bei jeder Operation, bei der ein solches Array gebraucht wird, zu vermeiden, wollen wir ein neues Dataframe erstellen, welches nur die Werte der Verbrechen enthält, die im Jahr 2019 passiert sind

# %%
nur2019 = data_cleaned.loc[data_cleaned['Year'] == 2019]

# %% [markdown]
# ***Ende Data Cleaning kapitel***

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
#  - Idee: Mit Mittelwert Analyse der Long und Lat den Mittelpunkt der Karte bestimmen

# %%
map_obj = fl.Map(location = [41.88194, -87.62778], zoom_start = 10)

map_obj

# %%
map_obj.save("folium_map.html")

# %% [markdown]
# ### Nun erstellen wir ein Array der Latitude und Longitude Variablen: test

# %%
lat_long = nur2019[['Latitude', 'Longitude']].values.tolist()
HeatMap(lat_long, 0.3).add_to(map_obj)
map_obj

# %%

# %%

# %%
