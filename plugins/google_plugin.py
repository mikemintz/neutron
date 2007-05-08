#$ neutron_plugin 01

import google

def google_remove_html(text):
	nobold = text.replace('<b>', '').replace('</b>', '')
	nobreaks = nobold.replace('<br>', ' ')
	noescape = nobreaks.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
	return noescape

def google_search(query):
	try:
    	    data = google.doGoogleSearch(query)
	except SOAP.HTTPError:
	    return 'Google API Error.'    
	try:
		first = data.results[0]
		url = first.URL
		title = google_remove_html(first.title)
		if first.summary:
			summary = google_remove_html(first.summary)
		else:
			summary = google_remove_html(first.snippet)
		searchtime = str(round(data.meta.searchTime, 3))
		total = str(data.meta.estimatedTotalResultsCount)
		return url + ' - ' + title + ' - ' + summary + ' (' + searchtime + 'sec) (' + total + ' sites)'
	except:
		return 'No Results'

def handler_google_google(type, source, parameters):
	results = google_search(parameters)
	smsg(type, source, results)

def handler_google_spell(type, source, parameters):
	correction = google.doSpellingSuggestion(parameters)
	if not correction:
		correction = 'No Suggestion'
	smsg(type, source, correction)

def handler_google_jepsearch(type, source, parameters):
	results = google_search(parameters + ' site:www.jabber.org "/jeps/jep-" -jeplist.html')
	smsg(type, source, results)

register_command_handler(handler_google_google, '!google', 0, 'Looks up search terms on google.', '!google <query>', ['!google "mike mintz"'])
register_command_handler(handler_google_spell, '!spell', 0, 'Returns a spelling suggestion from google.', '!spell <query>', ['!spell "pithon nutron"'])
register_command_handler(handler_google_jepsearch, '!jepsearch', 0, 'Searches google for a JEP.', '!jep <query>', ['!google "jep-0001"'])
