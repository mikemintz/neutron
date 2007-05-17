#$ neutron_plugin 01

CURRENT_POLL = {}

def handler_vote_vote(type, source, parameters):
	global CURRENT_POLL
	if GROUPCHATS.has_key(source[1]) and GROUPCHATS[source[1]].has_key(source[2]):
		if CURRENT_POLL:
			if isadmin(GROUPCHATS[source[1]][source[2]]['jid']) or not GROUPCHATS[source[1]][source[2]]['jid'] in CURRENT_POLL['jids']:
				if CURRENT_POLL['options'].has_key(parameters.strip().lower()):
					CURRENT_POLL['options'][parameters.strip().lower()] += 1
					CURRENT_POLL['jids'].append(GROUPCHATS[source[1]][source[2]]['jid'])
					smsg(type, source, 'Vote Counted')
				else:
					smsg(type, source, 'Option Not Available')
			else:
				smsg(type, source, 'You already voted.')
		else:
			smsg(type, source, 'There\'s no poll going on right now.')
	else:
		smsg(type, source, 'You must vote from the groupchat.')

def handler_vote_newpoll(type, source, parameters):
	global CURRENT_POLL
	if CURRENT_POLL:
		poll_text = 'New Poll (' + source[2] + ') - ' + CURRENT_POLL['question'] + '\n'
		for option in CURRENT_POLL['options'].keys():
			poll_text += '  *  ' + option + '\n'
		poll_text += 'To vote, type or message me the following: !vote <option>'
		msg(source[1], poll_text)
	else:
		CURRENT_POLL = {'options': {}, 'question': parameters, 'jids': []}
		smsg(type, source, 'Poll Created')

def handler_vote_polloption(type, source, parameters):
	global CURRENT_POLL
	if CURRENT_POLL:
		CURRENT_POLL['options'][parameters.strip().lower()] = 0
		smsg(type, source, 'Option Added')
	else:
		smsg(type, source, 'Error: No Poll')

def handler_vote_endpoll(type, source, parameters):
	global CURRENT_POLL
	if CURRENT_POLL:
		poll_text = 'Poll Results (' + source[2] + ') - ' + CURRENT_POLL['question'] + '\n'
		num = 1
		for option in CURRENT_POLL['options'].keys():
			poll_text += str(CURRENT_POLL['options'][option]) + ' - ' + option + '\n'
			num += 1
		msg(source[1], poll_text)
		CURRENT_POLL = {}
	else:
		smsg(type, source, 'Error: No Poll')

register_command_handler(handler_vote_vote, '!vote', 0, 'Casts a vote for current poll.', '!vote <option>', ['!vote yes'])
register_command_handler(handler_vote_newpoll, '!newpoll', 100, 'Creates a new poll, or if options are added, submits the poll to current channel.', '!newpoll [question]', ['!newpoll Do you like turtles?', '!newpoll'])
register_command_handler(handler_vote_polloption, '!polloption', 100, 'Adds an option to the current poll.', '!polloption <option>', ['!polloption yes'])
register_command_handler(handler_vote_endpoll, '!endpoll', 100, 'Ends the poll and returns the results.', '!endpoll]', ['!endpoll'])
