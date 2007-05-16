# -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  xep.py

#  Copyright (C) 2007 Anaël Verrier <elghinn@free.fr>

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

from re import compile as re_compile
from time import time
from urllib import urlopen

class Xep:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = '0.4.2'
        self.name = 'Xep'
        self.description = 'Search and display informations about xeps'
        self.homepageurl = ''
        self.updateurl = None
        self.command_handlers = [
            [self.handler_xep, '!xep', 0,
             'Search and display informations about xeps.',
             '!xep <expression>', ['!xep 45', '!xep archiving']]
            ]
        self.re_line = re_compile(r"""<tr class='tablebody'>
<td valign='top'><a href='http://www.xmpp.org/extensions/xep-\d+.html'>XEP-(\d+)</a></td>
<td valign='top'>(.+)</td>
<td valign='top'>(.+)</td>
<td valign='top'>(.+)</td>
<td valign='top'>(.+)</td>
</tr>""")
        self.cache = None
        self.cache_time = 0

    def handler_xep(self, type_, source, parameters):
        parameters = parameters.strip()
        if not parameters:
            self.conn.smsg(type_, source, 'I\'m not a toy')
            return
        if self.cache_time < int(time()) or not self.cache:
            try:
                page = urlopen('http://www.xmpp.org/extensions/').read()
                self.cache = self.re_line.findall(page)
                self.cache_time = int(time()) + 30
            except IOError:
                self.conn.smsg(type_, source, 'xmpp.org is down, retry later')
                return
        number = 0
        result = list()
        try:
            number = int(parameters)
            for xep in self.cache:
                if int(xep[0]) == number:
                    result.append('XEP-%s: %s is %s (%s, %s) See: \
http://xmpp.org/extensions/xep-%s.html'
                                  % (xep[0], xep[1], xep[2], xep[3], xep[4],
                                     xep[0]))
        except ValueError:
            pattern = parameters.lower()
            for xep in self.cache:
                if pattern in xep[1].lower():
                    result.append('XEP-%s: %s is %s (%s, %s) See: \
http://xmpp.org/extensions/xep-%s.html'
                                  % (xep[0], xep[1], xep[2], xep[3], xep[4],
                                     xep[0]))
        error = ''
        if not result:
            error = 'No match found'
        elif len(result) > 3:
            if len(parameters) < 4:
                error = 'Your search is too vague'
            else:
                count = len(result)
                result = result[:3]
                result.append('Your search is too vague (%s results)' % count)
        if error:
            self.conn.smsg(type_, source, error)
        else:
            self.conn.msg(source[1], '\n'.join(result))

