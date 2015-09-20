from app import app as app
from app.db import db as DB
from flask import request, render_template, render_template
from app import core as Core
import json

#Creating object(s)
CoreObj = Core.Core()
DatabaseObj = DB.Database()

### Routes ###
#Load Home template
@app.route('/')
def route_home():
	return render_template('main.html')

##########################
## Module Related Routes##
##########################

#Get/Post/Put Modules#
@app.route('/api/modules', methods=['GET','POST','PUT'])
def route_api_modules():
	if request.method == 'GET':
		#Getting ALL modules
		modules = DatabaseObj.GetAllModules()
		return json.dumps(modules)

	elif request.method == 'POST':
		#Inserting new module
		insert_name = request.form['name']
		insert_author = request.form['author']
		insert_filename = request.form['filename']
		insert_status = request.form['status']
		insert_priority = request.form['priority']

		#Writting to SQLite
		result = DatabaseObj.CreateModule(insert_name,insert_author,insert_filename,insert_status,insert_priority)

		#Checking to see if record was updated
		if result:
			return "Module successfully inserted."
		else:
			return "System Error. Could not insert module."

	elif request.method == 'PUT':

		#Update current module
		update_id = request.form['id']
		update_name = request.form['name']
		update_author = request.form['author']
		update_filename = request.form['filename']
		update_status = request.form['status']
		update_priority = request.form['priority']

		#Updating SQLite
		result = DatabaseObj.UpdateModule(update_id,update_name,update_author,update_filename,update_status,update_priority)

		#Checking to see if record was updated
		if result:
			return "Module successfully updated."
		else:
			return "System Error. Could not update module."

#Getting module info by id
@app.route('/api/module/<module_id>', methods=['GET','POST'])
def route_api_module(module_id):
	if request.method == "GET":
		#Getting module
		module_info = DatabaseObj.GetModule(module_id)
		return json.dumps(module_info)

	elif request.method == "POST":
		#Disabling module
		module_status = DatabaseObj.ToggleModuleStatus(module_id)
		return str(module_status)
##########################
## End Module Routes##
##########################

##########################
## User Related Routes##
##########################
#Get/Post/Put Users#
@app.route('/api/users', methods=['GET','POST','PUT'])
def route_api_users():
	if request.method == 'GET':
		#Getting ALL modules
		modules = DatabaseObj.GetAllUsers()
		return json.dumps(modules)

	elif request.method == 'POST':
		#Inserting new module
		insert_name = request.form['name']
		insert_author = request.form['author']
		insert_filename = request.form['filename']
		insert_status = request.form['status']
		insert_priority = request.form['priority']

		#Writting to SQLite
		result = DatabaseObj.CreateUser(fname,lname,login,password,zipcode,gender)

		#Checking to see if record was updated
		if result:
			return "User successfully inserted."
		else:
			return "System Error. Could not insert user."

	elif request.method == 'PUT':

		#Update current module
		update_id = request.form['id']
		update_name = request.form['name']
		update_author = request.form['author']
		update_filename = request.form['filename']
		update_status = request.form['status']
		update_priority = request.form['priority']

		#Updating SQLite
		result = DatabaseObj.UpdateModule(update_id,update_name,update_author,update_filename,update_status,update_priority)

		#Checking to see if record was updated
		if result:
			return "Module successfully updated."
		else:
			return "System Error. Could not update module."

##########################
## End User Routes##
##########################





#Listen for queries
@app.route('/query', methods=['POST'])
def query_text():
	#Processing submitted requests
	#Posted request parameters are: 
	# -> apikey - str - contains users API Key
	# -> phrase - str - contains users request

	#Verifying request is a POST request
	if request.method == 'POST':

		#Getting POSTED parameters
		request_apikey = request.form['apikey']
		request_phrase = request.form['phrase']

		#Verifying parameters are not blank
		if request_apikey != "" and request_phrase != "":

			#Getting API Keys from SQLite
			db_apikeys = CoreObj.UserAPIKeys

			#Looping through API Keys
			for db_apikey in db_apikeys:

				#DEBUG:
				#print db_apikey

				#Checking if key from DB is key user POSTED
				if request_apikey == db_apikey[0]:
					#Is valid API Key

					#Locating correct response
					response = CoreObj.Main(request_phrase,request_apikey)

					#Returning response to user
					return str(response)

		#Error because:
		# -> Not API Keys in DB
		# -> User POSTED an invalid API Key
		# -> User did not POST API Key
		# -> User did not POST phrase 
		return "Not Authorized"

### End of Routes ###