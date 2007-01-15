#$ neutron_plugin 01

def handler_help_help(type, source, parameters):
	if parameters and COMMANDS.has_key(parameters):
		reply = COMMANDS[parameters]['description'] + ' Usage: ' + COMMANDS[parameters]['syntax'] + '\nExamples:'
		for example in COMMANDS[parameters]['examples']:
			reply += '\n  *  ' + example
		reply += '\nRequired Access Level: ' + str(COMMANDS[parameters]['access'])
	else:
		reply = 'Type !commands for a list of commands.'
	smsg(type, source, reply)

def handler_help_commands(type, source, parameters):
    commandlist = []
    for command in COMMANDS.keys():
        if has_access(source, COMMANDS[command]['access']):
            commandlist.append(command)
    commandlist.sort()
    commandlist = string.join(commandlist)
    smsg('private', source, commandlist)

register_command_handler(handler_help_help, 'help', 0, 'Send basic help message or gives information on specified command.', 'help [command]', ['help', 'help help'])
register_command_handler(handler_help_commands, '!commands', 0, 'Send list of commands.', '!commands', ['!commands'])
