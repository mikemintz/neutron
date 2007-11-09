#$ neutron_plugin 01
# -*- coding: koi8-u -*-

import urllib2,re,urllib

from re import compile as re_compile

strip_tags = re_compile(r'<[^<>]+>')

def handler_bashorg_get(type, source, parameters):
    if parameters.strip():
        req = urllib2.Request('http://bash.org/?'+parameters.strip())
    else:
        req = urllib2.Request('http://bash.org/?random')
    req.add_header = ('User-agent', 'Mozilla/5.0')
    r = urllib2.urlopen(req)
    target = r.read()
    od = re.search('<p class="qt">',target)
    message = target[od.end():]
    message = message[:re.search('</p>',message).start()]
    message = decode(message)
    message='\n' + message.strip()
    smsg(type,source,unicode(message,'windows-1251'))

def handler_ukrbashorg_get(type, source, parameters):
    if parameters.strip()=='':
        req = urllib2.Request('http://ukrbash.org/random')
    else:
        req = urllib2.Request('http://ukrbash.org/quote/'+parameters.strip())
    req.add_header = ('User-agent', 'Mozilla/5.0')
    try:
	r = urllib2.urlopen(req)
	target = r.read()
	od = re.search('</div><div>',target)
	message = target[od.end():]
	message = message[:re.search('</div></div></div>',message).start()]
	message = decode(message)
	message = '\n' + message.strip()
	smsg(type,source,unicode(message,'utf-8'))
    except:
        smsg(type,source,unicode('Інтернету немає, торба, приїхали... ','koi8-u'))

def handler_bashorgru_get(type, source, parameters):
    if parameters.strip()=='':
        req = urllib2.Request('http://bash.org.ru/random')
    else:
        req = urllib2.Request('http://bash.org.ru/quote/'+parameters.strip())
    req.add_header = ('User-agent', 'Mozilla/5.0')
    try:
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<div>',target)
        message = target[od.end():]
        message = message[:re.search('</div>',message).start()]
        message = decode(message)
        message = '\n' + message.strip()
        smsg(type,source,unicode(message,'windows-1251'))
    except:
        smsg(type,source,unicode('Кончился интернет, всё, приехали... ','koi8-u'))

def handler_ostrie_get(type, source, parameters):
    if parameters.strip()=='':
        req = urllib2.Request('http://ostrie.moskva.com/?do=TopToday')
    else:
        req = urllib2.Request('http://ostrie.moskva.com/?do=Item&id='+parameters.strip())
    req.add_header = ('User-agent', 'Mozilla/5.0')
    try:
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<dd>',target)
        message = target[od.end():]
        message = message[:re.search('<div class="instr">',message).start()]
        message = decode(message)
        message = '\n' + message.strip()
        smsg(type,source,unicode(message,'koi8-r'))
    except:
        smsg(type,source,unicode('Кончился интернет, всё, приехали... ','koi8-u'))

def handler_irclv_get(type, source, parameters):
    if parameters.strip()=='':
        parameters = '105090'
    else:
	pass
    req = urllib2.Request('http://irc.lv/qna/view?question_id='+parameters.strip())
    req.add_header = ('User-agent', 'Mozilla/5.0')
    try:
        r = urllib2.urlopen(req)
        target = r.read()
        od = re.search('<div class="qtopic">',target)
        message = target[od.end():]
        message = message[:re.search('<div class="folders"><span class="topic">',message).start()]
        message = decode(message)
        message = '\n' + message.strip()
	question = message
	od = re.search('<span class="topic">',target)
        message = target[od.end():]
        message = message[:re.search('<span class="topic">',message).start()]
        message = decode(message)
        message = '\n' + message.strip()
	answer = message
	reply = question + '\n' + answer
        smsg(type,source,unicode(reply,'utf-8'))
    except:
	print printc(color_white, str(sys.exc_info()[0].__name__) + ' -- ' + str(sys.exc_info()[1]))
        smsg(type,source,unicode('Кончился интернет, всё, приехали... ','koi8-u'))

def handler_linuxorgru_get(type, source, parameters):
    req = urllib2.Request('http://linux.org.ru/index.jsp')
    req.add_header = ('User-agent', 'Mozilla/5.0')
    r = urllib2.urlopen(req)
    target = r.read()
    od = re.search('<hr noshade class="news-divider">',target)
    message = target[od.end():]
    message = message[:re.search('<div class=sign>',message).start()]
    message = decode(message)
    message = '\n' + message.strip()
    smsg(type,source,unicode(message,'koi8-r'))

def handler_pyorg_get(type, source, parameters):
    req = urllib2.Request('http://python.org')
    req.add_header = ('User-agent', 'Mozilla/5.0')
    r = urllib2.urlopen(req)
    target = r.read()
    od = re.search('<h2 class="news">',target)
    message = target[od.end():]
    message = message[:re.search('</div>',message).start()]
    message = decode(message)
    message = '\n' + message.strip()
    reply = ''
    for line in message.split('\n'):
        if line.strip():
            reply += line + '\r\n'
    reply='\n' + reply	    
    smsg(type,source,unicode(reply,'koi8-r'))


def handler_bbc_get(type, source, parameters):
    req = urllib2.Request('http://news8.thdo.bbc.co.uk/low/russian/news/default.stm')
    req.add_header = ('User-agent', 'Mozilla/5.0')
    r = urllib2.urlopen(req)
    target = r.read()
    od = re.search('<a name="startcontent">',target)
    message = target[od.end():]
    message = message[:re.search('<hr>',message).start()]
    message = decode(message)
    message = re.sub("^\s*?","",message).replace('\n','')
    message = message.replace('<br clear="all" /> ','\n')
    message = '\n' + message.strip()
    reply = ''
    for line in message.split('\n'):
        if line.strip():
            reply += line + '\r\n'
    smsg(type,source,unicode(reply,'windows-1251'))

#=======
def handler_linuxorgru_get(type, source, parameters):
    req = urllib2.Request('http://linux.org.ru/index.jsp')
    req.add_header = ('User-agent', 'Mozilla/5.0')
    r = urllib2.urlopen(req)
    target = r.read()
    od = re.search('<hr noshade class="news-divider">',target)
    message = target[od.end():]
    message = message[:re.search('<hr noshade class="news-divider">',message).start()]
    message = decode(message)
    message = '\n' + message.strip()
    smsg(type, source, unicode(message, 'koi8-r'))

def handler_2ipru_get(type, source, parameters):
    if parameters.strip()=='':
	smsg(type, source, 'Empty Input')
	return
    else:
	parameters = parameters.strip()
	if len(parameters)>15:
			smsg(type, source, 'Wrong format')
			return
	postData = urllib.urlencode({'ip':parameters,'parse':'поиск'})
        req2 = urllib2.Request('http://2ip.ru/server.php',postData)
	req2.add_header = ('User-agent', 'Mozilla/5.0')
        try:
    	    r = urllib2.urlopen(req2)
    	    target = r.read()
    	    od = re.search('<br>-----------------------<br>',target)
    	    message = target[od.end():]
    	    message = message[:re.search('<br><br><br><br>',message).start()]
    	    message = decode(message)
	    if len(message) != 0:
    		message = '\n' + message.strip()
	    else:
		message = 'Ooops. Nothing ;-)'
    	    smsg(type,source,unicode(message,'windows-1251'))
        except:
    	    smsg(type,source,unicode('Кончился интернет, всё, приехали... ','koi8-u'))

def decode(text):
    data = text.replace('<br>','\n').replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('<br />','\n').replace('<li>','\r\n')
    return strip_tags.sub('', data)

#
register_command_handler(handler_2ipru_get, '!2ip', 0, 'Get ip info from 2ip.ru', '!2ip', ['!2ip 22.32.42.53'])
#
register_command_handler(handler_bashorg_get, '!bo', 0, 'Get quote from bash.org', '!bo', ['!bo 22'])
register_command_handler(handler_bashorg_get, '!bashorg', 0, 'Get quote from bash.org', '!bashorg', ['!bashorg 22'])
#
register_command_handler(handler_ukrbashorg_get, '!ubo', 0, 'Get quote from ukrbash.org', '!ubo', ['!ubo 22'])
register_command_handler(handler_ukrbashorg_get, '!ukrbashorg', 0, 'Get quote from ukrbash.org', '!ukrbashorg', ['!ukrbashorg 22'])
#
register_command_handler(handler_bashorgru_get, '!bor', 0, 'Get quote from bash.org.ru', '!bor', ['!bor 22'])
register_command_handler(handler_bashorgru_get, '!bashorgru', 0, 'Get quote from bash.org.ru', '!bashorgru', ['!bashorgru 22'])
#
register_command_handler(handler_irclv_get, '!irclv', 0, 'Get quote from irc.lv', '!irclv', ['!irclv 105005'])
register_command_handler(handler_ostrie_get, '!ost', 0, 'Get quote from ostrie.ru', '!ost', ['!ost 838923'])
register_command_handler(handler_linuxorgru_get, '!lor', 0, 'Get latest news post from linux.org.ru. Note: Parameters ignored.', '!lor', ['!lor 22'])
register_command_handler(handler_pyorg_get, '!pyorg', 0, 'Get latest news post from python.org. Note: Parameters ignored.', '!pyorg', ['!lor 22'])
register_command_handler(handler_bbc_get, '!bbc', 0, 'Get latest news post from BBC in Russian. Note: Parameters ignored.', '!bbc', ['!bbc 22'])
