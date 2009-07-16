#$ neutron_plugin 01

from sys import exc_info
from urllib import urlopen
from xml.dom.minidom import parseString
from xml.dom.minidom import Node
TNODE = Node.TEXT_NODE

def handler_wcom(type, source, parameters):
    param = parameters.strip()
    if param:
        param = str(parameters).upper()
    else:
        param = 'UKXX0010'
    title = ""
    if len(param) <> 8 :
        param = 'UKXX0010'
        title = '\n*** Wrong format, falling back ***\n'			
    try:
	# temporary solution, details here: http://www.rainmeter.net/forum/viewtopic.php?f=4&t=588&start=30
        response = urlopen('http://xml.weather.com/weather/local/'+param+'?cc=*&dayf=1&unit=m', proxies=proxies)
    except:
        print "Unexpected error:", exc_info()[0]
	
    doc = parseString(response.read().strip()) 
    mapping = {}
    for node in doc.getElementsByTagName("weather"): 
        P = node.getElementsByTagName("loc")
        for node4 in P:
            L = node4.getElementsByTagName("dnam")
            for node2 in L:
                for node3 in node2.childNodes:
                    if node3.nodeType == TNODE:
                        title += 'Weather report for: ' + node3.data + '\n'
            LT = node4.getElementsByTagName("tm")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Local time: ' + node31.data+'\n'
            LT = node4.getElementsByTagName("lat")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Latitude: ' + node31.data+'\n'
            LT = node4.getElementsByTagName("lon")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Longitude: '+ node31.data+'\n'
            LT = node4.getElementsByTagName("sunr")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Sunrise: ' + node31.data+'\n'
            LT = node4.getElementsByTagName("suns")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Sunset: ' + node31.data+'\n'
            LT = node4.getElementsByTagName("zone")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Zone: ' + node31.data+'\n'
        P = node.getElementsByTagName("cc")
        for node4 in P:
            L = node4.getElementsByTagName("lsup")
            for node2 in L:
                for node3 in node2.childNodes:
                    if node3.nodeType == TNODE:
                        title += 'Latest update: ' + node3.data + '\n'
            LT = node4.getElementsByTagName("obst")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Observation station: ' + node31.data+'\n'
            LT = node4.getElementsByTagName("tmp")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Temperature: ' + node31.data+'\n'
            LT = node4.getElementsByTagName("flik")
            for node21 in LT:
                for node31 in node21.childNodes:
                    if node31.nodeType == TNODE:
                        title += 'Windchill: ' + node31.data+'\n'
    smsg(type, source, title)

register_command_handler(handler_wcom, '!w', 0, 'Weather plugin, try searching your city at weather.yahoo.com', '!w', ['!w NLXX0002'])

