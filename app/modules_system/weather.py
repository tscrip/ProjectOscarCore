def check(phrase,apikey):
	#Keywords
	KEYWORDS = ['weather','forecast','today','week','temperature','outside']
	
	#Matches variables
	MINIMUM_MATCHES = 2
	MATCHES = 0

	#Comparing parse against KEYWORDS
	for keyword in KEYWORDS:
		if keyword.lower() in phrase.lower():
			MATCHES += 1

	#Checking if module should be used 
	if MATCHES >= MINIMUM_MATCHES:
		if "today" in phrase.lower():
			return execute("today",apikey) 
		elif "week" in phrase.lower():
			return execute("week",apikey)
		else:
			return execute("today",apikey)
	else:
		return {'success': False, 'text': "Not enough keywords found to use module: Weather", 'voice': "Not enough keywords found to use module: Weather"}	
def execute(parameter,apikey):
	import requests, json
	from app.db import db

	#Creating Database Object
	DatabaseObj = db.Database()

	#Getting user info from SQLite
	userinfo = DatabaseObj.GetUserbyAPIKey(apikey)

	#Getting 4th element(zip code)
	zipcode = userinfo[4]

	#Getting JSON
	weather_url = 'http://query.yahooapis.com/v1/public/yql?q=select%20item%20from%20weather.forecast%20where%20location%3D"'+zipcode+'"&format=json'
	html = requests.get(weather_url)

	#Identifying what type of data to get
	if parameter == "today":
		return GetTodayWeather(json.loads(html.text))
	elif parameter == "week":
		return GetWeekWeather(json.loads(html.text))

def GetTodayWeather(json_weather):
	import unicodedata, re

	#Getting City, State via RegEx
	citystate = re.search(ur'for (.*) at',json_weather['query']['results']['channel']['item']['title']).groups(1)[0]

	#Getting information out of JSON
	display = "Currently the Temperature in "+citystate+" is "+json_weather['query']['results']['channel']['item']['condition']['temp'] \
				+" degrees with a "+"High of "+json_weather['query']['results']['channel']['item']['forecast'][0]['high']+" and a" \
				+" Low of "+json_weather['query']['results']['channel']['item']['forecast'][0]['low']+"." \
				+"\nConditions "+json_weather['query']['results']['channel']['item']['forecast'][0]['text']+"."
	verbal = "Currently the Temperature"+citystate+" is "+json_weather['query']['results']['channel']['item']['condition']['temp'] \
				+". Conditions "+json_weather['query']['results']['channel']['item']['forecast'][0]['text']+"."

	#Converting Unicode to ASCII
	display = unicodedata.normalize('NFKD', display).encode('ascii','ignore')
	verbal = unicodedata.normalize('NFKD', verbal).encode('ascii','ignore')

	#Returning data
	return {'success': True , 'text': display, 'voice': verbal}

def GetWeekWeather(json_weather):
	import datetime, re
	import unicodedata

	#Getting City, State via RegEx
	citystate = re.search(ur'for (.*) at',json_weather['query']['results']['channel']['item']['title']).groups(1)[0]

	today_plus_1 = ConvertDay(json_weather['query']['results']['channel']['item']['forecast'][1]['day'])
	today_plus_2 = ConvertDay(json_weather['query']['results']['channel']['item']['forecast'][2]['day'])
	today_plus_3 = ConvertDay(json_weather['query']['results']['channel']['item']['forecast'][3]['day'])
	today_plus_4 = ConvertDay(json_weather['query']['results']['channel']['item']['forecast'][4]['day'])

	#Getting information out of JSON
	display="The forecast for "+citystate+" is as follows" \
			+"\nToday " \
			+"High of "+json_weather['query']['results']['channel']['item']['forecast'][0]['high']+" " \
			+"Low of "+json_weather['query']['results']['channel']['item']['forecast'][0]['low']+"" \
			+".\nConditions "+json_weather['query']['results']['channel']['item']['forecast'][0]['text']+".\n\n " \
			+"\n"+today_plus_1+" " \
			+"High of "+json_weather['query']['results']['channel']['item']['forecast'][1]['high']+" " \
			+"Low of "+json_weather['query']['results']['channel']['item']['forecast'][1]['low']+" " \
			+".\nConditions "+json_weather['query']['results']['channel']['item']['forecast'][1]['text']+".\n\n" \
			+"\n"+today_plus_2+" " \
			+"High of "+json_weather['query']['results']['channel']['item']['forecast'][2]['high']+" " \
			+"Low of "+json_weather['query']['results']['channel']['item']['forecast'][2]['low']+" " \
			+".\nConditions "+json_weather['query']['results']['channel']['item']['forecast'][2]['text']+".\n\n" \
			+"\n"+today_plus_3+" " \
			+"High of "+json_weather['query']['results']['channel']['item']['forecast'][3]['high']+" " \
			+"Low of "+json_weather['query']['results']['channel']['item']['forecast'][3]['low']+" " \
			+".\nConditions "+json_weather['query']['results']['channel']['item']['forecast'][3]['text']+".\n\n" \
			+"\n"+today_plus_4+" " \
			+"High of "+json_weather['query']['results']['channel']['item']['forecast'][4]['high']+" " \
			+"Low of "+json_weather['query']['results']['channel']['item']['forecast'][4]['low']+" " \
			+".\nConditions "+json_weather['query']['results']['channel']['item']['forecast'][4]['text']+".\n\n"

	verbal= "The forecast for "+citystate+" is as follows. " \
			"Today "+json_weather['query']['results']['channel']['item']['forecast'][0]['text']+". " \
			+today_plus_1+" "+json_weather['query']['results']['channel']['item']['forecast'][1]['text']+". " \
			+today_plus_2+" "+json_weather['query']['results']['channel']['item']['forecast'][2]['text']+". " \
			+today_plus_3+" "+json_weather['query']['results']['channel']['item']['forecast'][3]['text']+". " \
			+today_plus_4+" "+json_weather['query']['results']['channel']['item']['forecast'][4]['text']+".";

	#Converting Unicode to ASCII
	display = unicodedata.normalize('NFKD', display).encode('ascii','ignore')
	verbal = unicodedata.normalize('NFKD', verbal).encode('ascii','ignore')

	#Returning results
	return {'success': True, 'text': display, 'voice': verbal}

def ConvertDay(short_day):
	if (short_day == "Mon"):
		return "Monday"
	elif (short_day == "Tue"):
		return "Tuesday"
	elif (short_day == "Wed"):
		return "Wednesday"
	elif (short_day == "Thu"):
		return "Thursday"
	elif (short_day == "Fri"):
		return "Friday"
	elif (short_day == "Sat"):
		return "Saturday"
	elif (short_day == "Sun"):
		return "Sunday"