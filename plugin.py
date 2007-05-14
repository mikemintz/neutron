#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  plugin.py

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

from config import Config
from logging import getLogger
from os import access, F_OK

class Plugin:
    logger = getLogger('plugin')
    
    def __init__(self):
        pass

    def Plugin(self, cls, conn):
        cls.conn = conn
        cls.config = Config()
        cls.initialize_file = self.initialize_file
        cls.read_file = self.read_file
        cls.write_file = self.write_file
        cls.logger = getLogger('plugin.%s' % str(cls).split('.')[1])
        obj = cls()
        if obj.__dict__.has_key(self.__class__.__name__):
            Plugin.logger.error('Plugin %s v%s already plugged' % \
                                (obj.name, obj.version))
            raise
        obj.__dict__[self.__class__.__name__] = self
        for key in ('description', 'homepageurl', 'updateurl'):
            if obj.__dict__.has_key(key):
                continue
            obj.__dict__[key] = None
        for key, nb_args in [['message_handlers', 4],
                             ['outgoing_message_handlers', 3],
                             ['join_handlers', 3],
                             ['part_handlers', 3],
                             ['iq_handlers', 2],
                             ['presence_handlers', 2],
                             ['groupchat_invite_handlers', 7],
                             ['groupchat_decline_handlers', 4],
                             ['groupchat_config_handlers', 4]]:
            if obj.__dict__.has_key(key) and obj.__dict__[key]:
                for handler in obj.__dict__[key]:
                    if handler.func_code.co_argcount != nb_args:
                        Plugin.logger.error('Plugin %s v%s : handler %s doesn\'t have %s arguments !' % (obj.name, obj.version, handler.func_code.co_name, nb_args))
                        raise
                conn.__dict__[key].extend(obj.__dict__[key])
        if obj.__dict__.has_key('command_handlers') and \
               obj.__dict__['command_handlers']:
            for handler, command, access, description, syntax, examples in \
                    obj.__dict__['command_handlers']:
                if handler.func_code.co_argcount != 4:
                    Plugin.logger.error('Plugin %s v%s : handler %s doesn\'t have 4 arguments !' % (obj.name, obj.version, handler.func_code.co_name))
                    raise
                conn.__dict__['command_handlers'][command] = {
                    'handler' : handler,
                    'access' : access,
                    'description' : description,
                    'syntax' : syntax,
                    'examples' : examples}
        return obj

    def initialize_file(self, filename, data=''):
        if not access(filename, F_OK):
            fp = file(filename, 'w')
            if data:
                fp.write(data)
            fp.close()

    def read_file(self, filename):
        fp = file(filename)
        data = fp.read()
        fp.close
        return data

    def write_file(self, filename, data):
        fp = file(filename, 'w')
        fp.write(data)
        fp.close()

