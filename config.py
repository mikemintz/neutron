#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-

#  Neutron
#  config.py

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

from os import getpid
from random import randrange
from sys import exit as sys_exit
from types import InstanceType
from xml.dom.minidom import parse as xml_parse

class Config(object):
    _ref = None
    _ref2 = None

    def __new__(cls, *args, **kw):
        if cls._ref is None:
            cls._ref = super(Config, cls).__new__(cls, *args, **kw)
        return cls._ref
    
    def __init__(self, filename = 'config.txt'):
        if Config._ref2 is None:
            Config._ref2 = 42
        else:
            return
        self.filename = filename
        doc = xml_parse(self.filename)
        self.getElements = doc.documentElement.getElementsByTagName
        #nodes = [('node-name', parse?),...]
        nodes = [('server', False), ('port', False),
                 ('username', False), ('password', False),
                 ('resource', True), ('default-nick', True),
                 ('admin-password', True), ('auto-restart', False),
                 ('public-log-dir', True), ('private-log-dir', True)]
        selfdict = self.__dict__
        for node in nodes:
            selfdict[node[0].replace('-','_')] = self.getValue(node[0], node[1])
        self.admins = list()
        for e in self.getElements('admin'):
            self.admins.append(e.firstChild.data)
        self.access = dict()
        for e in self.getElements('access'):
            pass
        self.groupchats = dict()
        for e in self.getElements('groupchat'):
            autojoin = int(e.getAttribute('autojoin'))
            jid = e.getElementsByTagName('jid')[0].firstChild.data
            nick = e.getElementsByTagName('nick')[0].firstChild.data
            self.groupchats[jid] = {'autojoin': autojoin, 'nick': nick,
                                    'participants': dict()}

        del self.getElements #GC can now erase doc

        for jid in self.admins:
            self.change_access_perm(jid, 100)
            
        need_save_config = False
        for jid in self.access.keys():
            if self.access[jid] == 0:
                need_save_config = True
                del self.access[jid]
        if need_save_config:
            self.save('access')

    def getValue(self, name, parse):
        if parse:
            return self.parse_string(self.getElements(name)[0])
        value = self.getElements(name)[0].firstChild.data
        try:
            return int(value)
        except ValueError:
            return value

    def parse_string(self, parent):
        string = list()
        app = string.append
        for node in parent.childNodes:
            if node.nodeName == '#text':
                app(node.data)
            elif node.nodeName == 'pid':
                app(str(getpid()))
            elif node.nodeName == 'random':
                rmin, rmax, rstep = 0, 42, 1
                if node.hasAttribute('min'):
                    rmin = int(node.getAttribute('min'))
                if node.hasAttribute('max'):
                    rmax = int(node.getAttribute('max'))
                if node.hasAttribute('step'):
                    rstep = int(node.getAttribute('step'))
                app(str(randrange(rmin, rmax, rstep)))
            else:
                print 'ERROR: config file is corrupt'
                sys_exit(1)
        return ''.join(string)

    def save(self, element):
        if element == 'access':
            pass
        elif element == 'groupchats':
            pass
        else:
            pass

    def change_access_temp(self, source, level=0):
        jid = self.get_true_jid(source)
        try:
            level = int(level)
        except:
            level = 0
        self.access[jid] = level

    def change_access_perm(self, source, level=0):
        jid = self.get_true_jid(source)
        try:
            level = int(level)
        except:
            level = 0
        #temp_access = eval(read_file(ACCESS_FILE))
        #temp_access[jid] = level
        #write_file(ACCESS_FILE, str(temp_access))
        self.access[jid] = level

    def user_level(self, source):
        jid = self.get_true_jid(source)
        if self.access.has_key(jid):
            return self.access[jid]
        else:
            return 0

    def has_access(self, source, required_level):
        jid = self.get_true_jid(source)
        if self.user_level(jid) >= required_level:
            return 1
        return 0

    def get_true_jid(self, jid):
        true_jid = ''
        if isinstance(jid, list):
            jid = jid[0]
        if isinstance(jid, InstanceType):
            jid = unicode(jid) # str(jid)
        split_jid = jid.split('/', 1)
        stripped_jid = split_jid[0]
        resource = ''
        if len(split_jid) == 2:
            resource = split_jid[1]
        if (self.groupchats.has_key(stripped_jid) and
            self.groupchats[stripped_jid].has_key(resource)):
            true_jid = unicode(self.groupchats[stripped_jid][resource]['jid']).split('/', 1)[0]
        else:
            true_jid = stripped_jid
        return true_jid

    def is_admin(self, jid):
        admin_list = self.admins
        if type(jid) is types.ListType:
            jid = jid[0]
        jid = str(jid)
        stripped_jid = jid.split('/', 1)[0]
        resource = ''
        if len(jid.split('/', 1)) == 2:
            resource = jid.split('/', 1)[1]
        if stripped_jid in admin_list:
            return 1
        elif self.groupchats.has_key(stripped_jid):
            if self.groupchats[stripped_jid].has_key(resource):
                if self.groupchats[stripped_jid][resource]['jid'].split('/', 1)[0] in admin_list:
                    return 1
        return 0
