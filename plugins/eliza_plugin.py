#$ neutron_plugin 01

import eliza
therapist = eliza.eliza()

def handler_eliza_en(type,source, body):
	
	if type == 'public' and get_nick(source[1])!=source[2] and source[2]!='' and re.search('^'+get_nick(source[1])+':',body)!=None:
		result=therapist.respond(body.replace(get_nick(source[1])+':','').strip())
		smsg(type,source, result)
	pass
	
register_message_handler(handler_eliza_en)
