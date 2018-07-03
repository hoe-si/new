#/usr/bin/python3 

import sqlite3, random, pymysql
from time import time

from dbconf import a as conf







class DB():
    
    def __init__(this):
        #set a database
        return None
        
    #get the money
    def getKontostand(this,kto):

        money = 0
        sql="select betrag from transaktion where ankto='"+str(kto)+"' AND erledigt=1;"
        this.db.execute(sql)
        add = this.db.fetchall()
        for i in add:
            money+=int(i["betrag"])
        sql="select betrag from transaktion where vonkto='"+str(kto)+"' AND erledigt=1;"
        this.db.execute(sql)
        sub = this.db.fetchall()
        for i in sub:
            money-=int(i["betrag"])
        return money

        
    #initialise transaction
    def initTransaktion(this,ktof,ktot,msum):
        #Generate the random tid
        tid=random.randint(1000000,9999999)
        this.db.execute("select * from transaktion where tid='"+str(tid)+"';")
        while(len(this.db.fetchmany(100))>=1):
            tid=random.randint(1000,9999)
            this.db.execute("select * from transaktion where tid='"+str(tid)+"';")
            
            
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
        this.db.execute("select * from transaktion where tid='"+str(tid)+"' and vonkto='"+str(vonkto)+"' and ankto='"+str(ankto)+"' and betrag='"+str(betrag)+"';")
        apfel = this.db.fetchmany(2)
        if(len(apfel)>= 1):
            this.db.execute("update transaktion set erledigt = 1 where tid='"+str(tid)+"';")
            this.dbfile.commit()
            return True
        return False
        
    #check for the pin
    def checkPin(this, kto, pin):
#        checkLogfileSql="select * from logfile where erledigt='0' and zeit > " + str(time()-5*60) + " and  kto='"+str(kto) + "';"
#        this.db.execute(checkLogfileSql)
#        wrongKeyTries=this.db.fetchmany(101)
        print(kto)
        print(pin)
        
        this.db.execute("select pin from konto where kto="+str(kto)+" and pin="+str(pin) + ";")
        f = this.db.fetchall()
        print(f)
        success = len(f)>=1
        timestamp = time()
#        logfile_sql="insert into logfile(zeit,kto,erledigt) values ('" + str(timestamp) + "','" + str(kto) + "','" + str(int(success)) + "');"
#        this.db.execute(logfile_sql)
        return success # and len(wrongKeyTries) <= 100
        
    def resetConnection(self):
        self.dbfile.commit()
        self.dbfile.close()
        self.dbfile = pymysql.connect(host='localhost',
                                      user=conf["user"],
                                      password=conf["password"],
                                      db='hoesi',
                                      charset='utf8mb4',
                                      cursorclass=pymysql.cursors.DictCursor)
        self.db = this.dbfile.cursor()











class DBsqlite(DB):
    
    def __init__(this):
        #set a database
        super()
        this.dbpath = "database.db"
        this.dbfile = sqlite3.connect(this.dbpath)
        this.db = this.dbfile.cursor()
        print("apfel")
        

        















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
        

