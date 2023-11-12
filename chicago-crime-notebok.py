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

print("Der Datensatz hat nach dem Data Cleaning noch " + str(data_cleaned.shape[0]) + "/" + str(chicago_crime_data.shape[0]) + " (" + str(prozent_reihen_uebrig) + ") Reihen")

# %% [markdown]
# *Die Anzahl an Datenfeldern ist dabei mehr als 1 Prozent gesunken, da pro fehlender Wert die gesamte Reihe an Daten (22 Datenfelder) gelöscht wird, nicht nur das fehlende Datenfeld*
#
# ### Begrenzung auf ein Jahr
# In manchen Auswertungen wollen wir nur ein bestimmtes Jahr beachten. Um das ressourcenintensive Erstellen eines Dataframes bei jeder Operation, bei der ein solches Array gebraucht wird, zu vermeiden, wollen wir ein neues Dataframe erstellen, welches nur die Werte der Verbrechen enthält, die im Jahr 2019 passiert sind

# %%
nur2019 = data_cleaned[data_cleaned['Year'] == 2019]

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

# %% [markdown]
# # I. Vergleich früher/heute.

# %% [markdown]
# ## 1. Vorbereitung der Daten.

# %% [markdown]
# Um Konflikte zu vermeiden, wird in diesem Teil zunächst der Datensatz nochmal in ein neues Data Frame geladen.

# %%
chicago_crime_data_vergleich_frueher_heute = pd.read_csv('crimes-chicago-dataset.csv')

# %% [markdown]
# Und die einzige Spalten die behalten werden sind die Spalte Date und die Spalte Primary Type.

# %%
columns_to_keep = ['Date', 'Primary Type']
chicago_crime_data_vergleich_frueher_heute = chicago_crime_data_vergleich_frueher_heute[columns_to_keep]

# %% [markdown]
# Damit die Analyse einfacher wird, werden in die Spalte Date nur die Jahre behalten.

# %%
chicago_crime_data_vergleich_frueher_heute['Date'] = pd.to_datetime(chicago_crime_data_vergleich_frueher_heute['Date'])
chicago_crime_data_vergleich_frueher_heute['Year'] = chicago_crime_data_vergleich_frueher_heute['Date'].dt.year
chicago_crime_data_vergleich_frueher_heute = chicago_crime_data_vergleich_frueher_heute.drop('Date', axis=1)

# %% [markdown]
# ## 2. Klassifizierung der Verbrechen.

# %% [markdown]
# Verbrechen sind vielfältig und reichen von vergleichsweise harmlosen Vorkommnissen bis hin zu schwerwiegenden Delikten. In diesem Teil der Analyse werden Verbrechen anhand verschiedener Kriterien wie Gewaltanwendung, potenzielle Schädlichkeit für Opfer und die Schwere der Gesetzesverletzung klassifiziert. Vorfälle, die physische oder emotionale Bedrohungen, schwerwiegende Schäden oder schwerwiegende Gesetzesverstöße aufweisen, werden als schwerwiegend eingestuft. Vorfälle, die geringere Gefahren oder weniger erhebliche Gesetzesübertretungen darstellen, werden als weniger schwerwiegend betrachtet.

# %% [markdown]
# Zunächst wird versucht, eine klare Klassifizierung durchzuführen.

# %%
unique_types = chicago_crime_data_vergleich_frueher_heute['Primary Type'].unique()
print(unique_types)

# %%
schwerwiegende_verbrechen = ['THEFT', 'ASSAULT', 'WEAPONS VIOLATION','SEX OFFENSE','CRIM SEXUAL ASSAULT','MOTOR VEHICLE THEFT','CRIMINAL TRESPASS','ROBBERY','PUBLIC PEACE VIOLATION','CRIMINAL SEXUAL ASSAULT','HOMICIDE', 'KIDNAPPING','HUMAN TRAFFICKING']


# %%
def classify_crime(crime_type):
    if crime_type in schwerwiegende_verbrechen:
        return 'Schwerwiegend'
    else:
        return 'Nicht Schwerwiegend'

chicago_crime_data_vergleich_frueher_heute['Schwere Klassifizierung'] = chicago_crime_data_vergleich_frueher_heute['Primary Type'].apply(classify_crime)

# %% [markdown]
# ## 3.Gruppierung nach Jahren.

# %% [markdown]
# Um die Analyse durchführen zu können, werden jetzt die Daten nach Jahren gruppiert, und die Anzahl schwerwiegende und nicht schwerwiegende Verbrechen für jedes Jahr summiert.

# %%
grouped_data = chicago_crime_data_vergleich_frueher_heute.groupby(['Year', 'Schwere Klassifizierung']).size().unstack()

grouped_data = grouped_data.fillna(0)

print(grouped_data)

# %% [markdown]
# Diese Daten werden jetzt in Graphen, um Sie zu veranschaulichen, präsentiert.

# %%
grouped_data.plot(kind='bar', stacked=True, color=['lightgrey','#FF6347'])
plt.title('Anzahl der schwerwiegenden und nicht-schwerwiegenden Verbrechen pro Jahr')
plt.xlabel('Jahr')
plt.ylabel('Anzahl Verbrechen')
plt.legend(title='Schwere Klassifizierung')
plt.show()

# %%
grouped_data['Schwerwiegend'].plot(kind='line', color='red', marker='o', label='Schwerwiegend')
grouped_data['Nicht Schwerwiegend'].plot(kind='line', color='gray', marker='o', label='Nicht Schwerwiegend')
plt.title('Anzahl der schwerwiegenden und nicht-schwerwiegenden Verbrechen pro Jahr')
plt.xlabel('Jahr')
plt.ylabel('Anzahl Verbrechen')
plt.legend(title='Schwere Klassifizierung')
plt.show()

# %% [markdown]
# Es ist zu erkennen, dass die Gesamtzahl an Verbrechen sich stark reduziert hat. Aber es ist nicht wegzulassen, dass im Jahr 2022 die Anzahl an schwerwiegende Verbrechen stark gewachsen ist, und diese zum ersten Mal die Anzahl der nicht schwerwiegende Verbrechen übertroffen hat.

# %%
# Filtern nach schwerwiegenden Verbrechen
schwere_verbrechen_2021 = crimes_2021[crimes_2021['Schwere Klassifizierung'] == 'Schwerwiegend']
schwere_verbrechen_2022 = crimes_2022[crimes_2022['Schwere Klassifizierung'] == 'Schwerwiegend']

# Gruppieren und Zählen der schwerwiegenden Verbrechen für 2021 und 2022
schwere_verbrechen_2021_grouped = schwere_verbrechen_2021.groupby('Primary Type').size().sort_values(ascending=False)
schwere_verbrechen_2022_grouped = schwere_verbrechen_2022.groupby('Primary Type').size().sort_values(ascending=False)

# Zunahme der schwerwiegenden Verbrechen im Jahr 2022 im Vergleich zu 2021
increase_schwere_verbrechen_2022_vs_2021 = schwere_verbrechen_2022_grouped - schwere_verbrechen_2021_grouped
print(increase_schwere_verbrechen_2022_vs_2021)

# %%
import matplotlib.pyplot as plt

increase_schwere_verbrechen_2022_vs_2021.plot(kind='bar', color='red')
plt.title('Zunahme schwerwiegender Verbrechen 2022 vs. 2021')
plt.xlabel('Verbrechenstyp')
plt.ylabel('Zunahme')
plt.xticks(rotation=90)
plt.show()

# %% [markdown]
# Es ist klar zu erkennen, dass Verbrechen, die mit Diebstahl zu tun haben, im Jahr 2022 stark gewachsen sind.

# %% [markdown]
# ## 5. Schlussfolgerungen und Implikationen:

# %% [markdown]
# Nach den Daten ist es klar zu erkennen, dass die Anzahl der gemeldeten Straftaten seit 2001 stark gesunken ist, was eine positive Entwicklung nachweist.
# Nicht desto trotz ist die Anzahl der gemeldeten Diebstahlfälle im Jahr 2022 im Vergleich zum Jahr 2021 stark gewachsen, deswegen ist es ratsam, in einen Trip nach Chicago dies mitzurechnen und wertvolle Gegenstände nicht mit sich mitnehmen.
# Aber als klare Schlussfolgerung kann man sagen, dass Chicago heute viel sicherer ist im Vergleich zu früheren Jahren.
