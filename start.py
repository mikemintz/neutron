#!/usr/bin/env python

# Author: Bohdan Turkynewych, AKA Gh0st, 2006-2007, tb0hdan[at]gmail[dot]com
# Distributed under the terms of GPLv2

# Run this script under screen (man screen)
# It will restart neutron over and over again.
# And plz, do not forget to set AUTO_RESTART to 0 in config.txt file.

from time import sleep as time_sleep
from sys import exit as sys_exit
from os import walk as os_walk, remove as os_remove, system as os_system
from re import sub as re_sub
from os.path import join as os_path_join, getsize as os_path_getsize

def pyc_cleanup():
    lines_count = 0
    print 'Removing python byte-compiled files...'
    for root, dirs, files in os_walk('modules'):
	for name in files:
	    fpath =  os_path_join(root, name)
	    fsize =  os_path_getsize(fpath)
	    if re_sub('(^.*\.pyc$)','',fpath) == '':
		print 'File: ' + str(fpath) + ' Bytes: ' + str(fsize)
		try:
		    os_remove(fpath)
		except:
		    print 'Check permissions and/or FS.'
		    raise
		lines_count += 1
    print 'Done. %s file(s) removed'%str(lines_count)
    
while True:
    try:
	# some strange bugs, when .pyc files remain...
	pyc_cleanup()
	# do launch neutron
        os_system("python ./neutron.py")
	# give time for User Interrupt.
	# and avoid high CPU load
	# if something is wrong with
	# neutron.py
	time_sleep(10)
    except KeyboardInterrupt:
        sys_exit()
