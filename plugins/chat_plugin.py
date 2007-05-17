#$ neutron_plugin 01

def chat_personal(type, source, body):
	replies = ['What\'s that?', 'I don\'t understand.', 'Sorry, could you speak up please?']
	reply = random.choice(replies)
	if type == 'public':
		if source[1]:
			smsg(type, source, reply)
	elif type == 'private':
		smsg(type, source, reply)

def handler_chat_message(type, source, body):
	if type == 'public':
		firstword = string.split(body)[0]
		if string.split(string.split(firstword, '_')[0], ':')[0].lower() == 'neutron' and firstword[-1] == ':':
			if len(string.split(body)) > 1:
				parameters = body[(body.find(' ') + 1):]
			else:
				parameters = ''
			chat_personal(type, source, parameters)
	elif type == 'private':
		if not COMMANDS.has_key(string.split(body)[0]):
			chat_personal(type, source, body)

#register_message_handler(handler_chat_message)
