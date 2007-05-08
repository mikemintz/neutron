#$ neutron_plugin 01

import urllib2,re,time
def prog_grab(code):
	
		kod=code.lower()
		req = urllib2.Request('http://tv.yandex.ru/?mode=print&channel='+kod)
		r = urllib2.urlopen(req)
		radky=r.readlines()
                program =""
		for x in radky:
			if x.find('<div>')!=-1:
			  if re.search('<.*?>\d',x):
			     program+="\n"+re.sub(r'<.*?>','',x).replace("\n",'')
			   
                return program

def prog_list():
	
		req = urllib2.Request('http://tv.yandex.ru/')
		r = urllib2.urlopen(req)
		radky=r.readlines()
                program ="\n"	
		for x in radky:
			if x.find('<option value="')!=-1:
			     program+=re.sub('\xa0','',re.sub('/s*','',re.sub(r'</.*?>','',x)).replace('">','-').replace('<option value="','').replace("\n",'').replace("\t",'').replace("\r",''))+", "		   
                return program


def handler_TV_get(type, source, parameters):
	smsg(type,source,unicode(prog_grab(parameters),'windows-1251'))
def handler_TV_list(type, source, parameters):
	smsg(type,source,unicode(prog_list(),'windows-1251'))	
	

register_command_handler(handler_TV_get, '!tv', 0, 'Returns TV program for given channel.', '!tv <channel>', ['!tv ct1'])
register_command_handler(handler_TV_list, '!tv_list', 0, 'Returns TV program for given channel.', '!tv_list', ['!tv_list'])
