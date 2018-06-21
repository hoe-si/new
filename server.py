from bottle import route, run, static_file, template, request

@route('/init.html')
def page_init():
  return template('./website/init.html', kto=request.query.kto or "fehlerhaft")


@route('/pin.html', method='POST')
def page_pin():
  params = {
    "vonkto":request.forms.get("vonkto"),
    "ankto":request.forms.get("ankto"),
    "betrag":request.forms.get("betrag")}
  
  return template('./website/pin.html', **params)

run(host='localhost', port=8000, debug=True)
