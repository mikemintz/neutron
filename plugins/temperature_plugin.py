#$ neutron_plugin 01

def handler_temperature_temperature(type, source, parameters):
	if parameters:
		splitdata = string.split(parameters)
		try:
			input_value = float(splitdata[0])
			if len(splitdata) > 1:
				unit_system = splitdata[1][0]
			else:
				unit_system = 'f'
		except ValueError:
			try:
				input_value = float(splitdata[0][:-1])
			except ValueError:
				smsg(type, source, 'Syntax Error')
				return
			unit_system = splitdata[0][-1]
		unit_system = string.lower(unit_system)
		if unit_system == 'c':
			reply = str(round(input_value * 9 / 5 + 32, 1)) + ' F'
		else:
			reply = str(round((input_value - 32) * 5 / 9, 1)) + ' C'
	else:
		reply = 'C=(F-32)*5/9 F=C*9/5+32'
	smsg(type, source, reply)

register_command_handler(handler_temperature_temperature, '!temperature', 0, 'Converts temperatures from Celcius to Fahrenheit and vice versa.', '!temperature <#> <C/F>', ['!temperature 10 F', '!temperature 29 C'])
