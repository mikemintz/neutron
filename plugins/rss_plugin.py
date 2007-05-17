#$ neutron_plugin 01

from xml.sax import make_parser, handler

RSS_CACHE_FILE = 'dynamic/RSS_CACHE.txt'
RSS_INTERVAL = 30
RSS_QUERY_DELAY = 10
RSS_ITEM_DELAY = 120

RSS_CACHE = {}
last_query = 0
UNSENT_HEADLINES = []
RSS_IS_ENABLED = 0

initialize_file(RSS_CACHE_FILE, "{'channels': {}}")

################################################################################

import re
def rss_remove_html(text):
	exp = re.compile('<[^>]*>')
	text = exp.sub('', text)
	notags = text.replace('&lt;', '<').replace('&gt;', '>')
	noescape = notags.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	noescape = noescape.replace('&lt;p&gt;', '')
	noescape = noescape.replace('&lt;/p&gt;', '')
	noescape = noescape.replace('&lt;p /&gt;', '').replace('&lt;p/&gt;', '')
	return noescape

""" OLD CODE: REMOVE LATER IF NEW FUNCTION (added 2005-10-12) WORKS
def rss_remove_html(text):
	notags = text.replace('&lt;', '<').replace('&gt;', '>')
	noescape = notags.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	noescape = noescape.replace('&lt;p&gt;', '')
	noescape = noescape.replace('&lt;/p&gt;', '')
	noescape = noescape.replace('&lt;p /&gt;', '').replace('&lt;p/&gt;', '')
	return noescape
"""

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
		print 'Querying Channels'
		last_query = time.time()
		for channel in RSS_CACHE['channels']:
			rss_query_channel(channel)
			time.sleep(RSS_QUERY_DELAY)
		print 'Finished Querying Headlines'

def rss_query_channel(channel):
	print 'Querying: "' + channel + '"'
	parser = make_parser()
	parser.setContentHandler(RSSHandler(channel))
	try:
		parser.parse(RSS_CACHE['channels'][channel]['url'])
	except:
		#raise
		print 'error parsing: ' + channel

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
	for groupchat in RSS_CACHE['channels'][channel]['subscribers']:
		if GROUPCHATS.has_key(groupchat):
			print channel + ': Sending Headline To: ' + groupchat
			msg(groupchat, reply)

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
	smsg(type, source, 'Enabled RSS')

def handler_rss_stop(type, source, parameters):
	rss_end_loop()
	smsg(type, source, 'Disabled RSS')

def handler_rss_add(type, source, parameters):
	if len(string.split(parameters)) > 1:
		(name, url) = string.split(parameters)
		rss_add_channel(name, url)	
		smsg(type, source, 'Added: ' + name + ' - ' + url)
	else:
		smsg(type, source, 'Invalid Syntax')

def handler_rss_remove(type, source, parameters):
	if len(string.split(parameters)) > 0:
		name = parameters
		rss_remove_channel(name)	
		smsg(type, source, 'Removed: ' + name)
	else:
		smsg(type, source, 'Invalid Syntax')

def handler_rss_subscribe(type, source, parameters):
	if len(string.split(parameters)) > 1:
		(name, jid) = string.split(parameters)
		rss_subscribe(name, jid)	
		smsg(type, source, 'Subscribed: ' + jid + ' to ' + name)
	else:
		smsg(type, source, 'Invalid Syntax')

def handler_rss_unsubscribe(type, source, parameters):
	if len(string.split(parameters)) > 1:
		(name, jid) = string.split(parameters)
		rss_unsubscribe(name, jid)	
		smsg(type, source, 'Unsubscribed: ' + jid + ' from ' + name)
	else:
		smsg(type, source, 'Invalid Syntax')

def handler_rss_info(type, source, parameters):
	if parameters.strip():
		name = parameters.strip()
		message = name + ' - ' + RSS_CACHE['channels'][name]['url'] + ' - ' + RSS_CACHE['channels'][name]['title'] + ' - ' + RSS_CACHE['channels'][name]['link'] + ' - ' + RSS_CACHE['channels'][name]['description']
		message += ' - Subscribers:'
		for subscriber in RSS_CACHE['channels'][name]['subscribers']:
			message += ' ' + subscriber
		if not len(RSS_CACHE['channels'][name]['subscribers']):
			message += 'NONE'
		smsg(type, source, message)
	else:
		message = 'Channels:'
		for channel in RSS_CACHE['channels'].keys():
			message += ' ' + channel
		smsg(type, source, message)

register_command_handler(handler_rss_start, '!rss_start', 100, 'Enables the RSS headline feature.', '!rss_start', ['!rss_start'])
register_command_handler(handler_rss_stop, '!rss_stop', 100, 'Disables the RSS headline feature.', '!rss_stop', ['!rss_stop'])
register_command_handler(handler_rss_add, '!rss_add', 100, 'Adds an RSS channel.', '!rss_add <name> <url>', ['!rss_add slashdot http://www.slashdot.org/slashdot.rdf'])
register_command_handler(handler_rss_remove, '!rss_remove', 100, 'Removes an RSS channel.', '!rss_add <name>', ['!rss_remove slashdot'])
register_command_handler(handler_rss_subscribe, '!rss_subscribe', 100, 'Subscribes a channel to an RSS channel.', '!rss_subscribe <name> <jid>', ['!rss_subscribe slashdot jabber@conference.jabber.org'])
register_command_handler(handler_rss_unsubscribe, '!rss_unsubscribe', 100, 'Unsubscribes a channel from an RSS channel.', '!rss_unsubscribe <name> <jid>', ['!rss_unsubscribe slashdot jabber@conference.jabber.org'])
register_command_handler(handler_rss_info, '!rss_info', 0, 'Requests information on specified RSS channel or gets the list of channels.', '!rss_info [name]', ['!rss_info slashdot', '!rss_info'])

