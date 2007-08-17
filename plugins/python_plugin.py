#$ neutron_plugin 01

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
register_command_handler(handler_python_eval, '!eval', 100, 'Evaluates and returns a Python expression.', '!eval <expression>', ['!eval 1+1'])
register_command_handler(handler_python_exec, '!exec', 100, 'Runs a Python statement.', '!exec <statement>', ['!eval pass'])
register_command_handler(handler_python_sh, '!sh', 100, 'Executes a shell command.', '!sh <command>', ['!sh ls'])
