# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  domain.py

#  Copyright (C) 2002-2006 Mike Mintz <mikemintz@gmail.com>
#  Copyright (C) 2007 Mike Mintz <mikemintz@gmail.com>
#                     Anaël Verrier <elghinn@free.fr>

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

import socket

from rwhois import WhoisRecord

class Domain:
    def __init__(self):
	self.neutron_version = ('0.5.42')
	self.version = '2.0'
	self.name = 'Domain'
	self.description = ''
	self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
	self.updateurl = None
        self.command_handlers = [[self.handler_domain_domain, '!domain', 0, 'Returns information on specified domain.', '!domain <domain>', ['!domain jabber.org']]]


    def handler_domain_domain(self, type, source, parameters):
	rec = WhoisRecord(parameters)
	try:
	    rec.whois()
	    reply = 'Registered'
	except 'NoSuchDomain', reason:
	    reply = 'AVAILABLE'
	except socket.error, (ecode,reason):
	    reply = 'Socket Error'
	except "TimedOut", reason:
            reply = 'Timed Out'
	self.conn.smsg(type, source, reply)

