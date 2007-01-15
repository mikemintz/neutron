#$ neutron_plugin 01

def handler_presence_presence(prs):
	type = prs.getType()
	who = prs.getFrom()
	if not type:
		type = 'available'
	if type == 'subscribe':
		JCON.send(xmpp.Presence(to=who, typ='subscribed'))
		#JCON.send(xmpp.Presence(to=who, typ='subscribe'))
	elif type == 'unsubscribe':
		JCON.send(xmpp.Presence(to=who, typ='unsubscribed'))
		#JCON.send(xmpp.Presence(to=who, typ='unsubscribe'))
	elif type == 'subscribed':
		pass
	elif type == 'unsubscribed':
		pass
	elif type == 'available':
		pass
	elif type == 'unavailable':
		pass

register_presence_handler(handler_presence_presence)
