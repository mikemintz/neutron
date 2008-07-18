#!/usr/bin/env python
# -*- coding: utf8 -*-


from xml.sax import make_parser, handler
import thread
import re
import os
import random
import time

RSS_CACHE_FILE = 'RSS_CACHE.txt'
RSS_INTERVAL = 30
RSS_QUERY_DELAY = 10
RSS_ITEM_DELAY = 120

RSS_CACHE = {}
last_query = 0
UNSENT_HEADLINES = []
RSS_IS_ENABLED = 0
# Parts of code from modules/xmpp/debug.py
# Wanna some colors :)
color_none         = chr(27) + "[0m"
color_black        = chr(27) + "[30m"
color_red          = chr(27) + "[31m"
color_green        = chr(27) + "[32m"
color_brown        = chr(27) + "[33m"
color_blue         = chr(27) + "[34m"
color_magenta      = chr(27) + "[35m"
color_cyan         = chr(27) + "[36m"
color_light_gray   = chr(27) + "[37m"
color_dark_gray    = chr(27) + "[30;1m"
color_bright_red   = chr(27) + "[31;1m"
color_bright_green = chr(27) + "[32;1m"
color_yellow       = chr(27) + "[33;1m"
color_bright_blue  = chr(27) + "[34;1m"
color_purple       = chr(27) + "[35;1m"
color_bright_cyan  = chr(27) + "[36;1m"
color_white        = chr(27) + "[37;1m"


def initialize_file(filename, data=''):
	if not os.access(filename, os.F_OK):
		fp = file(filename, 'w')
		if data:
			fp.write(data)
		fp.close()

def read_file(filename):
	fp = file(filename)
	data = fp.read()
	fp.close()
	return data

def write_file(filename, data):
	fp = file(filename, 'w')
	fp.write(data)
	fp.close()

initialize_file(RSS_CACHE_FILE, "{'channels': {}}")

################################################################################
if os.environ.has_key('TERM'):
    colors_enabled=True
else:
    colors_enabled=False

def printc(prefix, msg):
    msg=msg.replace('\r','\\r').replace('\n','\\n').replace('><','>\n  <')
    if colors_enabled: 
        msg=prefix+msg+color_none
    else:
        msg=color_none+msg
    return msg



def rss_remove_html(text):
	exp = re.compile('<[^>]*>')
	text = exp.sub('', text)
	notags = text.replace('&lt;', '<').replace('&gt;', '>')
	noescape = notags.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	noescape = noescape.replace('&lt;p&gt;', '')
	noescape = noescape.replace('&lt;/p&gt;', '')
	noescape = noescape.replace('&lt;p /&gt;', '').replace('&lt;p/&gt;', '')
	return noescape

def rss_update_file():
	global RSS_CACHE
	write_file(RSS_CACHE_FILE, str(RSS_CACHE))

def rss_read_file():
	global RSS_CACHE
	RSS_CACHE = eval(read_file(RSS_CACHE_FILE))

def rss_add_channel(name, url):
	global RSS_CACHE
	if not RSS_CACHE['channels'].has_key(name):
		RSS_CACHE['channels'][name] = {'url': url, 'lastitem': '', 'subscribers': [], 'title': name, 'link': '', 'description': name}
		rss_update_file()
	else:
		RSS_CACHE['channels'][name]['url'] = url

def rss_remove_channel(name):
	global RSS_CACHE
	if RSS_CACHE['channels'].has_key(name):
		del RSS_CACHE['channels'][name]
		rss_update_file()

def rss_subscribe(name, jid):
	global RSS_CACHE
	if RSS_CACHE['channels'].has_key(name):
		if not jid in RSS_CACHE['channels'][name]['subscribers']:
			RSS_CACHE['channels'][name]['subscribers'].append(jid)
			rss_update_file()

def rss_unsubscribe(name, jid):
	global RSS_CACHE
	if RSS_CACHE['channels'].has_key(name):
		if jid in RSS_CACHE['channels'][name]['subscribers']:
			RSS_CACHE['channels'][name]['subscribers'].remove(jid)
			rss_update_file()

def rss_query_channels_loop():
	RSS_IS_ENABLED = 1
	while RSS_IS_ENABLED:
		rss_query_channels()
		time.sleep(RSS_ITEM_DELAY)
		if len(UNSENT_HEADLINES):
			random.shuffle(UNSENT_HEADLINES)
			(channel, item) = UNSENT_HEADLINES.pop()
			rss_dispatch_headline(channel, item)

def rss_end_loop():
	RSS_IS_ENABLED = 0

def rss_query_channels():
	global RSS_CACHE
	global last_query
	if time.time() > last_query + (RSS_INTERVAL * 60):
		print printc(color_blue,'Querying Channels')
		last_query = time.time()
		for channel in RSS_CACHE['channels']:
			rss_query_channel(channel)
			time.sleep(RSS_QUERY_DELAY)
		print printc(color_blue,'Finished Querying Headlines')

def rss_query_channel(channel):
	print printc(color_blue,'Querying: ') + '"' + channel + '"'
	parser = make_parser()
	parser.setContentHandler(RSSHandler(channel))
	try:
		parser.parse(RSS_CACHE['channels'][channel]['url'])
	except:
		print printc(color_bright_red,'error parsing: ') + channel

def rss_dispatch_headlines(channel, info, items):
	global RSS_CACHE
	RSS_CACHE['channels'][channel]['title'] = info['title']
	RSS_CACHE['channels'][channel]['link'] = info['link']
	RSS_CACHE['channels'][channel]['description'] = info['description']
	for item in items:
		if item == RSS_CACHE['channels'][channel]['lastitem']:	
			break
		else:
			UNSENT_HEADLINES.append((channel, item))
			print channel + ': Adding item to list.' 
	RSS_CACHE['channels'][channel]['lastitem'] = items[0]
	rss_update_file()

def rss_dispatch_headline(channel, item):
	global RSS_CACHE
	globaltitle = RSS_CACHE['channels'][channel]['title']
	title = rss_remove_html(item['title'])
	link = item['link']
	description = rss_remove_html(item['description'])
	reply = title + ' - '
	if description:
		reply += description + ' - '
	reply += link
	GROUPCHATS = bot.muc.load_groupchats()
	for groupchat in RSS_CACHE['channels'][channel]['subscribers']:
		if groupchat in GROUPCHATS:
			print printc(color_yellow,channel) + ': Sending Headline To: ' + printc(color_light_gray,groupchat)
			bot.muc.msg('groupchat', groupchat, reply)

################################################################################

class RSSHandler(handler.ContentHandler):
	def __init__(self, channel):
		handler.ContentHandler.__init__(self)

		self.channel = channel
		self.info = {'title': '', 'link': '', 'description': ''}
		self.items = []

		self._text = ''
		self._parent = None
		self._title = ''
		self._link = ''
		self._description = ''

	def startElement(self, name, attrs):
		if name == 'channel' or name == 'item':
			self._parent = name
		self._text = ''

	def endElement(self, name):
		if self._parent == 'channel':
			if name == 'title':
				self.info['title'] = self._text
			elif name == 'description':
				self.info['description'] = self._text
			elif name == 'link':
				self.info['link'] = self._text

		elif self._parent == 'item':
			if name == 'title':
				self._title = self._text
			elif name == 'link':
				self._link = self._text
			elif name == 'description':
				self._description = self._text
			elif name == 'item':
				self.items.append({'title': self._title, 'link': self._link, 'description': self._description})
				self._title = ''
				self._link = ''
				self._description = ''

		if name == 'rss' or name == 'rdf:RDF':
			rss_dispatch_headlines(self.channel, self.info, self.items)
				
	def characters(self, content):
		self._text = self._text + content

################################################################################

rss_read_file()

################################################################################

def handler_rss_start(type, source, parameters):
	thread.start_new(rss_query_channels_loop, ())
	source.msg(type, 'Enabled RSS')

def handler_rss_stop(type, source, parameters):
	rss_end_loop()
	source.msg(type, 'Disabled RSS')

def handler_rss_add(type, source, parameters):
	if len(string.split(parameters)) > 1:
		(name, url) = string.split(parameters)
		rss_add_channel(name, url)	
		source.msg(type, 'Added: ' + name + ' - ' + url)
	else:
		source.msg(type, 'Invalid Syntax')

def handler_rss_remove(type, source, parameters):
	if len(string.split(parameters)) > 0:
		name = parameters
		rss_remove_channel(name)	
		source.msg(type, 'Removed: ' + name)
	else:
		source.msg(type, 'Invalid Syntax')

def handler_rss_subscribe(type, source, parameters):
	if len(string.split(parameters)) > 1:
		(name, jid) = string.split(parameters)
		rss_subscribe(name, jid)	
		source.msg(type, 'Subscribed: ' + jid + ' to ' + name)
	else:
		source.msg(type, 'Invalid Syntax')

def handler_rss_unsubscribe(type, source, parameters):
	if len(string.split(parameters)) > 1:
		(name, jid) = string.split(parameters)
		rss_unsubscribe(name, jid)	
		source.msg(type, 'Unsubscribed: ' + jid + ' from ' + name)
	else:
		source.msg(type, 'Invalid Syntax')

def handler_rss_info(type, source, parameters):
	if parameters.strip():
		name = parameters.strip()
		message = name + ' - ' + RSS_CACHE['channels'][name]['url'] + ' - ' + RSS_CACHE['channels'][name]['title'] + ' - ' + RSS_CACHE['channels'][name]['link'] + ' - ' + RSS_CACHE['channels'][name]['description']
		message += ' - Subscribers:'
		for subscriber in RSS_CACHE['channels'][name]['subscribers']:
			message += ' ' + subscriber
		if not len(RSS_CACHE['channels'][name]['subscribers']):
			message += 'NONE'
		source.msg(type, message)
	else:
		message = 'Channels:'
		for channel in RSS_CACHE['channels'].keys():
			message += ' ' + channel
		source.msg(type, message)

bot.register_cmd_handler(handler_rss_start, '.rss_start', 100)
bot.register_cmd_handler(handler_rss_stop, '.rss_stop', 100)
bot.register_cmd_handler(handler_rss_add, '.rss_add', 100)
bot.register_cmd_handler(handler_rss_remove, '.rss_remove', 100)
bot.register_cmd_handler(handler_rss_subscribe, '.rss_subscribe', 100)
bot.register_cmd_handler(handler_rss_unsubscribe, '.rss_unsubscribe', 100)
bot.register_cmd_handler(handler_rss_info, '.rss_info', 9)

