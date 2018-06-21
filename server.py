from bottle import route, run, static_file, template, request

@route('/init.html')
def page_init():
  return template('./website/init.html', kto=request.query.kto or "fehlerhaft")

run(host='localhost', port=8000, debug=True)
