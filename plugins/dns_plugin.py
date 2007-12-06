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
	reply += '\r\n' + geoip_get(ipaddr)

    else:
	reply = 'Unable to resolve'
    return reply

def geoip_get(parameters):
    if parameters.strip()=='':
	smsg(type, source, 'Empty Input')
	return
    else:
	parameters = parameters.strip()
	if len(parameters)>15:
			smsg(type, source, 'Wrong format')
			return
	postData = urllib.urlencode({'ips':parameters,'type':'','u':'','p':''})
        req2 = urllib2.Request('http://www.maxmind.com/app/locate_ip',postData)
	req2.add_header = ('User-agent', 'Mozilla/5.0')
        try:
    	    r = urllib2.urlopen(req2)
    	    target = r.read()
    	    od = re.search('Edition Results</span><p>',target)
    	    message = target[od.end():]
    	    message = message[:re.search('</table>',message).start()]
	    if len(message) != 0:
    		message = '\n' + message.strip()
	    else:
		message = 'Ooops. Nothing ;-)'
	    reply = ''
	    mass=[]
	    for line in message.split('\n'):
    		if re.match(' ',line):
		    line = line.replace(' ','')
		if re.search('<(td|th)>',line) and not re.search('Hostname',line):
	    	    mass.append(decode(line))
	    for i in xrange(0,12):
		if mass[i+13].strip() != '':
		    reply += str(mass[i]) + ': ' + str(mass[i+13]) + '\r\n'
	    maplink = 'http://maps.google.com/maps?q=' + str(mass[19]) + ',+' + str(mass[20])+ '&iwloc=A&hl=en'
	    reply += 'Google Maps URL: ' + maplink
	    return reply
        except:
	    return 'Error occured while querying maxmind.com'

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
