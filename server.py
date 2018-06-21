from bottle import route, run, static_file, template, request
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

run(host='localhost', port=8000, debug=True)
