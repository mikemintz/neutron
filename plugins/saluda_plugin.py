#$ neutron_plugin 01

# Neutron plugin; spanish localized
# Author: Badlop
# Last Revision: 18 sept 2004

import codecs

SALUDOS_FILE = 'static/saludos.txt'
SALUDOS2_FILE = 'static/saludos2.txt'

def handler_quote_quote(type, source, parameters):
	reply = random.choice(codecs.open(SALUDOS_FILE, 'r', 'latin1').readlines()).strip()
	#smsg(type, source, reply)
	msg(source[1], reply)

def handler_quote_quote2(type, source, parameters):
	reply = random.choice(codecs.open(SALUDOS2_FILE, 'r', 'utf-8').readlines()).strip()
	#smsg(type, source, reply)
	msg(source[1], reply)

def handler_quote_gracias(type, source, parameters):
	smsg(type, source, 'de nada')

register_command_handler(handler_quote_gracias, 'gracias', 0, '', '', [''])

register_command_handler(handler_quote_quote, 'Hola', 0, 'Saluda', 'hola', ['hola'])
register_command_handler(handler_quote_quote, 'hola', 0, 'Saluda', 'hola', ['hola'])
register_command_handler(handler_quote_quote, 're', 0, 'Saluda', 'hola', ['hola'])
register_command_handler(handler_quote_quote, 'Buenas', 0, 'Saluda', 'hola', ['hola'])
register_command_handler(handler_quote_quote, 'buenas', 0, 'Saluda', 'hola', ['hola'])
register_command_handler(handler_quote_quote, 'nas', 0, 'Saluda', 'hola', ['hola'])

register_command_handler(handler_quote_quote2, 'Adios', 0, 'Despide', 'Adios', ['Adios'])
register_command_handler(handler_quote_quote2, 'deu', 0, 'Despide', 'Adios', ['Adios'])
register_command_handler(handler_quote_quote2, 'talue', 0, 'Despide', 'Adios', ['Adios'])
register_command_handler(handler_quote_quote2, 'taluego', 0, 'Despide', 'Adios', ['Adios'])

