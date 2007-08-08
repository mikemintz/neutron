#!/usr/bin/env python

# Run this script under screen (man screen)
# It will restart neutron over and over again.
# And plz, do not forget to set AUTO_RESTART to 0 in config.txt file.

import os
from os import system
import time
from sys import exit as sys_exit

def pyc_cleanup():
    lines_count = 0
    print 'Removing python byte-compiled files...'
    pipe = os.popen("sh -c 'find modules/ -name \'*.pyc\''")
    lines = pipe.read()
    s = str(0)
    if lines.strip():
	for line in lines.split('\n'):
	    if line.strip():
		print line
		try:
		    os.remove(line)
		except:
		    print 'Check permissions and/or FS.'
		    raise
		lines_count += 1
	s = str(lines_count)	
    print 'Done. %s file(s) removed'%s
    
while True:
    try:
	# some strange bugs, when .pyc files remain...
	pyc_cleanup()
	# do launch neutron
        system("python ./neutron.py")
	# give time for User Interrupt.
	# and avoid high CPU load
	# if something is wrong with
	# neutron.py
	time.sleep(10)
    except KeyboardInterrupt:
        sys_exit()
