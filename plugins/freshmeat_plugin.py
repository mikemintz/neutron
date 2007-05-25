#$ neutron_plugin 01

import urllib
from xml.dom.minidom import parse, parseString

def getVal(dom, var):
    return dom.getElementsByTagName(var)[0].childNodes[0].nodeValue

def handler_fm(type, source, pn):
    data = urllib.urlopen('http://freshmeat.net/projects-xml/' + pn, proxies=proxies).read()
    try:
        dom = parseString(data)
        reply = "*" + getVal(dom, "projectname_full")
        reply += "* (" + getVal(dom, "rating") + ") "
        reply += getVal(dom, "desc_full") + " " + getVal(dom, "url_homepage")
    except:
        reply = "This project not found on FreshMeat.net, sorry"
    # This was really stupid typo...
    smsg(type, source, reply)

register_command_handler(handler_fm, '!fm', 0, 'Gives information about program from FreshMeat.net', '!fm program', ['!fm', '!fm Gajim'])
