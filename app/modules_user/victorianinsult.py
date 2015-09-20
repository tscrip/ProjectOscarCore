def check(phrase,apikey):
	#Keywords
	KEYWORDS = ['tell me','give me','victorian','insult','come back']

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
		return {'success': 0, 'text': "Not enough keywords found to use module: Victorian Insult", 'voice': "Not enough keywords found to use module: Victorian Insult"}	
def execute():
	import requests, json, unicodedata

	#Getting JSON
	url = 'http://quandyfactory.com/insult/json'
	json = json.loads(requests.get(url).text)

	#Getting information out of JSON
	display = json['insult'].replace(",",";")
	verbal = json['insult'].replace(",",";")

	#Converting Unicode to ASCII
	display = unicodedata.normalize('NFKD', display).encode('ascii','ignore')
	verbal = unicodedata.normalize('NFKD', verbal).encode('ascii','ignore')

	#Returning results
	return {'success': 1, 'text': display, 'voice': verbal}