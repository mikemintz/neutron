import re, string, urllib

__where = [re.compile(r'<span id="r_text" name="r_text">([^<]*)')]

class BabelizerError(Exception):
	pass

class LanguageNotAvailableError(BabelizerError):
	pass
class BabelfishChangedError(BabelizerError):
	pass
class BabelizerIOError(BabelizerError):
	pass

def clean(text):
	return ' '.join(string.replace(text.strip(), "\n", ' ').split())

def translate(phrase, from_lang, to_lang):
	from_lang = from_lang.lower()
	to_lang = to_lang.lower()
	if from_lang == 'es':
		from_lang = 's'
	if to_lang == 'es':
		to_lang = 's'
	if from_lang[0] not in ['e', 's', 'r', 'i', 'g', 'f'] or to_lang[0] not in ['e', 's', 'r', 'i', 'g', 'f']:
		raise LanguageNotAvailableError(lang)
	direction = from_lang[0] + to_lang[0]
	phrase=phrase.encode('cp1251')
	params = urllib.urlencode( {
		'lang': 'en',
		'status': 'translate',
		'source': phrase,
		'direction': direction,
		'template': 'General',
	} )
	try:
		response = urllib.urlopen('http://www.translate.ru/text.asp', params)
	except IOError, what:
		raise BabelizerIOError("Couldn't talk to server: %s" % what)
	except:
		print "Unexpected error:", sys.exc_info()[0]

	html = unicode(response.read(), 'CP1251')
	for regex in __where:
		match = regex.search(html)
		if match: break
	if not match: raise BabelfishChangedError("Can't recognize translated string.")
	"""
	current_unichr = ''
	result = ''
	words = string.split(clean(match.group(1)))
	chars = list(clean(match.group(1)))
	for char in chars:
		if char == '&':
			current_unichr = '&'
			continue
		elif current_unichr:
			if char == '#':
				pass
	  		elif char == ';':
	  			result += unichr(int(current_unichr[1:]))
	  			current_unichr = ''
			else:
				current_unichr += char
			continue
   		result += char
	"""
	#if to_lang == 'r':
	result = clean(match.group(1))
	#result = unicode(result, 'CP1251')
	#else:
	#	result = string.split(string.split(html, '<span id="r_text" name="r_text">')[1], '<')[0]
	#result = string.split(string.split(html, '<span id="r_text" name="r_text">')[1], '<')[0]
	return result
		
#print translate('hello')
