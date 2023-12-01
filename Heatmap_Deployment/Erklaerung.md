### Abfragen basierte Anwendung der Heatmap
Wenn dieses Jupyter Notebook interaktiv zur Hand liegt (d.h. der Datensatz ist ebenfalls verfügbar), können auch Koordinaten eingegben werden, damit diese dann automatisch auf der Heatmap als Marker angezeigt werden. Da ein Input in einem Jupyter Notebook aber zu Problemen bei der Ausführung führen kann, ist diese Funktion in diesem Code standardmäßig deaktiviert. Die Schritte zur Verwendung der Funktion lauten wie folgt:

1: Ein Hotel und deren Koordinaten finden, z.B. auf Google Maps ein Hotel rechtsklicken, mit einem Klick auf die dann angezeigten Koordinaten werden diese dann kopiert.  
2: Die Koordinaten müssen im Format "Latitude, Longitude" sein (von Google Maps kopierte Daten sind automatisch auf diese Weise formatiert). Ein Beispiel ist "41.88409255624877, -87.63483254654416"  
3: Die untere Zelle ausführen  
4: Koordinaten in das angefragte Inputfeld einkopieren  
5: wenn gewünscht Name eingeben  (ansonsten ohne Eingabe Enter drücken)
6: wenn gewünscht Link eingeben  
7: wenn gewünscht Kommando eingeben:  
> "Stop": Stoppt die Eingabeschleife und gibt das Kartenobjekt aus  

Wenn nicht "Stop" eingegeben wird wird weiter nach Hotels abgefragt, bis Stop eingegeben wird. 
8: Im gleichen Ordner Heatmap.html öffnen