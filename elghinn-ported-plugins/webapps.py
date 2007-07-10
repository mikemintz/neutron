# -*- coding: koi8-u -*-

#  Neutron plugin
#  webapps.py

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

import urllib2,re,urllib
from re import compile as re_compile


class Webapps:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = '0.1'
        self.name = 'Webapps'
        self.description = 'Miscellanous web-utils'
        self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
        self.updateurl = None
        self.command_handlers = [
            [self.handler_bashorg_get, '!bo', 0, 'Get quote from bash.org', '!bo', ['!bo 22']],
	    [self.handler_bashorg_get, '!bashorg', 0, 'Get quote from bash.org', '!bashorg', ['!bashorg 22']],
	    [self.handler_bashorgru_get, '!bor', 0, 'Get quote from bash.org.ru', '!bor', ['!bor 22']],
	    [self.handler_bashorgru_get, '!bashorgru', 0, 'Get quote from bash.org.ru', '!bashorgru', ['!bashorgru 22']],
	    [self.handler_linuxorgru_get, '!lor', 0, 'Get latest news post from linux.org.ru. Note: Parameters ignored.', '!lor', ['!lor 22']],
	    [self.handler_pyorg_get, '!pyorg', 0, 'Get latest news post from python.org. Note: Parameters ignored.', '!pyorg', ['!lor 22']],
	    [self.handler_bbc_get, '!bbc', 0, 'Get latest news post from BBC in Russian. Note: Parameters ignored.', '!bbc', ['!bbc 22']]]

    

    def decode(self, text):
	strip_tags = re_compile(r'<[^<>]+>')
        return strip_tags.sub('', text.replace('<br>','\n')).replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('<br />','\r\n')


    def handler_bashorg_get(self, type, source, parameters):
	if parameters.strip():
    	    req = urllib2.Request('http://bash.org/?'+parameters.strip())
	else:
    	    req = urllib2.Request('http://bash.org/?random')
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	target = r.read()
	od = re.search('<p class="qt">',target)
	message = target[od.end():]
	message = message[:re.search('</p>',message).start()]
	message = self.decode(message)
	message='\n' + message.strip()
	self.conn.smsg(type,source,unicode(message,'windows-1251'))

    def handler_bashorgru_get(self, type, source, parameters):
	if parameters.strip()=='':
    	    req = urllib2.Request('http://bash.org.ru/random')
	else:
    	    req = urllib2.Request('http://bash.org.ru/quote/'+parameters.strip())
	req.add_header = ('User-agent', 'Mozilla/5.0')
	try:
    	    r = urllib2.urlopen(req)
    	    target = r.read()
    	    od = re.search('<div>',target)
    	    message = target[od.end():]
    	    message = message[:re.search('</div>',message).start()]
    	    message = self.decode(message)
    	    message = '\n' + message.strip()
    	    self.conn.smsg(type,source,unicode(message,'windows-1251'))
	except:
    	    self.conn.smsg(type,source,unicode('Кончился интернет, всё, приехали... ','koi8-u'))

    def handler_linuxorgru_get(self, type, source, parameters):
	req = urllib2.Request('http://linux.org.ru/index.jsp')
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	target = r.read()
        od = re.search('<hr noshade class="news-divider">',target)
	message = target[od.end():]
        message = message[:re.search('<div class=sign>',message).start()]
        message = self.decode(message)
        message = '\n' + message.strip()
	self.conn.smsg(type,source,unicode(message,'koi8-r'))

    def handler_pyorg_get(self, type, source, parameters):
        req = urllib2.Request('http://python.org')
	req.add_header = ('User-agent', 'Mozilla/5.0')
        r = urllib2.urlopen(req)
	target = r.read()
        od = re.search('<h2 class="news">',target)
        message = target[od.end():]
        message = message[:re.search('</div>',message).start()]
	message = self.decode(message)
        message = '\n' + message.strip()
	reply = ''
        for line in message.split('\n'):
	    if line.strip():
    	        reply += line + '\r\n'
	    reply='\n' + reply	    
        self.conn.smsg(type,source,unicode(reply,'koi8-r'))


    def handler_bbc_get(self, type, source, parameters):
	req = urllib2.Request('http://news8.thdo.bbc.co.uk/low/russian/news/default.stm')
        req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	target = r.read()
        od = re.search('<a name="startcontent">',target)
        message = target[od.end():]
        message = message[:re.search('<hr>',message).start()]
        message = self.decode(message)
        message = re.sub("^\s*?","",message).replace('\n','')
	message = message.replace('<br clear="all" /> ','\n')
        message = '\n' + message.strip()
        reply = ''
        for line in message.split('\n'):
	    if line.strip():
    	        reply += line + '\r\n'
        self.conn.smsg(type,source,unicode(reply,'windows-1251'))

    #=======
    def handler_linuxorgru_get(self, type, source, parameters):
	req = urllib2.Request('http://linux.org.ru/index.jsp')
        req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<hr noshade class="news-divider">',target)
        message = target[od.end():]
        message = message[:re.search('<hr noshade class="news-divider">',message).start()]
        message = self.decode(message)
        message = '\n' + message.strip()
        self.conn.smsg(type, source, unicode(message, 'koi8-r'))

