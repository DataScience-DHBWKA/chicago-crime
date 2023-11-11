# Chicago-Crime
## Group Members:
- Eduardo Stein Mössner
- Benjamin Esch
- Christof Warsinsky
- Vincent Merkel
## Unsere Fragestellung
Wir finden eine spannende und passende frage zu unserem Projekt wäre, wie solltet man Urlaub nach Chicago planen?
## Leitfragen
- Welche regionen sind am gefährlichsten in Chicago?
- Wo sind die meiste schwerwiegende verbrechen geschehen?

## Jupytext installieren:
Einleitung: Da das mergen von .jypnb Dateien fast immer Konflikte verursacht, müssen wir eine Art workaround verwenden. Anstatt eine .jypnb Datei auf Github zu haben, die wir verändern und mergen, speichern wir unser Notebook mit der jupytext Anwendung als .py Datei (im percent Format). Wenn du nun daheim am Notebook arbeiten willst, lade dir einfach mit pull die neueste Version des repositorys runter und öffne die .py Datei dann in Jupyterlab als Notebook. Wenn du dann speicherst, wird vollautomatisch eine lokale .jypnb Datei erstellt, in der du dann arbeitest. Deine Änderungen werden dabei sowohl in der .jpynb Datei als auch in der .py Datei gespeichert, wenn du dann aber commitest (=hochlädst), wird nur die .py Datei hochgeladen. So vermeiden wir die konflikte, da .py Dateien sich konfliktlos mergen lassen

mehr infos: https://github.com/mwouts/jupytext

***Um mit Jupytext arbeiten zu können (benötigt für dieses Projekt), musst du die folgenden Schritte befolgen***

1: Anaconda Navigator > Enviroments > Base(root) > "Play button drücken" > open terminal

2: Eingeben: 
pip install jupytext

*Die Schritte ab hier musst du jedes Mal machen wenn du am Projekt arbeiten willst:*

3: Jupyter Lab starten

4: chicago-crime-notebook.py in Jupyterlab rechtsklicken > open with > notebook

5: Datei, save

6: Jetzt gibt es eine lokale .jypnb jupyter notebook datei *(bzw deine veraltete .jpynb Datei wird aktualisiert.* Diese Doppelklicken in Jupyterlab

7: Run > Run All Cells

Diese Datei kannst du dann verändern, wenn du speicherst werden die Änderungen automatisch auf .py und auf .jpynb gespeichert.
Wenn du commitest, wird nur die .py Datei übertragen, da sich mit dieser konfliktlos arbeiten lässt :)

Übrigens: Deine .jpynb Datei wird automatisch beim Commit Prozess ignoriert. Benutze also gerne den projektordner als Arbeitsordner, du musst die .jypnb Datei nicht extra löschen

## Datensatz installieren:
1: Datensatz runterladen:
```    
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2
```
export Button > CSV

- *Online Benutzung des Datensatzes wäre zwar möglich, ist aber langsamer und dann muss bei jeder Benutzung der Link neu eingegeben werden. Deshalb bitte einfach die Anweisungen hier befolgen, denn sonst wird bei jedem commit der Datensatz Ort im Notebook verändert --> alle andern müssen ihn dann wieder bei sich ändern. Mit der hier gezeigten Methode bleibt es konsistent und jeder kann einfach loslegen mit programmieren, ohne den Datensatz Ort zu verändern*

2: Datei umbenennen auf:
```
crimes-chicago-dataset
```
*csv Dateiendung beibehalten*

3: Den Datensatz jetzt in den Projektordner verschieben (der Ordner chicago-crime, der nach dem pullen von github auf deinem Pc erstellt wird)

4: Jetzt kann der das Notebook ausgeführt werden und der Datensatz sollte sofort richtig erkannt werden

***Datensatz nicht woanders speichern und im Code den Ort ändern, das das nach dem Commit alle beinflusst***
