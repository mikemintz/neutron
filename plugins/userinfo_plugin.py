#$ neutron_plugin 01

import thread
import time

LOCALDB_FILE = 'dynamic/localdb.txt'

def handler_userinfo_join(groupchat, nick):
	GROUPCHATS[groupchat][nick] = {'idle': time.time(), 'jid': groupchat + '/' + nick, 'fullname': None, 'nickname': None, 'email': None, 'url': None, 'client': None, 'version': None, 'os': None}
	
	browse_iq = xmpp.Iq(groupchat + '/' + nick, 'get')
	browse_iq.setQueryNS('jabber:iq:browse')
	JCON.send(browse_iq)
	
	time.sleep(2)
	
	version_iq = xmpp.Iq(groupchat + '/' + nick, 'get')
	version_iq.setQueryNS('jabber:iq:version')
	JCON.send(version_iq)

	time.sleep(2)

	vcard_iq = xmpp.Iq(groupchat + '/' + nick, 'get')
	vcard_iq.setQueryNS('vcard-temp')
	JCON.send(vcard_iq)

def handler_userinfo_message(type, source, body):
	if type == 'public':
		if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(source[2]):
			GROUPCHATS[source[1]][source[2]]['idle'] = time.time()

def handler_userinfo_iq(iq):
	type = iq.getType()
	namespace = iq.getQueryNS()
	if not namespace:
		if iq.getTag('user'):
			namespace = iq.getTag('user').getNamespace()
		elif iq.getTag('VCARD') or iq.getTag('vCard') or iq.getTag('vcard'):
			vcard = iq.getTag('VCARD') or iq.getTag('vCard') or iq.getTag('vcard')
			namespace = vcard.getNamespace()
	groupchat = iq.getFrom().getStripped()
	nick = iq.getFrom().getResource()
	
	if GROUPCHATS.has_key(groupchat) and GROUPCHATS[groupchat].has_key(nick):
		if type == 'result':
			if namespace == 'jabber:iq:browse':
				if iq.getTag('user'):
					GROUPCHATS[groupchat][nick]['jid'] = iq.getTag('user').getTag('user').getAttr('jid')
					#fp = open('userlog.txt', 'a')
					#fp.write(groupchat + '/' + nick + '\n' + GROUPCHATS[groupchat][nick]['jid'] + '\n\n')
					#fp.close()					
					#if string.split(GROUPCHATS[groupchat][nick]['jid'], '/')[0] in ADMINS:
					fp = open(LOCALDB_FILE, 'r')
					localdb = eval(fp.read())
					fp.close()
					if GROUPCHATS[groupchat][nick]['jid'] and localdb.has_key(string.split(GROUPCHATS[groupchat][nick]['jid'], '/')[0]):
						msg(groupchat, nick + ': ' + localdb[string.split(string.split(GROUPCHATS[groupchat][nick]['jid'], '/')[0], '/')[0]])
					#elif localdb.has_key(nick):
					#	msg(groupchat, nick + ': ' + localdb[nick])
					#else:
					#	msg(groupchat, nick + ': ' + 'Welcome')
			elif namespace == 'vcard-temp':
				vcard = iq.getTag('VCARD') or iq.getTag('vCard') or iq.getTag('vcard')
				if vcard.getTag('FN'):
					GROUPCHATS[groupchat][nick]['fullname'] = vcard.getTag('FN').getData()
				elif vcard.getTag('N') and vcard.getTag('N').getTag('GIVEN') and vcard.getTag('N').getTag('FAMILY'):
					GROUPCHATS[groupchat][nick]['fullname'] = vcard.getTag('N').getTag('GIVEN').getData() + ' ' + vcard.getTag('N').getTag('FAMILY').getData()
				if vcard.getTag('NICKNAME'):
					GROUPCHATS[groupchat][nick]['nickname'] = vcard.getTag('NICKNAME').getData()
				if vcard.getTag('EMAIL'):
					GROUPCHATS[groupchat][nick]['email'] = vcard.getTag('EMAIL').getData()
				if vcard.getTag('URL'):
					GROUPCHATS[groupchat][nick]['url'] = vcard.getTag('URL').getData()
			elif namespace == 'jabber:iq:version':
				info = iq.getTag('query')
				GROUPCHATS[groupchat][nick]['client'] = info.getTag('name').getData()
				GROUPCHATS[groupchat][nick]['version'] = info.getTag('version').getData()
				GROUPCHATS[groupchat][nick]['os'] = info.getTag('os').getData()

def handler_userinfo_whois(type, source, parameters):
	groupchat = source[1]
	if GROUPCHATS.has_key(groupchat) and GROUPCHATS[groupchat].has_key(parameters):
		info = GROUPCHATS[groupchat][parameters]
		reply = ''
		if info.has_key('jid') and info['jid']:
			reply += '<' + info['jid'] + '> '
		if info.has_key('fullname') and info['fullname']:
			reply += info['fullname'] + ' '
		if info.has_key('nickname') and info['nickname']:
			reply += '(' + info['nickname'] + ') '
		if info.has_key('email') and info['email']:
			reply += '<' + info['email'] + '> '
		if info.has_key('client') and info['client']:
			reply += '- ' + info['client'] + ' ' + info['version'] + ' - ' + info['os']
		reply += ' [' + parameters + ']'
		smsg(type, source, reply)
	else:
		smsg(type, source, 'User Not In Chat [' + parameters + ']')

def handler_userinfo_idle(type, source, parameters):
	if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(parameters):
		nick = parameters
		groupchat = source[1]
		idletime = int(time.time() - GROUPCHATS[groupchat][nick]['idle'])
		reply = ''
		seconds = idletime % 60
		minutes = (idletime / 60) % 60
		hours = (idletime / 3600) % 60
		days = idletime / 216000
		if days: reply += str(days) + 'd '
		if hours: reply += str(hours) + 'h '
		if minutes: reply += str(minutes) + 'm '
		reply += str(seconds) + 's' + ' [' + parameters + ']'
	else:
		reply = 'Unknown' + ' [' + parameters + ']'
	smsg(type, source, reply)

def handler_userinfo_probe(type, source, parameters):
	iq = xmpp.Iq(parameters, 'get')
	iq.setQueryNS('jabber:iq:browse')
	response = JCON.SendAndWaitForResponse(iq)
	if response:
		iqtype = response.getType()
	else:
		iqtype = 'error'
	if iqtype == 'result':
		reply = 'Online [' + parameters + ']'
	else:
		reply = 'Offline [' + parameters + ']'
	smsg(type, source, reply)

def handler_userinfo_getlast(type, source, parameters):
	if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(parameters):
		nick = parameters
		groupchat = source[1]
		last_iq = xmpp.Iq(groupchat + '/' + nick, 'get')
		last_iq.setQueryNS('jabber:iq:last')
		last_result = JCON.SendAndWaitForResponse(last_iq)
		if last_result and last_result.getType() == 'result':
			idletime = int(last_result.getTag('query').getAttr('seconds'))
			reply = ''
			seconds = idletime % 60
			minutes = (idletime / 60) % 60
			hours = (idletime / 3600) % 60
			days = idletime / 216000
			if days: reply += str(days) + 'd '
			if hours: reply += str(hours) + 'h '
			if minutes: reply += str(minutes) + 'm '
			reply += str(seconds) + 's' + ' [' + parameters + ']'
		else:
			reply = 'Unknown' + ' [' + parameters + ']'
	else:
		reply = 'Unknown'
	smsg(type, source, reply)

def handler_userinfo_gettime(type, source, parameters):
	if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(parameters):
		nick = parameters
		groupchat = source[1]
		time_iq = xmpp.Iq(groupchat + '/' + nick, 'get')
		time_iq.setQueryNS('jabber:iq:time')
		time_result = JCON.SendAndWaitForResponse(time_iq)
		if time_result and time_result.getType() == 'result':
			timestring = time_result.getTag('query').getTag('display').getData()
			timezone = time_result.getTag('query').getTag('tz').getData()
			reply = timestring + ' - ' + timezone + ' [' + parameters + ']'
		else:
			reply = 'Unknown' + ' [' + parameters + ']'
	else:
		reply = 'Unknown' + ' [' + parameters + ']'
	smsg(type, source, reply)

register_join_handler(handler_userinfo_join)
register_message_handler(handler_userinfo_message)
register_iq_handler(handler_userinfo_iq)
register_command_handler(handler_userinfo_whois, '!whois', 0, 'Gives information on specified groupchat user.', '!whois [nick]', ['!whois mikem'])
register_command_handler(handler_userinfo_idle, '!idle', 0, 'Gives the idle time of a groupchat nick.', '!idle [nick]', ['!idle mikem'])
register_command_handler(handler_userinfo_probe, '!probe', 0, 'Tells if a server, agent, or user is online.', '!probe [JID]', ['!probe mikem@jabber.org', '!probe jabber.org', '!probe msn.jabber.org'])
register_command_handler(handler_userinfo_getlast, '!getlast', 0, 'Gives the iq:last idle reply of specified nick in groupchat.', '!getlast [nick]', ['!getlast mikem'])
register_command_handler(handler_userinfo_gettime, '!gettime', 0, 'Gives the iq:time time reply of specified nick in groupchat.', '!gettime [nick]', ['!gettime mikem'])
