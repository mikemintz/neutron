# -*- coding: koi8-u -*-

#  Neutron plugin
#  functions.py

#  Copyright (C) 2002-2006 Mike Mintz <mikemintz@gmail.com>
#  Copyright (C) 2007 Mike Mintz <mikemintz@gmail.com>
#                     AnaКl Verrier <elghinn@free.fr>
#  Parts of code:
#  Author: Bohdan Turkynewych, AKA Gh0st, tb0hdan[at]gmail.com
    
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

import time

class Functions:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = '0.1'
        self.name = 'Functions'
        self.description = 'Misc functions, like time, date, temperature, etc'
        self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
        self.updateurl = None
        self.command_handlers = [
	    [self.handler_time_date, '!date', 0, 'Gives the current time and date.', '!date', ['!date']],
	    [self.handler_time_swatch, '!swatch', 0, 'Gives the current Swatch Internet time.', '!swatch', ['!swatch']],
	    [self.handler_temperature_temperature, '!temperature', 0, 'Converts temperatures from Celcius to Fahrenheit and vice versa.', '!temperature <#> <C/F>', ['!temperature 10 F', '!temperature 29 C']]]

    def handler_temperature_temperature(self, type, source, parameters):
	if parameters:
		splitdata = string.split(parameters)
		try:
			input_value = float(splitdata[0])
			if len(splitdata) > 1:
				unit_system = splitdata[1][0]
			else:
				unit_system = 'f'
		except ValueError:
			try:
				input_value = float(splitdata[0][:-1])
			except ValueError:
				smsg(type, source, 'Syntax Error')
				return
			unit_system = splitdata[0][-1]
		unit_system = string.lower(unit_system)
		if unit_system == 'c':
			reply = str(round(input_value * 9 / 5 + 32, 1)) + ' F'
		else:
			reply = str(round((input_value - 32) * 5 / 9, 1)) + ' C'
	else:
		reply = 'C=(F-32)*5/9 F=C*9/5+32'
	self.conn.smsg(type, source, reply)



    def handler_time_date(self, type, source, parameters):
	reply = time.strftime('%a %d %b %H:%M:%S UTC %Y', time.gmtime())
	self.conn.smsg(type, source, reply)

    def handler_time_swatch(self, type, source, parameters):
	seconds_per_beat = 86.4
	(hour, minute, second) = time.gmtime()[3:6]
	gmt_seconds = (3600 * hour) + (60 * minute) + second
	seconds = gmt_seconds + 3600
	beats = float(seconds) / float(seconds_per_beat)
	if beats < 10:
		prefix = '00'
	elif beats < 100:
		prefix = '0'
	else:
		prefix = ''
	reply = '@' + prefix + str(round(beats, 2))	
	self.conn.smsg(type, source, reply)

