# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  help.py

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

class Help:
    def __init__(self):
	self.neutron_version = ('0.5.42')
	self.version = '2.0'
	self.name = 'Help'
	self.description = 'Some help about Neutron\'s commands'
	self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
	self.updateurl = None
        self.command_handlers = [
            [self.handler_help_help, 'help', 0, 'Send basic help message or gives information on specified command.', 'help [command]', ['help', 'help help']],
            [self.handler_help_commands, '!commands', 0, 'Send list of commands.', '!commands', ['!commands']]]

    def handler_help_help(self, type, source, parameters):
        if parameters and self.conn.command_handlers.has_key(parameters):
            reply = self.conn.command_handlers[parameters]['description'] + ' Usage: ' + self.conn.command_handlers[parameters]['syntax'] + '\nExamples:'
            for example in self.conn.command_handlers[parameters]['examples']:
                reply += '\n  *  ' + example
            reply += '\nRequired Access Level: ' + str(self.conn.command_handlers[parameters]['access'])
        else:
            reply = 'Type !commands for a list of commands.'
        self.conn.smsg(type, source, reply)

    def handler_help_commands(self, type, source, parameters):
        commandlist = []
        for command in self.conn.command_handlers.keys():
            if self.config.has_access(source, self.conn.command_handlers[command]['access']):
                commandlist.append(command)
        commandlist.sort()
        commandlist = ' '.join(commandlist)
        self.conn.smsg('private', source, commandlist)

