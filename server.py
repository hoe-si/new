#! /usr/bin/python3.6

from bottle import route, run, static_file, template, request, error

import dbmanager

from time import localtime
import conf

dbmanager.conf = conf.a
if conf.dbtype == "sqlite":
    db = dbmanager.DBsqlite()
else:
    db = dbmanager.DBmysql()

def getNOf(IntOrString, ifError=0):
    # function returns integer value of any other value or the value in ifError, if converting to int is impossible
    if type(IntOrString) != int:
        try:
            return int(IntOrString)
        except:
            return ifError
    return abs(IntOrString)


def getHTable(tlist,kto):
    out= '<table><tr><td>Typ</td><td>Zeitpunkt</td><td>Betrag</td><td></td><td>&Uuml;berweisungspartner</td></tr>'
    for i in tlist:
        if i["ankto"]==kto:
            aov = "von:"
            partner = str(i["vonkto"])
            typ = "+"
        else:
            aov = "an:"
            partner = str(i["ankto"])
            typ = '-'
        zeit = localtime(i['zeit'])
        zeit = str(zeit[3]) + ':' + str(zeit[4]) + ':' + str(zeit[5])
        out += ( '<tr><td>' + typ + '</td><td>' + zeit + '</td><td>' + str(i["betrag"]) + ' H&ouml;Si </td><td>' + aov + '</td><td>' + partner + '</td></tr>')
    out += '</table>'
    return out
         


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='./static')

@route('/init.html')
@route('/pin.html')
def page_init():
    return template('./templates/init.html', kto=request.query.kto or "fehlerhaft")


@route('/pin.html', method='POST')
def page_pin():
    params = {
        "vonkto":request.forms.get("vonkto"),
        "ankto":request.forms.get("ankto"),
        "betrag":request.forms.get("betrag"),
        "tid":db.initTransaktion(getNOf(request.forms.get("vonkto")), getNOf(request.forms.get("ankto")), getNOf(request.forms.get("betrag")))
    }
    
    return template('./templates/pin.html', **params)



@route('/return.html', method="POST")
def page_return():
    params = {
        "vonkto":request.forms.get("vonkto"),
        "ankto":request.forms.get("ankto"),
        "betrag":request.forms.get("betrag"),
        "hintergrund":"#ff0000",
        "erledigt":"Fehlgeschlagen"
    }
    
    tid= getNOf(request.forms.get("tid"))
    vonkto= getNOf(request.forms.get("vonkto"))
    ankto = getNOf(request.forms.get("ankto"))
    betrag = getNOf(request.forms.get("betrag"))
    pin = getNOf(request.forms.get("pin"))
                    
    if db.checkPin(vonkto,pin):
        if int(db.getKontostand(vonkto)) >= betrag:   # !!! Kann im Betrag geändert werden, um falsche Überweilungen zu machnen
            if db.setErledigt(tid, vonkto, ankto, betrag):
                params["erledigt"]="Erfolgreich"
                params["hintergrund"]="#00ff00"
            else:
                params["erledigt"]="Überweisung fehlgeschlagen!"
        else:
            params["erledigt"]="Unzureichender Kontostand"
    else:
        params["erledigt"]="Pin oder Kontonummer falsch"
    return template('./templates/return.html', **params)



@route("/select.html")
def page_select():
    return template('./templates/select.html', kto= request.query.kto or "fehlerhaft")


@route("/kontostand.html", method="POST")
def page_kontostand():
    reqKto = getNOf(request.forms.get("kto"))
    reqPin = getNOf(request.forms.get("pin"))
    if db.checkPin(reqKto,reqPin):
        history= db.getHistory(reqKto)
        hTable = getHTable(history,reqKto)
        return template("./templates/kontostand.html",kto = reqKto, betrag= db.getKontostand(reqKto),history=hTable)
    else:
        return page_error_403("dummy")



@route("/check.html")
def page_check():
    return template('./templates/check.html', kto= request.query.kto or "fehlerhaft")

@error(500)
def page_error_500(error):
    return send_static('/errors/500.html')

@error(404)
def page_error_404(error):
    return send_static('/errors/404.html')

@error(403)
def page_error_403(error):
    return send_static('/errors/403.html')

@route("<filename:path>")
def page_index(filename):
    if filename.endswith("/"):
        filename += "index.html"
        print(filename)
    return send_static(filename)







run(host='0.0.0.0', port=8035, debug=True)
