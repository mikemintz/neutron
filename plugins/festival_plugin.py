#$ neutron_plugin 01

# This plugin is part of Neutron jabber bot software.
# Licensed under GPLv2
# Author: Bohdan Turkynewych, 2009, <tb0hdan@gmail.com>

from socket import socket as socket_socket, error as socket_error
from socket import AF_INET as socket_AF_INET, SOCK_STREAM as socket_SOCK_STREAM
from socket import gethostbyname as socket_gethostbyname
from thread import start_new_thread as thread_start_new_thread
from os import popen as os_popen, system as os_system
from time import sleep as time_sleep
from re import sub as re_sub
from string import letters as string_letters, digits as string_digits

def say_text(type, source, text):

    def runit(txt):
	pipe = os_popen("ps -C festival -o pid=")
	if pipe.read().strip() == '':
    	    thread_start_new_thread(os_system,("festival --server 2>&1 >/dev/null",))
	    time_sleep(3)
	conn = socket_socket(socket_AF_INET, socket_SOCK_STREAM)
	try:
	    conn.connect((socket_gethostbyname('localhost'),1314))
	    conn.send('(SayText \"' + txt + '\")')
	    return
	except socket_error:
	    pass

    if re_sub('([' + string_letters + '|' + string_digits + '|.|,|!|-|\ ])','',text) == '':
	pipe = os_popen("festival --version 2>/dev/null")
	if pipe.read().strip() != '':
	    runit(text)
	else:
	    smsg(type, source, 'Festival package not installed')


def handler_speech(type, source, parameters):
	if parameters.strip()=='':
	    smsg(type, source, '!help !fstival')
	    return
	say_text(type, source, parameters)

register_command_handler(handler_speech,'!fstival', 100, 'Converts text to speech using Festival', '!fstival', ['!fstival Hello world.'])