#$ neutron_plugin 01

# Author: Bohdan Turkynewych, AKA Gh0st, tb0hdan[at]gmail.com
# requires: mpd from http://www.musicpd.org/
#

import socket
import re
import string
from string import *

# Please, adjust these values!
mpc_server='localhost'
mpc_port=6600

def sec2minsec(in_seconds):
    seconds = str(in_seconds % 60)
    if len(seconds) == 1:
	    seconds = '0' + seconds
    minutes = str(in_seconds / 60)
    if len(minutes) == 1:
	    minutes = '0' + minutes
    return_value = minutes + ':' + seconds
    return return_value
		
def mpc_command(command):
    err = 0
    global mpc_server
    global mpc_port
    suffix='\r\nclose\r\n'
    reply=''
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
	conn.connect((socket.gethostbyname(mpc_server),mpc_port))
	conn.send(command+suffix)
	s = conn.recv(1024)
	conn.close()
    except socket.error:
	err = 1
	pass
    if err == 0:	
	if re.search('OK',s):
	    for line in s.split('\n'):
		if line.strip():
		    if not re.search('OK',line):
			reply += line + '\r\n'
	    if reply.strip() == '':
		reply = 'OK'
    else:
		reply = 'Connection Error.'		
    return reply		    

def current_song(dummy):
	artist=''
	album=''
	title=''
	date=''
	return_value=''
	s=mpc_command('currentsong')
	for line in s.split('\r\n'):
		if line.find('Date:') == 0:
            	     date = line.replace('Date:','')
		     date = strip(date)
		if line.find('Artist:') == 0:
            	     artist = line.replace('Artist:','')
		     artist = strip(artist)
		if line.find('Album:') == 0:
		     album = line.replace('Album:','')
		     album = strip(album)
		if line.find('Title:') == 0:
            	     title = line.replace('Title:','')
		     title = strip(title)

	if len(artist)<>0:
		return_value = artist

	if len(album)<>0:
		if len(artist)<>0:
			return_value += ' - ' + album
		else:
			return_value  = album
	if len(date)<>0:
		if len(return_value)<>0:
			return_value += '(' + date + ') - '
		else:
			return_value = '(' + date + ')'
	if len(title)<>0:
		if len(return_value)<>0:
			if len(album) == 0:
			    return_value += ' - ' + title
			else:
			    return_value += title    
		else:
			return_value = title			
					 
	return return_value

def status(dummy):
	state=''
	volume=''
	repeat=''
	random=''
	song=''
	total=''
	timepos = ''
	timestr = ''
	perc = ''
	return_value = ''
	s=mpc_command('status')
	for line in s.split('\r\n'):
		if line.find('state:') == 0:
            	     state = line.replace('state:','')
		     state = strip(state)
		     if state == "play":
		    	    state = 'playing'
		     if state == "pause":
		    	    state = 'paused'
		     if state == "stop":
		    	    state = 'stopped'	    	    
		if line.find('volume:') == 0:
            	     volume = line.replace('volume:','')
		     volume = strip(volume)
		if line.find('repeat:') == 0:
		     repeat = line.replace('repeat:','')
		     if strip(repeat) == '0':
		    	    repeat = 'off'
		     if strip(repeat) == '1':
		    	    repeat = 'on'	    
		if line.find('random:') == 0:
            	     random = line.replace('random:','')
		     if strip(random) == '0':
		    	    random = 'off'
		     if strip(random) == '1':
		    	    random = 'on'
		if line.find('song:') == 0:
            	     sng = line.replace('song:','')
		     song = str(int(sng.strip()) + 1)
		if line.find('playlistlength:') == 0:
            	     pl = line.replace('playlistlength:','')
		     total = str(int(pl.strip()))
		if line.find('time:') == 0:
		     timestr = line.replace('time:','')
		     curpos = int(timestr.split(':')[0])
		     allpos = int(timestr.split(':')[1])
		     curposs = sec2minsec(curpos)
		     allposs = sec2minsec(allpos)
		     timepos = curposs + '/' + allposs
		     perc = str(int(((curpos + 0.0)/allpos)*100))
		          
	if dummy != "maxid":
	    
	    if len(state)<>0:
		return_value = '\n' + '[' + state + ']'

	    if len(song)<>0:
		if len(state)<>0:
			return_value += ' #' + song
		else:
			return_value  = ' #' + song
	    if len(total)<>0:
		if len(return_value)<>0:
			if total != '0':
			    return_value += '/' + total + '  '
		else:
			return_value = ' Total: ' + total
	    if len(timepos)<>0:
		if len(return_value)<>0:
			return_value += timepos  + ' '
		else:
			return_value = 'Timepos: ' + timepos
	    if len(perc)<>0:
		if len(return_value)<>0:
			return_value += '(' + perc  + '%)'
		else:
			return_value = 'Percentage: (' + perc + '%)'
	
	    if (volume<>"") and (repeat<>"") and (random<>""):
    		return_value += '\n' + 'volume: ' + volume + '% ' +  '  repeat: ' + repeat + '    random: ' + random
	else:
	    return_value = total    
	return return_value

def toggle_handler(command):
	if mpc_command(command) == 'OK':
		return_value = current_song('') + status('')
	else:
		return_value='Error.'
	return return_value	

def on_off_handler(parameters, command):
	return_value = ''
	if not parameters.strip() == "":
		if str(parameters) == "off" or str(parameters) == "on":
		    if parameters == "off":
			    parameters = '0'
		    elif parameters == "on":
			    parameters = '1'
		    if mpc_command(command + ' ' + str(parameters)) == 'OK':
    				    return_value = current_song('') + status('')
		else:
		    return_value='Error.'	
	else:
	    return_value='Error.'
	return return_value    

###################################################
#
#
#
####################################################

def handler_mpc(type, source, parameters):
	return_value = current_song('') + status('')
	smsg(type, source, return_value)


def handler_mpc_play(type, source, parameters):
	return_value = toggle_handler('play')
	smsg(type, source, return_value)


def handler_mpc_pause(type, source, parameters):
	return_value = toggle_handler('pause')
	smsg(type, source, return_value)

def handler_mpc_next(type, source, parameters):
	return_value = toggle_handler('next')
	smsg(type, source, return_value)

def handler_mpc_prev(type, source, parameters):
	return_value = toggle_handler('previous')
	smsg(type, source, return_value)

def handler_mpc_shuffle(type, source, parameters):
	return_value = toggle_handler('shuffle')
	smsg(type, source, return_value)


def handler_mpc_random(type, source, parameters):
	return_value = on_off_handler(parameters,'random')
	smsg(type, source, return_value)

def handler_mpc_repeat(type, source, parameters):
	return_value = on_off_handler(parameters, 'repeat')
	smsg(type, source, return_value)

def handler_mpc_volume(type, source, parameters):
	return_value = ''
	if parameters.strip() != '' and int(parameters):
		if int(parameters) <= 100 and int(parameters) >= 1:
		    if mpc_command('setvol ' + str(parameters)) == 'OK':
    				    return_value = current_song('') + status('')
		else:
		    return_value='Error.'	
	else:
	    return_value='Error.'	
	smsg(type, source, return_value)

def handler_mpc_playid(type, source, parameters):
	return_value = ''
	min_id = 1
	if status('maxid').strip() != '' and int(status('maxid')):
	    max_id = int(status('maxid'))
	if parameters.strip() != '' and int(parameters):
	    if int(parameters) >= min_id and int(parameters) <= max_id:
		    parameters = str(int(parameters) - 1)
		    if mpc_command('playid ' + str(parameters)) == 'OK':
    				    return_value = current_song('') + status('')
	    else:
		    return_value='ID out of range. Valid values are: ' + str(min_id) + ' to ' + str(max_id)
	else:
	    return_value='Error.'	
	smsg(type, source, return_value)
	


# useful for console development
#def smsg(type, source, parameters):
#	print parameters

register_command_handler(handler_mpc, '!mpc', 100, 'Shows status of mpd.', '!mpc', ['!mpc'])	
register_command_handler(handler_mpc_play, '!mpc_play', 100, 'Start playing in mpd.', '!mpc_play', ['!mpc_play'])
register_command_handler(handler_mpc_playid, '!mpc_playid', 100, 'Start playing ID in mpd.', '!mpc_playid 50', ['!mpc_playid 50'])
register_command_handler(handler_mpc_pause, '!mpc_pause', 100, 'Pauses playing in mpd.', '!mpc_pause', ['!mpc_pause'])
register_command_handler(handler_mpc_next, '!mpc_next', 100, 'Plays next song in mpd.', '!mpc_next', ['!mpc_next'])
register_command_handler(handler_mpc_prev, '!mpc_prev', 100, 'Plays previous song in mpd.', '!mpc_prev', ['!mpc_prev'])
register_command_handler(handler_mpc_shuffle, '!mpc_shuffle', 100, 'Shuffles playlist in mpd.', '!mpc_shuffle', ['!mpc_shuffle'])
register_command_handler(handler_mpc_random, '!mpc_random', 100, 'Randomizes playing in mpd.', '!mpc_random', ['!mpc_random'])
register_command_handler(handler_mpc_volume, '!mpc_volume', 100, 'Changes volume in mpd.', '!mpc_volume 50', ['!mpc_volume 50'])
