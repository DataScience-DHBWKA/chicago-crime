import numpy as np
import pandas as pd
import folium as fl
from folium.plugins import HeatMap
from folium.plugins import DualMap

#Dataset importieren
crime_2023 = pd.read_csv('deployment_dataset.csv')

#Heatmap erstellen, siehe Hauptnotebook für Erklärungen
karte_Chicago_Inputmarker = fl.Map(location = [41.863474, -87.613654], zoom_start = 11, control_scale=True,)
lat_long = crime_2023[['Latitude', 'Longitude']].values.tolist()
HeatMap(lat_long, radius=(30), blur=(30),).add_to(karte_Chicago_Inputmarker)

#Inputabfragen
input_verwenden = True
if (input_verwenden == True):
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
karte_Chicago_Inputmarker.save('Heatmap.html')