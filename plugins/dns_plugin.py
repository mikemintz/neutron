#$ neutron_plugin 01

import socket
import string

# Begin Gh0st addition
def get_extended_info(name):
    server = name.strip()
    if len(server) == 0:
	    server = 'www.sex.com'
    port = 80
    has_ip = 1
    try:
	ipaddr = socket.gethostbyname(server) 
    except:
	has_ip = 0
    reply = ''
    server_string = ''
    s = ''
    if has_ip == 1:    
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
	    conn.connect((socket.gethostbyname(server),port))
	    conn.send('HEAD / HTTP/1.0 \r\n\r\n')
	    s = conn.recv(256)
	    conn.close()
	except socket.error:
	    pass	

	if len(s) !=0 :
	    for line in string.split(s, "\r\n"):
        	if string.find(line,'Server:') == 0:
            	    server_string = line
		    server_string = string.replace(server_string, 'Server:', '')
	
	    if len(server_string) == 0:	
		for line in string.split(s, "\r\n"):
		    if string.find(line,'X-Powered-By:') == 0:
            		server_string = line
			server_string = string.replace(server_string, 'X-Powered-By:', '')

	reply = 'IP Address: ' + ipaddr + '\r\n'

	if len(server_string) !=0:

	    reply = reply +  'Server Type: ' + server_string + '\r\n'
	    server_web = 'active'	

	else:
	    server_web = 'offline'
	reply = reply +  'Website Status: ' + server_web 	

    else:
	reply = 'Unable to resolve'
    return reply

# End Gh0st addition
def dns_query(query):
	try:
		int(query[-1])
	except ValueError:
		# Patched by Gh0st
		return get_extended_info(query)
		
	else:
		try:
			(hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(query)
		except socket.herror:
			return 'Unable to Resolve'
		return hostname + ' ' + string.join(aliaslist) + ' ' + string.join(aliaslist)

def handler_dns_dns(type, source, parameters):
	if parameters.strip():
		result = dns_query(parameters)
		smsg(type, source, result)
	else:
		smsg(type, source, 'Invalid Syntax')

register_command_handler(handler_dns_dns, '!dns', 0, 'Returns the DNS lookup for a host or IP address.', '!dns <host/IP>', ['!dns jabber.org', '!dns 127.0.0.1'])
