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



"""
TERMS OF USE: You are not authorized to access or query our Whois 
database through the use of electronic processes that are high-volume and 
automated except as reasonably necessary to register domain names or 
modify existing registrations; the Data in VeriSign Global Registry 
Services' ("VeriSign") Whois database is provided by VeriSign for 
information purposes only, and to assist persons in obtaining information 
about or related to a domain name registration record. VeriSign does not 
guarantee its accuracy. By submitting a Whois query, you agree to abide 
by the following terms of use: You agree that you may use this Data only 
for lawful purposes and that under no circumstances will you use this Data 
to: (1) allow, enable, or otherwise support the transmission of mass 
unsolicited, commercial advertising or solicitations via e-mail, telephone, 
or facsimile; or (2) enable high volume, automated, electronic processes 
that apply to VeriSign (or its computer systems). The compilation, 
repackaging, dissemination or other use of this Data is expressly 
prohibited without the prior written consent of VeriSign. You agree not to 
use electronic processes that are automated and high-volume to access or 
query the Whois database except as reasonably necessary to register 
domain names or modify existing registrations. VeriSign reserves the right 
to restrict your access to the Whois database in its sole discretion to ensure 
operational stability.  VeriSign may restrict or terminate your access to the 
Whois database for failure to abide by these terms of use. VeriSign 
reserves the right to modify these terms at any time. 
"""

def handler_domain_rwhois(type, source, parameters):
	parameters = parameters.strip()
	if not parameters:
		reply = 'Wrong Syntax'
		smsg(type, source, reply)
		return
	rec = rwhois.WhoisRecord();
	whoisserver=None
	domain = parameters
	if string.find(domain,'@')!=-1:
		(domain,whoisserver)=string.split(domain,'@')
	try:
		rec.whois(domain,whoisserver)
		reply =  rec.page
	except 'NoSuchDomain', reason:
		reply =  "ERROR: no such domain %s" % domain
	except socket.error, (ecode,reason):
		reply =  reason
	except "TimedOut", reason:
		reply = "Timed out", reason
	smsg(type, source, reply)
	

register_command_handler(handler_domain_domain, '!domain', 0, 'Returns information on specified domain.', '!domain <domain>', ['!domain jabber.org'])
register_command_handler(handler_domain_rwhois, '!rwhois', 100, 'Returns information on specified domain.', '!rwhois <domain>', ['!rwhois jabber.org'])
