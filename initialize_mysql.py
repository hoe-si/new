#! /usr/bin/python3

import pymysql, random
from conf import a as conf
dbpath = "hoesi"
dbfile = pymysql.connect(host='localhost',
                         user=conf["user"],
                         password=conf["password"],
                         db='hoesi',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
db = dbfile.cursor()
print("writing new database into mysql database "+dbpath)
#tables={"konto":(("kto","INTEGER"),("pin","INTEGER")),"transaktion":(("tid","INTEGER PRIMARY KEY"),("vonkto","INTEGER"),("ankto","INTEGER"),("betrag","INTEGER"),("erledigt","INTEGER"),("zeit","INTEGER")),"logfile":(("zeit","INTEGER"),("kto","INTEGER"),("erledigt","INTEGER")),"gruppen":(("skto","INTEGER PRIMARY KEY"),("gkto","INTEGER"))}
#for i in tables:
#    fNt = ""
#    for e in tables[i]:
#        fNt+=e[0]+" "+e[1]+", "
#    executeable = "create table {tn} ({fn})".format(tn = i, fn = fNt)
#    db.execute(executeable[0:len(executeable)-4]+")")
#    print("added table "+i)
#create groups
for i in range(20000,20003):
    pin = random.randint(1000,9999)
    db.execute("insert into konto (kto, pin) values ("+str(i)+","+str(pin)+")")
#create pupils
groups = (20000,20002,20001)
for i in range(10000,10050):
    grp = groups[random.randint(0,2)]
    pin = random.randint(1000,9999)
    db.execute("insert into konto (kto, pin) values ("+str(i)+","+str(pin)+");")
    db.execute("insert into gruppen (skto,gkto) values("+str(i)+","+str(grp)+");")
    db.execute("insert into transaktion (tid,vonkto,ankto,betrag,erledigt,zeit) values("+str(i)+",00000,"+str(i)+",10,1,0)")
#save everything
dbfile.commit()
dbfile.close()
print("finished writing database")
