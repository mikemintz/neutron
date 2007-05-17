#$ neutron_plugin 01

import rwhois

def handler_domain_domain(type, source, parameters):
	rec = rwhois.WhoisRecord(parameters)
	try:
		rec.whois()
		reply = 'Registered'
	except 'NoSuchDomain', reason:
		reply = 'AVAILABLE'
	except socket.error, (ecode,reason):
		reply = 'Socket Error'
	except "TimedOut", reason:
		reply = 'Timed Out'
	smsg(type, source, reply)

register_command_handler(handler_domain_domain, '!domain', 0, 'Returns information on specified domain.', '!domain <domain>', ['!domain jabber.org'])
