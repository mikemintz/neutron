#$ neutron_plugin 01
import urllib2,re,time
def prog_grab(code):
	kody={'ct1':'%C8T1', 'ct2':'%C8T2', 'nova':'Nova', 'prima':'Prima', 'hbo':'HBO', 'hbo2':'HBO2', 'csfilm':'%C8S+Film', 'filmplus':'Film%2B', 'cinemax':'Cinemax', 'hallmark':'Hallmark', 'galaxiesport':'Galaxie+Sport', 'eurosport':'EuroSport', 'eurosport2':'EuroSport2', 'ct24':'%C8T24', '24cz':'24cz', 'jetix':'Jetix', 'minimax':'Minimax', 'animeplus':'Anime%2B', 'spektrum':'Spektrum', 'discovery':'Discovery', 'animalplanet':'AnimalPlanet', 'nationalgeographic':'National+Geographic', 'viasatexplorer':'Viasat+Explorer', 'viasathistory':'Viasat+History', 'realitytv':'Reality+TV', 'axn':'AXN', 'romantica':'Romantica', 'ocko':'%D3%E8ko', 'tvpaprika':'TV+Paprika', 'markiza':'Mark%EDza', 'joj':'JOJ', 'stv1':'STV1', 'stv2':'STV2', 'ta3':'TA3', 'tvp1':'TVP1', 'tvp2':'TVP2', 'polonia':'Polonia', 'tvn':'TVN', 'tvn7':'TVN7', 'polsat':'Polsat', 'tv4':'TV4', 'rtl2':'RTL2', 'kabel1':'Kabel1', 'superrtl':'SuperRTL', 'pro7':'PRO7', 'sat1':'SAT1', '3sat':'3SAT', 'orf1':'ORF1', 'orf2':'ORF2', 'ard':'ARD', 'dsf':'DSF', 'vox':'VOX', 'zdf':'ZDF', 'viva':'VIVA', 'viva+':'VIVA%2B', 'mtv':'MTV', 'mtv2':'MTV2', 'mtvbase':'MTV+Base', 'mtvhits':'MTV+Hits', 'vh1':'VH1', 'vh1classic':'VH1+Classic', 'cartoon-network':'Cartoon+Network', 'boomerang':'Boomerang', 'tcm':'TCM', 'club':'&apos;Club', 'bbcprime':'BBC+Prime', 'espn-classic-sport':'ESPN+Classic+Sport', 'extreme':'Extreme', 'privateblue':'Private+Blue', 'privategold':'Private+Gold', 'cnn':'CNN', 'mezzo':'Mezzo'}
	if code.lower() in kody.keys():
		kod=kody[code.lower()]
		req = urllib2.Request('http://365dni.sms.cz/index.php?typ=televize&formular_datum=&formular_casod=&formular_typprg=&televize_tvarray='+kod)
		r = urllib2.urlopen(req)
		radky=r.readlines()
		program=''
		porad0_0={}
		porad_od0_0={}
		for x in radky:
			if x.find('porad0_0[0] = ')!=-1:
				program=x
		kusy=program.split(';')
		for x in kusy:
			prikaz=x.replace('\\"',"").replace("'","")
			prikaz=re.sub('</.*>','',prikaz)
			prikaz=re.sub('<.*>','',prikaz)
			#print prikaz
			if prikaz.strip()!='':
				exec(prikaz)
		# toz a vcil muzem zformatovat vystup ..
		n=range(0,len(porad0_0))
		vystup='\n'
		for x in n:
			vystup+=time.strftime('%H:%M',time.localtime((porad_od0_0[x])/1000))+' - '+porad0_0[x]+'\n'
		return vystup	
	else:
		vystup='Channels: \n'
		kanaly=kody.keys()
		kanaly.sort()
		for x in kanaly:
			vystup+=x+ ' '
		return vystup


def handler_TV_get(type, source, parameters):
	smsg(type,source,unicode(prog_grab(parameters),'windows-1250'))
	

register_command_handler(handler_TV_get, '!tv', 0, 'Returns TV program for given channel.', '!tv <channel>', ['!tv ct1'])
