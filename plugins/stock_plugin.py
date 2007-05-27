#$ neutron_plugin 01

import urllib

def handler_stock_stock(type, source, parameters):
	if parameters:
		data = urllib.urlopen('http://finance.yahoo.com/d/quotes.csv?s=' + parameters + '&f=sl1d1t1c1ohgv&e=.csv', proxies=proxies).read()
		data = data.replace('"', '')
		(stock_name, stock_current, stock_date, stock_time, stock_change, stock_open, stock_high, stock_low, stock_volume) = string.split(data.strip(), ',')
		if stock_change == 'N/A':
			reply = 'No Match For: ' + parameters
		else:
			reply = stock_name + ': ' + stock_current + ' (' + stock_change + ') - Volume: ' + stock_volume + ' - High: ' + stock_high + ' - Low: ' + stock_low
	else:
		reply = 'Please Enter Stock Symbol'
	smsg(type, source, reply)

register_command_handler(handler_stock_stock, '!stock', 0, 'Returns information on a particular stock (provided by Yahoo).', '!stock <code>', ['!stock AOL'])
