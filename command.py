import cmd,dbmanager,conf,time
from printer import *

dbsheme = {"konto":(("kto","INTEGER"),("pin","INTEGER")),"transaktion":(("tid","INTEGER PRIMARY KEY"),("vonkto","INTEGER"),("ankto","INTEGER"),("betrag","INTEGER"),("erledigt","INTEGER"),("zeit","INTEGER")),"logfile":(("zeit","INTEGER"),("kto","INTEGER"),("erledigt","INTEGER")),"gruppen":(("skto","INTEGER PRIMARY KEY"),("gkto","INTEGER"))}

dbmanager.conf= conf.a

if conf.dbtype == "sqlite":
    db = dbmanager.DBsqlite()
else:
    db = dbmanager.DBmysql()


class commands(cmd.Cmd):
    
    def __init__(self):
        super()
        pass
    
    def do_copy(self):
        iprint('Mit diesem Befehl wird unter nachfolgendem Namen im Ordner "safe" eine Sicherungskopie angelegt. Es besteht die möglichkeit den vom Programm vorgeschlagenen Namen zu modifizieren. Davon wird allerdings abgeraten, da dies zu Folge hat, dass bei einer Wiederherstellung der Sicherungskopie eine nicht aktuelle Datei verwendet wird.',imp=2)
        space(2)
        newname = time.ctime()
        newname = newname.replace(" ","_") + ".db"
        newname = imput("Name der Sicherungskopie:", newname)
        
        safeDb = setupSqlite()
        safeCurs = safeDb.cursor()
        curs = safeDb.cursor()
        for i in dbsheme.keys():
            curs.execute("select * from " + i)
            data = curs.fetchall()
            safeCurs.
        