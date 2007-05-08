#$ neutron_plugin 01
# -*- coding: koi8-u -*-

import urllib2,re,urllib

def handler_bashorg_get(type, source, parameters):
	if parameters.strip()=='':
		req = urllib2.Request('http://bash.org/?random')
	else:
		req = urllib2.Request('http://bash.org/?'+parameters.strip())
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	target=r.read()
	od=re.search('<p class="qt">',target)
	message=target[od.end():]
	message=message[:re.search('</p>',message).start()]
	message=message.replace('<br />','\n')
	message=re.sub("<[^<>]+>", "",message).replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
	message='\n' + message.strip()
	smsg(type,source,unicode(message,'windows-1251'))

def handler_bashorgru_get(type, source, parameters):
	if parameters.strip()=='':
		req = urllib2.Request('http://bash.org.ru/quote.php')
	else:
		req = urllib2.Request('http://bash.org.ru/quote.php?num='+parameters.strip())
	req.add_header = ('User-agent', 'Mozilla/5.0')
	try:
	    r = urllib2.urlopen(req)
	    target=r.read()
	    od=re.search('<td class="dat">',target)
	    message=target[od.end():]
	    message=message[:re.search('</td>',message).start()]
	    message=message.replace('<br>','\n')
	    message=re.sub("<[^<>]+>", "",message).replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
	    message='\n' + message.strip()
	    smsg(type,source,unicode(message,'windows-1251'))
	except:
	    smsg(type,source,unicode('Кончился интернет, всё, приехали... ','koi8-u'))

def handler_linuxorgru_get(type, source, parameters):
	req = urllib2.Request('http://linux.org.ru/index.jsp')
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	target=r.read()
	od=re.search('<hr noshade class="news-divider">',target)
	message=target[od.end():]
	message=message[:re.search('<div class=sign>',message).start()]
	message=message.replace('<br>','\n')
	message=re.sub("<[^<>]+>", "",message).replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
	message='\n' + message.strip()
	smsg(type,source,unicode(message,'koi8-r'))

def handler_pyorg_get(type, source, parameters):
	req = urllib2.Request('http://python.org')
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	target=r.read()
	od=re.search('<h2 class="news">',target)
	message=target[od.end():]
	message=message[:re.search('</div>',message).start()]
	message=message.replace('<br>','\n')
	message=re.sub("<[^<>]+>", "",message).replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
	message='\n' + message.strip()
	reply=''
	for line in message.split('\n'):
	    if line.strip():
		    reply += line + '\r\n'
	reply='\n' + reply	    
	smsg(type,source,unicode(reply,'koi8-r'))


def handler_bbc_get(type, source, parameters):
	req = urllib2.Request('http://news8.thdo.bbc.co.uk/low/russian/news/default.stm')
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	target=r.read()
	od=re.search('<a name="startcontent">',target)
	message=target[od.end():]
	message=message[:re.search('<hr>',message).start()]
	message=message.replace('<br>','\n')
	message=re.sub("<[^<>]+>", "",message).replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
	message=re.sub("^\s*?","",message).replace('\n','')
	message=message.replace('<br clear="all" /> ','\n')
	message='\n' + message.strip()
	reply=''
	for line in message.split('\n'):
	    if line.strip():
		    reply += line + '\r\n'
	smsg(type,source,unicode(reply,'windows-1251'))

#=======
def handler_linuxorgru_get(type, source, parameters):
	req = urllib2.Request('http://linux.org.ru/index.jsp')
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	target=r.read()
	od=re.search('<hr noshade class="news-divider">',target)
	message=target[od.end():]
	message=message[:re.search('<hr noshade class="news-divider">',message).start()]
	message=message.replace('<br>','\n')
	message=re.sub("<[^<>]+>", "",message).replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"')
	message='\n' + message.strip()
	smsg(type,source,unicode(message,'koi8-r'))


register_command_handler(handler_bashorg_get, '!bo', 0, 'Get quote from bash.org', '!bo', ['!bo 22'])
register_command_handler(handler_bashorg_get, '!bashorg', 0, 'Get quote from bash.org', '!bashorg', ['!bashorg 22'])
register_command_handler(handler_bashorgru_get, '!bor', 0, 'Get quote from bash.org.ru', '!bor', ['!bor 22'])
register_command_handler(handler_bashorgru_get, '!bashorgru', 0, 'Get quote from bash.org.ru', '!bashorgru', ['!bashorgru 22'])
register_command_handler(handler_linuxorgru_get, '!lor', 0, 'Get latest news post from linux.org.ru. Note: Parameters ignored.', '!lor', ['!lor 22'])
register_command_handler(handler_pyorg_get, '!pyorg', 0, 'Get latest news post from python.org. Note: Parameters ignored.', '!pyorg', ['!lor 22'])
register_command_handler(handler_bbc_get, '!bbc', 0, 'Get latest news post from BBC in Russian. Note: Parameters ignored.', '!bbc', ['!bbc 22'])