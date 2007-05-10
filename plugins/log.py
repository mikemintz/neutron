## -*- coding: ISO-8859-15 -*-

#  Neutron plugin
#  log.py

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

import re

from math import modf
from os import access, makedirs, path
from os import F_OK
from time import localtime, strftime, time

class Log:
    def __init__(self):
	self.neutron_version = ('0.5.42')
	self.version = '2.0'
	self.name = 'Log'
	self.description = 'Log conversations'
	self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
	self.updateurl = None
        self.log_cache_file = 'logcache.txt'
        self.initialize_file(self.log_cache_file, '{}')
        self.log_cache = eval(self.read_file(self.log_cache_file))
        #if self.config.public_log_dir or self.config.private_log_dir:
        self.message_handlers = [self.log_handler_message]
        #if self.config.private_log_dir:
        self.outgoing_message_handlers = [self.log_handler_outgoing_message]
        self.join_handlers = [self.log_handler_join]
        self.part_handlers = [self.log_handler_part]

    def log_write_header(self, fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
        date = strftime('%A, %B %d, %Y', (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
        fp.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<title>%s</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<style type="text/css">
<!--
.timestamp {color: #aaa;}
.timestamp a {color: #aaa; text-decoration: none;}
.system {color: #090; font-weight: bold;}
.emote {color: #a09;}
.self {color: #c00;}
.normal {color: #00a;}
#mark { color: #aaa; text-align: right; font-family: monospace; letter-spacing: 3px }
h1 { color: #369; font-family: sans-serif; border-bottom: #246 solid 3pt; letter-spacing: 3px; margin-left: 20pt; }
h2 { color: #639; font-family: sans-serif; letter-spacing: 2px; text-align: center }
//-->
</style>
</head>
<body>
<div id="mark">neutron log</div>
<h1>%s</h1>
<h2>%s</h2>
<div>
<tt>
""" % (' - '.join([source, date]), source, date))

    def log_write_footer(self, fp):
        fp.write('\n</tt>\n</div>\n</body>\n</html>')

    def log_get_fp(self, type, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings)):
        if type == 'public':
            logdir = self.config.public_log_dir
        else:
            logdir = self.config.private_log_dir
        if logdir[-1] == '/':
            logdir = logdir[:-1]
        str_year = str(year)
        str_month = str(month)
        str_day = str(day)
        filename = '.'.join(['/'.join([logdir, source, str_year, str_month, str_day]), 'html'])
        alt_filename = '.'.join(['/'.join([logdir, source, str_year, str_month, str_day]), '_alt.html'])
        if not path.exists('/'.join([logdir, source, str_year, str_month])):
            makedirs('/'.join([logdir, source, str_year, str_month]))
        if self.log_cache.has_key(source):
            if self.log_cache[source] != filename:
                fp_old = file(self.log_cache[source], 'a')
                self.log_write_footer(fp_old)
                fp_old.close()
            if path.exists(filename):
                fp = file(filename, 'a')
                return fp
            else:
                self.log_cache[source] = filename
                self.write_file(self.log_cache_file, str(self.log_cache))
                fp = file(filename, 'w')
                self.log_write_header(fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
                return fp
        else:
            if path.exists(filename):
                self.log_cache[source] = filename
                self.write_file(self.log_cache_file, str(self.log_cache))
                fp = file(alt_filename, 'a')
                # self.log_write_header(fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
                return fp
            else:
                self.log_cache[source] = filename
                #self.write_file(self.log_cache_file, str(self.log_cache))
                fp = file(filename, 'w')
                self.log_write_header(fp, source, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
                return fp

    def log_regex_url(self, matchobj):
        # 06.03.05(Sun) slipstream@yandex.ru urls parser
        return '<a href="' + matchobj.group(0) + '">' + matchobj.group(0) + '</a>'

    def log_handler_message(self, type, source, body):
        if not body:
            return
        if type == 'public' and self.config.public_log_dir:
            groupchat = source[1]
            nick = source[2]
            self.log_write(body, nick, type, groupchat)
        elif type == 'private' and self.config.private_log_dir:
            jid = self.config.get_true_jid(source)
            self.log_write(body, jid.split('@')[0], type, jid)

    def log_handler_outgoing_message(self, target, body):
        if self.config.groupchats.has_key(target) or not body:
            return
        self.log_write(body, self.config.default_nick, 'private',
                       self.config.get_true_jid(target))

    def log_write(self, body, nick, type, jid):
        jid = self.config.get_true_jid(jid)
        decimal = str(int(modf(time())[0]*100000))
        (year, month, day, hour, minute, second, weekday, yearday, daylightsavings) = localtime()
        # 06.03.05(Sun) slipstream@yandex.ru urls parser & line ends
        body = body.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
        body = re.sub('(http|ftp)(\:\/\/[^\s<]+)', self.log_regex_url, body)
        body = body.replace('\n', '<br />')
        body = body.encode('utf-8');
        nick = nick.encode('utf-8');
        timestamp = '[%.2i:%.2i:%.2i]' % (hour, minute, second)
        fp = self.log_get_fp(type, jid, (year, month, day, hour, minute, second, weekday, yearday, daylightsavings))
        fp.write('<span class="timestamp"><a id="t' + timestamp[1:-1] + '.' + decimal + '" href="#t' + timestamp[1:-1] + '.' + decimal + '">' + timestamp + '</a></span> ')
        if not nick:
            fp.write('<span class="system">' + body + '</span><br />\n')
        elif body[:3].lower() == '/me':
            fp.write('<span class="emote">* %s%s</span><br />\n' % (nick, body[3:]))
        elif ((type == 'public' and nick == self.config.groupchats[jid]['nick'].encode('utf-8')) or
              nick == self.config.default_nick):
            fp.write('<span class="self">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
        else:
            fp.write('<span class="normal">&lt;%s&gt;</span> %s<br />\n' % (nick, body))
        fp.close()

    def log_handler_join(self, groupchat, nick):
        self.log_write('%s has become available' % (nick), '', 'public', groupchat)

    def log_handler_part(self, groupchat, nick):
        self.log_write('%s has left' % (nick), '', 'public', groupchat)
