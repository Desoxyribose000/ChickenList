# ChickenList
Zusätzlich zu allen standart Einrichtungsschritten müssen für die GUI-Anwendung
folgende Umgebungsvariablen gesetzt werden:


Pycharm Debug Configuration:
DBUSER=mainAccess
DBHOST=chickenlist2.cw6wqybtdspv.us-east-1.rds.amazonaws.com
DBPASSWD=6M98EPzBt0Ll0jM2
DBNAME=postgres
WEBHOST=http://ec2-174-129-186-136.compute-1.amazonaws.com			 nur in ChickenList, nicht in ChickenListCloud

Zum Umfang:
Das Projet umfasste 3 Abschnitte:
1. Qualitätscheck
Hier habe ich im wesentlichen die Dateien, nach ihrer Funktion getrennt. UI in UI.py, Datenbankabfragen in db_access.py etc.
Weiterhin habe ich entsprechend der Empfehlung von PyCharm die meisten PeP8 verstöße beseitigt.
Und schließlich kleinere Bugs gefixed. (z.B.: kein refresh in AddTerminMultiple, dadurch bei start mit leerer DB keine Verwendbarkeit)

2. Erweiterung der Standartfunktionen:
Dazu habe ich das ändern der Daten vom Besitzer und der Impftermine eingeführt. 
Die entsprechenden neuen Klassen sind Mit OOSL gekennzeichnet, um sie von den bereits bestehenden abzuheben.

3. Erweitern um Extrafunktionen:
Die erste Extrafunktion die Ich eigeführt habe, war die Funktion PDFs erstellen lassen zu können.
	Dazu gibt es 2 Versionen, die erste für das Amt, welches benötigt wird, wenn ein Impfstatus nachgewiesen werden muss.
	Die zweite Version ist eine für den Besitzer, die Ihm die möglichkeit verschafft sich über den Impfstatus zu erkundigen.

Und damit zur zwieten wesentlichen Funtktion: der online Abfrage:

Das Programm erstellt hierzu einen QR-Code und speichert diesen auf dem PDF ab.
Dieser scannbare QR-Code enthält eine URL, die auf meine Webseite zeigt. 
Ausserdem übergibt diese als Parameter einen gehashten String aus dem Nachnamen, der Impftermin ID und einem random String
und als zweiten Parameter den String.	(2.1)
Dies soll dafür sorgen, dass keine internen Daten einfach lesbar übers Netz verschickt werden.	(2.5)

Die Webseite sucht, wenn sie mit diesen 2 Parametern angefragt wird, in der Datenbank nach allen Benutzern und deren Impfterminen.
Der Server hasht alle Nachnamen + iid mit dem string aus dem GET-Parameter und sucht nach übereinstimmungen mit den Hashcode. (2.3)

Wenn eine solche gefunden wurde, werden der letzte, der nächste Impftermin und die vergangene Zeit seit dem letzten Termin ausgegeben.
Zudem wird eine Kurze Statusmitteilung gegeben, ob man sich um einen neuen Termin bemühen sollte. (2.4)
