#$ neutron_plugin 01

import time

def IDOS(prvni,druha,datum,cas):
	import urllib2,re,urllib
	
	con=urllib2.Request('http://idos.cz/ConnForm.asp?tt=c')
	link=urllib2.urlopen(con)
	form=link.read()
	code=re.search('name=\"link\" value=\"',form)
	kod=form[code.end():code.end()+4]
	
	req = urllib2.Request('http://idos.cz/ConnForm.asp?tt=c')
	req.add_header = ('User-agent', 'Mozilla/5.0')
	req.add_data(urllib.urlencode({'FromStn':urllib.quote(prvni),'ToStn':urllib.quote(druha),'ViaStn':'','ConnDate':datum,'ConnTime':cas,'ConnIsDep':'1','ConnAlg':'0','tt':'c','changeext':'0','Mask1':'-1','Min1':'5','Max1':'240','Std1':'1','Mask2':"-1",'Min2':"0","Max2":"240","Std2":"0","beds":"0","alg": "1","chn":"5","odch":"50","odcht":"0","ConnFromList":"-1","ConnToList":"-1","ConnViaList":"-1","recalc":"0","pars":"0","process":"0","link":kod}))
	r = urllib2.urlopen(req)
	cele=r.read()
	#print cele
	zacatek=re.search('<table border=.0. width=.100%. cellspacing=.0. cellpadding=.0. Class=.TDForm.>',cele)
	if zacatek!=None:
		kus_1=cele[zacatek.end():]
		kus_2=kus_1[re.search('</table>',kus_1).end():]
		telo=kus_2[:re.search('</table>',kus_2).start()]
		out_date=re.findall('<td align="right">([0-9]{0,2}\.[0-9]{0,2}\.)',telo)
		out_st=re.findall('<td nowrap>(((<a [^<>]*>)?[^<>]+(</a>)?.+<br>)+.+)</td>',telo)
		out_arrivs=re.findall('<td align="right" nowrap>(&#160;)*(((<br>&#160;)*<br>[0-9]{0,2}:[0-9]{0,2})+)</td>',telo)
		out_departs=re.findall('<td align="right">((([0-9]{0,2}:[0-9]{0,2})<br>(&#160;<br>)*)+)</td>',telo)
		out_nrs=re.findall("(<img [^<>]+>&nbsp;(<a href='Route\.asp\?cl=C&tt=.&i=[^<>]+>)?([^<>]+)(</a>)?(&nbsp;)*(<img [^<>]+>( )*)*(<br>)?)+",telo)
		#print out_arrivs,out_date,out_departs,out_nrs,out_st
		
		nrs=[]
		for i in out_nrs:
			o=re.sub("<[^<>]+>", "",i[0])
			o=re.sub("&nbsp;", "",o)
			nrs.append(o)
		
		
		arrivs=[]
		for i in out_arrivs:
			o=re.sub('<br>','',i[1])
			arrivs.append(o)
		
		
		departs=[]
		for i in out_departs:
			o=re.sub('<br>','',i[1])
			departs.append(o)	
		
		
		st=[]
		for i in out_st:
			o=[]
			stanice=i[0].split('<br>')
			o.append(re.sub("<[^<>]+>", "",stanice[0]).replace('&nbsp;',''))
			o.append(re.sub("<[^<>]+>", "",stanice[1]).replace('&nbsp;',''))
			st.append(o)
	
		#print arrivs,departs,nrs,st
		
		vysl=len(nrs)
		out=''
		for n in range(0,vysl):
			out+='\n'+st[n][0]+'('+departs[n]+') - '+st[n][1]+'('+arrivs[n]+')'
		return out
	else:
		if cele.find('vyberte ze seznamu objekt')!=-1:
			kus=cele[re.search('<select name=\"ToStn\" size=\"1\">',cele).end():]
			kus=kus[:re.search('</select>',kus).start()]
			kus=re.sub("<[^<>]+>", "",kus)
			mista=kus.split()
			mista=mista[0,-1]
			out='Vyberte stanici ze seznamu:'
			for x in mista:
				out+='\n'+x
			return out
		else:
			return 'CHYBA! >> spojeni nelze nalezt/spatny pozadavek'
			print cele

def handler_IDOS_get(type, source, parameters):
	par=parameters.split('*')
	if len(par)==2:
		
		datum=time.localtime()
		par.append(str(datum[2])+'.'+str(datum[1])+'.'+str(datum[0]))
		par.append(str(datum[3])+':'+str(datum[4]))
	elif len(par)==3:
		par.append(str(datum[3])+':'+str(datum[4]))
	smsg(type,source,unicode(IDOS(par[0],par[1],par[2],par[3]),'windows-1250'))
	

register_command_handler(handler_IDOS_get, '!spoj', 0, '', '!spoj <odkud>*<kam>*<datum>*<cas>', ['!spoj praha*ostrava*3.3.2006*10:21'])
