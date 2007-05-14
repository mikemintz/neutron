#!/usr/bin/env python
# -*- coding: ISO-8859-15 -*-

#  Neutron
#  connection.py

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

import thread

from logging import getLogger
from os import execl, name as os_name
from string import split
from sys import argv, exit as sys_exit, executable as sys_executable
from time import sleep, time
from xmpp import Client, Iq, JID, Message, Presence
from xmpp import NS_CLIENT, NS_MUC, NS_MUC_USER, NS_VERSION

from config import Config

class Connection(Client):
    def __init__(self):
        self.Namespace = NS_CLIENT
        self.DBG = 'client'
        Client.__init__(self, server=Config().server,
                        port=Config().port,
                        debug=[])
        self.message_handlers = []
        self.outgoing_message_handlers = []
        self.join_handlers = []
        self.part_handlers = []
        self.iq_handlers = []
        self.presence_handlers = []
        self.groupchat_invite_handlers = []
        self.groupchat_decline_handlers = []
        self.groupchat_config_handlers = []
        self.command_handlers = {}
        self.logger = getLogger('connection')

    def connect(self):
        if Client.connect(self):
            self.RegisterHandler('message', self.MessageHandler)
            self.RegisterHandler('presence', self.PresenceHandler)
            self.RegisterHandler('iq', self.IqHandler)
            self.RegisterDisconnectHandler(self.DisconnectHandler)
            return True
        return False

    def MessageHandler(self, con, msg):
        #print unicode(msg)
        for x_node in msg.getTags('x', {}, NS_MUC_USER):
            decline = msg.getTag('decline')
            if decline:
                reason = decline.getTagData('reason')
                decliner_jid = JID(decline.getAttr('from'))
                if decliner_jid:
                    self.call_groupchat_decline_handlers(
                        [decliner_jid, decliner_jid.getStripped(),
                         decliner_jid.getResource()], msg.getAttr('from'),
                        reason)
                else: #is it possible ?
                    self.call_groupchat_decline_handlers([None, None, None],
                                                         x_node.getAttr('jid'),
                                                         reason)
                return
            invite = msg.getTag('invite')
            if invite:
                reason = invite.getTagData('reason')
                groupchat = JID(msg.getFrom())
                inviter_jid = JID(invite.getFrom())
                body = msg.getBody()
                password = x_node.getTagData('password')
                subject = msg.getSubject()
                self.call_groupchat_invite_handlers(
                    [inviter_jid, inviter_jid.getStripped(),
                     inviter_jid.getResource()], groupchat, subject, body,
                    reason, password)
                return
            statutes = x_node.getTags('status')
            if statutes:
                for status in statutes:
                    code = status.getAttr('code')
                    if code == 170:
                        element, new_value = 'logging', 'enabled'
                    elif code == 171:
                        element, new_value = 'logging', 'disabled'
                    elif code == 172:
                        element, new_value = 'room', 'non-anonymous'
                    elif code == 173:
                        element, new_value = 'room', 'semi-anonymous'
                    elif code == 174: #NOT RECOMMENDED by XEP-0045
                        element, new_value = 'room', 'fully-anonymous'
                    groupchat = JID(msg.getFrom())
                    self.call_groupchat_config_handlers(groupchat, element,
                                                        new_value)
                return
        msgtype = msg.getType()
        body = msg.getBody()
        if not body or not body.strip():
            return
        body = body.strip()
        fromjid = msg.getFrom()
        command = ''
        parameters = ''
        if body and body.split():
            command = body.split()[0].lower()
            if body.count(' '):
                parameters = body[(body.find(' ') + 1):]
        if not msg.timestamp:
            if msgtype == 'groupchat':
                t = 'public'
            else:
                t = 'private'
            self.call_message_handlers(t, [fromjid, fromjid.getStripped(),
                                           fromjid.getResource()], body)
            if command in self.command_handlers.keys():
                self.call_command_handlers(command, t, [fromjid,
                                                        fromjid.getStripped(),
                                                        fromjid.getResource()],
                                           parameters)

    def PresenceHandler(self, con, prs):
        #print unicode(prs)
        self.call_presence_handlers(prs)
        t = prs.getType()
        groupchat = prs.getFrom().getStripped()
        nick = prs.getFrom().getResource()
	
        if groupchat in Config().groupchats:
            if t == 'available' or t == None:
                if not Config().groupchats[groupchat]['participants'].has_key(nick):
                    jid = prs.getJid()
                    if jid:
                        jid = JID(jid)
                    else:
                        jid = prs.getFrom()
                    Config().groupchats[groupchat]['participants'][nick] = {'jid': jid, 'idle': time()}
                    self.call_join_handlers(groupchat, nick)
                    sleep(0.5)
            elif t == 'unavailable':
                if Config().groupchats[groupchat]['participants'].has_key(nick):
                    self.call_part_handlers(groupchat, nick)
                    del Config().groupchats[groupchat]['participants'][nick]
            elif t == 'error':
                try:
                    code = prs.asNode().getTag('error').getAttr('code')
                except:
                    code = None
                if code == '409': # name conflict
                    self.join(groupchat, nick + '_')
                    sleep(0.5)

    def IqHandler(self, con, iq):
        if iq.getTags('query', {}, NS_VERSION):
            result = iq.buildReply('result')
            query = result.getTag('query')
            query.setTagData('name', 'Neutron')
            query.setTagData('version', '0.5.42')
            query.setTagData('os', os_name)
            self.send(result)
        self.call_iq_handlers(iq)

    def DisconnectHandler(self):
        self.logger.info('disconnected')
        if Config().auto_restart:
            self.logger.info('waiting for restart...')
            sleep(240) # sleep for 240 seconds
            self.logger.info('restarting')
            execl(sys_executable, sys_executable, argv[0])
        else:
            sys_exit(0)

    def call_message_handlers(self, type, source, body):
        for handler in self.message_handlers:
            thread.start_new(handler, (type, source, body))

    def call_outgoing_message_handlers(self, target, body):
        for handler in self.outgoing_message_handlers:
            thread.start_new(handler, (target, body))

    def call_join_handlers(self, groupchat, nick):
        for handler in self.join_handlers:
            thread.start_new(handler, (groupchat, nick))

    def call_part_handlers(self, groupchat, nick):
        for handler in self.part_handlers:
            thread.start_new(handler, (groupchat, nick))

    def call_iq_handlers(self, iq):
        for handler in self.iq_handlers:
            thread.start_new(handler, (iq,))

    def call_presence_handlers(self, prs):
        for handler in self.presence_handlers:
            thread.start_new(handler, (prs,))

    def call_groupchat_invite_handlers(self, source, groupchat, subject, body,
                                       reason, password):
        for handler in self.groupchat_invite_handlers:
            thread.start_new(handler, (source, groupchat, subject, body,
                                       reason, password))

    def call_groupchat_decline_handlers(self, source, groupchat, reason):
        for handler in self.groupchat_decline_handlers:
            thread.start_new(handler, (source, groupchat, reason))

    def call_groupchat_config_handlers(self, groupchat, element, new_value):
        for handler in self.groupchat_config_handlers:
            thread.start_new(handler, (groupchat, element, new_value))

    def call_command_handlers(self, command, type, source, parameters):
        if self.command_handlers.has_key(command):
            if Config().has_access(source, self.command_handlers[command]['access']):
                thread.start_new(self.command_handlers[command]['handler'], (type, source, parameters))
            else:
                self.smsg(type, source, 'Unauthorized')
        
    def msg(self, target, body):
        msg = Message(target, body)
        if Config().groupchats.has_key(target):
            msg.setType('groupchat')
        else:
            msg.setType('chat')
        self.send(msg)
        self.call_outgoing_message_handlers(target, body)

    def smsg(self, type, source, body):
        if type == 'public':
            self.msg(source[1], source[2] + ': ' + body)
        elif type == 'private':
            self.msg(source[0], body)

    def join(self, groupchat, nick=None, password=None, auto=False):
        if nick is None:
            if Config().groupchats.has_key(groupchat):
                nick = Config().groupchats[groupchat]['nick']
            else:
                nick = Config().default_nick
        p = Presence(groupchat + '/' + nick)
        x = p.setTag('x', namespace=NS_MUC)
        if password:
            x.setTagData('password', password)
        self.send(p)
        Config().groupchats[groupchat] = {'autojoin': auto, 'nick': nick,
                                          'participants': dict()}
        Config().save('groupchats')

    def part(self, groupchat):
        self.send(Presence(groupchat, 'unavailable'))
        if Config().groupchats.has_key(groupchat):
            Config().groupchats[groupchat]['autojoin'] = False
            Config().save('groupchats')

    def get_groupchat(self, jid):
        if type(self, jid) is types.ListType:
            jid = jid[1]
        jid = unicode(jid).split('/')[0] # str(jid)
        if Config().groupchats.has_key(jid):
            return jid
        else:
            return None

