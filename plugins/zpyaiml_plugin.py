#$ neutron_plugin 01

import string
import aiml
from string import *

def load_aiml():
    global k
    # The Kernel object is the public interface to
    # the AIML interpreter.
    k = aiml.Kernel()

    # Use the 'learn' method to load the contents
    # of an AIML file into the Kernel.
    k.learn("modules/standard/std-startup.xml")

    # Use the 'respond' method to compute the response
    # to a user's input string.  respond() returns
    # the interpreter's response, which in this case
    # we ignore.
    k.respond("load aiml b")

def chat_pyaiml(type, source, body):
    reply = k.respond(body)
    smsg(type, source, reply)
    
def handler_pyaiml(type, source, body):
    if type == 'private':
		if not COMMANDS.has_key(string.split(body)[0]):
			chat_pyaiml(type, source, body)
    if type == 'public' and get_nick(source[1])!=source[2] and source[2]!='' and re.search('^'+get_nick(source[1])+':',body)!=None:
		if not COMMANDS.has_key(string.split(body)[0]):
			chat_pyaiml(type, source, body.replace(get_nick(source[1])+':','').strip())
			

# Uncomment this if you want PyAIML support.
# Note: sessions are still not implemented.
#register_message_handler(handler_pyaiml)

if __name__ == "__main__":
	#load_aiml()
	pass
