from bottle import route, run, static_file, template, request, error
from dbmanager import DB

db = DB()


def getIntOf(IntOrString, ifError=0):
    # function returns integer value of any other value or the value in ifError, if converting to int is impossible
    if type(IntOrString) != int:
        try:
            return int(IntOrString)
        except ValueError:
            return ifError
    return IntOrString




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
        "tid":db.initTransaktion(getIntOf(request.forms.get("vonkto")), getIntOf(request.forms.get("ankto")), getIntOf(request.forms.get("betrag")))
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
    
    if db.checkPin(getIntOf(request.forms.get("vonkto")),getIntOf(request.forms.get("pin"))):
        if int(db.getKontostand(getIntOf(request.forms.get("vonkto")))) >= getIntOf(request.forms.get("betrag")):   # !!! Kann im Betrag geändert werden, um falsche Überweilungen zu machne
            if db.setErledigt(getIntOf(request.forms.get("tid")), getIntOf(request.forms.get("vonkto")), getIntOf(request.forms.get("ankto")), getIntOf(request.forms.get("betrag"))):
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







run(host='localhost', port=8000, debug=True)
