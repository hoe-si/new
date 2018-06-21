#/usr/bin/python3 

import sqlite3, random
from datetime import datetime


class DB():
    
    def __init__(this):
        #set a database
        this.dbpath = "database.db"
        this.dbfile = sqlite3.connect(this.dbpath)
        this.db = this.dbfile.cursor()
        print("apfel")
    #get the money
    def getM(this,kto):
        money = 0
        sql="select betrag from transaktion where ankto="+str(kto)+" AND erledigt=1;"
        add = this.db.execute(sql).fetchall()
        for i in add:
            money+=int(i[0])
        sql="select betrag from transaktion where vonkto="+str(kto)+" AND erledigt=1;"
        sub = this.db.execute(sql).fetchall()
        for i in sub:
            money-=int(i[0])
        return money
    #initialise transaction
    def initT(this,ktof,ktot,msum):
        #Generate the random tid
        tid=random.randint(1000,9999)
        while(len(this.db.execute("select * from transaktion where tid='"+str(tid)+"';").fetchmany(100))>=1):
            tid=random.randint(1000,9999)
        #genereate the timestamp
        apfel = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #prouce the sql
        vls = "("+str(tid)+","+str(ktof)+","+str(ktot)+","+str(msum)+",0,'"+str(apfel)+"')"
        #execute it!
        this.db.execute("insert into transaktion (tid,vonkto,ankto,betrag,erledigt,zeit) values "+vls+";")
        this.dbfile.commit()
        return tid
    #confirm the transaction
    def setT(this,tid):
        this.db.execute("update transaktion set erledigt = 1 where tid="+str(tid)+";")
        this.dbfile.commit()
    #check for the pin
    def checkP(this, kto, pin):
        f = this.db.execute("select pin from konto where kto='"+str(kto)+"';").fetchone()
        if str(f[0]) == str(pin):
            return True
        else:
            return False

