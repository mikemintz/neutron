# -*- coding: utf-8 -*-

#  Neutron plugin
#  iqver.py

#  Copyright (C) 2002-2006 Mike Mintz <mikemintz@gmail.com>
#  Copyright (C) 2007 Mike Mintz <mikemintz@gmail.com>
#                     Anaël Verrier <elghinn@free.fr>
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

# Talisman author: dimichxp
# Talisman further developer: Als
# Parts of code, Als
# (c) Bohdan Turkynewych, AKA Gh0st.

from xmpp import Node as xmpp_Node, Iq as xmpp_Iq
from random import randrange as random_randrange
from time import time as time_time, sleep as time_sleep

class Iqver:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = '0.1'
        self.name = 'Iqver'
        self.description = 'fdasfsadf'
        self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
        self.updateurl = None
	self.version_pending=[]
	self.time_pending=[]
	self.last_pending=[]
	self.ping_pending=[]
	self.ping_start=0.0
        self.command_handlers = [
	    [self.handler_version, '!version', 0, 'Returns client version.', '!version <nick>', ['!version Neutron']],
	    [self.handler_time, '!time', 0, 'Returns client time.', '!time <nick>', ['!time Neutron']],
	    [self.handler_ping, '!ping', 0, 'Returns client ping by using iq:version.', '!ping <nick>', ['!ping Neutron']],
	    [self.handler_rega, '!register', 0, 'Registers account on foreign server using iq:register.', '!register <nick>@<server> <password>', ['!register Neutron@jabber.orgg mypassword']],
	    [self.handler_pong,'!pong',0,'','',['']]]

    def handler_version(self, type, source, parameters):
	nick = source[2]
	groupchat=source[1]
	jid=groupchat+'/'+nick
	iq = xmpp_Iq('get')
	id='vers'+str(random_randrange(1000, 9999))
	self.version_pending.append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	if parameters:
		args = parameters.split(' ')
		nick = ' '.join(args[0:])
		jid=groupchat+'/'+nick
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				iq.setTo(jid)
	else:
		jid=groupchat+'/'+nick
		iq.setTo(jid)
	self.conn.SendAndCallForResponse(iq, self.handler_version_answ, {'type': type, 'source': source})
	return

    def handler_ping(self, type, source, parameters):
	nick = source[2]
	groupchat=source[1]
	jid=groupchat+'/'+nick
	iq = xmpp_Iq('get')
	id='vers'+str(random_randrange(1000, 9999))
	self.ping_pending.append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:version');
	if parameters:
		args = parameters.split(' ')
		nick = ' '.join(args[0:])
		jid=groupchat+'/'+nick
		if GROUPCHATS.has_key(source[1]):
			nicks = GROUPCHATS[source[1]].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				iq.setTo(jid)
	else:
		jid=groupchat+'/'+nick
		iq.setTo(jid)
	self.ping_start = time_time()
	self.conn.SendAndCallForResponse(iq, self.handler_ping_answ, {'type': type, 'source': source})
	return

    def handler_time(self, type, source, parameters):
	nick = source[2]
	groupchats = self.config.groupchats
	groupchat=source[1]
	jid=groupchat+'/'+nick
	iq = xmpp_Iq('get')
	id='time'+str(random_randrange(1000, 9999))
	self.time_pending.append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:time');
	if parameters:
		args = parameters.split(' ')
		nick = ' '.join(args[0:])
		jid=groupchat+'/'+nick
		if groupchats.has_key(source[1]):
			nicks = groupchats[source[1]].keys()
			param = parameters.strip()
			if not nick in nicks:
				iq.setTo(param)
			else:
				iq.setTo(jid)
	else:
		jid=groupchat+'/'+nick
		iq.setTo(jid)
	self.conn.SendAndCallForResponse(iq, self.handler_time_answ, {'type': type, 'source': source})
	return

    def handler_version_answ(self, coze, res, type, source):
	id=res.getID()
	if len(self.version_pending)<>0:
		self.version_pending.remove(id)
	else:
		print 'someone is doing wrong...'
		return
	rep =''
	if res:
		if res.getType() == 'result':
			name = ''
			version = ''
			os = '&apos;'
			props = res.getQueryChildren()
			for p in props:
				if p.getName() == 'name':
					name = p.getData()
				elif p.getName() == 'version':
					version = p.getData()
				elif p.getName() == 'os':
					os = p.getData()
			if name:
				rep = name
			if version:
				rep +=' '+version
			if os:
				rep +=u' on '+os
		else:
			rep = u'unable to retrieve'
	else:
		rep = u'not found'
	self.conn.smsg(type, source, rep)

    def handler_time_answ(self, coze, res, type, source):
	id=res.getID()
	if len(self.time_pending)<>0:
		self.time_pending.remove(id)
	else:
		print 'someone is doing wrong...'
		return
	rep = 'Your time is: '
	display = ''
	if res:
		if res.getType() == 'result':
			
			props = res.getQueryChildren()
			for p in props:
			    if p.getName() == 'display':
					display = p.getData()
			    if display:
				    rep +=u' '+unicode(display)
		else:
			rep = u'unable to retrieve'
	else:
		rep = u'not found'
	self.conn.smsg(type, source, rep)

    def handler_ping_answ(self, coze, res, type, source):
	id=res.getID()
	if len(self.ping_pending)<>0:
		self.ping_pending.remove(id)
	else:
		print 'someone is doing wrong...'
		return
	rep = ''
	if res:
		if res.getType() == 'result':
		    idletime = time_time() - self.ping_start
		    reply = 'Pong after: '
		    rep = reply + str(idletime)[:4] + ' sec.'
		else:
			rep = u'unable to retrieve'
	else:
		rep = u'not found'
	self.conn.smsg(type, source, rep)

    def handler_pong(self, type, source, parameters):
	    self.conn.smsg(type, source, '!ping')

    def handler_rega_response(self, bla, response, type, source):
	if response:
		if response.getType() == 'result':
			self.conn.smsg(type, source, 'Registration successful')
			return
		else:
			reply = 'Error whilst registering account.'
	else:
		reply = 'Zero sized reply.'
	self.conn.smsg(type, source, reply)	

    def handler_rega(self, type, source, parameters):
	parameters = parameters.strip()
	if parameters:
	    if len(parameters.split(' ')) == 2:
		jid = parameters.split(' ')[0]
		password = parameters.split(' ')[1]
		if len(jid.split('@')) == 2:
		    username = jid.split('@')[0]
		    server = jid.split('@')[1]
		    reply = 'Registering account:  Username: %s '%username + 'Server: %s '%server + 'Password: %s'%password
		else:
		    reply = 'Wrong syntax'
		    self.conn.smsg(type, source, reply)
		    return
	    else:
		reply = 'Wrong syntax'
	        self.conn.smsg(type, source, reply)
	        return
	self.conn.smsg(type, source, reply)
	iq = xmpp_Iq('set')
	iq.setTo(server)
	iq.setID('rega_'+str(random_randrange(1000, 9999)))
	query = xmpp_Node('query')
	query.setNamespace('jabber:iq:register')
	query.setTagData('username', username)
	query.setTagData('password', password)
	iq.addChild(node=query)
	time_sleep(10)
	self.conn.SendAndCallForResponse(iq, self.handler_rega_response, {'type': type, 'source': source})
