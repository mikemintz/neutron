#$ neutron_plugin 01

ELEMENT_FILE = 'static/elements.txt'
TLD_FILE = 'static/tlds.txt'

def fact_element(query):
	fp = open(ELEMENT_FILE, 'r')
	while 1:
		line = fp.readline()
		if not line:
			return 'Not Found'
		(key, value) = string.split(line, ' ', 1)
		if string.lower(query).strip() == string.lower(key).strip():
			return value.strip()

def fact_tld(query):
	fp = open(TLD_FILE, 'r')
	while 1:
		line = fp.readline()
		if not line:
			return 'Not Found'
		(key, value) = string.split(line, ': ', 1)
		if string.lower(query).strip() == string.lower(key).strip():
			return value.strip()

def handler_fact_element(type, source, parameters):
	result = fact_element(parameters.strip())
	smsg(type, source, result)

def handler_fact_tld(type, source, parameters):
	result = fact_tld(parameters.strip())
	smsg(type, source, result)

register_command_handler(handler_fact_element, '!element', 0, 'Returns the name and number of an atomic element code.', '!element <code>', ['!element Li'])

register_command_handler(handler_fact_tld, '!tld', 0, 'Returns the location for a top level domain or a TLD for a location.', '!tld <location/TLD>', ['!tld com', '!tld antarctica'])
