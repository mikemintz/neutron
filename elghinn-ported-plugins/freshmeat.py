# -*- coding: koi8-u -*-

#  Neutron plugin
#  freshmeat.py

#  Copyright (C) 2002-2006 Mike Mintz <mikemintz@gmail.com>
#  Copyright (C) 2007 Mike Mintz <mikemintz@gmail.com>
#                     AnaКl Verrier <elghinn@free.fr>
#  Parts of code:
#  Author: Bohdan Turkynewych, AKA Gh0st, tb0hdan[at]gmail.com
    
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import urllib
from xml.dom.minidom import parse, parseString

class Freshmeat:
    def __init__(self):
	self.neutron_version = ('0.5.42')
	self.version = '0.1'
	self.name = 'Freshmeat'
	self.description = 'Provides Freshmeat requesting interface'
	self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
	self.updateurl = None
        self.command_handlers = [[self.handler_fm, '!fm', 0, 'Gives information about program from FreshMeat.net', '!fm program', ['!fm Gajim', '!fm xmpppy']]]

    def getVal(self, dom, var):
	return dom.getElementsByTagName(var)[0].childNodes[0].nodeValue

    def handler_fm(self, type, source, pn):
	data = urllib.urlopen('http://freshmeat.net/projects-xml/' + pn).read()
        try:
	    dom = parseString(data)
    	    reply = "*" + self.getVal(dom, "projectname_full")
            reply += "* (" + self.getVal(dom, "rating") + ") "
	    reply += self.getVal(dom, "desc_full") + " " + self.getVal(dom, "url_homepage")
        except:
	    reply = "This project not found on FreshMeat.net, sorry"
        # This was really stupid typo...
	self.conn.smsg(type, source, reply)

