# -*- coding: koi8-u -*-

#  Neutron plugin
#  ddns.py

#  Copyright (C) 2002-2006 Mike Mintz <mikemintz@gmail.com>
#  Copyright (C) 2007 Mike Mintz <mikemintz@gmail.com>
#                     AnaКl Verrier <elghinn@free.fr>
#  Parts of code:
#  Author: Bohdan Turkynewych, AKA Gh0st, tb0hdan[at]gmail.com
    
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import socket
import string

class Ddns:
    def __init__(self):
	self.neutron_version = ('0.5.42')
	self.version = '0.1'
	self.name = 'Ddns'
	self.description = 'Provides DNS resolve/backresolve capability'
	self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
	self.updateurl = None
        self.command_handlers = [[self.handler_domain_dns, '!dns', 0, 'Returns the DNS lookup for a host or IP address', '!dns <domain/IP>', ['!dns jabber.org']]]


    # Begin Gh0st addition
    def get_extended_info(self, name):
	server = name.strip()
	if len(server) == 0:
	    # any other names may appear offensive to someone.
	    server = 'nowhere.org'
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
    def dns_query(self, query):
	    try:
		int(query[-1])
	    except ValueError:
		# Patched by Gh0st
		return self.get_extended_info(query)
		
	    else:
		    try:
		    	(hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(query)
		    except socket.herror:
			return 'Unable to Resolve'
		    return hostname + ' ' + string.join(aliaslist) + ' ' + string.join(aliaslist)

    def handler_domain_dns(self, type, source, parameters):
		if parameters.strip():
			result = self.dns_query(parameters)
		        self.conn.smsg(type, source, result)
		else:
		    self.conn.smsg(type, source, 'Invalid Syntax')
