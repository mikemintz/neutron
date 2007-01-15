# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  access.py

#  Copyright (C) 2002-2006 Mike Mintz <mikemintz@gmail.com>
#  Copyright (C) 2007 Mike Mintz <mikemintz@gmail.com>
#                     Anaël Verrier <elghinn@free.fr>

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

class Access:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = "2.0"
        self.name = 'Access'
        self.description = 'Allow to control Neutron access'
        self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
        self.updateurl = None
        self.command_handlers = [
		[self.handler_access_login, '!login', 0, 'Logs in as admin.', '!login <password>', ['!login mypassword']],
		[self.handler_access_login, '!logout', 0, 'Logs out of admin.', '!logout', ['!logout']],
		[self.handler_access_view_access, '!view_access', 0, 'Returns access level of specified JID. JID defaults to requester.', '!view_access [JID]', ['!view_access', '!view_access mikem@jabber.org']],
		[self.handler_access_set_access, '!set_access', 100, 'Sets the access level of specified JID to specified level. If a third parameter is defined, the change will be permanent, otherwise it will reset when Neutron exits.', '!set_access <JID> <level#> [permanent]', ['!set_access mikem@jabber.org 100', '!set_access mikem@jabber.org 100 blabla']]]

    def handler_access_login(self, type, source, parameters):
        if type == 'public':
	    self.conn.smsg(type, source, 'Please login privately so others do not see the password.')
        elif type == 'private':
            jid = self.config.get_true_jid(source)
            if parameters.strip() == self.config.admin_password:
                change_access_temp(jid, 100)
                self.conn.smsg(type, source, 'Access Granted')
            else:
                self.conn.smsg(type, source, 'Access Denied')

    def handler_access_logout(self, type, source, parameters):
        jid = self.config.get_true_jid(source)
        self.config.change_access_temp(jid, 0)
        self.conn.smsg(type, source, 'Successfully Logged Out')

    def handler_access_view_access(self, type, source, parameters):
        if not parameters.strip():
            self.conn.smsg(type, source, str(self.config.user_level(source)))
        else:
            self.conn.smsg(type, source, str(self.config.user_level(parameters)))

    def handler_access_set_access(self, type, source, parameters):
	splitdata = parameters.split()
	if len(splitdata) == 2:
		self.config.change_access_temp(splitdata[0], splitdata[1])
		self.conn.smsg(type, source, 'Temporary Access Change Successful')
	elif len(splitdata) == 3:
		self.config.change_access_perm(splitdata[0], splitdata[1])
		self.conn.smsg(type, source, 'Permanent Access Change Successful')
	else:
		self.conn.smsg(type, source, 'Invalid Syntax')



