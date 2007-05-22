
    Neutron - a Jabber bot in Python
    --------------------------------

     Copyright 2002-2007 Mike Mintz   http://www.mikemintz.com/

     http://ejabberd.jabber.ru/neutron


    Introduction
    ------------

Neutron is a plugin-based Jabber bot written in Python that provides
functionalities for individuals and chatrooms. To use it, you only need
to create an account on a Jabber server, configure Neutron to log into
that account and start it. Neutron will allow users to subscribe to its 
presence, enter into chatrooms and answer to commands.


    Install
    -------

1. Get the source code from the SVN repository
svn checkout http://svn.hypothetic.org/neutron/trunk neutron

2. Prepare permissions (optional)
addgroup jabber
adduser neutron
adduser neutron jabber
chown neutron:jabber neutron-0.5 -R
chmod 750 neutron-0.5 -R

cd neutron

3. Configure
Edit config.txt and put the username, server and password of the Jabber
account where Neutron must login.

4. Execute
./neutron.py

5. Execute as different user in daemon mode (optional)
su neutron -c "./neutron.py &"


    Directory structure
    -------------------

# Directories
chatlogs  Chatroom logs in HTML format
dynamic   Files automatically generated
localized Localized plugins: copy them to 'plugins/' to enable them
modules   Python modules required to run Neutron and plugins
plugins   Plugins that extend Neutron functionalities
private   Logs of private chats
static    Files with static data

# Files
neutron.py             Neutron executable
neutron.cfg            Main configuration file
neutron.rc             Init script with commands to execute on initialization
dynamic/chatrooms.cfg  List of chatrooms where Neutron will enter
dynamic/log.txt        Log of all XMPP traffic (does not work)


    Plugins
    -------

# Bot
access   Gives access to admin privileges
admin    Commands to administer Neutron 
chat
help     Shows help
log      Logs private chats, chatrooms and debug info
python   Evaluates a Python expression, statement or shell command

# Jabber related
presence Allows contacts to subscribe to its presence
sg       Asks a server its statistics
userinfo Gives information on JIDs

# Chatrooms
chatbot  Joins a chatroom and speaks to Chatbot (useless)
eliza    Talks with chat participants (uses Eliza)
rss      Subscribes a chatroom to a RSS feed
vote     Polls

# Utilities
query       Create word definitions and stores in file 
temperature Converts temperatures to and from C and F
time        Gives UTC and Internet time

# Reads database
quote    Gives a random quote or fortune

# Asks Internet
babel    Translate between languages [babelfish]
dict     Shows the DICT definition of a word
dns      Returns the DNS lookup for a host or IP address
domain   Returns information on specified domain
google   Performs a Google search. Set your Google key on modules/googlekey.txt
stock    Returns information on stock [yahoo]
weather  Shows weather from NOAA

# Local plugins
  Czech:
idos     Searches IDOS for direct connection between two places in Czech Republic
kino     Returns list of movies in cinemas for given city in Czech Rep.
lamer    Shows random message from www.lamer.cz
tv       Returns TV programme for one of supported channels
  Other:
update   Updates Neutron from Internet (does not work)
  Russian:
bashorg  Gives random quotes from bash.org / bash.org.ru  / linux.org.ru / python.org
tv	 Returns TV programme for one of supported channels
quiz     Quiz in chatroom (requires quizdata.txt)
  Spanish:
saluda   It's a modification of quote plugin (requires saludos.txt and saludos2.txt)
  USA:
fact-usa Shows info in Area code and ZIP code (requires areacodes.txt and zipcodes.txt)


    Start using it
    --------------

Now that Neutron is logged on his account in a Jabber server, you can add it
to your roster and start to chat with him. Some example commands:
  help
  !commands
  help !domain
  !domain jabber.org
  help !join


    RSS plugin
    ----------

1. Add a RSS feed to Neutron:
	!rss_add identifier link
	!rss_add planetjab http://planet.jabber.org/rss10.xml
2. Subscribe room to it:
	!rss_subscribe identifier room
	!rss_subscribe planetjab group@conference.jabber.no 
3. Finally start the RSS fetching loop::
	!rss_start 


    Feature Requests
    ----------------

# help_plugin
- !commands should show only commands that the user has privileges enought to use

- Give helpful error on invalid username/password for initial login
