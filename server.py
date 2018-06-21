from http.server import *
import os


repdict={"name":"Julius","knf":"!search","stand":"1"}
sites={"/index.html":{"knf":"!search"},
"/init.html":{"knf":"!search"},
"/css/style.css":{},
"pin.html":{"knf":"!data","knt":"!data","mnt":"!data"},
"return.html":{"knf":"!data","knt":"!data","mnt":"!data"}}






class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(this):
        this.anyway(this.path,data("dummy",""))
    
    def do_POST(this):
        try:
            LEN= int(self.headers.get("content-length"))
            pack = self.rfile.read(LEN)
        except:
            print(">> converter: content-length missing or wrong")
            this.send_error(400)
            return None
        this.anyway(this.path,{"!data":pack})
		
    def anyway(this,uri,data):
	    a=resource(uri,data)
	    print("1. state: "+str(a.getState()))
	    a.replace()
	    print("2. state: "+str(a.getState()))
	    if a.getState()==200:
	        this.send_response(200)
	        this.end_headers()
	        this.wfile.write(a.getEnd())
	    else:
	        this.send_error(a.getState())


class data(dict):
    rtype=""
    
    def __init__(this,name,raw):
        super()
        print("created data object")
        this.rtype=getStringOf(name)
        this.update(decparamform(raw))
        
        
    def getBin(this,key):
        try:
            return(this.get(getBinOf(key)))
        except KeyError:
            return 400
            
    def getString(this,key):
        try:
            return getStringOf(this[getBinOf(key)])
        except UnicodeDecodeError:
            return 400
        except KeyError:
            return 400
    
    def getValue(this,key):
        if key in this.keys():
            return this[key]
        else:
            return 400
            



class resource:
    # class for any data of which the path is saved in "sites"
    # it is able to open the file, replace everything there has to be replaced in the site
    # 
    replaces={}
    code=b""
    endcode= b""
    uri=""
    givens={}
    state=200
    
    def __init__(this,uri,indata):
        
        temp= uri.split("?")
        this.uri=temp[0]
        if len(temp)>=2:
            params= temp[1]
            newdata=data("search",params)
            this.givens.update({"search":newdata})
        if this.uri.endswith("/"):
            this.uri += "index.html"
        this.givens=indata
        
        try:
            this.replaces=sites[this.uri]
        except KeyError:
            this.state= 404
            return None
        code= open("website"+this.uri,"rb").read()
        this.endcode= code
        this.state= 200
    
    def replace(this):
        for i in this.replaces:
            if this.state==200:
                this.state= this.repOne(i)
            else:
                print(i)
                return this.state
    
    def repOne(this,rep):
        repn=repdict[rep]   #rep was given by the sites dict
        rep=getBinOf(rep)
        rep= b"[$"+rep+ b"$]"   #the full string which has to be replaced
        by=this.givens.get(repn,400)
        if type(by)==data:
            by=by.getBin(repn)
        if type(by)==data:
            this.endcode= this.endcode.replace(rep,repn)
            return 200
        else:
            return by   #is html error (int) if anything went wrong
    
    def getState(this):
        return this.state
    
    def getEnd(this):
        return this.endcode



def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def decparamform(parastring):
    # sets keys to bytestring format for making it easyer to work with given resource
    # the parameterstring will be called search here
    params={}
    spsearch=parastring.split("&")    #different search arguments
    for i in spsearch:    #update key:parameter dictionnary
	    a=i.split("=")
	    if len(a)==2:
	        params.update({getBinOf(a[0]):a[1]})
	    else:
	        params.update({b"default":a[0]})
    
    return params

def getBinOf(inp):
    if type(inp)==str:
        inp=inp.encode()
    return inp

def getStringOf(inp):
    if type(inp)==bytes:
        inp=inp.decode()
    return inp



run() 
