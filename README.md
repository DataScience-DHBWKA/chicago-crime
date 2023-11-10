# Chicago-Crime
## Group Members:
- Eduardo Stein Mössner
- Benjamin Esch
- Christof Warsinsky
- Vincent Merkel
## Unsere Fragestellung
Wir finden eine spannende und passende frage zu unserem Projekt wäre, wie solltet man Urlaub nach Chicago planen?
## Konkretere fragen um unseren Projekt zu leiten
- Welche regionen sind am gefährlichsten in Chicago?
- Wo sind die meiste schwerwiegende verbrechen geschehen?

## jupytext installieren:
Einleitung: Da das mergen von .jypnb Dateien fast immer Konflikte verursacht, müssen wir eine Art workaround verwenden. Anstatt eine .jypnb Datei auf Github zu haben, die wir verändern und mergen, speichern wir unser Notebook mit der jupytext Anwendung als .py Datei (im percent Format). Wenn du nun daheim am Notebook arbeiten willst, lade dir einfach mit pull die neueste Version des repositorys runter und öffne die .py Datei dann in Jupyterlab als Notebook. Wenn du dann speicherst, wird vollautomatisch eine lokale .jypnb Datei erstellt, in der du dann arbeitest. Deine Änderungen werden dabei sowohl in der .jpynb Datei als auch in der .py Datei gespeichert, wenn du dann aber commitest (=hochlädst), wird nur die .py Datei hochgeladen. So vermeiden wir die konflikte, da .py Dateien sich konfliktlos mergen lassen

mehr infos: https://github.com/mwouts/jupytext

***Um mit jupytext arbeiten zu können (benötigt für dieses Projekt), musst du die folgenden Schritte befolgen***

1: Anaconda Navigator > Enviroments > Base(root) > "Play button drücken" > open terminal

2: Eingeben: 
pip install jupytext

*Die Schritte ab hier musst du jedes Mal machen wenn du am Projekt arbeiten willst:*

3: Jupyter Lab starten

4: chicago-crime-notebook.py in Jupyterlab rechtsklicken > open with > notebook

5: Datei, save

6: Jetzt gibt es eine lokale .jypnb jupyter notebook datei *(bzw deine veraltete .jpynb Datei wird aktualisiert.* Diese Doppelklicken in Jupyterlab

Diese kannst du dann verändern, wenn du speicherst werden die Änderungen automatisch auf .py und auf .jpynb gespeichert.
Wenn du commitest, wird nur die .py Datei übertragen, da sich mit dieser konfliktlos arbeiten lässt :)

Übrigens: Deine .jpynb Datei wird automatisch beim Commit Prozess ignoriert. Benutze also gerne den projektordner als Arbeitsordner, du musst die .jypnb Datei nicht extra löschen
