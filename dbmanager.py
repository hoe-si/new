import sqlite3


class db():
    
    def __init__(this):
        this.dbpath = "database.db"
        this.dbfile = sqlite3.connect(this.dbpath)
        this.db = this.dbfile.cursor()
        print("apfel")
    def getM(this,kto):
        return 10
    
    def initT(this,ktof,ktot,msum):
        return 200
    
    def setT(this,rid):
        return 200
        
    def checkP(this, kto, pin):
        f = this.db.execute("select pin from konto where kto='"+str(kto)+"';").fetchone()
        if str(f[0]) == str(pin):
            return True
        else:
            return False
