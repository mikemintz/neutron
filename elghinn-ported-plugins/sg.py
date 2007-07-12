# -*- coding: koi8-u -*-

#  Neutron plugin
#  sg.py

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

import xmpp

class Sg:
    def __init__(self):
	self.neutron_version = ('0.5.42')
	self.version = '0.1'
	self.name = 'Sg'
	self.description = 'Provides server statistics capability'
	self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
	self.updateurl = None
        self.command_handlers = [[self.handler_SG_get, '!server_stats', 0, 'Returns server statistics according to JEP-0039.', '!server_stats <server>', ['!server_stats njs.netlab.cz']]]
	
    def handler_SG_get(self, type, source, parameters):
		groupchat = source[1]
		iq = xmpp.Iq('get')
		iq.setQueryNS('http://jabber.org/protocol/stats')
		if parameters!='':
			iq.setTo(parameters.strip())
		else:
			iq.setTo(SERVER)
			parameters=SERVER
		self.conn.SendAndCallForResponse(iq,self.first_handler,{'parameters':parameters,'type':type,'source':source})

    def first_handler(self, coze,res,parameters,type,source):
	#print par
	payload=res.getQueryPayload()
	if res.getType()=='error':
		self.conn.smsg(type,source,'Error '+res.getErrorCode()+ ': '+res.getError())
		pass
	elif res.getType()=='result':
		iq = xmpp.Iq('get')
		iq.setQueryNS('http://jabber.org/protocol/stats')
		iq.setQueryPayload(payload)
		iq.setTo(parameters.strip())
		self.conn.SendAndCallForResponse(iq,self.second_handler,{'parameters':parameters,'type':type,'source':source})

    def second_handler(self, coze,stats,parameters,type,source):
	pay=stats.getQueryPayload()
	if stats.getType()=='result':
		result='Informations about ' + parameters + ':\n'
		for stat in pay:
			result=result+stat.getAttrs()['name']+': '+stat.getAttrs()['value'] + ' '+stat.getAttrs()['units'] + '\n'
			
		self.conn.smsg(type,source,result)


