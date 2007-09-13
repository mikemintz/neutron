#$ neutron_plugin 01

import wsgiserver
import thread
# used example from wsgiserver as template
# (c) 2006-2007 Bohdan Turkynewych, AKA Gh0st, tb0hdan[at]gmail.com

HEADER = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!--
.timestamp {color: #AAAAAA;}
.system {color: #009900; font-weight: bold;}
.emote {color: #AA0099;}
.self {color: #CC0000;}
.normal {color: #0000AA;}
h1 { color: #336699; font-family: sans-serif; border-bottom: #224466 solid 3pt; letter-spacing: 3px; margin-left: 20pt; }
h2 { color: #663399; font-family: sans-serif; letter-spacing: 2px; text-align: center }
a { margin-left: 20pt; margin-right: 20pt; font-family: arial,helvetica; font-weight: bold; color: #0D0D0D; }
//-->
</style>
<title>Welcome to Neutron Web Server</title>
</head>
<body>
<div style="color: #AAAAAA; text-align: right; font-family: monospace; letter-spacing: 3px">neutron web server</div> """


FOOTER =  """</body>
</html>
"""

REDIRECTOR = """<html>
<head>
<title></title>
<meta http-equiv="Refresh" content="0; URL=/index.html">
<style></style>
</head>
<body>
</body>
</html>"""

def index_page(environ, start_response):
    global HEADER
    status = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    DATA = """
    <div align="center">
    <a href="/plugins.html">Plugins</a>|<a href="/status.html">Status</a>|<a href="/roster.html">Roster</a>
    </div>"""
    data = HEADER + DATA + FOOTER
    return data

def index_redir(environ, start_response):
    global REDIRECTOR
    status = '200 OK'
    response_headers = [('Content-type','text/html')]
    start_response(status, response_headers)
    data = REDIRECTOR
    return data

wsgi_apps = [('/', index_redir),('/index.html', index_page)]

server = wsgiserver.CherryPyWSGIServer(('localhost', 12345), wsgi_apps,
                                           server_name='localhost')

def starter():
    try:
        server.start()
    except:
        server.stop()
    
if __name__ == '__main__':
	thread.start_new(starter,())
