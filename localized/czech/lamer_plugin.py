#$ neutron_plugin 01
import urllib2,re,urllib

def handler_lamer_get(type, source, parameters):
	if parameters.strip()=='':
		req = urllib2.Request('http://lamer.cz/?item=show&action=random')
	else:
		req = urllib2.Request('http://lamer.cz/?item=show&id='+parameters.strip())
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	cele=r.read()
	od=re.search('<div id="quotes">',cele)
	hlaska=cele[od.end():]
	hlaska=hlaska[:re.search('</div>',hlaska).start()]
	hlaska=hlaska.replace('<br />','\n')
	hlaska=re.sub("<[^<>]+>", "",hlaska).replace('&nbsp;',' ').replace('&lt;','<').replace('&gt;','>')
	smsg(type,source,unicode(hlaska,'windows-1250'))

register_command_handler(handler_lamer_get, '!lamer', 0, 'Vypise hlasku z lamer.cz', '!lamer', ['!lamer 22'])
