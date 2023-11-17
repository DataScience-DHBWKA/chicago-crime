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
import os
from folium.plugins import HeatMap
from folium.plugins import DualMap

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
# # Data Cleaning
#  Die meisten Datensätze sind nicht vollständig. Die fehlenden Stellen können z.B. entweder fehlender Sorgfalt beim Füllen des Datensatzes von Menschen geschuldet sein, oder manche Daten sind einfach nicht verfügbar. 
#
# Die Anzahl dieser fehlenden Datenstellen können wir mit isnull().sum() auslesen. Außerdem berechnen wir für ein besseres Verständnis die Prozentzahl von Daten, die fehlen:

# %%
null_daten_count = chicago_crime_data.isnull().sum() #zählt Anzahl an NaN Werten pro Spalte
null_stellen_count = null_daten_count.sum() #zählt Anzahl an Daten die insgesamt fehlen
daten_stellen_Insg = chicago_crime_data.shape[0]*chicago_crime_data.shape[1] #zur Darstellung mit print 
prozent_fehlend = round(100 * null_stellen_count / daten_stellen_Insg, 2)

print("Insgesamt fehlen " + str(null_stellen_count) + " von " + str(daten_stellen_Insg) + " (" + str(prozent_fehlend) + "%) Daten")
print("Pro Spalte fehlen: ")
print(null_daten_count)

# %% [markdown]
# Fehlende Werte (NaN) im Datensatz können manche Auswertungen erschweren oder sogar unmöglich machen. Unser Datensatz hat 7,9 Millionen Reihen, deshalb können wir ohne Probleme Reihen mit NaN löschen, ohne die Statistische Relevanz der Auswertung zu verlieren. Deshalb löschen wir mit .dropna() alle Reihen aus unserem Datansatz, die mindestens ein NaN haben: 

# %%
data_cleaned = chicago_crime_data.dropna(ignore_index='true')

# %% [markdown]
# Nun sollten im neuen Dataframe data_cleaned 0 Reihen vorhanden sein, die mindestens ein NaN enthalten:

# %%
#Berechnung der Anzahl von Feldern ohne Wert
null_stellen_count = data_cleaned.isnull().sum().sum() #zählt Anzahl an Daten die insgesamt fehlen
daten_stellen_Insg = data_cleaned.shape[0]*data_cleaned.shape[1] #zur Darstellung mit print 
prozent_fehlend = round(100 * null_stellen_count / daten_stellen_Insg, 2) #Berechnung der Prozentzahl

print("Nun fehlen " + str(null_stellen_count) + " von " + str(daten_stellen_Insg) + " (" + str(prozent_fehlend) + "%) Daten")

#Berechnung der Anzahl an Reihen gesamt, die ohne Wert waren
prozent_reihen_uebrig = round(100 * data_cleaned.shape[0] / chicago_crime_data.shape[0], 2)

print("Der Datensatz hat nach dem Data Cleaning noch " + str(data_cleaned.shape[0]) + "/" + str(chicago_crime_data.shape[0]) + " (" + str(prozent_reihen_uebrig) + "%) Reihen")

# %% [markdown]
# *Die Anzahl an Reihen ist dabei mehr als 1 Prozent gesunken, da pro fehlender Wert die gesamte Reihe an Daten (22 Datenfelder) gelöscht wird, nicht nur das fehlende Datenfeld*
#
# ### Auschließung von häusliche Verbrechen
# Da wir mit unserer Auswertung herausfinden wollen, wo ein Urlaubstrip nach Chicago am sichersten ist, können wir alle Verbrechen aus dem Datensatz herausfiltern, die nicht in der Öffentlichkeit geschehen sind. Häusliche Verbrechen betreffen uns als Urlauber schließlich eher nicht.

# %%
crimes_public = data_cleaned.loc[data_cleaned['Domestic'] == False]

#Prozent Berechnung der Übrigen Reihen nach Ausschluss von häuslichen Verbrechen
prozent_reihen_uebrig = round(100 * crimes_public.shape[0] / data_cleaned.shape[0], 2)
print("Der Datensatz hat nach Ausschließung der häuslichen Verbrechen noch " + str(crimes_public.shape[0]) + "/" + str(data_cleaned.shape[0]) + "(" + str(prozent_reihen_uebrig) + "%) Reihen vom vorher gesäuberten Datensatz übrig")
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
# # Heatmap von Chicago

# %% [markdown]
# Große Städte verändern sich ständig. Stadtmittelpunkte, Touristenattraktionen und andere Orte von Menschenansammlungen verändern und verschieben sich, wenn neue Orte ausgebaut werden und alte Geschäfte/Viertelgeschlossen werden. Deswegen werden wir für die Heatmap nur die Verbrechen beachten, die seit Anfang 2015 geschehen sind. Das Jahr 2015 wurde gewählt, weil so in den vergangenen 7 11/12 Jahren genügend Daten angefallen sind und die Geodaten aber trotzdem aktuell genug sein sollten, um verlässliche Aussagen über die Sicherheit der Orte zu treffen.
#
# Wir erstellen also ein neues Dataframe, in dem nur die Verbrechen ab 2019 enthalten sind:

# %%
crimes_nach_2015 = data_cleaned.loc[data_cleaned['Year'] >= 2015]

# %% [markdown]
# ### Kartenerstellung
# Wir beginnen, indem wir ein neues Kartenobjekt mit dem Namen "karte_Chicago" erstellen, dessen Mittelpunkt eine Koordinate in Chicago ist. Außerdem erstellen wir einen Ordner (falls dieser nicht bereits exisitert), in dem wir alle Karten speichern werden:

# %%
karte_Chicago = fl.Map(location = [41.863474, -87.613654], zoom_start = 11, control_scale=True,)
os.makedirs('Karten', exist_ok=True)
karte_Chicago.save('Karten/Chicago_Karte.html')
karte_Chicago

# %% [markdown]
# Nun werden die Latitude und Longitude Koordinatenpaare jedes im Datenframe "data_cleaned" vorkommenden Verbrechen (s.O. für eine Liste der darin ausgeschlossenen Verbrechen) im Array lats_longs gespeichert. Daraus können wir dann eine Heatmap erstellen, in der alle in der Öffentlichkeit nach dem Jahr 2015 passierten Verbrechen gezeigt werden. Durch die Zoom Funktion besteht auch die Möglichkweit, mit simplen Mausbewegungen einzelne Blöcke und Straßen mit den dort geschehenen Verbrechen anzusehen.

# %%
lat_long = crimes_nach_2015[['Latitude', 'Longitude']].values.tolist()
karte_Chicago_Heatmap = karte_Chicago #Übertragen der vorher erstellten Karte zur Weiterverwendung
HeatMap(lat_long, 0.3).add_to(karte_Chicago_Heatmap)

karte_Chicago_Heatmap.save('Karten/Chicago_Heatmap.html')
karte_Chicago_Heatmap

# %% [markdown]
# Aus der Verteilung der Verbrechen in Chicago kann man den Schluss ziehen, das es in dichter besiedelten Gebieten mehr Verbrechen gibt. Um dies zu bestätigen, können wir mit der Folium Library auch einen Vergleich der Heatmap mit einer leeren Satellitenkarte herstellen.
#
# ### Vergleich mit Satellitenbildern
# Dafür erstellern wir zuerst ein neues Folium Kartenobjekt "vergleich":

# %%
vergleich = fl.plugins.DualMap(location=(41.849429, -87.597334), tiles=None, zoom_start=11, control_scale=True,)

# %% [markdown]
# Daraufhin erstellen wir die zwei untergeordneten Kartenobjekte m1 und m2, die zum Dualmap Kartenobjekt "vergleich" gehören. Als Kartenquelle fügen wir die Api der Esri World Imagery Karte ein, die frei verfügbar ist:
#
# https://www.arcgis.com/home/item.html?id=10df2279f9684e4a9f6a7f08febac2a9

# %%
fl.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri World Imagery',
).add_to(vergleich.m1);
fl.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Esri World Imagery',
).add_to(vergleich.m2);

# %% [markdown]
# Nun fügen wir wie oben die im Array "lats_longs" gespeicherten Koordinaten der Verbrechen als Heatmap zur "m1" Karte hinzu und zeigen die neue "vergleich" Karte danach an:

# %%
HeatMap(lat_long, 0.3).add_to(vergleich.m1)
#Steuerungsobjekte hinzufügen
fl.LayerControl(collapsed=True, show=False).add_to(vergleich)

#Ausgabe der Karte
vergleich.save('Karten/Chicago_Vergleich_Heatmap_Satellit.html')
vergleich

# %% [markdown]
# Wir können also sehen, das in dichter besiedelten und bebauten Gebieten mehr Verbrechen geschehen. Somit kann man als allgemeine Handlungsempfehlung sagen, das man für einen möglichst sicheren Chicago Trip dicht besiedelte Orte eher meiden sollte.
#
# Um nun konkretere Reiseempfelungen treffen zu können, sollte man interesannte Reiseziele oder Hotels erst in dieser Karte aufsuchen, um deren Sicherheit zu bestimmen. Als Beispiel fügen wir einige Hotels mit deren Koordinaten in die karte als Marker ein:

# %%
marker_Chicago_Heatmap = karte_Chicago_Heatmap
marker_Chicago_Heatmap.zoom_start= 11
marker_Chicago_Heatmap.location= [41.88612445681384, -87.63367468354781]

fl.Marker(
    location=[41.895194867728925, -87.61606169978471],
    tooltip="W Chicago - Lakeshore",
    popup="https://maps.app.goo.gl/kRhLEB6UwdkJGLiJA",
    icon=fl.Icon(color="red", icon="1", prefix='fa',),).add_to(marker_Chicago_Heatmap);
fl.Marker(
    location=[41.88612445681384, -87.63367468354781],
    tooltip="The Allegro Royal Sonesta Hotel Chicago Loop",
    popup="https://maps.app.goo.gl/eNWMsavhf1eFtzj47",
    icon=fl.Icon(color="red", icon="2", prefix='fa',),).add_to(marker_Chicago_Heatmap);
fl.Marker(
    location=[41.8378989795599, -87.65697241489531],
    tooltip="The Polo Inn Bed & Breakfast",
    popup="https://maps.app.goo.gl/U61Rx65AYDoEDjsu9",
    icon=fl.Icon(color="red", icon="3", prefix='fa',),).add_to(marker_Chicago_Heatmap);

marker_Chicago_Heatmap.save('Karten/Chicago_Heatmap_Marker.html')
marker_Chicago_Heatmap


# %% [markdown]
# Durch einen klick mit dem Mauszeiger kann auch direkt auf der Karte der Name des Hotels und der entsprechende Google Maps link eingesehen werden. Da aber nicht jeder die Karte interaktiv zur Hand haben wird, sind hier auch noch einmal die Informationen sowie die Sicherheitseinschätzung des Gebiets dem Datensatz zufolge aufgelistet:
#
# Hotel 1:  
# W Chicago - Lakeshore  
# https://maps.app.goo.gl/kRhLEB6UwdkJGLiJA  
# Einschätzung: Das "W Chicago - Lakeshore" Hotel ist offensichtlich keine gute Wahl, da der roten Umgebungsfarbe nach zu urteilen die Umgebung nicht sehr sicher ist. 
#
# Hotel 2:  
# The Allegro Royal Sonesta Hotel Chicago Loop  
# https://maps.app.goo.gl/eNWMsavhf1eFtzj47  
# Einschätzung: Auch dieses Hotel liegt in einem sehr roten Berreich, deshalb ist dem Datensatz nach zu schließen auch dieses Hotel und der umliegende Berreich zu meiden.  
#
# Hotel 3:  
# The Polo Inn Bed & Breakfast  
# https://maps.app.goo.gl/U61Rx65AYDoEDjsu9  
# Einschätzung: Dieses Hotel dagegen ist im Vergleich zum Rest von Chicago in einem sichereren Berreich, und ist deshalb dem Datensatz zufolge zu empfehlen
#
# ### Anwendung auf andere Hotels/Reiseziele
# Die Schritte sind somit:  
# 1: Ein Hotel auf einer Karte finden  
# 2: Das Hotel visuell auf der Heatmap aufsuchen und die Röte des Gebiets im Vergleich zum Rest der Heatmap begutachten  
# 3: Je nach Tiefe der Röte entscheiden, ob der Ort den Sicherheitsanforderungen entspricht  
#
# Wenn dieses Jupyter Notebook interaktiv zur Hand liegt (d.h. der Datensatz ist ebenfalls verfügbar), können auch Koordinaten eingegben werden, damit diese dann automatisch auf der Heatmap als Marker angezeigt werden. Da ein Input in einem Jupyter Notebook aber zu Problemen bei der Eingabe führen kann, ist diese Funktion in diesem Code standardmäßig deaktiviert. Die Schritte zur Verwendung der Funktion lauten wie folgt:
#
# 1: Die Variable input_verwenden auf True setzen ("False" mit "True" ersetzen) 
# 2: Ein Hotel und deren Koordinaten finden, z.B. auf Google Maps ein Hotel rechtsklicken, mit einem Klick auf die dann angezeigten Koordinaten werden diese dann kopiert.  
# 3: Die Koordinaten müssen im Format "Latitude, Longitude" sein (von Google Maps kopierte Daten sind automatisch auf diese Weise formatiert). Ein Beispiel ist "41.88409255624877, -87.63483254654416"  
# 4: Die untere Zelle ausführen  
# 5: Koordinaten in das angefragte Inputfeld einkopieren  
# 6: wenn gewünscht Name eingeben  
# 7: wenn gewünscht Link eingeben  
# 8: wenn gewünscht Kommando eingeben:  
#         "Stop": Stoppt die Eingabeschleife und gibt das Kartenobjekt aus  
#         Wenn nicht "Stop" eingegeben wird wird weiter nach Hotels abgefragt, bis Stop eingegeben wird. Dann wird eine Karte mit allen hinzugefügten Hotelmarkern angezeigt  
# 5: Enter drücken, die nächste Zelle ausführen und auf das Output warten  
#
#

# %%
input_verwenden = False
if (input_verwenden == True):
    karte_Chicago_Inputmarker = karte_Chicago_Heatmap
    input_command = " "
    while (input_command != "Stop"):
        #Eingaben abfragen und speichern
        input_koordinaten = input("Koordinaten: ")
        input_name = input("Name (kann auch leer sein): ")
        input_link = input("Link (kann auch leer sein): ")
        input_command = input("Command (kann auch leer sein, siehe oben): ")
        
        #Eingabe der Koordinaten aufteilen in zwei Float Variablen
        input_latitude, input_longitude = map(float, input_koordinaten.split(', '))
        
        #Marker zur Karte hinzufügen
        fl.Marker(
        location=[input_latitude, input_longitude],
        tooltip=input_name,
        popup=input_link,
        icon=fl.Icon(color="red", icon="bed", prefix='fa',),).add_to(karte_Chicago_Inputmarker);

# %%
#Karte ausgeben und speichern   
if (input_verwenden == True):
    karte_Chicago_Inputmarker.save('Karten/Chicago_Inputmarker_heatmap.html')
    display(karte_Chicago_Inputmarker)

# %% [markdown]
# # Vergleich früher/heute.

# %% [markdown]
# ## Vorbereitung der Daten.

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
# ## Klassifizierung der Verbrechen.

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
# ## Gruppierung nach Jahren.

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
# ## Schlussfolgerungen und Implikationen:

# %% [markdown]
# Nach den Daten ist es klar zu erkennen, dass die Anzahl der gemeldeten Straftaten seit 2001 stark gesunken ist, was eine positive Entwicklung nachweist.
# Nicht desto trotz ist die Anzahl der gemeldeten Diebstahlfälle im Jahr 2022 im Vergleich zum Jahr 2021 stark gewachsen, deswegen ist es ratsam, in einen Trip nach Chicago dies mitzurechnen und wertvolle Gegenstände nicht mit sich mitnehmen.
# Aber als klare Schlussfolgerung kann man sagen, dass Chicago heute viel sicherer ist im Vergleich zu früheren Jahren.
