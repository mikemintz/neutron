#$ neutron_plugin 01

import socket

def dns_query(query):
	try:
		int(query[-1])
	except ValueError:
		try:
			return socket.gethostbyname(query)
		except socket.gaierror:
			return 'Unable to Resolve'
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
