# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  admin.py

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

from os import abort, execv
from sys import exit as sys_exit

class Admin:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = '2.0'
        self.name = 'Admin'
        self.description = 'Allow to control Neutron'
        self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
        self.updateurl = None
        self.command_handlers = [
            [self.handler_admin_join, '!join', 100, 'Joins specified groupchat.', '!join <groupchat> [nick]', ['!join jabber@conference.jabber.org', '!join jdev@conference.jabber.org neutron2']],
            [self.handler_admin_part, '!part', 100, 'Joins specified (or current) groupchat.', '!leave [groupchat]', ['!leave jabber@conference.jabber.org', '!leave']],
            [self.handler_admin_msg, '!msg' , 100, 'Sends a message to specified JID.', '!msg <jid> <message>', ['!msg mikem@jabber.org hey mike!']],
            [self.handler_admin_say, '!say', 100, 'Sends a message to current groupchat or to your JID if message is not through groupchat.', '!say <message>', ['!say hi']],
            [self.handler_admin_restart, '!restart', 100, 'Restarts me.', '!restart', ['!restart']],
            [self.handler_admin_exit, '!exit', 100, 'Exits completely.', '!exit', ['!exit']]]
        self.groupchat_invite_handlers = [self.admin_groupchat_invite_handler]


    def admin_groupchat_invite_handler(self, source, groupchat, subject, body,
                                       reason, password):
        if self.config.has_access(source, self.conn.command_handlers['!join']['access']):
            self.conn.join(groupchat, password=password)

    def handler_admin_join(self, type, source, parameters):
        if parameters:
            if len(parameters.split()) > 1:
                (groupchat, nick) = parameters.lstrip().split(' ', 1)
                self.conn.join(groupchat, nick)
            else:
                groupchat = parameters.strip()
                self.conn.join(groupchat)
            self.conn.smsg(type, source, 'Joined ' + groupchat)
        else:
            self.conn.smsg(type, source, 'Invalid Syntax')

    def handler_admin_part(self, type, source, parameters):
        if len(parameters.split()) > 0:
            groupchat = parameters.strip()
        else:
            groupchat = source[1]
        self.conn.part(groupchat)
        self.conn.smsg(type, source, 'Left ' + groupchat)

    def handler_admin_msg(self, type, source, parameters):
        self.conn.msg(parameters.split()[0], ' '.join(parameters.split()[1:]))
        self.conn.smsg(type, source, 'Message Sent')

    def handler_admin_say(self, type, source, parameters):
        if parameters:
            self.conn.msg(source[1], parameters)
        else:
            self.conn.smsg(type, source, 'Enter Message')

    def handler_admin_restart(self, type, source, parameters):
        ##os.startfile(sys.argv[0])
        self.conn.smsg(type, source, 'Restarting')
        self.conn.disconnect()
        execv('./neutron.py', sys.argv)

    def handler_admin_exit(self, type, source, parameters):
        ##os.startfile(sys.argv[0])
        self.conn.smsg(type, source, 'Exiting')
        self.config.halt = True
        self.conn.disconnect()
        sys_exit(0)

