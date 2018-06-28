import sqlite3


standard="""<td>
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
</td>"""


a=open("a.html","a")

a.write('<html><body><table cellspacing="0" border="1">')



def newdiv(pid,Name,Store,pw,nl=False):
	a=standard.replace("<!-- Name pupil --!>",Name.rjust(10))
	a=a.replace("<!-- Geschaeft --!>",Store.rjust(10))
	a=a.replace("<!-- id pupil --!>",pid)
	a=a.replace("<!-- pw --!>",pw.rjust(10))
	if nl:
		a+= "</tr><tr>"
	return a

dbf=sqlite3.connect("database.db")
db=dbf.cursor()
plist=db.execute("select distinct konto.kto, konto.pin, gruppen.gkto from gruppen, konto where konto.kto=gruppen.skto").fetchall()
c=0
for i in plist:
	c+=1
	if c % 4 ==0:
		anl=True
	else:
		anl=False
	a.write(newdiv(str(i[0]),"Hans",str(i[2]),str(i[1]),nl=anl))
	print(c)
a.write("</table></body></html>")
a.close()
db.close()
