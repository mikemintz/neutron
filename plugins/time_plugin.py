#$ neutron_plugin 01

import socket
import struct

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

# Modified by Gh0st, AKA Bohdan Turkynewych


# Based on Simon Foster's simple SNTP client from ASPN Python cookbook.
# Adapted by Paul Rubin; this script lives at:
#    http://www.nightsong.com/phr/python/setclock.py


def handler_time_ntptime(type, source, parameters):
    reply = ''
    time_server = (socket.gethostbyname('pool.ntp.org'), 123)
    TIME1970 = 2208988800L      # Thanks to F.Lundh
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    data = '\x1b' + 47 * '\0'
    client.sendto(data, time_server)
    data, address = client.recvfrom( 1024 )
    if data:
	reply = 'Response received from ' + str(address[0]) + '\n'
	t = struct.unpack( '!12I', data )[10]
	if t == 0:
    	    reply = 'invalid response'
	ct = time.asctime(time.gmtime(t - TIME1970))
	reply += 'Current time (GMT/UTC): ' + str(ct)
    else:
	reply =  'no data returned'
    smsg(type, source, reply)

# end of setclock.py

register_command_handler(handler_time_ntptime, '!ntptime', 0, 'Gives the current time and date from pool.ntp.org.', '!ntptime', ['!ntptime'])
register_command_handler(handler_time_date, '!date', 0, 'Gives the current time and date.', '!date', ['!date'])
register_command_handler(handler_time_swatch, '!swatch', 0, 'Gives the current Swatch Internet time.', '!swatch', ['!swatch'])
