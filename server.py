from http.server import *
import os


repdict={"name":"Julius","knf":"!search","stand":"1"}
sites={"/index.html":("name","knf","stand"),
"/init.html":("knf",),
"/css/style.css":(),
"pin.html":("knf",)}






class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(this):
        a=resource(this.path)
        a.replace()
        if a.getState()==200:
            this.send_response(200)
            this.end_headers()
            this.wfile.write(a.getEnd())
        else:
            this.send_error(a.getState())
        




class resource:
    replaces=()
    code=b""
    endcode= b""
    uri=""
    search={}
    state=200
    
    def __init__(this,uri):
        
        temp= uri.split("?")
        this.uri=temp[0]
        if len(temp)>=2:
            this.search=decparamform(temp[1])
        
        
        if True:
            code= open("website"+this.uri,"rb").read()
        else:
            print("Site not found")
            return None
        this.endcode= code
        this.replaces = getSreps(this.uri)
        this.status= 200
    
    def replace(this):
        for i in this.replaces:
            if this.state==200:
                this.state= this.repOne(i)
            else:
                return this.state
    
    def repOne(this,rep):
        repn=repdict[rep]
        rep=getBinOf(rep)
        rep= b"[$"+rep+ b"$]"
        if repn == "!search":
            if "knf" in this.search.keys():
                repn= this.search["knf"]
            else:
                return 400
        
        repn=getBinOf(repn)
        this.endcode= this.endcode.replace(rep,repn)
        return 200
    
    def getState(this):
        return this.state
    
    def getEnd(this):
        return this.endcode

def getSreps(uri):
    return sites[uri]


def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def decparamform(parastring):
	# the parameterstring will be called search here
	params={}
	spsearch=parastring.split("&")    #different search arguments
	for i in spsearch:    #update key:parameter dictionnary
		a=i.split("=")
		if len(a)==2:
			params.update({a[0]:a[1]})
	
	return params

def getBinOf(inp):
    if type(inp)==str:
        inp=inp.encode()
    return inp



run() 
