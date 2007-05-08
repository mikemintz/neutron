#!/usr/bin/env python

# Run this script under screen (man screen)
# It will restart neutron over and over again.
# And plz, do not forget to set AUTO_RESTART to 0 in config.txt file.
 
import os

while True:
	try:
		os.system("python ./neutron.py")

        except KeyboardInterrupt:
                sys.exit()
				
