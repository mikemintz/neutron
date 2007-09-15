#$ neutron_plugin 01
# Authors: Psi (\u03a8) AKA Ctac & Gh0st AKA Bohdan Turkynewych, 2006-2007

import re

def is_palindrome(phrase):
	reply = ''
	spaceless = re.sub('(\!|\.|\,|\_|\-|\ |\n|\'|\"|\`)', '', phrase)
	if spaceless == spaceless[::-1]:
		reply += '\n' + """Phrase "%s" *is* a palindrome"""%phrase
	else:
		reply += '\n' + """Phrase "%s" is *not* a palindrome"""%phrase
	return reply

def palindrome_handler(type, source, parameters):
	    parameters = parameters.strip()
	    if parameters:
		    smsg(type, source, is_palindrome(parameters))
	    else:
		    smsg(type, source, 'Empty input ignored.')

register_command_handler(palindrome_handler, '!palindrome', 0, 'Tests phrase if it is a palindrome', '!palindrome', ['!palindrome'])