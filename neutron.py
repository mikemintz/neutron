#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-

#  Neutron
#  neutron.py

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

from datetime import datetime
from optparse import OptionParser
from os import access, getcwd, getpid, listdir
from os import F_OK, R_OK, W_OK
from os.path import join as path_join
from sys import exc_info, exit as sys_exit, path
from traceback import print_exc

from config import Config
from connection import Connection
from plugin import Plugin

path.insert(1, 'modules')

class Neutron:
    def __init__(self):
        parser  =  OptionParser() 
        parser.add_option('-c',  '--config-file',
                          action='store',
                          type='string',
                          dest='config_filename',
                          help='the pathname of the config file',
                          metavar="PATHNAME",
                          default='neutron.cfg')
        parser.add_option('-p',  '--pid-file',
                          action='store',
                          type='string',
                          dest='pid_filename',
                          help='the pathname of the process ID file',
                          metavar='PATHNAME',
                          default='neutron.pid')
        (self.options, args) = parser.parse_args()

        try:
            fp = open(self.options.pid_filename, 'w')
            fp.write(str(getpid()))
            fp.close()
        except(IOError):
            print 'ERROR: pid-file "%s" is not accessible' % \
                  (self.options.config_filename)
            sys_exit(1)
        try:
            self.config = Config(self.options.config_filename)
        except(IOError):
            print 'ERROR: config-file "%s" is not accessible' % \
                  (self.options.config_filename)
            sys_exit(1)
        self.conn = Connection()
        self.loaded_sysplugins = []
        self.loaded_plugins = []

    def __del__(self):
        if(self.__dict__.has_key('options') and self.options.pid_filename):
            from os import unlink
            unlink(self.options.pid_filename)

    def connect(self):
        if self.conn.connect():
            print 'Connected'
        else:
            print 'ERROR: Couldn\'t connect'
            sys_exit(1)
        if self.conn.auth(self.config.username,
                          self.config.password,
                          self.config.resource):
            print 'Logged In'
        else:
            print 'ERROR: %s %s' % (self.conn.lastErrCode, self.conn.lastErr)
            sys_exit(1)
        self.conn.sendInitPresence()


    def autojoin_rooms(self):
        for groupchat in Config().groupchats.iterkeys():
            self.conn.join(groupchat)
            #time.sleep(0.5)

    def load_plugins(self):
        plugins = listdir('plugins')
        plugins.remove('__init__.py')
        for plugin in plugins:
            if plugin[-3:].lower() == '.py':
                try:
                    plugin_name = plugin[:-3]
                    plug = __import__(''.join(['plugins.', plugin_name]))
                    cls = getattr(getattr(plug, plugin_name),
                                  plugin_name.capitalize())
                    obj = Plugin().Plugin(cls, self.conn)
                    self.loaded_plugins.append(obj) 
                    print 'plugin %s v%s loaded' % (obj.name, obj.version)
                    plug = None
                except:
                    print 'WARNING: Coulndn\'t load plugin "%s"' % (plugin)
                    print '>>%s: %s' % (exc_info()[0].__name__, exc_info()[1])

    def loop(self):
        while 1:
            self.conn.Process(10)

        
#-----------------------------------------------------------------------------
if __name__ == '__main__':
    t0 = datetime.now()
    try:
        neutron = Neutron()
        neutron.load_plugins()
        neutron.connect()
        neutron.autojoin_rooms()
        neutron.loop()
    except KeyboardInterrupt:
        print 'Keyboard Interrupt'
    except SystemExit:
        pass
    except:
        print_exc()
    print 'uptime: %s' % (str(datetime.now() - t0))
    print 'Bye :\'('


