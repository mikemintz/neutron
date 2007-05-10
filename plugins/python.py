# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  python.py

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

from os import popen
from sys import exc_info

class Python:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = '2.0'
        self.name = 'Python'
        self.description = ''
        self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
        self.updateurl = None
        self.command_handlers = [
            [self.handler_python_eval, '!eval', 100, 'Evaluates and returns a Python expression.', '!eval <expression>', ['!eval 1+1']],
            [self.handler_python_exec, '!exec', 100, 'Runs a Python statement.', '!exec <statement>', ['!eval pass']],
            [self.handler_python_sh, '!sh', 100, 'Executes a shell command.', '!sh <command>', ['!sh ls']]]
		

    def handler_python_eval(self, type, source, parameters):
        try:
            return_value = str(eval(parameters))
        except:
            return_value = str(exc_info()[0]) + ' - ' + str(exc_info()[1])
        self.conn.smsg(type, source, return_value)

    def handler_python_exec(self, type, source, parameters):
        if '\n' in parameters and parameters[-1] != '\n':
            parameters += '\n'
        try:
            exec parameters in globals()
            return_value = 'Successful Execution'
        except:
            return_value = str(exc_info()[0]) + ' - ' + str(exc_info()[1])
        self.conn.smsg(type, source, return_value)

    def handler_python_sh(self, type, source, parameters):
        pipe = popen('sh -c ' + parameters)
        #time.sleep(0.5)
        return_value = pipe.read(1024)
        self.conn.smsg(type, source, return_value)

