from http.server import *
import os


repdict={"Name":"Julius","id":"123","stand":"1"}
sites={"/index.html":("Name","id","stand")}






class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(this):
        a=resource(this.path)
        a.replace()
        this.send_response(200)
        this.end_headers()
        this.wfile.write(a.getEnd())
        




class resource:
    replaces=()
    code=b""
    endcode= b""
    uri=""
    
    def __init__(this,uri):
        
        this.uri= uri
        if True:
            code= open("website"+uri,"rb").read()
        else:
            print("Site not found")
            return None
        this.endcode= code
        this.replaces = getSreps(this.uri)
    
    def replace(this):
        for i in this.replaces:
            this.repOne(i)
    
    def repOne(this,rep):
        repn=repdict[rep]
        if type(repn)==str:
            repn=repn.encode()
        if type(rep)== str:
            rep=rep.encode()
        this.endcode= this.endcode.replace(rep,repn)
    
    def getEnd(this):
        return this.endcode

def getSreps(uri):
    return sites[uri]


def run(server_class=HTTPServer, handler_class=MyHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()





run() 
