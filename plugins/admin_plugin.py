#$ neutron_plugin 01

def admin_groupchat_invite_handler(source, groupchat, body):
	if has_access(source, COMMANDS['!join']['access']):
		join_groupchat(groupchat)

def handler_admin_join(type, source, parameters):
	if parameters:
		if len(string.split(parameters)) > 1:
			(groupchat, nick) = string.split(parameters.lstrip(), ' ', 1)
		else:
			groupchat = parameters.strip()
			nick = DEFAULT_NICK
		smsg(type, source, 'Joined ' + groupchat)
		join_groupchat(groupchat, nick)
	else:
		smsg(type, source, 'Invalid Syntax')

def handler_admin_leave(type, source, parameters):
	if len(string.split(parameters)) > 0:
		groupchat = parameters.strip()
	else:
		groupchat = source[1]
	leave_groupchat(groupchat)
	smsg(type, source, 'Left ' + groupchat)


def handler_admin_msg(type, source, parameters):
	msg(string.split(parameters)[0], string.join(string.split(parameters)[1:]))
	smsg(type, source, 'Message Sent')

def handler_admin_say(type, source, parameters):
	if parameters:
		msg(source[1], parameters)
	else:
		smsg(type, source, 'Enter Message')

def handler_admin_restart(type, source, parameters):
	#os.startfile(sys.argv[0])
	smsg(type, source, 'Restarting')
	JCON.disconnect()
	os.execv('./neutron.py', sys.argv)

def handler_admin_exit(type, source, parameters):
	#os.startfile(sys.argv[0])
	smsg(type, source, 'Exiting')
	JCON.disconnect()
	os.abort()

def handler_admin_uptime(type, source, parameters):
	if BOOTUP_TIMESTAMP:
		idletime = int(time.time() - BOOTUP_TIMESTAMP)
		reply = 'Neutron bot is up for: '
		seconds = idletime % 60
		minutes = (idletime / 60) % 60
		hours = (idletime / 3600) % 60
		days = idletime / 216000
		if days: reply += str(days) + 'd '
		if hours: reply += str(hours) + 'h '
		if minutes: reply += str(minutes) + 'm '
		reply += str(seconds) + 's'
	else:
		reply = 'Unknown'
	smsg(type, source, reply)

def handler_admin_rooms(type, source, parameters):
	initialize_file(GROUPCHAT_CACHE_FILE, '[]')
	groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
        reply = '\nTotal Rooms: '+ str(len(groupchats)) + '\n' + '\n'.join(groupchats)
	smsg(type, source, reply)


register_command_handler(handler_admin_join, '!join', 100, 'Joins specified groupchat.', '!join <groupchat> [nick]', ['!join jabber@conference.jabber.org', '!join jdev@conference.jabber.org neutron2'])
register_command_handler(handler_admin_leave, '!leave', 100, 'Joins specified (or current) groupchat.', '!leave [groupchat]', ['!leave jabber@conference.jabber.org', '!leave'])
register_command_handler(handler_admin_msg, '!msg' ,100, 'Sends a message to specified JID.', '!msg <jid> <message>', ['!msg mikem@jabber.org hey mike!'])
register_command_handler(handler_admin_say, '!say', 100, 'Sends a message to current groupchat or to your JID if message is not through groupchat.', '!say <message>', ['!say hi'])
register_command_handler(handler_admin_restart, '!restart', 100, 'Restarts me.', '!restart', ['!restart'])
register_command_handler(handler_admin_exit, '!exit', 100, 'Exits completely.', '!exit', ['!exit'])
register_command_handler(handler_admin_uptime, '!uptime', 100, 'Returns Neutron uptime.', '!uptime', ['!uptime'])
register_command_handler(handler_admin_rooms, '!rooms', 100, 'Returns Neutron\'s rooms.', '!rooms', ['!rooms'])

register_groupchat_invite_handler(admin_groupchat_invite_handler)
