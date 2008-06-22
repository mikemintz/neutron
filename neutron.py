#! /usr/bin/env python

import sys
import os
os.chdir(os.path.dirname(sys.argv[0]))

sys.path.insert(1, 'modules')

import xmpp
import string
import time
import thread
import random
import types
import traceback
import getopt
#
import ircbot
import irclib
#
import urllib
import urllib2
#
import aiml
#
import iq

################################################################################
iq.version = "0.5.x"
iq.vername = "Neutron"
#
CONFIGURATION_FILE = 'dynamic/config.cfg'

GENERAL_CONFIG_FILE = 'config.txt'

fp = open(GENERAL_CONFIG_FILE, 'r')
GENERAL_CONFIG = eval(fp.read())
fp.close()

SERVER = GENERAL_CONFIG['SERVER']
PORT = GENERAL_CONFIG['PORT']
USERNAME = GENERAL_CONFIG['USERNAME']
PASSWORD = GENERAL_CONFIG['PASSWORD']
RESOURCE = GENERAL_CONFIG['RESOURCE']

NICKS_CACHE_FILE = 'dynamic/chatnicks.cfg'
GROUPCHAT_CACHE_FILE = 'dynamic/chatrooms.cfg'
ACCESS_FILE = 'dynamic/access.cfg'
PLUGIN_DIR = 'plugins'

DEFAULT_NICK = GENERAL_CONFIG['DEFAULT_NICK']
ADMINS = GENERAL_CONFIG['ADMINS']
ADMIN_PASSWORD = GENERAL_CONFIG['ADMIN_PASSWORD']

AUTO_RESTART = GENERAL_CONFIG['AUTO_RESTART']

PUBLIC_LOG_DIR = GENERAL_CONFIG['PUBLIC_LOG_DIR']
PRIVATE_LOG_DIR = GENERAL_CONFIG['PRIVATE_LOG_DIR']

INITSCRIPT_FILE = GENERAL_CONFIG['INITSCRIPT_FILE']

#  Gh0st addition
HTTP_PROXY = GENERAL_CONFIG['HTTP_PROXY']

if HTTP_PROXY != "":
    proxy_support = urllib2.ProxyHandler({"http" : HTTP_PROXY})
    # urllib
    proxies = {'http': HTTP_PROXY}
    # environment variable for urllib
    http_proxy = HTTP_PROXY
    # urllib2
    opener = urllib2.build_opener(proxy_support, '', urllib2.CacheFTPHandler)
    urllib2.install_opener(opener)
else:
    proxies = {}
# end of addition
BOOTUP_TIMESTAMP = time.time()

################################################################################

COMMANDS = {}

GROUPCHATS = {}

MESSAGE_HANDLERS = []
OUTGOING_MESSAGE_HANDLERS = []
JOIN_HANDLERS = []
LEAVE_HANDLERS = []
IQ_HANDLERS = []
PRESENCE_HANDLERS = []
GROUPCHAT_INVITE_HANDLERS = []

COMMAND_HANDLERS = {}

ACCESS = {}

JCON = None

CONFIGURATION = {}

################################################################################

optlist, args = getopt.getopt(sys.argv[1:], '', ['pid='])
for opt_tuple in optlist:
	if opt_tuple[0] == '--pid':
		pid_filename = opt_tuple[1]
		fp = open(pid_filename, 'w')
		fp.write(str(os.getpid()))
		fp.close()

################################################################################

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

################################################################################

initialize_file(CONFIGURATION_FILE, '{}')
try:
	CONFIGURATION = eval(read_file(CONFIGURATION_FILE))
except:
	print 'Error Parsing Configuration File'

def config_get(category, key):
	if CONFIGURATION.has_key(category):
		if CONFIGURATION[category].has_key(key):
			return CONFIGURATION[category][key]
		else:
			return None
	else:
		return None

def config_set(category, key, value):
	if not CONFIGURATION.has_key(category):
		CONFIGURATION[category] = {}
	CONFIGURATION[category][key] = value
	config_string = '{\n'
	for category in CONFIGURATION.keys():
		config_string += repr(category) + ':\n'
		for key in CONFIGURATION[category].keys():
			config_string += '\t' + repr(key) + ': ' + repr(CONFIGURATION[category][key]) + '\n'
		config_string += '\n'
	config_string += '}'
	write_file(CONFIGURATION_FILE, config_string)

################################################################################

def register_message_handler(instance):
	MESSAGE_HANDLERS.append(instance)
def register_outgoing_message_handler(instance):
	OUTGOING_MESSAGE_HANDLERS.append(instance)
def register_join_handler(instance):
	JOIN_HANDLERS.append(instance)
def register_leave_handler(instance):
	LEAVE_HANDLERS.append(instance)
def register_iq_handler(instance):
	IQ_HANDLERS.append(instance)
def register_presence_handler(instance):
	PRESENCE_HANDLERS.append(instance)
def register_groupchat_invite_handler(instance):
	GROUPCHAT_INVITE_HANDLERS.append(instance)

def register_command_handler(instance, command, access=0, description='', syntax='', examples=[]):
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'access': access, 'description': description, 'syntax': syntax, 'examples': examples}

def call_message_handlers(type, source, body):
	for handler in MESSAGE_HANDLERS:
		thread.start_new(handler, (type, source, body))
def call_outgoing_message_handlers(target, body):
	for handler in OUTGOING_MESSAGE_HANDLERS:
		thread.start_new(handler, (target, body))
def call_join_handlers(groupchat, nick):
	for handler in JOIN_HANDLERS:
		thread.start_new(handler, (groupchat, nick))
def call_leave_handlers(groupchat, nick):
	for handler in LEAVE_HANDLERS:
		thread.start_new(handler, (groupchat, nick))
def call_iq_handlers(iq):
	for handler in IQ_HANDLERS:
		thread.start_new(handler, (iq,))
def call_presence_handlers(prs):
	for handler in PRESENCE_HANDLERS:
		thread.start_new(handler, (prs,))
def call_groupchat_invite_handlers(source, groupchat, body):
	for handler in GROUPCHAT_INVITE_HANDLERS:
		thread.start_new(handler, (source, groupchat, body))

def call_command_handlers(command, type, source, parameters):
	if COMMAND_HANDLERS.has_key(command):
		if has_access(source, COMMANDS[command]['access']):
			thread.start_new(COMMAND_HANDLERS[command], (type, source, parameters))
		else:
			smsg(type, source, 'Unauthorized')

################################################################################

def find_plugins():
	valid_plugins = []
	possibilities = os.listdir('plugins')
	for possibility in possibilities:
		if possibility[-3:].lower() == '.py':
			try:
				fp = file(PLUGIN_DIR + '/' + possibility)
				data = fp.read(20)
				if data == '#$ neutron_plugin 01':
					valid_plugins.append(possibility)
			except:
				pass
	return valid_plugins

def load_plugins():
	valid_plugins = find_plugins()
	for valid_plugin in valid_plugins:
		try:
			print 'Plugin: ' + valid_plugin
			#execfile(PLUGIN_DIR + '/' + valid_plugin)
			fp = file(PLUGIN_DIR + '/' + valid_plugin)
			exec fp in globals()
			fp.close()
		except:
			raise

def load_initscript():
	print 'Executing Init Script'
	fp = file(INITSCRIPT_FILE)
	exec fp in globals()
	fp.close()


################################################################################

def get_true_jid(jid):
	true_jid = ''
	if type(jid) is types.ListType:
		jid = jid[0]
	if type(jid) is types.InstanceType:
		jid = unicode(jid) # str(jid)
	stripped_jid = string.split(jid, '/', 1)[0]
	resource = ''
	if len(string.split(jid, '/', 1)) == 2:
		resource = string.split(jid, '/', 1)[1]
	if GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			true_jid = string.split(unicode(GROUPCHATS[stripped_jid][resource]['jid']), '/', 1)[0]
		else:
			true_jid = stripped_jid
	else:
		true_jid = stripped_jid
	return true_jid
	
def get_groupchat(jid):
	if type(jid) is types.ListType:
		jid = jid[1]
	jid = string.split(unicode(jid), '/')[0] # str(jid)
	if GROUPCHATS.has_key(jid):
		return jid
	else:
		return None

def get_nick(groupchat):
	try:
		nicks_string = read_file(NICKS_CACHE_FILE)
	except:
		fp = file(NICKS_CACHE_FILE, 'w')
		fp.write('{}')
		fp.close()
		nicks_string = '{}'
		print 'Initializing ' + NICKS_CACHE_FILE
	nicks = eval(nicks_string)
	if nicks.has_key(groupchat):
		return nicks[groupchat]
	else:
		return DEFAULT_NICK

def set_nick(groupchat, nick=None):
	nicks = eval(read_file(NICKS_CACHE_FILE))
	if nick:
		nicks[groupchat] = nick
	elif groupchat:
		del nicks[groupchat]
	fp = file(NICKS_CACHE_FILE, 'w')
	fp.write(str(nicks))
	fp.close()	

################################################################################

def get_access_levels():
	global ACCESS
	initialize_file(ACCESS_FILE, '{}')
	ACCESS = eval(read_file(ACCESS_FILE))
	for jid in ADMINS:
		change_access_perm(jid, 100)
	for jid in ACCESS.keys():
		if ACCESS[jid] == 0:
			del ACCESS[jid]
	write_file(ACCESS_FILE , str(ACCESS))

def change_access_temp(source, level=0):
	global ACCESS
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		level = 0
	ACCESS[jid] = level

def change_access_perm(source, level=0):
	global ACCESS
	jid = get_true_jid(source)
	try:
		level = int(level)
	except:
		level = 0
	temp_access = eval(read_file(ACCESS_FILE))
	temp_access[jid] = level
	write_file(ACCESS_FILE, str(temp_access))
	ACCESS[jid] = level

def user_level(source):
	global ACCESS
	jid = get_true_jid(source)
	if ACCESS.has_key(jid):
		return ACCESS[jid]
	else:
		return 0

def has_access(source, required_level):
	jid = get_true_jid(source)
	if user_level(jid) >= required_level:
		return 1
	return 0

################################################################################

def join_groupchat(groupchat, nick=None):
	if nick:
		set_nick(groupchat, nick)
	else:
		nick = get_nick(groupchat)
	JCON.send(xmpp.Presence(groupchat + '/' + nick))
	if not GROUPCHATS.has_key(groupchat):
		GROUPCHATS[groupchat] = {}
		write_file(GROUPCHAT_CACHE_FILE, str(GROUPCHATS.keys()))

def leave_groupchat(groupchat):
	JCON.send(xmpp.Presence(groupchat, 'unavailable'))
	if GROUPCHATS.has_key(groupchat):
		del GROUPCHATS[groupchat]
		write_file(GROUPCHAT_CACHE_FILE, str(GROUPCHATS.keys()))

def msg(target, body):
	msg = xmpp.Message(target, body)
	if GROUPCHATS.has_key(target):
		msg.setType('groupchat')
	else:
		msg.setType('chat')
	JCON.send(msg)
	call_outgoing_message_handlers(target, body)

def smsg(type, source, body):
	if type == 'public':
		msg(source[1], source[2] + ': ' + body)
	elif type == 'private':
		msg(source[0], body)

def isadmin(jid):
	admin_list = ADMINS
	if type(jid) is types.ListType:
		jid = jid[0]
	jid = str(jid)
	stripped_jid = string.split(jid, '/', 1)[0]
	resource = ''
	if len(string.split(jid, '/', 1)) == 2:
		resource = string.split(jid, '/', 1)[1]
	if stripped_jid in admin_list:
		return 1
	elif GROUPCHATS.has_key(stripped_jid):
		if GROUPCHATS[stripped_jid].has_key(resource):
			if string.split(GROUPCHATS[stripped_jid][resource]['jid'], '/', 1)[0] in admin_list:
				return 1
	return 0

################################################################################

def messageCB(con, msg):
	msgtype = msg.getType()
	body = msg.getBody()
	if body != None:
		body = body.strip()
	fromjid = msg.getFrom()
	command = ''
	parameters = ''
	if body and string.split(body):
		command = string.lower(string.split(body)[0])
		if body.count(' '):
			parameters = body[(body.find(' ') + 1):]
	if not msg.timestamp:
		if msgtype == 'groupchat':
				call_message_handlers('public', [fromjid, fromjid.getStripped(), fromjid.getResource()], body)
				if command in COMMANDS:
					call_command_handlers(command, 'public', [fromjid, fromjid.getStripped(), fromjid.getResource()], parameters)
		else:
			call_message_handlers('private', [fromjid, fromjid.getStripped(), fromjid.getResource()], body)
			if command in COMMANDS:
				call_command_handlers(command, 'private', [fromjid, fromjid.getStripped(), fromjid.getResource()], parameters)
	for x_node in msg.getTags('x', {}, 'jabber:x:conference'):
		inviter_jid = None
		muc_inviter_tag = msg.getTag('x', {}, 'http://jabber.org/protocol/muc#user')
		if muc_inviter_tag:
			if muc_inviter_tag.getTag('invite'):
				if muc_inviter_tag.getTag('invite').getAttr('from'):
					inviter_jid = xmpp.JID(muc_inviter_tag.getTag('invite').getAttr('from'))
		if not inviter_jid:
			inviter_jid = fromjid
		call_groupchat_invite_handlers([inviter_jid, inviter_jid.getStripped(), inviter_jid.getResource()], x_node.getAttr('jid'), body)

def presenceCB(con, prs):
	call_presence_handlers(prs)
	type = prs.getType()
	groupchat = prs.getFrom().getStripped()
	nick = prs.getFrom().getResource()
	
	if groupchat in GROUPCHATS:
		if type == 'available' or type == None:
			if not GROUPCHATS[groupchat].has_key(nick):
				GROUPCHATS[groupchat][nick] = {'jid': prs.getFrom(), 'idle': time.time()}
				call_join_handlers(groupchat, nick)
				time.sleep(0.5)
		elif type == 'unavailable':
			if GROUPCHATS[groupchat].has_key(nick):
				call_leave_handlers(groupchat, nick)
				del GROUPCHATS[groupchat][nick]
		elif type == 'error':
			try:
				code = prs.asNode().getTag('error').getAttr('code')
			except:
				code = None
			if code == '409': # name conflict
				join_groupchat(groupchat, nick + '_')
				time.sleep(0.5)



def iqCB(con, iq):
	    call_iq_handlers(iq)

def dcCB():
	print 'DISCONNECTED'
	if AUTO_RESTART:
		print 'WAITING FOR RESTART...'
		time.sleep(240) # sleep for 240 seconds
		print 'RESTARTING'
		os.execl(sys.executable, sys.executable, sys.argv[0])
	else:
		sys.exit(0)

def load_aiml():
    global k
    # The Kernel object is the public interface to
    # the AIML interpreter.
    k = aiml.Kernel()

    # Use the 'learn' method to load the contents
    # of an AIML file into the Kernel.
    k.learn("std-startup.xml")

    # Use the 'respond' method to compute the response
    # to a user's input string.  respond() returns
    # the interpreter's response, which in this case
    # we ignore.
    k.respond("load aiml b")

################################################################################

def start():
	global JCON
	JCON = xmpp.Client(server=SERVER, port=PORT, debug=[])

	get_access_levels()
	load_plugins()
	# Uncomment if you want PyAIML support.
	# load_aiml()
	load_initscript()

	if JCON.connect():
		print "Connected"
	else:
		print "Couldn't connect"
		sys.exit(1)

	if JCON.auth(USERNAME, PASSWORD, RESOURCE):
		print 'Logged In'
	else:
		print "eek -> ", JCON.lastErr, JCON.lastErrCode
		time.sleep(10) # sleep for 10 seconds
		sys.exit(1)

	JCON.RegisterHandler('message', messageCB)
	JCON.RegisterHandler('presence', presenceCB)
	JCON.RegisterHandler('iq', iqCB)
	## Parts of code from:
	## OJAB iq module
	## Copyright (C) Boris Kotov <admin@avoozl.ru>
	JCON.RegisterHandler('iq', iq.versionCB, 'get', xmpp.NS_VERSION)
	JCON.RegisterHandler('iq', iq.versionresultCB, 'result', xmpp.NS_VERSION)
	JCON.RegisterHandler('iq', iq.versionerrorCB, 'error', xmpp.NS_VERSION)
	JCON.RegisterHandler('iq', iq.timeCB, 'get', xmpp.NS_TIME)
	JCON.RegisterHandler('iq', iq.timeresultCB, 'result', xmpp.NS_TIME)
	JCON.RegisterHandler('iq', iq.timeerrorCB, 'error', xmpp.NS_TIME)
	#####################
	JCON.RegisterDisconnectHandler(dcCB)
	JCON.UnregisterDisconnectHandler(JCON.DisconnectHandler)

	JCON.getRoster()
	JCON.sendInitPresence()
	print 'Presence Sent'

	initialize_file(GROUPCHAT_CACHE_FILE, '[]')
	groupchats = eval(read_file(GROUPCHAT_CACHE_FILE))
	for groupchat in groupchats:
		join_groupchat(groupchat)
		time.sleep(0.5)

	while 1:
		JCON.Process(10)

if __name__ == "__main__":
	try:
		start()
	except KeyboardInterrupt:
		print '\nINTERUPT'
		sys.exit(1)
	except:
		if AUTO_RESTART:
			if sys.exc_info()[0] is not SystemExit:
				traceback.print_exc()
			try:
				JCON.disconnected()
			except IOError:
				# IOError is raised by default DisconnectHandler
				pass
			try:
				time.sleep(3)
			except KeyboardInterrupt:
				print '\nINTERUPT'
				sys.exit(1)
			print 'RESTARTING'
			os.execl(sys.executable, sys.executable, sys.argv[0])
		else:
			raise

#EOF
