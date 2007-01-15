#$ neutron_plugin 01

def handler_chatbot_nick_leave(groupchat, nick):
	if nick == 'ChatBot':
		join_groupchat(groupchat, 'ChatBot')
		msg(groupchat, 'Take that, ChatBot!')

#register_leave_handler(handler_chatbot_nick_leave)
