#$ neutron_plugin 01

LOCALDB_FILE = 'dynamic/localdb.txt'

initialize_file(LOCALDB_FILE, '{}')

def handler_query_get(type, source, parameters):
	localdb = eval(read_file(LOCALDB_FILE))
	if localdb.has_key(string.lower(parameters)):
		smsg(type, source, localdb[string.lower(parameters)] + ' [' + parameters + ']')
	else:
		smsg(type, source, 'Not Found [' + parameters + ']')

def handler_query_set(type, source, parameters):
	localdb = eval(read_file(LOCALDB_FILE))
	keyval = string.split(parameters, '=', 1)
	key = string.lower(keyval[0]).strip()
	value = keyval[1].strip()
	if not value:
		if localdb.has_key(key):
			del localdb[key]
		smsg(type, source, key + ' Is Deleted')
	else:
		localdb[key] = keyval[1].strip()
		smsg(type, source, key + ' == ' + keyval[1].strip())
	write_file(LOCALDB_FILE, str(localdb))

register_command_handler(handler_query_get, '!?', 0, 'Looks up a query in the local database.', '!? <query>', ['!? neutron', '!? multiple words'])
register_command_handler(handler_query_set, '!!', 100, 'Sets a query in the local database.', '!! <query> = <definition>', ['!! neutron = the best!', '!! multiple words ='])
