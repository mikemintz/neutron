# -*- coding: koi8-u -*-

#  Neutron plugin
#  google_plugin.py

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

import google
import SOAP

class Googlep:
    def __init__(self):
        self.neutron_version = ('0.5.42')
        self.version = '0.1'
        self.name = 'Googlep'
        self.description = 'Google API support'
        self.homepageurl = 'http://ejabberd.jabber.ru/neutron'
        self.updateurl = None
        self.command_handlers = [
            [self.handler_google_google, '!google', 0, 'Looks up search terms on google.', '!google <query>', ['!google "mike mintz"']],
	    [self.handler_google_spell, '!spell', 0, 'Returns a spelling suggestion from google.', '!spell <query>', ['!spell "pithon nutron"']],
	    [self.handler_google_jepsearch, '!jepsearch', 0, 'Searches google for a JEP.', '!jep <query>', ['!google "jep-0001"']]]
	    
    def google_remove_html(self, text):
	nobold = text.replace('<b>', '').replace('</b>', '')
	nobreaks = nobold.replace('<br>', ' ')
	noescape = nobreaks.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	return noescape

    def google_search(self, query):
	try:
    	    data = google.doGoogleSearch(query)
	except SOAP.HTTPError:
	    return '\r\nGoogle API Error.'
	except SOAP.faultType:
	    return '\r\nInvalid Google Key. Maybe still default??\r\nTake a look on modules/googlekey.txt'    
	try:
		first = data.results[0]
		url = first.URL
		title = self.google_remove_html(first.title)
		if first.summary:
			summary = self.google_remove_html(first.summary)
		else:
			summary = self.google_remove_html(first.snippet)
		searchtime = str(round(data.meta.searchTime, 3))
		total = str(data.meta.estimatedTotalResultsCount)
		return url + ' - ' + title + ' - ' + summary + ' (' + searchtime + 'sec) (' + total + ' sites)'
	except:
		return 'No Results'

    def handler_google_google(self, type, source, parameters):
	results = self.google_search(parameters)
	self.conn.smsg(type, source, results)

    def handler_google_spell(self, type, source, parameters):
	correction = google.doSpellingSuggestion(parameters)
	if not correction:
		correction = 'No Suggestion'
	self.conn.smsg(type, source, correction)

    def handler_google_jepsearch(self, type, source, parameters):
	results = self.google_search(parameters + ' site:www.jabber.org "/jeps/jep-" -jeplist.html')
	self.conn.smsg(type, source, results)

