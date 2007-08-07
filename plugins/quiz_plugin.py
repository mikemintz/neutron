#$ neutron_plugin 01

QUIZ_FILE = 'static/quizdata.txt'
QUIZ_TOTAL_LINES = 16197
QUIZ_TIME_LIMIT = 60
QUIZ_IDLE_LIMIT = 5

QUIZ_RECURSIVE_MAX = 20
QUIZ_SCORES = {}
QUIZ_CURRENT_ANSWER = {}
QUIZ_CURRENT_HINT = {}
QUIZ_CURRENT_TIME = {}
QUIZ_IDLENESS = {}

def quiz_timer(groupchat, start_time):
	time.sleep(QUIZ_TIME_LIMIT)
	if QUIZ_CURRENT_TIME.has_key(groupchat) and QUIZ_CURRENT_ANSWER.has_key(groupchat) and start_time == QUIZ_CURRENT_TIME[groupchat]:
		QUIZ_CURRENT_ANSWER[groupchat]
		msg(groupchat, '[QUIZ] Time is up! ' + str(QUIZ_TIME_LIMIT) + ' seconds have elapsed. The correct answer was: ' + QUIZ_CURRENT_ANSWER[groupchat])
		if QUIZ_IDLENESS.has_key(groupchat):
			QUIZ_IDLENESS[groupchat] += 1
		else:
			QUIZ_IDLENESS[groupchat] = 1
		if QUIZ_IDLENESS[groupchat] >= QUIZ_IDLE_LIMIT:
			msg(groupchat, '[QUIZ] Quiz has automatically ended due to inactivity for ' + str(QUIZ_IDLE_LIMIT) + ' questions. Please type !quiz_start to restart the quiz.')
			del QUIZ_CURRENT_ANSWER[groupchat]
			quiz_list_scores(groupchat)
		else:
			quiz_ask_question(groupchat)

def quiz_new_question():
	line_num = random.randrange(16197)
	fp = file(QUIZ_FILE)
	for n in range(line_num + 1):
		if n == line_num:
			try:
				(question, answer) = string.split(fp.readline().strip(), '|', 1)
				return (unicode(question), unicode(answer))
			except:
				QUIZ_RECURSIVE_MAX -= 1
				if QUIZ_RECURSIVE_MAX:
					return quiz_new_question()
				else:
					QUIZ_RECURSIVE_MAX = 20
					return ('Parsing Error: Line ' + str(n), '')
		else:
			fp.readline()

def quiz_ask_question(groupchat):
	(question, answer) = quiz_new_question()
	QUIZ_CURRENT_ANSWER[groupchat] = answer
	QUIZ_CURRENT_HINT[groupchat] = None
	QUIZ_CURRENT_TIME[groupchat] = time.time()
	thread.start_new(quiz_timer, (groupchat, QUIZ_CURRENT_TIME[groupchat]))
	msg(groupchat, '[QUIZ] New Question: ' + question)

def quiz_answer_question(groupchat, nick, answer):
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		if QUIZ_CURRENT_ANSWER[groupchat] == answer:
			if QUIZ_IDLENESS.has_key(groupchat):
				del QUIZ_IDLENESS[groupchat]
			answer_time = int(time.time() - QUIZ_CURRENT_TIME[groupchat])
			points = QUIZ_TIME_LIMIT / answer_time / 3 + 1
			msg(groupchat, '[QUIZ] ' + nick + ' was correct for +' + str(points) + ' points! The answer was: ' + answer)			
			if not QUIZ_SCORES.has_key(groupchat):
				QUIZ_SCORES[groupchat] = {}
			if QUIZ_SCORES[groupchat].has_key(nick):
				QUIZ_SCORES[groupchat][nick] += points
			else:
				QUIZ_SCORES[groupchat][nick] = points
			quiz_list_scores(groupchat)
			quiz_ask_question(groupchat)

def quiz_list_scores(groupchat):
	if QUIZ_SCORES.has_key(groupchat):
		if QUIZ_SCORES[groupchat]:
			if QUIZ_IDLENESS.has_key(groupchat):
				del QUIZ_IDLENESS[groupchat]
			result = '[QUIZ] Current Scores'
			for nick in QUIZ_SCORES[groupchat]:
				result += '\n' + nick + ': ' + str(QUIZ_SCORES[groupchat][nick])
			msg(groupchat, result)

def handler_quiz_start(type, source, parameters):
	groupchat = get_groupchat(source)
	if not groupchat:
		smsg(type, source, 'Not in groupchat.')
		return
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		smsg(type, source, 'Quiz already exists.')
		return
	QUIZ_SCORES[groupchat] = {}
	if QUIZ_IDLENESS.has_key(groupchat):
		del QUIZ_IDLENESS[groupchat]
	msg(groupchat, '[QUIZ] Quiz has begun. Scores reset.')
	quiz_ask_question(groupchat)

def handler_quiz_stop(type, source, parameters):
	groupchat = get_groupchat(source)
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		del QUIZ_CURRENT_ANSWER[groupchat]
		msg(groupchat, '[QUIZ] Quiz has ended.')
		quiz_list_scores(groupchat)
	else:
		smsg(type, source, 'No quiz to stop.')

def handler_quiz_hint(type, source, parameters):
	groupchat = get_groupchat(source)
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		if QUIZ_IDLENESS.has_key(groupchat):
			del QUIZ_IDLENESS[groupchat]
		if QUIZ_CURRENT_HINT[groupchat] == None:
			QUIZ_CURRENT_HINT[groupchat] = 0
			#msg(groupchat, '[QUIZ] Answer has ' + str(len(QUIZ_CURRENT_ANSWER[groupchat])) + ' letters.')
		QUIZ_CURRENT_HINT[groupchat] += 1
		hint = QUIZ_CURRENT_ANSWER[groupchat][0:QUIZ_CURRENT_HINT[groupchat]]
		hint += '...'
		#hint += ' _' * (len(QUIZ_CURRENT_ANSWER[groupchat]) - QUIZ_CURRENT_HINT[groupchat])
		msg(groupchat, '[QUIZ] Hint: ' + hint)
	else:
		smsg(type, source, 'No quiz exists.')

def handler_quiz_scores(type, source, parameters):
	groupchat = get_groupchat(source)
	if QUIZ_CURRENT_ANSWER.has_key(groupchat):
		quiz_list_scores(groupchat)
	else:
		smsg(type, source, 'No quiz exists.')

def handler_quiz_message(type, source, body):
	groupchat = get_groupchat(source)
	if groupchat and QUIZ_CURRENT_ANSWER.has_key(groupchat):
		quiz_answer_question(source[1], source[2], body.strip())

register_command_handler(handler_quiz_start, '!quiz_start', 0, 'Starts a quiz in the groupchat.', '!quiz_start', ['!quiz_start'])
register_command_handler(handler_quiz_stop, '!quiz_stop', 0, 'Stops a quiz in the groupchat.', '!quiz_stop', ['!quiz_stop'])
register_command_handler(handler_quiz_hint, '!hint', 0, 'Asks for a hint on the current quiz question.', '!hint', ['!hint'])
register_command_handler(handler_quiz_scores, '!quiz_scores', 0, 'Request scores for current quiz.', '!quiz_scores', ['!quiz_scores'])
register_message_handler(handler_quiz_message)
