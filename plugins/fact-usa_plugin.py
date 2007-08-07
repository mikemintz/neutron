#$ neutron_plugin 01

AREACODE_FILE = 'static/areacodes.txt'
ZIPCODE_FILE = 'static/zipcodes.txt'

def fact_areacode(query):
	try:
		int(query)
	except:
		return 'Invalid'
	fp = open(AREACODE_FILE, 'r')
	while 1:
		line = fp.readline()
		if not line:
			return 'Not Found'
		elif query == line[:3]:
			return line[4:].strip()
		elif int(query) < int(line[:3]):
			return 'Not Found'

def fact_zipcode(query):
	try:
		int(query)
	except:
		return 'Invalid'
	fp = open(ZIPCODE_FILE, 'r')
	while 1:
		line = fp.readline()
		if not line:
			return 'Not Found'
		code, region, city, state = string.split(line, '\t', 3)
		if query == code:
			return region + ', ' + city + ', ' + state.strip()
		elif int(query) < int(code):
			return 'Not Found'

def handler_fact_areacode(type, source, parameters):
	result = fact_areacode(parameters.strip())
	smsg(type, source, result)

def handler_fact_zipcode(type, source, parameters):
	result = fact_zipcode(parameters.strip())
	smsg(type, source, result)

register_command_handler(handler_fact_areacode, '!areacode', 0, 'Returns the location of a U.S. area code.', '!areacode <###>', ['!areacode 800'])

register_command_handler(handler_fact_zipcode, '!zipcode', 0, 'Returns the location of a U.S. zipcode.', '!zipcode <#####>', ['!zipcode 12345'])
