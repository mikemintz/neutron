#$ neutron_plugin 01

import urllib

QUOTE_FILE = 'static/quotes.txt'

def handler_quote_quote(type, source, parameters):
	reply = random.choice(open(QUOTE_FILE, 'r').readlines()).strip()
	smsg(type, source, reply)

def handler_quote_fortune(type, source, parameters):
	# Requires *nix and fortune installed
	handler_python_sh(type, source, "fortune")

register_command_handler(handler_quote_fortune, '!fortune', 0, 'Gives a random fortune.', '!fortune', ['!fortune'])
register_command_handler(handler_quote_quote, '!quote', 0, 'Gives a random quote.', '!quote', ['!quote'])
