def check(phrase,apikey):
	#Variables
	KEYWORDS = ['wake up','turn on','power on','start','computer','pc','server']
	MINIMUM_MATCHES = 2
	MATCHES = 0

	#Comparing pharse against KEYWORDS
	for keyword in KEYWORDS:
		if keyword.lower() in phrase.lower():
			MATCHES += 1

	if MATCHES >= MINIMUM_MATCHES:
		return execute("Wake On Lan Module Used")
	else:
		return {'success': False, 'text': "Not enough keywords found to use module: Wake On Lan Alpha", 'voice': "Not enough keywords found to use module: Wake On Lan"}	
def execute(parameter):

	return {'success': True, 'text': parameter, 'voice': parameter}