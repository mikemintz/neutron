#$ neutron_plugin 01

import DICT
import urllib

def handler_dict_define(type, source, parameters):
	dc = DICT.DictConnection('dict.org')
	try:
		results = dc.get_definition(parameters.strip())
		if len(results):
			#reply = string.join(results[0], '\n')
			reply = 'http://www.dict.org/bin/Dict?Form=Dict1&Query=' + urllib.quote(parameters) + '&Strategy=*&Database=*'
			for result in results[:3]:
				reply += '\n\n' + string.join(result[:8], '\n')[:500][4:]
				if len(result) > 8:
					reply += ' . . .'
			reply = reply.replace('\n\n\n', '\n\n')
		else:
			reply = 'No Results'
	except:
		raise
		reply = 'Error'
	smsg(type, source, reply)

register_command_handler(handler_dict_define, '!define', 0, 'Defines a word using the DICT protocol.', '!define <word>', ['!define neutron'])
