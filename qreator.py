#! usr/bin/python3
import pymysql as sqlite3


standard='''<div style="float:left; border:3px solid black; page-break-inside: avoid;">
<font style="size:20">
<table height="200" width="600" border="0">
<tr><td colspan="3"><h1>H&ouml;Si-City 3.0</h1></td></tr>
<tr><td rowspan="4"><img src="https://www.qrcode-generator.de/phpqrcode/getCode.php?cht=qr&chl=http%3A%2F%2F192.168.178.54:8000%2Fselect.html%3Fkto%3D<!-- id pupil --!>&chs=180x180&choe=UTF-8&chld=L|0" height="200" width="200"></td><td>Name:<br><u><!-- Name pupil --!></u></td><td rowspan="2"><img src="smv.png" height="100" width="132"></td></tr>
<tr><td>Gesch&auml;ft:<br><u><!-- Geschaeft --!></u></td><td></td></tr>
<tr><td>ID:<u><!-- id pupil --!></u></td><td><img src="hosi.png" height="100" width="132"></td></tr>
<tr><td></td><td></td></tr>
</table>
</font>
<hr>
Passwort:<!-- pw --!></div>
</div>'''


a=open("qr-generator/a.html","a")

a.write('<html><body>')

from dbconf import a as conf

def newdiv(pid,Name,Store,pw,nl=False):
	a=standard.replace("<!-- Name pupil --!>",Name.rjust(10))
	a=a.replace("<!-- Geschaeft --!>",Store.rjust(10))
	a=a.replace("<!-- id pupil --!>",pid)
	a=a.replace("<!-- pw --!>",pw.rjust(10))
#	if nl:
#		a+= "</tr><tr>"
	return a

dbf=sqlite3.connect(host='localhost',
                    user=conf["user"],
                    password=conf["password"],
                    db='hoesi',
                    charset='utf8mb4',
                    cursorclass=sqlite3.cursors.DictCursor)
db=dbf.cursor()
db.execute("select distinct konto.kto, konto.pin, gruppen.gkto from gruppen, konto where konto.kto=gruppen.skto")
plist=db.fetchall()
print(plist)
c=0
for i in plist:
	c+=1
	if c % 4 ==0:
		anl=True
	else:
		anl=False
	a.write(newdiv(str(i["kto"]),"Hans",str(i["gkto"]),str(i["pin"]),nl=anl))
	print(c)
a.write("</body></html>")
a.close()
db.close()
