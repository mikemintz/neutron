#! /usr/bin/python --

"""
usage: %(progname)s [domain...]

Version: %(version)s

Contacts the apropriate whois database for each domain and displays
the result.

class WhoisRecord:
	self.domain			 -- Domain Name
	self.whoisserver		-- Whoisserver associated with domain
	self.page			   -- raw whois record data

	public methods:
		
		def WhoisRecord(domain=None)
			Whois object constructor
			
		def whois(domainname=None, server=None, cache=0)
			Fetches whoisrecord and places result in self.page
			Raises NoSuchDomain if the domain doesn't exist.
		
		
class DomainRecord(WhoisRecord):
	self.domainid		   -- domainid for this domain
	self.created			-- date in which the domain was created
	self.lastupdated		-- date in which the domain was last updated.
	self.expires			-- date in which the domain expires
	self.databaseupdated	-- date in which the database was last updated.
	self.servers			-- list of (hostname, ip) pairs of the nameservers. 
	self.registrant		 -- ContactRecord of domain owner. 
	self.contacts		   -- dictionary of contacts (ContactRecord objects)

	public methods:
		
	def DomainRecord(domain=None)
		Constructor for DomainRecord
		
	def Parse()
		Creates a parsed version of the information contained in 
		the whois record for domain from self.page
		raises NoParser if a parser does not exist for a registry.


	
class Contact:
	self.type			   -- Type of contact
	self.organization	   -- Organization associated with contact.
	self.person			 -- Person associated with contact.
	self.handle			 -- NIC Handle
	self.address			-- Street address of contact
	self.email			  -- Email address of contact
	self.phone			  -- Phone Number
	self.fax				-- Fax Number
	self.lastupdated		-- Last update of contact record
"""

_version = "1.1"

import os, sys, string, time, getopt, socket, select, re, errno, copy, signal


timeout=5

class WhoisRecord:	  
	
	defaultserver='whois.networksolutions.com'
	whoismap={ 'com' : 'whois.internic.net' , \
			   'org' : 'whois.internic.net' , \
			   'net' : 'whois.internic.net' , \
			   'edu' : 'whois.networksolutions.com' , \
			   'de'  : 'whois.denic.de' , \
			   'gov' : 'whois.nic.gov' , \
			   # See http://www.nic.gov/cgi-bin/whois 
			   'mil' : 'whois.nic.mil' , \
			   # See http://www.nic.mil/cgi-bin/whois
			   'ca'  : 'whois.cdnnet.ca' , \
			   'uk'  : 'whois.nic.uk' , \
			   'au'  : 'whois.aunic.net' , \
			   'hu'  : 'whois.nic.hu' , \
			   
			   # All the following are unverified/checked. 
			   'be'  : 'whois.ripe.net',
			   'it'  : 'whois.ripe.net' , \
			   # also whois.nic.it
			   'at'  : 'whois.ripe.net' , \
			   # also www.nic.at, whois.aco.net
			   'dk'  : 'whois.ripe.net' , \
			   'fo'  : 'whois.ripe.net' , \
			   'lt'  : 'whois.ripe.net' , \
			   'no'  : 'whois.ripe.net' , \
			   'sj'  : 'whois.ripe.net' , \
			   'sk'  : 'whois.ripe.net' , \
			   'tr'  : 'whois.ripe.net' , \
			   # also whois.metu.edu.tr
			   'il'  : 'whois.ripe.net' , \
			   'bv'  : 'whois.ripe.net' , \
			   'se'  : 'whois.nic-se.se' , \
			   'br'  : 'whois.nic.br' , \
			   # a.k.a. whois.fapesp.br?
			   'fr'  : 'whois.nic.fr' , \
			   'sg'  : 'whois.nic.net.sg' , \
			   'hm'  : 'whois.registry.hm' , \
			   # see also whois.nic.hm
			   'nz'  : 'domainz.waikato.ac.nz' , \
			   'nl'  : 'whois.domain-registry.nl' , \
			   # RIPE also handles other countries
			   # See  http://www.ripe.net/info/ncc/rir-areas.html
			   'ru'  : 'whois.ripn.net' , \
			   'ch'  : 'whois.nic.ch' , \
			   # see http://www.nic.ch/whois_readme.html
			   'jp'  : 'whois.nic.ad.jp' , \
			   # (use DOM foo.jp/e for english; need to lookup !handles separately)
			   'to'  : 'whois.tonic.to' , \
			   'nu'  : 'whois.nic.nu' , \
			   'fm'  : 'www.dot.fm' , \
			   # http request http://www.dot.fm/search.html
			   'am'  : 'whois.nic.am' , \
			   'nu'  : 'www.nunames.nu' , \
			   # http request
			   # e.g. http://www.nunames.nu/cgi-bin/drill.cfm?domainname=nunames.nu
			   #'cx'  : 'whois.nic.cx' , \		# no response from this server
			   'af'  : 'whois.nic.af' , \
			   'as'  : 'whois.nic.as' , \
			   'li'  : 'whois.nic.li' , \
			   'lk'  : 'whois.nic.lk' , \
			   'mx'  : 'whois.nic.mx' , \
			   'pw'  : 'whois.nic.pw' , \
			   'sh'  : 'whois.nic.sh' , \
			   # consistently resets connection
			   'tj'  : 'whois.nic.tj' , \
			   'tm'  : 'whois.nic.tm' , \
			   'pt'  : 'whois.dns.pt' , \
			   'kr'  : 'whois.nic.or.kr' , \
			   # see also whois.krnic.net
			   'kz'  : 'whois.nic.or.kr' , \
			   # see also whois.krnic.net
			   'al'  : 'whois.ripe.net' , \
			   'az'  : 'whois.ripe.net' , \
			   'ba'  : 'whois.ripe.net' , \
			   'bg'  : 'whois.ripe.net' , \
			   'by'  : 'whois.ripe.net' , \
			   'cy'  : 'whois.ripe.net' , \
			   'cz'  : 'whois.ripe.net' , \
			   'dz'  : 'whois.ripe.net' , \
			   'ee'  : 'whois.ripe.net' , \
			   'eg'  : 'whois.ripe.net' , \
			   'es'  : 'whois.ripe.net' , \
			   'fi'  : 'whois.ripe.net' , \
			   'gr'  : 'whois.ripe.net' , \
			   'hr'  : 'whois.ripe.net' , \
			   'lu'  : 'whois.ripe.net' , \
			   'lv'  : 'whois.ripe.net' , \
			   'ma'  : 'whois.ripe.net' , \
			   'md'  : 'whois.ripe.net' , \
			   'mk'  : 'whois.ripe.net' , \
			   'mt'  : 'whois.ripe.net' , \
			   'pl'  : 'whois.ripe.net' , \
			   'ro'  : 'whois.ripe.net' , \
			   'si'  : 'whois.ripe.net' , \
			   'sm'  : 'whois.ripe.net' , \
			   'su'  : 'whois.ripe.net' , \
			   'tn'  : 'whois.ripe.net' , \
			   'ua'  : 'whois.ripe.net' , \
			   'va'  : 'whois.ripe.net' , \
			   'yu'  : 'whois.ripe.net' , \
			   # unchecked
			   'ac'  : 'whois.nic.ac' , \
			   'cc'  : 'whois.nic.cc' , \
			   #'cn'  : 'whois.cnnic.cn' , \		# connection refused
			   'gs'  : 'whois.adamsnames.tc' , \
			   'hk'  : 'whois.apnic.net' , \
			   #'ie'  : 'whois.ucd.ie' , \		# connection refused
			   #'is'  : 'whois.isnet.is' , \# connection refused
			   #'mm'  : 'whois.nic.mm' , \		# connection refused
			   'ms'  : 'whois.adamsnames.tc' , \
			   'my'  : 'whois.mynic.net' , \
			   #'pe'  : 'whois.rcp.net.pe' , \		# connection refused
			   'st'  : 'whois.nic.st' , \
			   'tc'  : 'whois.adamsnames.tc' , \
			   'tf'  : 'whois.adamsnames.tc' , \
			   'th'  : 'whois.thnic.net' , \
			   'tw'  : 'whois.twnic.net' , \
			   'us'  : 'whois.isi.edu' , \
			   'vg'  : 'whois.adamsnames.tc' , \
			   #'za'  : 'whois.co.za'		# connection refused
			   }



	def __init__(self,domain=None):
		self.domain=domain
		self.whoisserver=None		
		self.page=None
		return
	
	def whois(self,domain=None, server=None, cache=0):
		if domain is not None:
			self.domain=domain
			pass
		
		if server is not None:
			self.whoisserver=server
			pass
		
		if self.domain is None:
			print "No Domain"
			raise "No Domain"

		if self.whoisserver is None:
			self.chooseserver()

		if self.whoisserver is None:
			print "No Server"
			raise "No Server"
		
		if cache:
			fn = "%s.dom" % domainname
			if os.path.exists(fn):
				return open(fn).read()
			pass
		
		self.page=self._whois()		
		
		if cache:
			open(fn, "w").write(page)
			pass
		
		return
	
	def chooseserver(self):
		try:
			(secondlevel,toplevel)=string.split(self.domain,'.')
			self.whoisserver=WhoisRecord.whoismap.get(toplevel)
			if self.whoisserver==None:
				self.whoisserver=WhoisRecord.defaultserver
				return
			pass
		except:
			self.whoisserver=WhoisRecord.defaultserver
			return
		
		if(toplevel=='com' or toplevel=='org' or toplevel=='net'):
			tmp=self._whois()
			m=re.search("Whois Server:(.+)",tmp)
			if m:
				self.whoisserver=string.strip(m.group(1))
				return
			self.whoisserver='whois.networksolutions.com'
			tmp=self._whois()
			m=re.search("Whois Server:(.+)",tmp)
			if m:
				self.whoisserver=string.strip(m.group(1))
				return
			pass
		return
	

	def _whois(self):
		def alrmhandler(signum,frame):
			raise "TimedOut", "on connect"
		
		s = None
		
		## try until we timeout
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setblocking(1)
		#signal.signal(signal.SIGALRM,alrmhandler)
		#signal.alarm(timeout)
		while 1:		
			try:
				s.connect((self.whoisserver, 43))
			except socket.error, (ecode, reason):
				if ecode==errno.EINPROGRESS: 
					continue
				elif ecode==errno.EALREADY:
					continue
				else:
					raise socket.error, (ecode, reason)
				pass
			
			break
		
		#signal.alarm(0)
		
		ret = select.select ([s], [s], [], 30)
		
		if len(ret[1])== 0 and len(ret[0]) == 0:
			s.close()
			raise TimedOut, "on data"
		
		s.setblocking(1)
		
		s.send("%s\n" % self.domain)
		page = ""
		while 1:
			data = s.recv(8196)
			if not data: break
			page = page + data
			pass
		
		s.close()
		
		
		if string.find(page, "No match for") != -1:
			raise 'NoSuchDomain', self.domain

		if string.find(page, "No entries found") != -1:
			raise 'NoSuchDomain', self.domain

		if string.find(page, "no domain specified") != -1:
			raise 'NoSuchDomain', self.domain

		if string.find(page, "NO MATCH:") != -1:
			raise 'NoSuchDomain', self.domain
		
		return page

##
## ----------------------------------------------------------------------
##
class ContactRecord:
	def __init__(self):
		self.type=None
		self.organization=None
		self.person=None
		self.handle=None
		self.address=None
		self.email=None
		self.phone=None
		self.fax=None
		self.lastupdated=None
		return
	def __str__(self):
		return "Type: %s\nOrganization: %s\nPerson: %s\nHandle: %s\nAddress: %s\nEmail: %s\nPhone: %s\nFax: %s\nLastupdate: %s\n" % (self.type,self.organization,self.person,self.handle,self.address,self.email,self.phone,self.fax,self.lastupdated)
	

class DomainRecord(WhoisRecord):
	
	parsemap={ 'whois.networksolutions.com' : 'ParseWhois_NetworkSolutions' , \
			   'whois.register.com'		 : 'ParseWhois_RegisterCOM' }
			   
	def __init__(self,domain=None):
		WhoisRecord.__init__(self,domain)
		self.domainid = None
		self.created = None
		self.lastupdated = None
		self.expires = None
		self.databaseupdated = None
		self.servers = None
		self.registrant = ContactRecord()
		self.registrant.type='registrant'
		self.contacts = {}
		return
	def __str__(self):
		con=''
		for (k,v) in self.contacts.items():
			con=con + str(v) +'\n'
		return "%s (%s):\nWhoisServer: %s\nCreated : %s\nLastupdated : %s\nDatabaseupdated : %s\nExpires : %s\nServers : %s\nRegistrant >>\n\n%s\nContacts >>\n\n%s\n" % (self.domain, self.domainid,self.whoisserver,self.created, self.lastupdated, self.databaseupdated, self.expires,self.servers, self.registrant, con)

	def Parse(self):
		self._ParseWhois()
		return
	
	def _ParseWhois(self):
		parser=DomainRecord.parsemap.get(self.whoisserver)
		if parser==None:
			raise 'NoParser'
		parser='self.'+parser+'()'
		eval(parser)
		return
	
	##
	## ----------------------------------------------------------------------
	##
	def _ParseContacts_RegisterCOM(self,page):
		
		parts = re.split("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", page)

		contacttypes = None
		for part in parts:
			if string.find(part, "Contact:") != -1:
				if part[-1] == ":": part = part[:-1]
				contacttypes = string.split(part, ",")
				continue
			part = string.strip(part)
			if not part: continue
			
			contact=ContactRecord()
			
			m = re.search("Email: (.+@.+)", part)
			if m:
				contact.email=string.lower(string.strip(m.group(1)))
				
			m = re.search("\s+Phone: (.+)", part)
			if m:
				contact.phone=m.group(1)
				end=m.start(0)
				
			start=0
		
			lines = string.split(part[start:end], "\n")
			lines = map(string.strip,lines)
			
			contact.organization = lines.pop(0)
			contact.person = lines.pop(0)
		
			contact.address=string.join(lines,'\n')
		
			for contacttype in contacttypes:
				contacttype = string.lower(string.strip(contacttype))
				contacttype = string.replace(contacttype, " contact", "")
				contact.type=contacttype
				self.contacts[contacttype] = copy.copy(contact)
				pass
			pass
		
		return


	def ParseWhois_RegisterCOM(self):
		m = re.search("Record last updated on.*: (.+)", self.page)
		if m: self.lastupdated = m.group(1)
	
		m = re.search("Created on.*: (.+)", self.page)
		if m: self.created = m.group(1)
	
		m = re.search("Expires on.*: (.+)", self.page)
		if m: self.expires = m.group(1)
	
		m = re.search("Phone: (.+)", self.page)
		if m: self.registrant.phone=m.group(1)
	
		m = re.search("Email: (.+@.+)",self.page)
		if m: self.registrant.email=m.group(1)
	
		m = re.search("Organization:(.+?)Phone:",self.page,re.S)
		if m: 
			start=m.start(1)
			end=m.end(1)
			registrant = string.strip(self.page[start:end])
			registrant = string.split(registrant, "\n")
			registrant = map(string.strip,registrant)
			
			self.registrant.organization = registrant[0]
			self.registrant.person =registrant[1]
			self.registrant.address = string.join(registrant[2:], "\n")
			pass
		
		m = re.search("Domain servers in listed order:\n\n(.+?)\n\n", self.page, re.S)
		if m:
			start = m.start(1)
			end = m.end(1)
			servers = string.strip(self.page[start:end])
			lines = string.split(servers, "\n")
			
			
			self.servers = []
			for line in lines:
				m=re.search("(\w|\.)+?\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",string.strip(line))
				if m:
					self.servers.append(m.group(1), m.group(2))
					pass
				pass
			pass

		m = re.search("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", self.page)
		if m:
			i = m.start()
			m = re.search("Domain servers in listed order", self.page)
			j = m.start()
			contacts = string.strip(self.page[i:j])
			pass
		self._ParseContacts_RegisterCOM(contacts)
		return

	
	def _ParseContacts_NetworkSolutions(self,page):
		
		parts = re.split("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", page)
	
		contacttypes = None
		for part in parts:
			if string.find(part, "Contact:") != -1:
				if part[-1] == ":": part = part[:-1]
				contacttypes = string.split(part, ",")
				continue
			part = string.strip(part)
			if not part: continue
	  
			record=ContactRecord()
		
			lines = string.split(part, "\n")
			m = re.search("(.+) \((.+)\) (.+@.+)", lines.pop(0))
			if m:
				record.person = string.strip(m.group(1))
				record.handle = string.strip(m.group(2))
				record.email = string.lower(string.strip(m.group(3)))
				pass
		
			record.organization=string.strip(lines.pop(0))
		
			flag = 0
			addresslines = []
			phonelines = []
			phonelines.append(string.strip(lines.pop()))
			for line in lines:
				line = string.strip(line)
				#m=re.search("^(\d|-|\+|\s)+$",line)
				#if m: flag = 1
				if flag == 0:
					addresslines.append(line)
				else:
					phonelines.append(line)
					pass
				pass
			record.phone = string.join(phonelines, "\n")
			record.address = string.join(addresslines, "\n")
			
			for contacttype in contacttypes:
				contacttype = string.lower(string.strip(contacttype))
				contacttype = string.replace(contacttype, " contact", "")
				record.type=contacttype
				self.contacts.update({contacttype:copy.copy(record)})
				pass
			pass
		return
		
	def ParseWhois_NetworkSolutions(self):
		 
		m = re.search("Record last updated on (.+)\.", self.page)
		if m: self.lastupdated = m.group(1)
		
		m = re.search("Record created on (.+)\.", self.page)
		if m: self.created = m.group(1)
		
		m = re.search("Database last updated on (.+)\.", self.page)
		if m: self.databaseupdated = m.group(1)
		
		m = re.search("Record expires on (.+)\.",self.page)
		if m: self.expires=m.group(1)
		
		m = re.search("Registrant:(.+?)\n\n", self.page, re.S)
		if m: 
			start= m.start(1)
			end = m.end(1)
			reg = string.strip(self.page[start:end])
			
			reg = string.split(reg, "\n")
			reg = map(string.strip,reg)
			self.registrant.organization = reg[0]
			self.registrant.address = string.join(reg[1:],'\n')
			
			m = re.search("(.+) \((.+)\)", self.registrant.organization)
			if m: 
				self.domainid   = m.group(2)
				pass
			pass
		
		m = re.search("Domain servers in listed order:\n\n", self.page)
		if m:
			i = m.end()
			m = re.search("\n\n", self.page[i:])
			j = m.start()
			servers = string.strip(self.page[i:i+j])
			lines = string.split(servers, "\n")
			self.servers = []
			for line in lines:
				m=re.search("(\w|\.)+?\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})",string.strip(line))
				if m:
					self.servers.append(m.group(1), m.group(2))
					pass
				pass
			pass
		
		m = re.search("((?:(?:Administrative|Billing|Technical|Zone) Contact,?[ ]*)+:)\n", self.page)
		if m:
			i = m.start()
			m = re.search("Record last updated on", self.page)
			j = m.start()
			contacts = string.strip(self.page[i:j])
			pass
		self._ParseContacts_NetworkSolutions(contacts)
		
		return

		
##
## ----------------------------------------------------------------------
##
		   



##
## ----------------------------------------------------------------------
##

def usage(progname):
	version = _version
	print __doc__ % vars()

def main(argv, stdout, environ):
	progname = argv[0]
	list, args = getopt.getopt(argv[1:], "", ["help", "version"])
	
	for (field, val) in list:
		if field == "--help":
			usage(progname)
			return
		elif field == "--version":
			print progname, _version
			return
	
	rec=WhoisRecord();
	
	for domain in args:
		whoisserver=None
		if string.find(domain,'@')!=-1:
			(domain,whoisserver)=string.split(domain,'@')
		try:
			rec.whois(domain,whoisserver)
			print rec.page
		except 'NoSuchDomain', reason:
			print "ERROR: no such domain %s" % domain
		except socket.error, (ecode,reason):
			print reason
		except "TimedOut", reason:
			print "Timed out", reason
			
if __name__ == "__main__":
	main(sys.argv, sys.stdout, os.environ)
