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

def mpc_command(command):
    err = 0
    global mpc_server
    global mpc_port
    suffix='\r\nclose\r\n'
    reply=''
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        conn.connect((socket.gethostbyname(mpc_server), mpc_port))
        conn.send(command+suffix)
        s = conn.recv(1024)
        conn.close()
    except socket.error:
        err = 1
    if err:	
        reply = 'Connection Error.'		
    else:
        if re.search('OK',s):
            for line in s.split('\n'):
                if line.strip() and not re.search('OK', line):
                    reply += line + '\r\n'
            if not reply.strip():
                reply = 'OK'
    return reply		    

def current_song(dummy):
    artist = ''
    album = ''
    title = ''
    date = ''
    return_value = ''
    s = mpc_command('currentsong')
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

    if len(artist):
        return_value = artist
    if len(album):
        if len(artist):
            return_value += ' - ' + album
        else:
            return_value  = album
    if len(date):
        if len(return_value):
            return_value += '(' + date + ') - '
        else:
            return_value = '(' + date + ')'
    if len(title):
        if len(return_value):
            if len(album):
                return_value += title    
            else:
                return_value += ' - ' + title
        else:
            return_value = title			
					 
    return return_value

def status(dummy):
    state = ''
    volume = ''
    repeat = ''
    random = ''
    song = ''
    total = ''
    timepos = ''
    timestr = ''
    perc = ''
    return_value = ''
    s = mpc_command('status')
    for line in s.split('\r\n'):
        if line.find('state:') == 0:
            state = line.replace('state:','')
            state = strip(state)
            if state == "play":
                state = 'playing'
            elif state == "pause":
                state = 'paused'
            elif state == "stop":
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
            song = unicode(int(sng.strip()) + 1)
        if line.find('playlistlength:') == 0:
            pl = line.replace('playlistlength:', '')
            total = unicode(int(pl.strip()))
        if line.find('time:') == 0:
            timestr = line.replace('time:','')
            curpos = int(timestr.split(':')[0])
            allpos = int(timestr.split(':')[1])
            curposs = "%.2i:%.2i" % (curpos/60, curpos%60)
            allposs = "%.2i:%.2i" % (allpos/60, allpos%60)
            timepos = curposs + '/' + allposs
            perc = unicode(int(((curpos + 0.0)/allpos)*100))
		          
    if dummy != "maxid":
        if len(state):
            return_value = '\n' + '[' + state + ']'

        if len(song):
            if len(state):
                return_value += ' #' + song
            else:
                return_value  = ' #' + song
        if len(total):
            if len(return_value):
                if total != '0':
                    return_value += '/' + total + '  '
            else:
                return_value = ' Total: ' + total
        if len(timepos):
            if len(return_value):
                return_value += timepos  + ' '
            else:
                return_value = 'Timepos: ' + timepos
        if len(perc):
            if len(return_value):
                return_value += '(' + perc  + '%)'
            else:
                return_value = 'Percentage: (' + perc + '%)'

        if volume and repeat and random:
            return_value += '\n' + 'volume: ' + volume + '% ' +  '  repeat: ' + repeat + '    random: ' + random
    else:
        return_value = total    
    return return_value

def on_off_handler(parameters):
    return_value = ''
    if (len(parameters) == 2 and parameters[1] in ('off', 'on') and
        mpc_command(parameters[0] + ' ' + {'off': 0,
                                           'on': 1}[parameters[1]]) == 'OK'):
        return_value = current_song('') + status('')
    else:
        return_value = 'Error.'
    return return_value    

###################################################
#
#
#
####################################################

def handler_mpc(type, source, parameters):
    return_value = ''
    parameters = parameters.split()
    if len(parameters) == 1 and parameters[0] in ('play', 'pause', 'next', 'previous', 'shuffle'):
        if mpc_command(parameters[0]) == 'OK':
            return_value = current_song('') + status('')
        else:
            return_value = 'Error.'
    elif len(parameters) > 1:
        if parameters[0] in ('random', 'repeat'):
            if (len(parameters) == 2 and parameters[1] in ('off', 'on') and
                mpc_command(
                parameters[0] + ' ' + {'off': 0,
                                       'on': 1}[parameters[1]]) == 'OK'):
                return_value = current_song('') + status('')
            else:
                return_value = 'Error.'
        elif parameters[0] == 'volume':
            if parameters[1] and int(parameters[1]):
                if int(parameters[1]) <= 100 and int(parameters[1]) >= 1:
                    if mpc_command('setvol ' + unicode(parameters[1])) == 'OK':
                        return_value = current_song('') + status('')
                else:
                    return_value = 'Error.'
            else:
                return_value = 'Error.'
        elif parameters[0] == 'playid':
            min_id = 1
            max_id = 1
            status_maxid = status('maxid')
            if status_maxid.strip() and int(status_maxid):
                max_id = int(status_maxid)
            if parameters[1] and int(parameters[1]):
                if int(parameters[1]) >= min_id and int(parameters[1]) <= max_id:
                    parameters = unicode(int(parameters[1]) - 1)
                    if mpc_command('playid ' + unicode(parameters)) == 'OK':
                        return_value = current_song('') + status('')
                else:
                    return_value = 'ID out of range. Valid values are: ' + unicode(min_id) + ' to ' + unicode(max_id)
            else:
                return_value = 'Error.'
        else:
            return_value = 'Error.'
    else:
        return_value = current_song('') + status('')
    smsg(type, source, return_value)



# useful for console development
#def smsg(type, source, parameters):
#	print parameters

register_command_handler(handler_mpc, '!mpc', 100, """Without option: Shows status of mpd.
With options:
 *play: Start playing in mpd.
 *playid <id>: Start playing ID in mpd.
 *pause: Pauses playing in mpd.
 *next: Plays next song in mpd.
 *previous: Plays previous song in mpd.
 *shuffle: Shuffles playlist in mpd.
 *random <off|on>: Sets random playing in mpd.
 *repeat <off|on>: Sets repeat playing in mpd.
 *volume <val>: Changes volume in mpd.
""", '!mpc [option [parameter]]', ['!mpc','!mpc play', '!mpc_playid 50'])
