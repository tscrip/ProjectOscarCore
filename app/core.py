import ConfigParser
import modules_system
import modules_user
from db import db

### Core Class ###
class Core():
	#Initialize method
	def __init__(self):
		#Importing config file
		self.GetSettings()
		
	#GetModules method
	def GetModules(self):
		#Creating object
		DatabaseObj = db.Database()

		#Getting modules
		self.modules = DatabaseObj.GetEnabledModules()

		#Modules array values
        #0 - module_id
        #1 - module_name
        #2 - module_type
        #3 - module_filename
        #4 - module_priority
        #5 - module_enabled

		#Looping and including modules
		for module in self.modules:
			#DEBUGGING print("Including: app.modules_"+module[2]+"."+module[3])
			__import__("app.modules_"+str(module[2])+"."+str(module[3]))

		print self.modules

		#Returning modules
		return self.modules

	#Main method
	def Main(self,phrase,apikey):
		import aiml

		#Importing modules
		self.modules = self.GetModules()

		#Looping through modules to find correct one
		for module in self.modules:
			#Modules array values
			#0 - module_id
			#1 - module_name
			#2 - module_type
			#3 - module_filename
			#4 - module_priority

			#Building full path to module
			self.fullpath = "modules_"+module[2]+"."+module[3]
			
			#Running check function in each  module
			self.result = eval(self.fullpath).check(phrase,apikey)

			#If success is true
			if self.result['success'] == True:
				
				#Return results
				return(self.result)
				break

		#No module found
		bot = aiml.Kernel();
		bot.setBotPredicate('name', 'Oscar')
		bot.setBotPredicate('master', 'Tscrip')
		bot.learn("app/db/aiml/Oscar.aiml");
		bot.learn("app/db/aiml/Custom.aiml");
		result = bot.respond("No Module Found")

		#Returning value
		return {'success': False, 'text': result, 'voice': result}

	def GetSettings(self):
		#Creating object
		DatabaseObj = db.Database()

		#Getting API Keys
		self.UserAPIKeys = DatabaseObj.GetAPIKeys()

		#Importing config file
		config = ConfigParser.ConfigParser()
		config.read('app/config/config.ini')

		#Getting webserver settings
		self.WebServerPort = int(config.get("WebServer", "PORT"))
		self.WebServerDebug = bool(config.getboolean("WebServer", "DEBUG_ENABLED"))