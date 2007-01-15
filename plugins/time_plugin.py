#$ neutron_plugin 01

def handler_time_date(type, source, parameters):
	reply = time.strftime('%a %d %b %H:%M:%S UTC %Y', time.gmtime())
	smsg(type, source, reply)

def handler_time_swatch(type, source, parameters):
	seconds_per_beat = 86.4
	(hour, minute, second) = time.gmtime()[3:6]
	gmt_seconds = (3600 * hour) + (60 * minute) + second
	seconds = gmt_seconds + 3600
	beats = float(seconds) / float(seconds_per_beat)
	if beats < 10:
		prefix = '00'
	elif beats < 100:
		prefix = '0'
	else:
		prefix = ''
	reply = '@' + prefix + str(round(beats, 2))	
	smsg(type, source, reply)

register_command_handler(handler_time_date, '!date', 0, 'Gives the current time and date.', '!date', ['!date'])
register_command_handler(handler_time_swatch, '!swatch', 0, 'Gives the current Swatch Internet time.', '!swatch', ['!swatch'])
