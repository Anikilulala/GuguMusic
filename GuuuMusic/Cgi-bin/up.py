import cgi, os
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
fileitem = form['filename']
if fileitem.filename:
   fn = os.path.basename(fileitem.filename)
   fp=os.path.join(os.getcwd(),'files',fn)
   open(fp,'wb').write(fileitem.file.read())
   message =fn + ' done !'   
else:
   message = 'oops'


print("""\
Content-Type: text/html\n
<html>
<head>
<meta charset="utf-8">
<title>upload</title>
</head>
<body>
   <p>%s</p>
</body>
</html>
""" % (message,))