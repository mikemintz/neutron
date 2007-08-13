#$ neutron_plugin 01

# Parts of code:
# Author: Bohdan Turkynewych, AKA Gh0st, tb0hdan[at]gmail.com

def handler_list_plugins(type, source, parameters):
	plugins_count = 0
	valid_plugins = find_plugins()
	total_plugins = len(valid_plugins)
	reply = '\nAvailable Neutron Plugins(stripped names, suitable for using !loadpl):\n'
	for plugin in valid_plugins:
	    reply += plugin.split('_plugin.py')[0] + '\n'
	reply += 'Total plugins: ' + str(total_plugins)
	smsg(type, source, reply)

def handler_load_plugin(type, source, parameters):
	valid_plugins = find_plugins()
	parameters = parameters.strip()
	reply = ''
	if parameters != '':
	    valid_plugin = parameters + '_plugin.py'
	    if valid_plugin in valid_plugins:
		try:
		    fp = file(PLUGIN_DIR + '/' + valid_plugin)
		    ErrMsg = ' Ok. '
		    try:
		        exec fp in globals()
		    except:
		        ErrMsg = ' Load Error. Check plugin.'
		        ErrMsg += '\r\nReason: '+ str(sys.exc_info()[0].__name__)+ ':\r\n' + str(sys.exc_info()[1])
		        pass    
		    fp.close()
		    reply = 'Plugin: ' + valid_plugin + ErrMsg
		except:
		    ErrMsg = str(sys.exc_info()[0].__name__)+ ':\r\n' + str(sys.exc_info()[1])
		    reply = 'Unknown critical error occured ' + ErrMsg
	    else:
		reply = 'That plugin was not found in list.'	    
	else:
	    reply = 'Usage: !loadpl <plugin>\nName can be retrieved from !plugins command output.'	
 	
	smsg(type, source, reply)

register_command_handler(handler_list_plugins, '!plugins', 100, 'Shows list of available plugins.', '!plugins', ['!plugins'])
register_command_handler(handler_load_plugin, '!loadpl', 100, 'Loads one of available plugins.', '!loadpl <plugin>', ['!loadpl admin'])