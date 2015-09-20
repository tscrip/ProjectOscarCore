def check(phrase,apikey):
	#Keywords
	KEYWORDS = ['song','goes like','has the lyrics','goes','sounds like','says','has the words']

	#Matches variables
	MINIMUM_MATCHES = 2
	MATCHES = 0

	#Comparing phrase against KEYWORDS
	for keyword in KEYWORDS:
		if keyword.lower() in phrase.lower():
			MATCHES += 1

	#Checking if module should be used 
	if MATCHES >= MINIMUM_MATCHES:
		return execute(phrase)
	else:
		return {'success': False, 'text': "Not enough keywords found to use module: Song Finder", 'voice': "Not enough keywords found to use module: Song Finder"}	
def execute(phrase):
	import requests, json, unicodedata, re
	import ConfigParser

	#Importing config file
	config = ConfigParser.ConfigParser()
	config.read('app/config/config.ini')

	#Creating variables
	SongFinder_API_Key = str(config.get("APIKeys", "SONG_FINDER"))

	#Getting lyric
	lyric_regex = re.match(r'(?:What Song goes|What song has the words) (.*)', phrase, re.MULTILINE | re.IGNORECASE)

	#Getting JSON
	url = 'http://api.lyricsnmusic.com/songs?api_key='+SongFinder_API_Key+'&lyrics='+lyric_regex.group(1)
	json = json.loads(requests.get(url).text)

	#Getting information out of JSON
	display = "The artist is "+json[0]['artist']['name']+" and the song title is "+json[0]['title']
	verbal = "The artist is "+json[0]['artist']['name']+" and the song title is "+json[0]['title']

	#Converting Unicode to ASCII
	display = unicodedata.normalize('NFKD', display).encode('ascii','ignore')
	verbal = unicodedata.normalize('NFKD', verbal).encode('ascii','ignore')

	#Returning results
	return {'success': True, 'text': display, 'voice': verbal}