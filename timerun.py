#! /usr/bin/python3

import dbmanager

db = dbmanager.DBsqlite()

curs = db.dbfile.cursor()
curs.execute("select distinct gkto from gruppen")
groups= curs.fetchall()
curs.close()
for i in groups:
    groupCurs = db.dbfile.cursor()
    groupMoney = db.getKontostand(i["gkto"])
    groupCurs.execute('select skto from gruppen where gkto = '+ str(i["gkto"])+' ;')
    pupsOfGroup = groupCurs.fetchall()
    pupMoney = int(groupMoney/len(pupsOfGroup))
    print("group:"+ str(i))
    for a in pupsOfGroup:
        print(a)
        tid = db.initTransaktion(i["gkto"],a["skto"],pupMoney)
        db.setErledigt(tid,i["gkto"],a["skto"],pupMoney)
    groupCurs.close()