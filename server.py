from bottle import route, run, static_file, template, request, error
from dbmanager import DB

db = DB()



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
        "tid":db.initTransaktion(request.forms.get("vonkto"), request.forms.get("ankto"), request.forms.get("betrag"))
    }
    
    return template('./templates/pin.html', **params)



@route('/return.html', method="POST")
def page_return():
    params = {
        "vonkto":request.forms.get("vonkto"),
        "ankto":request.forms.get("ankto"),
        "betrag":request.forms.get("betrag"),
        "erledigt":"Fehlgeschlagen"
    }
    if db.checkPin(request.forms.get("vonkto"),request.forms.get("pin")):   # wirft evtl. einen Fehler, wenn der Wert kein String ist
        if int(db.getKontostand(request.forms.get("vonkto"))) >= int(request.forms.get("betrag")):
            db.setErledigt(request.forms.get("tid"))
            params["erledigt"]="Erfolgreich"
    return template('./templates/return.html', **params)



@route("/select.html")
def page_select():
    return template('./templates/select.html', kto= request.query.kto or "fehlerhaft")


@route("/kontostand.html", method="POST")
def page_kontostand():
    reqKto=request.forms.get("kto")
    if db.checkPin(reqKto,request.forms.get("pin")):
        return template("./templates/kontostand.html",kto = request.forms.get("kto"), betrag= db.getKontostand(reqKto))

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







run(host='localhost', port=8000, debug=True)
