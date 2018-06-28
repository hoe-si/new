#/usr/bin/python3 

import sqlite3, random
from time import time


class DB():
    
    def __init__(this):
        #set a database
        this.dbpath = "database.db"
        this.dbfile = sqlite3.connect(this.dbpath)
        this.db = this.dbfile.cursor()
        print("apfel")
        
    #get the money
    def getKontostand(this,kto):
        money = 0
        sql="select betrag from transaktion where ankto='"+str(kto)+"' AND erledigt=1;"
        add = this.db.execute(sql).fetchall()
        for i in add:
            money+=int(i[0])
        sql="select betrag from transaktion where vonkto='"+str(kto)+"' AND erledigt=1;"
        sub = this.db.execute(sql).fetchall()
        for i in sub:
            money-=int(i[0])
        return money
        
    #initialise transaction
    def initTransaktion(this,ktof,ktot,msum):
        #Generate the random tid
        tid=random.randint(1000000,9999999)
        while(len(this.db.execute("select * from transaktion where tid='"+str(tid)+"';").fetchmany(100))>=1):
            tid=random.randint(1000,9999)
        #genereate the timestamp
        apfel = time()
        #prouce the sql
        vls = "("+str(tid)+","+str(ktof)+","+str(ktot)+","+str(msum)+",0,'"+str(apfel)+"')"
        #execute it!
        this.db.execute("insert into transaktion (tid,vonkto,ankto,betrag,erledigt,zeit) values "+vls+";")
        this.dbfile.commit()
        return tid
        
    #confirm the transaction
    def setErledigt(this,tid,vonkto,ankto,betrag):
        apfel = this.db.execute("select * from transaktion where tid='"+str(tid)+"' and vonkto='"+str(vonkto)+"' and ankto='"+str(ankto)+"' and betrag='"+str(betrag)+"';").fetchmany(2)
        if(len(apfel)>= 1):
            this.db.execute("update transaktion set erledigt = 1 where tid='"+str(tid)+"';")
            this.dbfile.commit()
        
    #check for the pin
    def checkPin(this, kto, pin):
        
        checkLogfileSql="select * from logfile where erledigt=0 and zeit > " + str(time()-5*60) + " and  kto='"+str(kto) + "';"
        wrongKeyTries=this.db.execute(checkLogfileSql).fetchmany(101)
        
        f = this.db.execute("select pin from konto where kto='"+str(kto)+"' and pin='"+str(pin) + "';").fetchmany(2)
        success = len(f)==1
        timestamp = time()
        logfile_sql="insert into logfile(zeit,kto,erledigt) values ('" + str(timestamp) + "','" + str(kto) + "','" + str(int(success)) + "');"
        this.db.execute(logfile_sql)
        print(success)
        print(wrongKeyTries)
        return success and len(wrongKeyTries) <= 100
        

