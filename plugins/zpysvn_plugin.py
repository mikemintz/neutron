#$ neutron_plugin 01

HASSVN = 1
try:
    import pysvn
except:
    HASSVN = 0

import os

def login(*args):
    return True, 'anonymous', 'password', False

def handler_update_neutron(type, source, parameters):

    if HASSVN == 0:
	smsg(type, source, 'PySVN module not installed. Please have close look at modules/pysvn')
	return

    reply = ''
    revision = ''
    update_path = ''
    client = pysvn.Client()
    client.callback_get_login = login
    files = os.listdir('./')
    if 'neutron.py' in files:
	update_path = './'
    else:
	update_path = '../'
    reply = str(client.update(update_path)).split('kind=')[1].split('>]')[0]
    if reply.split(' ')[0] == 'number':
	reply = 'Updated to revision: ' + reply.split(' ')[1]
	reply += ' on path ' + update_path
    else:
	reply = 'Unknown Error.'	
    smsg(type, source, reply)

register_command_handler(handler_update_neutron, '!svnup', 100, 'Updates neutron sources to last version.', '!svnup', ['!svnup'])

