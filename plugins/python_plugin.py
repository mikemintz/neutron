#$ neutron_plugin 01

def handler_python_eval(type, source, parameters):
	try:
		return_value = str(eval(parameters))
	except:
		return_value = str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	smsg(type, source, return_value)

def handler_python_exec(type, source, parameters):
	if '\n' in parameters and parameters[-1] != '\n':
		parameters += '\n'
	try:
		exec parameters in globals()
		return_value = 'Successful Execution'
	except:
		return_value = str(sys.exc_info()[0]) + ' - ' + str(sys.exc_info()[1])
	smsg(type, source, return_value)

def handler_python_sh(type, source, parameters):
	pipe = os.popen('sh -c ' + '"' + parameters + '"')
	#time.sleep(0.5)
	return_value = pipe.read(1024*4)
	smsg(type, source, return_value)

register_command_handler(handler_python_eval, '!eval', 100, 'Evaluates and returns a Python expression.', '!eval <expression>', ['!eval 1+1'])
register_command_handler(handler_python_exec, '!exec', 100, 'Runs a Python statement.', '!exec <statement>', ['!eval pass'])
register_command_handler(handler_python_sh, '!sh', 100, 'Executes a shell command.', '!sh <command>', ['!sh ls'])
