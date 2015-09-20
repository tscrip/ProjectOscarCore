def check(phrase,apikey):
	#Keywords
	KEYWORDS = ['tell me','give me','whats','what is','chuck norris','joke','riddle',]
	
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
		return {'success': 0, 'text': "Not enough keywords found to use module: Chuck Norris", 'voice': "Not enough keywords found to use module: Chuck Norris"}	
def execute():
	import requests, json, unicodedata

	#Getting JSON
	url = 'http://api.icndb.com/jokes/random?exclude=[explicit]'
	json = json.loads(requests.get(url).text)

	#Getting information out of JSON
	display = json['value']['joke']
	verbal = json['value']['joke']

	#Converting Unicode to ASCII
	display = unicodedata.normalize('NFKD', display).encode('ascii','ignore')
	verbal = unicodedata.normalize('NFKD', verbal).encode('ascii','ignore')

	#Returning results
	return {'success': 1, 'text': display, 'voice': verbal}