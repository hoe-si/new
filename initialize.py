#/usr/bin/python3

import sqlite3
from sqlite3 import Error

dbpath = "database.db"
dbfile = sqlite3.connect(dbpath)
db = dbfile.cursor()
print("writing new database as: "+dbpath)
tables={"konto":(("kto","INTEGER"),("pin","INTEGER")),"transaktion":(("tid","INTEGER PRIMARY KEY"),("vonkto","INTEGER"),("ankto","INTEGER"),("betrag","INTEGER"),("erledigt","INTEGER"),("zeit","INTEGER"))}
for i in tables:
    fNt = ""
    for e in tables[i]:
        fNt+=e[0]+" "+e[1]+", "
    executeable = "create table {tn} ({fn})".format(tn = i, fn = fNt)
    db.execute(executeable[0:len(executeable)-4]+")")
    print("added table "+i)
dbfile.commit()
dbfile.close()
print("finished writing database")
