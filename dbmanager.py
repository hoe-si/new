#/usr/bin/python3 

import sqlite3, random, pymysql
import pymysql.cursors
from time import time

from dbconf import a as conf







class DB():
    
    def __init__(this):
        #set a database
        return None
        
    #get the money
    def getKontostand(this,kto):
        db= this.dbfile.cursor()
        money = 0
        sql="select betrag from transaktion where ankto='"+str(kto)+"' AND erledigt=1;"
        db.execute(sql)
        add = db.fetchall()
        for i in add:
            money+=int(i["betrag"])
        sql="select betrag from transaktion where vonkto='"+str(kto)+"' AND erledigt=1;"
        db.execute(sql)
        sub = db.fetchall()
        for i in sub:
            money-=int(i["betrag"])
        return money
        db.close()

        
    #initialise transaction
    def initTransaktion(this,ktof,ktot,msum):
        db= this.dbfile.cursor()
        #Generate the random tid
        tid=random.randint(1000000,9999999)
        db.execute("select * from transaktion where tid='"+str(tid)+"';")
        while(len(db.fetchmany(100))>=1):
            tid=random.randint(1000,9999)
            db.execute("select * from transaktion where tid='"+str(tid)+"';")
            
        #genereate the timestamp
        apfel = time()
        #prouce the sql
        vls = "("+str(tid)+","+str(ktof)+","+str(ktot)+","+str(msum)+",0,'"+str(apfel)+"')"
        #execute it!
        db.execute("insert into transaktion (tid,vonkto,ankto,betrag,erledigt,zeit) values "+vls+";")
        db.close()
        return tid

        
    #confirm the transaction
    def setErledigt(this,tid,vonkto,ankto,betrag):
        db= this.dbfile.cursor()
        db.execute("select * from transaktion where tid='"+str(tid)+"' and vonkto='"+str(vonkto)+"' and ankto='"+str(ankto)+"' and betrag='"+str(betrag)+"';")
        apfel = db.fetchmany(2)
        if(len(apfel)>= 1):
            db.execute("update transaktion set erledigt = 1 where tid='"+str(tid)+"';")
            db.close()
            return True
        db.close()
        return False
        
    #check for the pin
    def checkPin(this, kto, pin):
        db= this.dbfile.cursor()
        checkLogfileSql="select * from logfile where erledigt='0' and zeit > " + str(time()-5*60) + " and  kto='"+str(kto) + "';"
        db.execute(checkLogfileSql)
        wrongKeyTries=db.fetchmany(101)
        
        db.execute("select pin from konto where kto="+str(kto)+" and pin="+str(pin) + ";")
        f = db.fetchall()
        success = len(f)>=1
        timestamp = time()
        logfile_sql="insert into logfile(zeit,kto,erledigt) values ('" + str(timestamp) + "','" + str(kto) + "','" + str(int(success)) + "');"
        db.execute(logfile_sql)
        db.close()
        return success  and len(wrongKeyTries) <= 100
        












class DBsqlite(DB):
    
    def __init__(this):
        #set a database
        super()
        this.dbpath = "database.db"
        this.dbfile = sqlite3.connect(this.dbpath)
        this.dbfile.row_factory = sqlite3.Row
        this.db = this.dbfile.cursor()
        print("apfel")
        

    def resetConnection(this):
        this.dbfile= sqlite3.connect(this.dbpath)
        this.dbfile.row_factory = sqlite3.Row
        this.db= this.dbfile.cursor()
        

        



#---------------------------------------------------------#
#---------------------------------------------------------#
#---------------------------------------------------------#
#               MySql database:                           #
#---------------------------------------------------------#









class DBmysql(DB):
    
    def __init__(this):
        #set a database
        super()
        this.dbfile = pymysql.connect(host='localhost',
                                      user=conf["user"],
                                      password=conf["password"],
                                      db='hoesi',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
        this.db = this.dbfile.cursor()
        print("apfel")
        

    def resetConnection(self):
        self.dbfile = pymysql.connect(host='localhost',
                                      user=conf["user"],
                                      password=conf["password"],
                                      db='hoesi',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
        self.db = self.dbfile.cursor()
        
        

