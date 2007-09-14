#$ neutron_plugin 01

def handler_presence_presence(prs):
	type = prs.getType()
	who = prs.getFrom()
	if not type:
		type = 'available'
	if type == 'subscribe':
		JCON.send(xmpp.Presence(to=who, typ='subscribed'))
		msg(who, 'Thanks for adding into your contacts.\ntype !commands to get list of available functionality.\nWBR, Neutron Bot.')
		print printc(color_yellow, 'Added to roster of: ' + str(who))
		#JCON.send(xmpp.Presence(to=who, typ='subscribe'))
	elif type == 'unsubscribe':
		JCON.send(xmpp.Presence(to=who, typ='unsubscribed'))
		msg(who, 'Why are you killing me?\nAt least, we were together ;-)\nWBR, Neutron Bot.')
		print printc(color_yellow, 'Removed from roster of: ' + str(who))
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
