#$ neutron_plugin 01
import urllib2,re,urllib
def kino_grab(vstup):
	
##	req = urllib2.Request('http://dokina.tiscali.cz/')
##	req.add_header = ('User-agent', 'Mozilla/5.0')
##	r = urllib2.urlopen(req)
##	cele=r.read()
##	#ripnem z toho seznam mest
##	m=re.search('<select name="city" size="1" class="programcombo">',cele)
##	mesta=cele[m.end():]
##	mesta=mesta[:re.search('<option value="0">',mesta).start()]
##	m_kusy=re.findall('<option value="\d+">[^\d<]+</option>',mesta)
##	slovnik={}
##	for i in m_kusy:
##		mesto=re.sub("<[^<>]+>", "",i)
##		cislo=re.search('\d+',i)
##		slovnik[mesto]=cislo.group()
##	print slovnik
	slovnik={'turnov': '189', 'kralupy-nad-vltavou': '116', 'uherske-hradiste': '16', 'jihlava': '26', 'znojmo': '125', 'pernink': '155', 'horsovsky-tyn': '158', 'ceske-budejovice': '3', 'sezimovo-usti': '120', 'opava': '20', 'zlin': '68', 'kamenicky-senov': '187', 'caslav': '153', 'blatna': '140', 'havlickuv-brod': '119', 'tabor': '5', 'hradec-kralove': '14', 'holesov': '28', 'klatovy': '166', 'vyskov': '131', 'hermanuv-mestec': '157', 'cernosice': '185', 'kutna-hora': '151', 'slany': '148', 'karlovy-vary': '67', 'frydek-mistek': '35', 'lysa-nad-labem': '114', 'veseli-nad-moravou': '179', 'pelhrimov': '39', 'tyn-nad-vltavou': '115', 'novy-bor': '169', 'prostejov': '121', 'ceska-lipa': '152', 'plana': '188', 'boskovice': '171', 'cheb': '149', 'jablonec-nad-nisou': '143', 'chrudim': '127', 'brno': '2', 'olomouc': '9', 'mnichovo-hradiste': '32', 'chomutov': '128', 'horovice': '159', 'jesenik': '113', 'beroun': '132', 'pardubice': '117', 'orlova': '191', 'kladno': '112', 'usti-nad-orlici': '18', 'kdyne': '12', 'dobrany': '177', 'humpolec': '150', 'prerov': '23', 'nymburk': '144', 'novy-jicin': '126', 'litomerice': '129', 'kolin': '130', 'blansko': '123', 'trebic': '19', 'sebetov': '10', 'cesky-krumlov': '6', 'straz-pod-ralskem': '183', 'ostrava': '8', 'kromeriz': '21', 'trest': '176', 'ostrov': '167', 'liberec': '147', 'uhersky-brod': '40', 'usti-nadlabem': '66', 'sumperk': '17', 'strakonice': '146', 'neratovice': '182', 'frystak': '175', 'praha': '1', 'decin': '162', 'pisek': '118', 'litomysl': '37', 'teplice': '124', 'karvina': '34', 'plzen': '7', 'havirov': '111', 'holice': '141', 'jilemnice': '173', 'koprivnice': '170'}

	
	tajm={'dnes':1,'zitra':2,'tyden':3, 'vikend':4,'mesic':5}
	
	par=vstup.split()
	if len(par)==1:
		par.append('dnes')
	if len(vstup.split())==0:
		klice=slovnik.keys()
		klice.sort()
		out='\n MESTA: \n'
		for i in klice:
			out+=' '+i
		out+='\n OBDOBI: \n'
		for i in tajm.keys():
			out+=' '+i
		return out
	elif par[0] in slovnik.keys() and par[1].lower() in tajm.keys():
		mesto=slovnik[par[0]]
		cas=tajm[par[1].lower()]
	else:
		return 'Chybny dotaz.'
	
	
	req = urllib2.Request('http://dokina.tiscali.cz/programy/program.asp?city='+str(mesto)+'&where_search=movie1&movie=&term='+str(cas)+'&order=cinema&filtr=0&multikino=true')
	req.add_header = ('User-agent', 'Mozilla/5.0')
	r = urllib2.urlopen(req)
	cele=r.read()
	
	od=re.search('<table border="0" width="100%" cellspacing="0" cellpadding="2"><tr><td colspan="4">&nbsp;</td></tr>',cele)
	vysledek=cele[od.end():]
	vysledek=vysledek[:re.search('</table><hr size="1">',vysledek).start()]
	kina_mass=vysledek.split('<table border="0" width="100%" cellspacing="0" cellpadding="0"><tr><td>')
	kina_mass=kina_mass[1:]
	out='\n'
	for f in kina_mass:
		kino=re.search('<a class="kinoprogram" href="/programy/showcinema.asp.id=\d+">.+</a></b></font><br>',f)
		data=re.findall('<strong>.+</strong>&nbsp;</td>',f)
		filmy=re.findall('<a class="kinoprogramdef" href="/filmy/f_info.asp.film_id=\d+">.+</a>',f)
		casy=re.findall('<strong>.+ h</strong></td>',f)
		out+=re.sub("<[^<>]+>", "",kino.group())+'\n'
		program=[]
		if len(data)==len(filmy) and len(data)==len(casy):
			for x in range(0,len(filmy)):
				text=re.sub("<[^<>]+>", "",data[x])+'\t: '+re.sub("<[^<>]+>", "",filmy[x])+ ' ('+re.sub("<[^<>]+>", "",casy[x])+')'
				program.append(text.replace('&nbsp;',' '))
				out+=text.replace('&nbsp;',' ')+'\n'
			#print program
		else:
			hlaska=re.search('<tr><td colspan="2" class="kinoprogramdef">.+</td></tr>',f)
			out+=re.sub("<[^<>]+>", "",hlaska.group())+'\n'
	return out
	
def handler_kino_get(type, source, parameters):
	
	smsg(type,source,unicode(kino_grab(parameters),'windows-1250'))
	
register_command_handler(handler_kino_get, '!kino', 0, 'Vypise program kin ve zvolenem meste a obdobi.', '!kino <mesto> <kdy>', ['!kino 8 1'])
