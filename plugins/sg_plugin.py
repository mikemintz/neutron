#$ neutron_plugin 01


def handler_SG_get(type, source, parameters):
		groupchat = source[1]
		iq = xmpp.Iq('get')
		iq.setQueryNS('http://jabber.org/protocol/stats')
		if parameters!='':
			iq.setTo(parameters.strip())
		else:
			iq.setTo(SERVER)
			parameters=SERVER
		JCON.SendAndCallForResponse(iq,first_handler,{'parameters':parameters,'type':type,'source':source})

def first_handler(coze,res,parameters,type,source):
	#print par
	payload=res.getQueryPayload()
	if res.getType()=='error':
		smsg(type,source,'Error '+res.getErrorCode()+ ': '+res.getError())
		pass
	elif res.getType()=='result':
		iq = xmpp.Iq('get')
		iq.setQueryNS('http://jabber.org/protocol/stats')
		iq.setQueryPayload(payload)
		iq.setTo(parameters.strip())
		JCON.SendAndCallForResponse(iq,second_handler,{'parameters':parameters,'type':type,'source':source})

def second_handler(coze,stats,parameters,type,source):
	pay=stats.getQueryPayload()
	if stats.getType()=='result':
		result='Informations about ' + parameters + ':\n'
		for stat in pay:
			result=result+stat.getAttrs()['name']+': '+stat.getAttrs()['value'] + ' '+stat.getAttrs()['units'] + '\n'
			
		smsg(type,source,result)


register_command_handler(handler_SG_get, '!server_stats', 0, 'Returns server statistics according to JEP-0039.', '!server_stats <server>', ['!server_stats njs.netlab.cz'])
	
