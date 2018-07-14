Dokumentation:

Den Server starten:
    Um den Server zu starten, muss eine valide Datenbank mit Kontodaten vorhanden sein, sowie die Datei conf.py, welche dem Server mitteilt, ob eine sqlite- oder eine mysql Datenbank verwendet werden soll
    Zudem muss conf.py ggf. die Logindaten zu einem mysql Server enthalten.
    Der das Serverskript ("server.py") kann ohne Argumente mittels eines Aufrufes des selben gestartet werden.
    
Die Gehaltsverteilung auslösen:
    Um die Gehaltsverteilung aus zu lösen, kass das Skript timerun.py (ohne Argumente) gestartet werden. Es berechnet, welcher Prozentsatz vom Guthaben von wohlhabenden Geschäften abgezogen werden muss, um ärmere Geschäfte dabei zu unterstützen, den Mindestlohn an seine Arbeiter aus zu zahlen.
    Wohlhabende Geschäfte sind dabei diejenigen, die mehr Geld besitzen als nötig wäre, um allen Arbeitern Mindestlohn zu überweisen.
    Der Steuersatz bezieht sich dabei lediglich auf das Geld, welches nach der Überweisung des Mindestlohns an alle Arbeiter noch übrig währe.