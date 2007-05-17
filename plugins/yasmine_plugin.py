#$ neutron_plugin 01

def handler_yasmine_uptime(type, source, parameters):
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

def handler_cache_rooms(type, source, parameters):
	reply = '' 
	initialize_file(GROUPCHAT_CACHE_FILE, '[]')
	groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
	for groupchat in groupchats:
		reply += str(groupchat) + '\n'
	smsg(type, source, reply)


register_command_handler(handler_yasmine_uptime, '!uptime', 0, 'Returns Neutron uptime.', '!uptime', ['!uptime'])
register_command_handler(handler_cache_rooms, '!rooms', 100, 'Returns Neutron\'s rooms.', '!rooms', ['!rooms'])
