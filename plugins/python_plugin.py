#$ neutron_plugin 01
# Requires: admin_plugin.py, help_plugin.py
# parts of code: Gh0st AKA Bohdan Turkynewych.

import re
import string

def handler_python_eval(type, source, parameters):
	try:
		return_value = str(eval(parameters))
		time.sleep(1)
	except:
		return_value = str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	smsg(type, source, return_value)

def handler_python_calc(type, source, parameters):
	parameters = parameters.strip()
	if re.sub('([' + string.digits +']|[\+\-\/\*\^\.])','',parameters).strip() == '':
	    try:
    		return_value = str(eval(parameters))
		time.sleep(1)
	    except:
		return_value = str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	else:
		return_value = 'Invalid syntax.'
	smsg(type, source, return_value)

def handler_python_domainc(type, source, parameters, oscommand):
	parameters = parameters.strip()
	return_value = ''
	if parameters != '':
	    parameters = string.split(parameters, ' ', 1)[0]
	    domainre   = '[a-zA-Z_0-9]+?(\.[a-zA-Z_0-9]{2,6}){1,4}'
	    ipre       = '^\d\d?\d?\.\d\d?\d?\.\d\d?\d?\.\d\d?\d?$'
	    if re.sub(domainre, '', parameters).strip() == '' or re.sub(ipre, '', parameters).strip() == '':
		try:
    		    handler_python_sh(type, source, oscommand + parameters) 
	            time.sleep(1)
		except:
		    return_value = 'Hmm... Something nasty is going on, sent message to admins.'
		    admin_bcast('handler_python_domainc ' + str(parameters) + ' From: ' + get_true_jid(source) + 'Command: ' + oscommand)
	    else:
		return_value = 'Invalid syntax.'
	else:
	    return_value = 'Empty input. Please refer to help !<command>.'
	smsg(type, source, return_value)
		

def handler_python_netping(type, source, parameters):
	handler_python_domainc(type, source, parameters, 'ping -c 3 ')

def handler_python_traceroute(type, source, parameters):
	handler_python_domainc(type, source, parameters, 'traceroute ')

def handler_python_exec(type, source, parameters):
	if '\n' in parameters and parameters[-1] != '\n':
		parameters += '\n'
	try:
		exec parameters in globals()
		time.sleep(1)
		return_value = 'Successful Execution'
	except:
		return_value = str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	smsg(type, source, return_value)

def handler_python_sh(type, source, parameters):
	# Send STDERR to STDOUT.
	pipe = os.popen('sh -c "%s" 2>&1' % parameters)
	# time.sleep(0.5)
	# 4k buffer equals to 2 standard console (80x25) pages.
	return_value = pipe.read(4096)
	smsg(type, source, unicode(return_value, 'utf8'))

register_command_handler(handler_python_calc, '!calc', 0, 'Evaluates and returns a Python arithmetic expression.', '!calc <expression>', ['!calc 1+1'])
register_command_handler(handler_python_netping, '!netping', 0, 'Executes ping from system. shell safe.', '!netping <host/ip>', ['!netping google.com'])
register_command_handler(handler_python_traceroute, '!traceroute', 0, 'Executes traceroute from system. shell safe.', '!traceroute <host/ip>', ['!traceroute google.com'])
register_command_handler(handler_python_eval, '!eval', 100, 'Evaluates and returns a Python expression.', '!eval <expression>', ['!eval 1+1'])
register_command_handler(handler_python_exec, '!exec', 100, 'Runs a Python statement.', '!exec <statement>', ['!eval pass'])
register_command_handler(handler_python_sh, '!sh', 100, 'Executes a shell command.', '!sh <command>', ['!sh ls'])

