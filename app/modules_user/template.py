def check(phrase,apikey):
	#Keywords
	KEYWORDS = ['','','','','']

	#Matches variables
	MINIMUM_MATCHES = 2
	MATCHES = 0

	#Comparing phrase against KEYWORDS
	for keyword in KEYWORDS:
		if keyword.lower() in phrase.lower():
			MATCHES += 1

	#Checking if module should be used 
	if MATCHES >= MINIMUM_MATCHES:
		return execute()
	else:
		return {'success': False, 'text': "Not enough keywords found to use module: INSERT_MODULE_NAME", 'voice': "Not enough keywords found to use module: INSERT_MODULE_NAME"}	
def execute():
	import requests, json, unicodedata

	#Getting JSON
	url = 'URL_TO_JSON'
	json = json.loads(requests.get(url).text)

	#Getting information out of JSON
	display = json['field']
	verbal = json['field']['test']['test']

	#Converting Unicode to ASCII
	display = unicodedata.normalize('NFKD', display).encode('ascii','ignore')
	verbal = unicodedata.normalize('NFKD', verbal).encode('ascii','ignore')

	#Returning results
	return {'success': True, 'text': display, 'voice': verbal}