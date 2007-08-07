#$ neutron_plugin 01


from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr


class TestBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        self.do_command(e, e.arguments()[0])

    def on_pubmsg(self, c, e):
        a = e.arguments()[0].split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def on_dccmsg(self, c, e):
        c.privmsg("You said: " + e.arguments()[0])

    def on_dccchat(self, c, e):
        if len(e.arguments()) != 2:
            return
        args = e.arguments()[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def sirc(self, type, e, cmd):
    	nick = nm_to_n(e.source())
    	c = self.connection
	c.privmsg(nick, nick + cmd)
    
    def do_command(self, e, cmd):
        nick = nm_to_n(e.source())
        c = self.connection
	#c.privmsg(nick, nick + cmd)
	call_message_handlers('privirc', nick, cmd)
	if cmd in COMMANDS:
		c.privmsg(nick, nick +': Found command: ' +  cmd)
		call_command_handlers(cmd, 'privirc', nick, '')
		c.privmsg(nick, IRC_MESSAGE)
    

def sirc(type,source,parameters):
	IRC_MESSAGE = parameters

def main():

    import sys
    global TestBot
    port = 6667
    channel = '#botzone'
    nickname = 'Neutron!'
    server = 'irc.someserver.net'

    bot = TestBot(channel, nickname, server, port)
    # Uncomment this... it still does not work correctly...
    # thread.start_new(bot.start,())

if __name__ == "__main__":
    main()
