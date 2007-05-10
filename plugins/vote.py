# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  vote.py

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

class Vote:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = '2.0'
        self.name = 'Admin'
        self.description = 'Allow to control Neutron'
        self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
        self.updateurl = None
        self.command_handlers = [
            [self.handler_vote_vote, '!vote', 0, 'Casts a vote for current poll.', '!vote <option>', ['!vote yes']],
            [self.handler_vote_newpoll, '!newpoll', 100, 'Creates a new poll, or if options are added, submits the poll to current channel.', '!newpoll [question]', ['!newpoll Do you like turtles?', '!newpoll']],
	    [self.handler_vote_polloption, '!polloption', 100, 'Adds an option to the current poll.', '!polloption <option>', ['!polloption yes']],
	    [self.handler_vote_endpoll, '!endpoll', 100, 'Ends the poll and returns the results.', '!endpoll]', ['!endpoll']]]
        self.current_poll = {}

    def handler_vote_vote(self, type, source, parameters):
        if self.config.groupchats.has_key(source[1]) and self.config.groupchats[source[1]].has_key(source[2]):
	    if self.current_poll:
		if self.config.isadmin(self.config.groupchats[source[1]][source[2]]['jid']) or not self.config.groupchats[source[1]][source[2]]['jid'] in self.current_poll['jids']:
                    if self.current_poll['options'].has_key(parameters.strip().lower()):
                        self.current_poll['options'][parameters.strip().lower()] += 1
                        self.current_poll['jids'].append(self.config.groupchats[source[1]][source[2]]['jid'])
                        self.conn.smsg(type, source, 'Vote Counted')
                    else:
                        self.conn.smsg(type, source, 'Option Not Available')
                else:
                    self.conn.smsg(type, source, 'You already voted.')
            else:
                self.conn.smsg(type, source, 'There\'s no poll going on right now.')
	else:
            self.conn.smsg(type, source, 'You must vote from the groupchat.')

    def handler_vote_newpoll(self, type, source, parameters):
        if self.current_poll:
            poll_text = 'New Poll (' + source[2] + ') - ' + self.current_poll['question'] + '\n'
            for option in self.current_poll['options'].keys():
                poll_text += '  *  ' + option + '\n'
            poll_text += 'To vote, type or message me the following: !vote <option>'
            self.conn.msg(source[1], poll_text)
        else:
            self.current_poll = {'options': {}, 'question': parameters, 'jids': []}
            self.conn.smsg(type, source, 'Poll Created')

    def handler_vote_polloption(self, type, source, parameters):
        if self.current_poll:
            self.current_poll['options'][parameters.strip().lower()] = 0
            self.conn.smsg(type, source, 'Option Added')
        else:
            self.conn.smsg(type, source, 'Error: No Poll')

    def handler_vote_endpoll(self, type, source, parameters):
        if self.current_poll:
            poll_text = 'Poll Results (' + source[2] + ') - ' + self.current_poll['question'] + '\n'
            num = 1
            for option in self.current_poll['options'].keys():
                poll_text += str(self.current_poll['options'][option]) + ' - ' + option + '\n'
                num += 1
            self.conn.msg(source[1], poll_text)
            self.current_poll = {}
        else:
            self.conn.smsg(type, source, 'Error: No Poll')

