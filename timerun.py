#! /usr/bin/python3.6

import dbmanager
from printer import iprint

db = dbmanager.DBsqlite()

curs = db.dbfile.cursor()
mindestlohn= 5

# finde Fehlendes und überflüssiges Geld bei den Gruppen

curs.execute("select distinct gkto from gruppen")
gruppen = curs.fetchall()
leftMoney = {}
lessMoney = {}
transferPerGroup = {}
for i in gruppen:
    curs.execute("select skto from gruppen where gkto = " + str(i["gkto"]) + ";")
    schuler = curs.fetchall();
    schulermenge = len(schuler)
    print("Gruppe ", i["gkto"], "besitzt", schulermenge, "Arbeiter")
    gmoney = db.getKontostand(i["gkto"])
    neededMoney = schulermenge * mindestlohn
    rest = gmoney - neededMoney
    if rest > 0:
        leftMoney.update({i["gkto"]:rest})
    else:
        lessMoney.update({i["gkto"]:rest*-1})
        
lessMoneySum = sum(lessMoney.values())
leftMoneySum = sum(leftMoney.values())
old = db.getKontostand(1)
print("lessMoney groups: ",lessMoney)
print("leftMoney groups: ",leftMoney)
print("\n\n\n\n")
if old < 0:
    lessMoneySum += old * -1
else:
    leftMoneySum += old

if leftMoneySum == 0:
    tax = 10
else:
    tax = lessMoneySum/leftMoneySum


print("Um alle durch den Mindestlohn entstandenen Verluste der Bank zu korrigieren, müsste ein Steuersatz von "+ str(tax * 100) +r"% erhoben werden",2)
iprint("Es besteht die Möglichkeit den errechneten Optimalsteuersatz zu korrigieren. Da der Mindestlohn weiterhin ausgezahlt wird, hätte dies zur Folge, dass Konto 1 entweder negativ wird, oder eine Summe an geld aufgespart wird, um bei der nächsten Gehaltsauszahlung die Steuern zu reduzieren.\n\n",2)
if tax >1:
    iprint("Der Sterersatz beträgt mehr als 100 Prozent",7)
    print("""Damit würden die Mitarbeiter Von Geschäften, welche ihre Kosten decken können, weniger als den Mindestlohn erhalten!
        Wir raten dringend davon ab, den Steuersatz bei diesem Wert zu belassen.""", "\n\n\n")
userTax=input("Gewünschter Steuersatz in Prozent [" + str(tax * 100) +"] :")
if userTax != "":
    tax = float(userTax)/100


curs.close()
for i in gruppen:
    print("Gruppe "+ str(i["gkto"]))
    groupCurs = db.dbfile.cursor()
    groupMoney = db.getKontostand(i["gkto"])
    if i["gkto"] in leftMoney.keys():
        endTax = int(leftMoney[i["gkto"]] * tax)
        taxTid = db.initTransaktion(i["gkto"],1,endTax)
        db.setErledigt(taxTid,i["gkto"],1,endTax)
        print("es wurden ", endTax, " von Gruppe ", i["gkto"], " abgezogen.")
    else:
        endTax = lessMoney[i["gkto"]]
        taxTid = db.initTransaktion(1,i["gkto"],endTax)
        db.setErledigt(taxTid,i["gkto"],1,endTax)
        print("es wurden ", endTax, " an Gruppe ", i["gkto"], "überwiesen.")
    groupCurs.execute('select skto from gruppen where gkto = '+ str(i["gkto"])+' ;')
    pupsOfGroup = groupCurs.fetchall()
    pupMoney = int(groupMoney/len(pupsOfGroup))
    for a in pupsOfGroup:
        print("Schüler ",a["skto"])
        tid = db.initTransaktion(i["gkto"],a["skto"],pupMoney)
        db.setErledigt(tid,i["gkto"],a["skto"],pupMoney)
    groupCurs.close()