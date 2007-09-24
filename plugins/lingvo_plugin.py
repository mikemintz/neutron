#$ neutron_plugin 01

# Author: (c) Gh0st AKA Bohdan Turkynewych 2006-2007, tb0hdan[at]gmail.com
# Distributed under the GPLv2

from codecs import open as codecs_open
from re import match as re_match
from time import sleep as time_sleep, time as time_time
from thread import start_new as thread_start_new
from sys import exit as sys_exit

"""
dictionary format:

word
    single/plural
    1) meaning 1
    2) meaning 2

word2
    single/plural
    1) meaning 1
    2) meaning 2

"""
# Get more info here:
# http://traduko.lib.ru/
# http://traduko.lib.ru/efremova_lingvo.html
# http://traduko.lib.ru/dics/Efremova-txt.rar

d1ct = 'static/efremova.txt'
d1ct_coding = 'cp1251'

def load_dict(file, coding):
    global dict
    global loaded_ok
    linenum = 0
    loaded_ok = 0
    file_ok = 0
    dict = []
    start_time = time_time()
    try:
	f = codecs_open(file,'r', encoding=coding)
	data = f.read()
	f.close()
	file_ok = 1
    except IOError:
	print printc(color_red, 'Something wrong with dictionary file...')
	file_ok = 0
    if file_ok:
	for line in data.split('\n'):
	    linenum += 1
	    dict.append(line.strip())
	dictlen = len(dict)
	elapsed = time_time() - start_time
	if elapsed > 60:
	    print printc(color_red, 'Dictionary loading took more that one minute, server overloaded?')
	print printc(color_blue, 'Dictionary loaded: ' + str(dictlen) + ' lines in ' + str(elapsed)[:4] + ' seconds.')
	loaded_ok = 1

def handler_search_dict(type, source, parameters):
    global dict
    global loaded_ok
    
    reply = ''
    word = parameters.strip()
    if len(word) == 0:
	reply = 'Empty input'
	smsg(type, source, reply)
	return	
    if len(dict) == 0:
	reply = 'Zero sized dictionary \n'
	smsg(type, source, reply)
	return

    if not loaded_ok:
	reply = 'Sleeping whilst loading dictionary...\n'
	# Wait until we have dictionary loaded
	while loaded_ok == 0:
	    time_sleep(1)
	#
    #word = unicode(word, 'utf-8')
    start_idx = 0
    linecnt = 0

    for idx in xrange(0,len(dict)):
        if word == dict[idx]:
    	    start_idx = idx
	    break

    time_sleep(0.5)

    if start_idx == 0:
	for idx in xrange(0,len(dict)):
	    # if not found complete word, provide similar
	    if re_match('(^' + word + '*)',dict[idx]):
		start_idx = idx
    		break

    time_sleep(0.5)

    if start_idx == 0:
	  reply += 'Word not found.'
	  smsg(type, source, reply)
	  return

    reply += dict[idx] + '\n'

    for idx in xrange(start_idx + 1, len(dict)):
	    linecnt += 1
	    if dict[idx] != '':
		reply += '\t' + dict[idx]
	    else:
	    	break
	    # Limit response length to 20 lines
	    if linecnt >= 20:
		break

    smsg(type, source, reply)


if __name__ == '__main__':

    thread_start_new(load_dict,(d1ct, d1ct_coding))

register_command_handler(handler_search_dict, '!lingvo', 0, 'Searches for word meaning using http://traduko.lib.ru/efremova_lingvo.html text version.', '!lingvo <word>', ['!lingvo'])

# For console developing
#    while 1:
#	try:
#	    time_sleep(1)
#	    try:
#		word = raw_input()
#	    except EOFError:
#		sys_exit(0)
#	    thread_start_new(search_dict,(word,))
#	except KeyboardInterrupt:
#	    sys_exit(0)


