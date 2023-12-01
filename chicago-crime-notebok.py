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

# %% [markdown]
# # Imports

# %%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium as fl
import os
from datetime import datetime
from folium.plugins import HeatMap
from folium.plugins import DualMap

# %% [markdown]
# # Einleitung

# %% [markdown]
# Als erstes lesen wir hier den Datensatz ein, und schauen uns ein paar Eigenschaften an, die für uns interressant sind.

# %%
chicago_crime_data = pd.read_csv('crimes-chicago-dataset.csv')

# %%
print('chicago_crime_data hat',chicago_crime_data.shape[1],'spalten und',chicago_crime_data.shape[0],'zeilen.' )

# %%
chicago_crime_data.head()

# %%
chicago_crime_data.info()

# %% [markdown]
# Hieraus können wir folgende, für uns weitergehend wichtige Erkenntnisse ziehen:
# 1. Wir wissen unser Code hat 7931583 Einträge mit 22 Datenspalten.
# 2. Wir haben eine Vorstellung davon, welche Daten wir vorliegen haben, um unser weiteres Vorgehen zu planen.
# 3. Wir wissen wie unsere Merkmalsausprägungen skaliert sind (die meisten nominal, aber z.B. die Spalte "Description" ist ordinal skaliert.
# 4. Wir können einordnen in welchen Datentypen die jeweiligen Daten gespeichert sind, und wissen wie wir weiter mit diesen vorgehen müssen.

# %% [markdown]
# # Data Cleaning
# Die meisten Datensätze sind nicht vollständig. Die fehlenden Felder können zum Beispiel entweder fehlender Sorgfalt beim Füllen des Datensatzes von Menschen geschuldet sein, oder manche Daten sind einfach nicht verfügbar. 
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
# # Ende Data Cleaning

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
# Große Städte verändern sich ständig. Stadtmittelpunkte, Touristenattraktionen und andere Orte von Menschenansammlungen verändern und verschieben sich, wenn neue Orte ausgebaut werden und alte Geschäfte/Viertel geschlossen werden. Deswegen werden wir für die Heatmap nur die Verbrechen beachten, die dieses Jahr geschehen sind. Dieser Zeitraum wurde so gewählt, weil so in den vergangenen 11 Monaten genügend Daten angefallen sind und die Geodaten aber trotzdem aktuell genug sein sollten, um verlässliche Aussagen über die Sicherheit der Orte zu treffen. Außerdem sind die Daten so weniger stark beinflusst von den temporär veränderten Öffentlichkeitsaufhalten der Bevölkerungen durch die Covid 19 Pandemie und deren Lockdowns, da im Jahr 2023 generell die meisten Beschränkungen aufgehoben wurden. 
#
# Wir erstellen also ein neues Dataframe, in dem nur die Verbrechen im Jahr 2019 enthalten sind:

# %%
crimes_2023 = data_cleaned.loc[data_cleaned['Year'] == 2023]

# %% [markdown]
# ### Kartenerstellung
# Wir beginnen, indem wir ein neues Kartenobjekt mit dem Namen "karte_Chicago" erstellen, dessen Mittelpunkt eine Koordinate in Chicago ist. Außerdem erstellen wir einen Ordner (falls dieser nicht bereits exisitert), in dem wir alle Karten speichern werden:

# %%
karte_Chicago = fl.Map(location = [41.863474, -87.613654], zoom_start = 11, control_scale=True,)
os.makedirs('Karten', exist_ok=True)

#Karte ausgeben und speichern
karte_Chicago.save('Karten/Chicago_Karte.html')
karte_Chicago

# %% [markdown]
# Nun werden die Latitude und Longitude Koordinatenpaare jedes im Datenframe "data_cleaned" vorkommenden Verbrechen (siehe oben für eine Liste der darin ausgeschlossenen Verbrechen) im Array lats_long gespeichert. Daraus können wir dann eine Heatmap erstellen, in der alle in der Öffentlichkeit im Jahr 2023 passierten Verbrechen gezeigt werden. Durch die Zoom Funktion besteht auch die Möglichkeit, mit simplen Mausbewegungen einzelne Häuserblöcke und Straßen mit den dort geschehenen Verbrechen anzusehen

# %%
lat_long = crimes_2023[['Latitude', 'Longitude']].values.tolist()
karte_Chicago_Heatmap = karte_Chicago #Referenzkopie der leeren Karte
HeatMap(lat_long, radius=(30), blur=(30),).add_to(karte_Chicago_Heatmap)

#Karte ausgeben und speichern
karte_Chicago_Heatmap.save('Karten/Chicago_Heatmap.html')
karte_Chicago_Heatmap

# %% [markdown]
# Aus der Verteilung der Verbrechen in Chicago kann man den Schluss ziehen, das es in dichter besiedelten Gebieten mehr Verbrechen gibt. Um dies zu bestätigen, können wir mit der Folium Library auch einen Vergleich der Heatmap mit einer leeren Satellitenkarte herstellen.
#
# ### Vergleich mit Satellitenbildern
# Dafür erstellern wir zuerst ein neues Folium DualMap Kartenobjekt "vergleich":

# %%
vergleich = fl.plugins.DualMap(location=(41.849429, -87.597334), tiles=None, zoom_start=11, control_scale=True,)

# %% [markdown]
# Daraufhin erstellen wir die zwei untergeordneten Kartenobjekte m1 und m2, die zum Dualmap Kartenobjekt "vergleich" gehören. Als Kartenquelle fügen wir für beide Karten die Api der Satellitenkarte "Esri World Imagery" ein, die frei verfügbar ist:
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
HeatMap(lat_long, radius=(30), blur=(30)).add_to(vergleich.m1)
#Steuerungsobjekte hinzufügen
fl.LayerControl(collapsed=True, show=False).add_to(vergleich)

#Karte ausgeben und speichern
vergleich.save('Karten/Chicago_Vergleich_Heatmap_Satellit.html')
vergleich

# %% [markdown]
# Wir können also sehen, das in dichter besiedelten und bebauten Gebieten mehr Verbrechen geschehen. Somit kann man als allgemeine Handlungsempfehlung sagen, das man für einen möglichst sicheren Chicago Trip dicht besiedelte Orte eher meiden sollte.
#
# ### Anwendung auf bestimmte Reiseziele
# Um nun konkretere Reiseempfelungen treffen zu können, sollte man interessante Reiseziele oder Hotels erst in dieser Karte aufsuchen, um deren Sicherheit zu bestimmen. Als Beispiel fügen wir einige Hotels mit deren Koordinaten in der Karte als Marker ein:

# %%
#Refernenzkopie der Karte auf ein neues Kartenobjekt, Zentrieren auf die Koordinaten von Hotel 2
marker_Chicago_Heatmap = karte_Chicago_Heatmap
marker_Chicago_Heatmap.zoom_start= 11
marker_Chicago_Heatmap.location= [41.88612445681384, -87.63367468354781]

#Hotelmarker hinzufügen
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

#Karte ausgeben und speichern
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
# #### Manuelle Verwendung der Karte
# Um ein anderes Hotel einschätzen zu können, müssen folgende Schritte befolgt werden:  
# 1: Ein Hotel auf einem Kartedienst finden (z.B. Google Maps)  
# 2: Das Hotel visuell auf der Heatmap aufsuchen und die Röte des Gebiets im Vergleich zum Rest der Heatmap begutachten  
# 3: Je nach Tiefe der Röte entscheiden, ob der Ort den Sicherheitsanforderungen entspricht  
#
#
# #### Abfragen basierte Anwendung der Heatmap
# Wenn dieses Jupyter Notebook interaktiv zur Hand liegt (d.h. der Datensatz ist ebenfalls verfügbar), können auch Koordinaten eingegben werden, damit diese dann automatisch auf der Heatmap als Marker angezeigt werden. Da ein Input in einem Jupyter Notebook aber zu Problemen bei der Ausführung führen kann, ist diese Funktion in diesem Code standardmäßig deaktiviert. Die Schritte zur Verwendung der Funktion lauten wie folgt:
#
# 1: Die Variable input_verwenden auf True setzen ("False" mit "True" ersetzen) 
# 2: Ein Hotel und deren Koordinaten finden, z.B. auf Google Maps ein Hotel rechtsklicken, mit einem Klick auf die dann angezeigten Koordinaten werden diese dann kopiert.  
# 3: Die Koordinaten müssen im Format "Latitude, Longitude" sein (von Google Maps kopierte Daten sind automatisch auf diese Weise formatiert). Ein Beispiel ist "41.88409255624877, -87.63483254654416"  
# 4: Die untere Zelle ausführen  
# 5: Koordinaten in das angefragte Inputfeld einkopieren  
# 6: wenn gewünscht Name eingeben  
# 7: wenn gewünscht Link eingeben  
# 8: wenn gewünscht Kommando eingeben:  
# > "Stop": Stoppt die Eingabeschleife und gibt das Kartenobjekt aus  
#
# Wenn nicht "Stop" eingegeben wird wird weiter nach Hotels abgefragt, bis Stop eingegeben wird. Dann wird eine Karte mit allen hinzugefügten Hotelmarkern angezeigt  
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
#
# # Sichere Tageszeiten?

# %% [markdown]
# Hier stellen wir die jeweilige Tageszeiten, zu denen Verbrechen geschehen sind, als Histogramm dar.
# Wir müssen zuerst die Date Spalte von Objects zu Datetimes konvetieren, um dann mit diesen einen Plot erstellen zu können, indem wir aus der Datetime direkt die Stunde rausziehen.

# %%
#Umformatierung der Daten zu Datetimes
data_cleaned['Date'] = pd.to_datetime(data_cleaned['Date'], format='%m/%d/%Y %I:%M:%S %p')
day_of_month_chicago_crime_data = data_cleaned['Date'].dt.hour
fig = sns.histplot(day_of_month_chicago_crime_data, kde=False, bins=24)
fig.set(xlabel='Hour', ylabel='Amount of commited Crimes')


# %% [markdown]
# Im Histogramm können wir nun die Tageszeiten der begangenen Verbrechen sehen.
# Man sieht deutlich, dass nachts (5 Uhr) am wenigsten Verbrechen geschehen, und diese fast stetig bis 18 Uhr zunehmen, und diese Anzahl sich wieder bis 5 Uhr verringert. Ausnahme davon sind 0 und 12 Uhr, unsere Vermutung hier ist, dass Verbrechen, bei denen nur eine ungefähre Uhrzeit zur Verfügung stand, entweder auf 0 oder auf 12 Uhr ab/aufgerundet wurden.
#
# Auf ersten Blick würde man also denken, dass die sicherste Tageszeit für einen Trip die Nacht wäre, aber da nachts normalerweise weniger Menschen aktiv sind, ist diese Statistik etwas trügerisch.
# Unser Fazit hier ist, dass wir aus diesem Histogramm leider keine erkenntliche Einsicht über eine empfehlenswerte Tageszeit zum rausgehen gewinnen können.

# %% [markdown]
# # Sichere Jahreszeiten?

# %% [markdown]
# Wir fangen an, indem wir eine Methode definieren, die uns die Jahreszeit je nach Monat angibt.
# Danach erstellen wir eine neue Spalte, die uns die Jahreszeit des jeweiligen Verbrechens zurückgibt.
# Wir erstellen daraufhin ein Balkendiagramm, dass uns eine visuelle Übersicht über die jeweilige Jahreszeit gibt.
#

# %%
def get_season(date):
    month = date.month
    if 3 <= month <= 5:
        return "Frühling"
    elif 6 <= month <= 8:
        return "Sommer"
    elif 9 <= month <= 11:
        return "Herbst"
    else:
        return "Winter"

data_cleaned['Jahreszeit'] = data_cleaned['Date'].apply(get_season)

chicago_crime_data_grouped = data_cleaned.groupby('Jahreszeit')['Case Number'].size()

plt.bar(chicago_crime_data_grouped.index, chicago_crime_data_grouped.values, color=['green', 'orange', 'red', 'blue'])
plt.title('Balkendiagramm nach Jahreszeiten')
plt.xlabel('Jahreszeit')
plt.ylabel('Summe der Werte')
plt.show()

# %% [markdown]
# Man kann deutlich sehen, dass die Anzahl der Verbrechen im Vergleich zu den Anderen Jahreszeiten im Winter stark sinkt, während im Sommer mehr Verbrechen geschehen.
# Für einen Trip nach Chicago würde sich also definitv der Winter anbieten!

# %% [markdown]
# # Klassifizierung der Verbrechen
# ### Klassifizierung

# %% [markdown]
# In unserem Datensatz sowie im echten Leben gibt es viele verschiedene Verbrechenskategorien. Diese variieren von vergleichsweise harmlosen Gesetzesverstößen wie Taschendiebstahl bis hin zu schweren Verbrechen wie Mord. Nicht alle Verbrechen betreffen uns aber als Urlauber in Chicago. 'LIQUOR LAW VIOLATION', d.H. ein Spirituosen Gesetzes Verstoß betrifft und als Urlauber nicht, obwohl es durchaus für die  Stadt ein größeres Problem darstellen könnte. Deshalb teilen wir die vielen verschiedenen Verbrechensarten in die zwei Kategorien schwerwiegend_Urlaub und belanglos_Urlaub ein. Besonders schwerwiegende Verbrechen, wie zum Beispiel solche, die schwere Sach-, Personen- oder psyschiche Schäden verursachen werden und von welchen wir als Urlauber ebenfalls potenziell betroffen sein könnten, werden als als schwerwiegend eingestuft, Verbrechen die eher geringfügige Schäden verursachen werden hingegen als weniger schwerwiegend eingestuft.
#
# Dazu rufen wir zunächst alle einzigartigen Verbrechensarten in der Kategorie 'Primary Type' auf und geben die daraus resultierende Liste mit print() aus:

# %%
unique_types = data_cleaned['Primary Type'].unique()
print(unique_types)

# %% [markdown]
# Nach einiger Überlegung und Evaluation stufen wir nun die folgenden Verbrechen als schwerwiegend für Urlauber ein: 'THEFT', 'ASSAULT', 'WEAPONS VIOLATION','SEX OFFENSE','CRIM SEXUAL ASSAULT','MOTOR VEHICLE THEFT','CRIMINAL TRESPASS','ROBBERY','PUBLIC PEACE VIOLATION','CRIMINAL SEXUAL ASSAULT','HOMICIDE', 'KIDNAPPING' und 'HUMAN TRAFFICKING'. Diese werden in der Liste schwerwiegend_Urlaub als Zeichenkette gespeichert:

# %%
schwerwiegende_verbrechen = ['THEFT', 'ASSAULT', 'WEAPONS VIOLATION','SEX OFFENSE','CRIM SEXUAL ASSAULT','MOTOR VEHICLE THEFT','CRIMINAL TRESPASS','ROBBERY','PUBLIC PEACE VIOLATION','CRIMINAL SEXUAL ASSAULT','HOMICIDE', 'KIDNAPPING','HUMAN TRAFFICKING']


# %% [markdown]
# Jetzt werden die Verbrechen im gesamten Datensatz bewertet und als "Schwerwiegend" oder "Nicht Schwerwiegend" entsprechend eingestuft. 
#
# Dazu erstellen wir die Methode "klassifizieren". Diese nimmt als Parameter einen 'crime_type' String. Wenn dieser Parameter in der Liste schwerwiegende_verbrechen enthalten ist, gibt die Methode 'Schwerwiegend' aus, wenn nicht wird 'Nicht Schwerwiegend' ausgegeben: 

# %%
def klassifizieren(crime_type):
    if crime_type in schwerwiegende_verbrechen:
        return 'Schwerwiegend'
    else:
        return 'Nicht Schwerwiegend'


data_cleaned['Schwere Klassifizierung'] = data_cleaned['Primary Type'].apply(klassifizieren)

# %% [markdown]
# ### Gruppierung nach Jahren

# %% [markdown]
# Um die Analyse durchführen zu können, werden jetzt die Daten nach Jahren gruppiert, und die Anzahl schwerwiegende und nicht schwerwiegende Verbrechen für jedes Jahr summiert.

# %%
gruppe = data_cleaned.groupby(['Year', 'Schwere Klassifizierung']).size().unstack()
gruppe = gruppe.fillna(0)
print(gruppe)

# %% [markdown]
# Diese Daten werden jetzt in Graphen, um Sie zu veranschaulichen, präsentiert.

# %%
gruppe.plot(kind='bar', stacked=True, color=['lightgrey','#FF6347'])
plt.title('Anzahl der schwerwiegenden und nicht-schwerwiegenden Verbrechen pro Jahr')
plt.xlabel('Jahr')
plt.ylabel('Anzahl Verbrechen')
plt.legend(title='Schwere Klassifizierung')
plt.show()

# %%
gruppe['Schwerwiegend'].plot(kind='line', color='red', marker='o', label='Schwerwiegend')
gruppe['Nicht Schwerwiegend'].plot(kind='line', color='gray', marker='o', label='Nicht Schwerwiegend')
plt.title('Anzahl der schwerwiegenden und nicht-schwerwiegenden Verbrechen pro Jahr')
plt.xlabel('Jahr')
plt.ylabel('Anzahl Verbrechen')
plt.legend(title='Schwere Klassifizierung')
plt.show()

# %% [markdown]
# Es ist zu erkennen, dass die Gesamtzahl an Verbrechen sich stark reduziert hat. Aber es ist nicht wegzulassen, dass im Jahr 2022 die Anzahl an schwerwiegenden Verbrechen stark gewachsen ist, und diese zum ersten Mal die Anzahl der nicht schwerwiegende Verbrechen übertroffen hat.

# %% [markdown]
# Diesen Ereigniss wird nochmal tiefer untersucht, um zu sehen welche konkrete verbrechen am meisten zugenommen haben.

# %% [markdown]
# Dafür werden die Daten aus den Jahren 2021 und 2022 extrahiert

# %%
schwere_verbrechen_2021 = data_cleaned[
    (data_cleaned['Schwere Klassifizierung'] == 'Schwerwiegend') &
    (data_cleaned['Year'] == 2021)
]
schwere_verbrechen_2022 = data_cleaned[
    (data_cleaned['Schwere Klassifizierung'] == 'Schwerwiegend') &
    (data_cleaned['Year'] == 2022)
]

# %% [markdown]
# Und dann werden davon die Schwerwiegende verbrechen gruppiert und extrahiert. Die Nicht Schwerwiegende werden ignoriert.

# %%
schwere_verbrechen_2021_anzahl = schwere_verbrechen_2021.groupby('Primary Type').size().sort_values(ascending=False)
schwere_verbrechen_2022_anzahl = schwere_verbrechen_2022.groupby('Primary Type').size().sort_values(ascending=False)

# %% [markdown]
# Und zulätzt für jeden Konkretes Schwerwiegendes Verbrechen die zunahme berechnet.

# %%
zunahme_schwere_verbrechen_2022_vs_2021 = schwere_verbrechen_2022_anzahl - schwere_verbrechen_2021_anzahl
print(zunahme_schwere_verbrechen_2022_vs_2021)

# %%
zunahme_schwere_verbrechen_2022_vs_2021.plot(kind='bar', color='red')
plt.title('Zunahme schwerwiegender Verbrechen 2022 vs. 2021')
plt.xlabel('Verbrechenstyp')
plt.ylabel('Zunahme')
plt.xticks(rotation=90)
plt.show()

# %% [markdown]
# Es ist klar zu erkennen, dass Verbrechen, die mit Diebstahl zu tun haben, im Jahr 2022 stark gewachsen sind.

# %% [markdown]
# ### Schlussfolgerungen und Implikationen:

# %% [markdown]
# Nach der durchgeführten Analyse ist es schlusszufolgern, dass die Anzahl der gemeldeten Straftaten seit 2001 stark gesunken ist, was eine positive Entwicklung nachweist.
# Nicht desto trotz ist die Anzahl der gemeldeten Diebstahlfälle im Jahr 2022 im Vergleich zum Jahr 2021 stark gewachsen, deswegen ist es ratsam, in einem Trip nach Chicago dies bei der Reisevorbereitung zu beachten und wertvolle Gegenstände nicht mit sich mitzunehmen.
# Aber es ist als Schlussfolgerung zu sagen, dass Chicago heute viel sicherer ist im Vergleich zu früheren Jahren.
