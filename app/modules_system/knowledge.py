def check(phrase,apikey):
	#Converting phrase to lowercase
	phrase = phrase.lower()

	#Checking to see if last answer was wrong
	if IsWrong(phrase):

		#Getting "Wrong Answer" phrase
		aiml_result = QueryAIML("Wrong Answer")

		#Remove last answer from temp DB
		sql_result = RemoveLastSQL(apikey)

		#Checking results
		if sql_result:
			#Last answer appears to be incorrect
			return {'success': True, 'text': aiml_result, 'voice': aiml_result}

		elif not sql_result:
			#Last answer appears to be incorrect
			return {'success': True, 'text': "No knowledge to remove", 'voice': "No knowledge to remove"}

	else:

		#Changing status of last answer to 'committed' = 1 in SQLite
		CommitLastKnowledge(apikey)

		#Keywords
		KEYWORDS = ['whats','what','how','where','when','is','do','a','who','was']

		#Matches variables
		MINIMUM_MATCHES = 2
		MATCHES = 0

		#Comparing phrase against KEYWORDS
		for keyword in KEYWORDS:
			if keyword.lower() in phrase:
				MATCHES += 1

		#Checking if module should be used 
		if MATCHES >= MINIMUM_MATCHES:

			result = execute(phrase,apikey)

			#Returning data
			return result
		else:
			return {'success': False, 'text': "Not enough keywords found to use module: knowledge", 'voice': "Not enough keywords found to use module: Knowledge"}	
def execute(parameter,apikey):
	import requests, unicodedata, xmltodict, urllib
	import ConfigParser

	#Importing config file
	config = ConfigParser.ConfigParser()
	config.read('app/config/config.ini')

	#Creating variables
	Wolfram_API_Key = str(config.get("APIKeys", "WOLFRAM_ALPHA"))

	#Looking up phrase in AIML file
	result = QueryAIML(parameter)

	#Checking to see if answer was found
	if result != "NA":
		print("Result in AIML XML")

		#Returning result
		return {'success': True, 'text': result, 'voice': result}
	else:
		print("Checking Wolfram Alpha")
		
		#URL encoding parameter
		encoded_parameter = urllib.quote_plus(parameter)

		#Getting XML
		url = 'http://api.wolframalpha.com/v2/query?appid='+Wolfram_API_Key+'&input='+encoded_parameter+'&format=plaintext'
		xml = requests.get(url)
		xml_obj = xmltodict.parse(xml.text)

		#Getting count of XML pods
		pod_count = xml_obj['queryresult']['@numpods']

		#Looping through XML pods
		for pod in range(0,int(pod_count)-1):
			if xml_obj['queryresult']['pod'][pod]['@title'] == "Result" or xml_obj['queryresult']['pod'][pod]['@title'] == "Definitions" or xml_obj['queryresult']['pod'][pod]['@title'] == "Definition":

				#Writing found answer to AIML file
				WriteToSQL(parameter,xml_obj['queryresult']['pod'][pod]['subpod']['plaintext'],apikey)

				#Retuning answer
				return {'success': True, 'text': str(xml_obj['queryresult']['pod'][pod]['subpod']['plaintext']), 'voice': str(xml_obj['queryresult']['pod'][pod]['subpod']['plaintext'])}

		print "HERE NAF"
		#No answer found
		return {'success': False, 'text': "Not enough keywords found to use module: INSERT_MODULE_NAME", 'voice': "Not enough keywords found to use module: INSERT_MODULE_NAME"}

def IsWrong(phrase):
	#Keywords
	KEYWORDS = ['that','thats','wrong','incorrect','not right','answer','remove','previous','last']

	#Matches variables
	MINIMUM_MATCHES = 2
	MATCHES = 0

	#Comparing phrase against KEYWORDS
	for keyword in KEYWORDS:
		if keyword.lower() in phrase:
			MATCHES += 1

	#Checking if module should be used 
	if MATCHES >= MINIMUM_MATCHES:

		return True
	else:
		return False

### SQLite Functions ###
# Used to write answer to SQLite
def WriteToSQL(phrase,answer,apikey):
	from app.db import db

	#Creating Database Object
	DatabaseObj = db.Database()
	Response = DatabaseObj.AddKnowledge(phrase,answer,apikey)

	#Checking if knowledge was added
	if Response == True:
		print("DEBUG: Successfully imported knowledge")
	else:
		print("DEBUG: Unable to import knowledge")

# Used to remove last answer from SQLite
def RemoveLastSQL(apikey):
	from app.db import db

	#Creating Database Object
	DatabaseObj = db.Database()
	Response = DatabaseObj.RemoveLastKnowledge(apikey)

	#Checking if temp knowledge is present
	if Response:
		print("DEBUG: Successfully removed knowledge")
		return True
	elif not Response:
		print("DEBUG: No knowledge to remove")
		return False
	else:
		print("DEBUG: An error occured")

# Used to make last answer as "committed" in SQLite
def CommitLastKnowledge(apikey):
	from app.db import db

	#Creating Database Object
	DatabaseObj = db.Database()

	#Writing to AIML
	Response = DatabaseObj.WriteLastToAIML(apikey)

	#Checking if knowledge was committed
	if Response == True:
		print("DEBUG: Successfully committed knowledge")
	else:
		print("DEBUG: No need to commit knowledge")

### End of SQLite Functions ###

#Querying AIML
def QueryAIML(input):
	import aiml

	bot = aiml.Kernel();
	bot.setBotPredicate('name', 'Oscar')
	bot.setBotPredicate('master', 'Tscrip')
	bot.learn("app/db/aiml/Oscar.aiml");
	bot.learn("app/db/aiml/Custom.aiml");
	result = bot.respond(input)

	return result
	#Returning Answer