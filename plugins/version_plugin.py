#$ neutron_plugin 01
# -*- coding: utf-8 -*-

# Talisman author: dimichxp
# further developer: Als
# Parts of code, Bohdan Turkynewych, AKA Gh0st.

version_pending=[]
time_pending=[]
last_pending=[]
ping_pending=[]
global ping_start

def handler_version(type, source, parameters):
	nick = source[2]
	groupchat=source[1]
	jid=groupchat+'/'+nick
	iq = xmpp.Iq('get')
	id='vers'+str(random.randrange(1000, 9999))
	globals()['version_pending'].append(id)
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
	JCON.SendAndCallForResponse(iq, handler_version_answ, {'type': type, 'source': source})
	return

def handler_ping(type, source, parameters):
	nick = source[2]
	groupchat=source[1]
	jid=groupchat+'/'+nick
	iq = xmpp.Iq('get')
	id='vers'+str(random.randrange(1000, 9999))
	globals()['ping_pending'].append(id)
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
	globals()['ping_start'] = time.time()
	JCON.SendAndCallForResponse(iq, handler_ping_answ, {'type': type, 'source': source})
	return

def handler_time(type, source, parameters):
	nick = source[2]
	groupchat=source[1]
	jid=groupchat+'/'+nick
	iq = xmpp.Iq('get')
	id='time'+str(random.randrange(1000, 9999))
	globals()['time_pending'].append(id)
	iq.setID(id)
	iq.addChild('query', {}, [], 'jabber:iq:time');
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
	JCON.SendAndCallForResponse(iq, handler_time_answ, {'type': type, 'source': source})
	return

def handler_version_answ(coze, res, type, source):
	id=res.getID()
	if id in globals()['version_pending']:
		globals()['version_pending'].remove(id)
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
	smsg(type, source, rep)

def handler_time_answ(coze, res, type, source):
	id=res.getID()
	if id in globals()['time_pending']:
		globals()['time_pending'].remove(id)
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
	smsg(type, source, rep)

def handler_ping_answ(coze, res, type, source):
	id=res.getID()
	if id in globals()['ping_pending']:
		globals()['ping_pending'].remove(id)
	else:
		print 'someone is doing wrong...'
		return
	rep = ''
	if res:
		if res.getType() == 'result':
		    idletime = time.time() - globals()['ping_start']
		    reply = 'Pong after: '
		    rep = reply + str(idletime)[:4] + ' sec.'
		else:
			rep = u'unable to retrieve'
	else:
		rep = u'not found'
	smsg(type, source, rep)
	
register_command_handler(handler_version, '!version', 0, 'Returns client version.', '!version <nick>', ['!version Neutron'])
register_command_handler(handler_time, '!time', 0, 'Returns client time.', '!time <nick>', ['!time Neutron'])
register_command_handler(handler_ping, '!ping', 0, 'Returns client ping by using iq:version.', '!ping <nick>', ['!ping Neutron'])
