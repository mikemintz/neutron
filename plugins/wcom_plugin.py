#$ neutron_plugin 01

import pprint
import string
from string import *
import urllib 
import xml.dom.minidom 
from xml.dom.minidom import Node


def handler_wcom(type, source, parameters):
	param = parameters.strip()
	if param=='':
	    param = 'UKXX0010'
	param = str(parameters)
	param = upper(param)
	 #print source
	 #print param
	 #proxies = {'http': 'http://192.168.0.1:3128'}
	title = ""
	if len(param) <> 8 :
		param = 'UKXX0010'
		title = '\n*** Wrong format, falling back ***\n'			
	try:
	 response = urllib.urlopen('http://xoap.weather.com/weather/local/'+param+'?cc=*&dayf=1&unit=m')
	 #response = urllib.urlopen('http://xoap.weather.com/weather/local/'+param+'?cc=*&dayf=1&unit=m', proxies=proxies)
	except:
	 print "Unexpected error:", sys.exc_info()[0]
	
	html = response.read()
	
	doc = xml.dom.minidom.parseString(string.strip(html)) 
	mapping = {} 
	for node in doc.getElementsByTagName("weather"): 
	 P = node.getElementsByTagName("loc")
	 for node4 in P:
	  L = node4.getElementsByTagName("dnam")
	  for node2 in L:
	   for node3 in node2.childNodes:
	    if node3.nodeType == Node.TEXT_NODE:
	     title += 'Weather report for: ' + node3.data + '\n'
	  LT = node4.getElementsByTagName("tm")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Local time: ' + node31.data+'\n'
	  LT = node4.getElementsByTagName("lat")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Latitude: ' + node31.data+'\n'
	  LT = node4.getElementsByTagName("lon")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Longitude: '+ node31.data+'\n'
	  LT = node4.getElementsByTagName("sunr")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Sunrise: ' + node31.data+'\n'
	  LT = node4.getElementsByTagName("suns")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Sunset: ' + node31.data+'\n'
	  LT = node4.getElementsByTagName("zone")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Zone: ' + node31.data+'\n'
         P = node.getElementsByTagName("cc")
	 for node4 in P:
	  L = node4.getElementsByTagName("lsup")
	  for node2 in L:
	   for node3 in node2.childNodes:
	    if node3.nodeType == Node.TEXT_NODE:
	     title += 'Latest update: ' + node3.data + '\n'
	  LT = node4.getElementsByTagName("obst")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Observation station: ' + node31.data+'\n'
	  LT = node4.getElementsByTagName("tmp")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Temperature: ' + node31.data+'\n'
	  LT = node4.getElementsByTagName("flik")
	  for node21 in LT:
	   for node31 in node21.childNodes:
	    if node31.nodeType == Node.TEXT_NODE:
	     title += 'Windchill: ' + node31.data+'\n'
    	smsg(type, source, title)

register_command_handler(handler_wcom, '!w', 0, 'Weather plugin, try searching your city at weather.yahoo.com', '!w', ['!w NLXX0002'])

