#$ neutron_plugin 01

import pymetar

WEATHERCODE_FILE = 'static/weather.txt'

def handler_weather_weather(type, source, parameters):
	if not parameters:
		smsg(type, source, 'Invalid Syntax')
		return
	info = pymetar.MetarReport(str(parameters).strip())
	try:
		location = info.getStationName()
		celsius = str(round(info.getTemperatureCelsius(), 1))
		fahrenheit = str(round(info.getTemperatureFahrenheit(), 1))
		#humidity = str(round(info.getHumidity(), 1))
		results = location + ' - ' + str(info.getWeather()) + ' - ' + celsius + 'C - ' + fahrenheit + 'F' # + ' - ' + humidity + '% Humdity'
	except Exception, ex:
		results = 'CHYBA!'
		print ex.__str__
	smsg(type, source, results)

def handler_weather_weathercode(type, source, parameters):
	if not parameters:
		smsg(type, source, 'Invalid Syntax')
		return
	if len(parameters)<=2:
		smsg(type, source, 'Query too short!')
		return
	results = ''
	query = string.lower(parameters)
	fp = open(WEATHERCODE_FILE, 'r')
	lines = fp.readlines()
	for line in lines:
		if string.count(string.lower(line), query):
			results += string.split(line, '=> ')[0]
	if results:
		smsg(type, source, results)
	else:
		smsg(type, source, 'No Results')

register_command_handler(handler_weather_weather, '!weather', 0, 'Looks up weather conditions from NOAA.', '!weather <4-letter-weather-code>', ['!weather panc'])
register_command_handler(handler_weather_weathercode, '!weathercode', 0, 'Looks up weather codes for use in !weather.', '!weathercode <query>', ['!weathercode anchorage'])
