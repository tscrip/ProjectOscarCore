import sqlite3 as sqlite
import sys
import datetime

### Data Access Class ###
class Database():
    def __init__(self):
        self.aiml_file = "app/db/aiml/Custom.aiml"
        self.sql_file = "app/db/sqlite/ProjectOscar.db"
    
    ### Modules Methods ###
    #Used to get modules from SQLite DB
    def GetEnabledModules(self):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()
        self.conn.text_factory = str

        #Modules array values
        #0 - module_id
        #1 - module_name
        #2 - module_type
        #3 - module_filename
        #4 - module_priority
        #5 - module_enabled

        self.query = "SELECT `Modules`.`module_id`,`Modules`.`module_name`,`Modules`.`module_type`,`Modules`.`module_filename`,`Modules`.`module_priority`,`Modules`.`module_enabled` FROM `Modules` WHERE `Modules`.`module_enabled` = '1' ORDER BY `Modules`.`module_priority`"
        self.cur.execute(self.query)
        self.modules = self.cur.fetchall()
        self.conn.close()
        return self.modules
    ### End of Methods ###

    ### Knowledge Methods ###
    #Used to add knowledge to the SQLite DB
    def AddKnowledge(self,phrase,answer,apikey):
        self.now = datetime.datetime.now()
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "INSERT INTO `Knowledge` (`question`,`answer`,`author`,`creation_date`,`committed`) VALUES (?,?,(SELECT `key_id` FROM `API_Keys` WHERE `key_value` = ?),?,?)"
        self.cur.execute(self.query, (phrase,answer,apikey,self.now.strftime("%Y-%m-%d"),"0"))
        self.conn.commit()
        self.conn.close()
        return True

    #Used to remove knowledge from SQLite DB
    def RemoveLastKnowledge(self,apikey):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        #Creating variables
        self.select_query = "SELECT * FROM `Knowledge` WHERE `committed` = '0'"
        self.delete_query = "DELETE FROM `Knowledge` WHERE `committed` = '0' AND `author` = (SELECT `key_id` FROM `API_Keys` WHERE `key_value` = ?)"

        #Checking for non-committed records
        self.cur.execute(self.select_query)

        if len(self.cur.fetchall()) > 0:
            #Records found

            #Deleting last record
            self.cur.execute(self.delete_query, (apikey,))
            self.conn.commit()

            #Closing connection
            self.conn.close()

            #Returning status of True
            return True

        else:
            #No records

            #Closing connection
            self.conn.close()

            #Returning status of False
            return False

    #Used to mark last knowledge as "Committed" in SQLite DB
    def CommitLastKnowledge(self,apikey):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "UPDATE `Knowledge` SET `committed`='1' WHERE `author` = (SELECT `key_id` FROM `API_Keys` WHERE `key_value` = ?) AND `id` = (SELECT `id` FROM `Knowledge` WHERE `committed` = '0'  ORDER BY `id` DESC LIMIT 1)"
        self.cur.execute(self.query, (apikey,))
        self.conn.commit()
        self.conn.close()
        return True

    #Used to get last knowledge from SQLite DB
    def GetLastKnowledge(self,apikey):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()
        self.conn.text_factory = str

        self.query = "SELECT `question`, `answer` FROM `Knowledge` WHERE `committed` = '0' AND `author` = (SELECT `key_id` FROM `API_Keys` WHERE `key_value` = ?) ORDER BY `id` DESC LIMIT 1"
        self.cur.execute(self.query, (apikey,))
        self.knowledge = self.cur.fetchone()
        self.conn.close()
        return self.knowledge

    ### End of Knowledge ###


    ### AIML Methods ###
    #Used to write last SQLite to AIML DB
    def WriteLastToAIML(self,apikey):
        import aiml
        from xml.dom.minidom import parse

        #Creating object
        DatabaseObj = Database()


        self.returnval = DatabaseObj.GetLastKnowledge(apikey)
        self.commitval = DatabaseObj.CommitLastKnowledge(apikey)
        
        #Checking to see if there is a LastKnowledge
        if self.returnval != None:
            #There is a LastKnowledge

            #Getting phrase and answer
            self.phrase = str(self.returnval[0])
            self.answer = str(self.returnval[1])
            
            #Opening AIML file
            self.dom = parse(self.aiml_file)

            #Creating elements
            self.category = self.dom.createElement("category")
            self.pattern = self.dom.createElement("pattern")
            self.template = self.dom.createElement("template")

            #Creating nodes
            self.pattern_text = self.dom.createTextNode(self.phrase.upper())
            self.template_text = self.dom.createTextNode(self.answer)

            #Building XML string
            self.pattern.appendChild(self.pattern_text)
            self.template.appendChild(self.template_text)
            self.category.appendChild(self.pattern)
            self.category.appendChild(self.template)
            self.dom.childNodes[0].appendChild(self.category)

            #Writing XML string to file
            with open(self.aiml_file, "wb") as f:
                #dom.writexml(f)
                f.write(self.dom.toprettyxml(indent='  ', newl='\r', encoding="utf-8"))

            #Returning True
            return True
        else:
            #There is no LastKnowledge

            return False



    #Used to clear up AIML XML
    def CleanUpXML(self):
        print "Here"


    ### End of AIML Methods ###

    ### Users Methods ###
    #Create User
    def GetUserbyAPIKey(self,apikey):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()
        self.conn.text_factory = str

        self.query = "SELECT `user_fname` AS `fname`,`user_lname` AS `lname`, `user_login` AS `login`, `user_password` AS `pass`, `user_zipcode` AS `zip`, `user_gender` AS `gender` FROM `Users` WHERE `user_id` = (SELECT `key_user_id` FROM `API_Keys` WHERE `key_value` = ?)"
        self.cur.execute(self.query, (apikey,))
        self.userinfo = self.cur.fetchone()
        self.conn.close()
        return self.userinfo

    def CreateUser(self,fname,lname,login,password,zipcode,gender):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "INSERT INTO `Users` (`user_fname`,`users_lname`,`user_login`,`user_password`,`user_zipcode`,`user_gender`) VALUES (?,?,?,?,?,?)"
        self.cur.execute(self.query, (fname,lname,login,password,zipcode,gender))
        self.conn.commit()
        self.conn.close()
        return True
        
    #Deleting User
    def DeleteUser(self,uid):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "DELETE FROM `Users` WHERE `user_id` = '?'"
        self.cur.execute(self.query, (uid))
        self.conn.commit()
        self.conn.close()

    #Update User
    def UpdateUser(self,fname,lname,login,password,zipcode,gender):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "UPDATE `Users` SET `user_fname`='?', `users_lname`='?', `user_login`='?',`user_password`='?',`user_zipcode`='?',`user_gender`='?'"
        self.cur.execute(self.query, (fname,lname,login,password,zipcode,gender))
        self.conn.commit()
        self.conn.close()
        return True
    ### End of Users Methods ###

    ### API Key Methods ###
    #Get Enabled API Keys
    def GetAPIKeys(self):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()
        self.conn.text_factory = str

        self.query = "SELECT `key_value` FROM `API_Keys` WHERE `key_enabled` = 1"
        self.cur.execute(self.query)
        self.apikeys = self.cur.fetchall()
        self.conn.close()

        return self.apikeys

    #Create API Key
    def CreateUser(self,fname,lname,login,password,zipcode,gender):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "INSERT INTO `Users` (`user_fname`,`users_lname`,`user_login`,`user_password`,`user_zipcode`,`user_gender`) VALUES (?,?,?,?,?,?)"
        self.cur.execute(self.query, (fname,lname,login,password,zipcode,gender))
        self.conn.commit()
        self.conn.close()
        return True
        
    #Delete API Key
    def DeleteUser(self,uid):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "DELETE FROM `Users` WHERE `user_id` = '?'"
        self.cur.execute(self.query, (uid))
        self.conn.commit()
        self.conn.close()

    #Update API Key
    def UpdateUser(self,fname,lname,login,password,zipcode,gender):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "UPDATE `Users` SET `user_fname`='?', `users_lname`='?', `user_login`='?',`user_password`='?',`user_zipcode`='?',`user_gender`='?'"
        self.cur.execute(self.query, (fname,lname,login,password,zipcode,gender))
        self.conn.commit()
        self.conn.close()
        return True
    ### End of API Key Methods ###

    ### Web Methods ###
    #Getting ALL modules
    def GetAllModules(self):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()
        self.conn.text_factory = str

        #Modules array values
        #0 - module_id
        #1 - module_name
        #2 - module_type
        #3 - module_filename
        #4 - module_priority
        #5 - module_enabled

        self.query = "SELECT `Modules`.`module_id`,`Modules`.`module_name`,`Modules`.`module_type`,`Modules`.`module_filename`,`Modules`.`module_priority`,`Modules`.`module_enabled` FROM `Modules` ORDER BY `Modules`.`module_priority`"
        self.cur.execute(self.query)
        self.modules = self.cur.fetchall()
        self.conn.close()
        return self.modules

    #Get module my id
    def GetModule(self,module_id):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()
        self.conn.text_factory = str

        #Modules array values
        #0 - module_id
        #1 - module_name
        #2 - module_type
        #3 - module_filename
        #4 - module_priority
        #5 - module_enabled
        #6 - module_author

        self.query = "SELECT `Modules`.`module_id`,`Modules`.`module_name`,`Modules`.`module_type`,`Modules`.`module_filename`,`Modules`.`module_priority`,`Modules`.`module_enabled`, `Modules`.`module_enabled` FROM `Modules` WHERE `module_id` = ?"
        self.cur.execute(self.query, (module_id,))
        self.module = self.cur.fetchone()
        self.conn.close()
        return self.module

    #Disable module
    def ToggleModuleStatus(self,module_id):
        self.conn = sqlite.connect(self.sql_file, check_same_thread = False)
        self.cur = self.conn.cursor()

        #Getting Status of module
        self.select_query = "SELECT `module_enabled` FROM `Modules` WHERE `module_id` = ?"
        self.cur.execute(self.select_query, (module_id,))
        self.current_status = self.cur.fetchone()

        print str(self.current_status[0])

        #Changing status
        if int(self.current_status[0]) == 0:
            #Enabling module
            self.update_query = "UPDATE `Modules` SET `module_enabled` = '1' WHERE `module_id` = ?"
            self.status = "Enabled"
        
        elif int(self.current_status[0]) == 1:
            #Disable module
            self.update_query = "UPDATE `Modules` SET `module_enabled` = '0' WHERE `module_id` = ?"
            self.status = "Disabled"

        print self.status
        self.cur.execute(self.update_query, (module_id,))
        self.conn.commit()
        self.conn.close()
        return self.status

    #Create Module in SQLite
    def CreateModule(self,name,author,filename,status,priority):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "INSERT INTO `Modules` (`module_enabled`, `module_type`, `module_author`, `module_priority`, `module_filename`, `module_name`) VALUES(?,'user',?,?,?,?)"
        self.cur.execute(self.query, (status,author,priority,filename,name))
        self.conn.commit()
        self.conn.close()
        return True

    #Update Module in SQLite
    def UpdateModule(self,module_id,name,author,filename,status,priority):
        self.conn = sqlite.connect(self.sql_file)
        self.cur = self.conn.cursor()

        self.query = "UPDATE `Modules` SET `module_enabled`=?, `module_type`='user', `module_author`=?, `module_priority`=?, `module_filename`=?, `module_name`=? WHERE `module_id` = ?"
        self.cur.execute(self.query, (status,author,priority,filename,name,module_id))
        self.conn.commit()
        self.conn.close()
        return True

class API_Keys(db.model):
    key_id = db.Column(db.Integer, primary_key=True)
    key_user_id = db.Column(db.Integer)
    key_value = db.Column(db.String(64), unique=True)
    key_devicename = db.Column(db.String(64), unique=True)
    key_enabled = db.Column(db.Boolean, default=True)

class Knowledge(db.model):
    knowledge_id = db.Column(db.Integer, primary_key=True)
    knowledge_question = db.Column(db.String(256))
    knowledge_answer = db.Column(db.String(256))
    knowledge_author = db.Column(db.String(64))
    knowledge_committed = db.Column(db.Boolean, default=False)
    knowledge_creation_date = db.Column(db.String(64))


class Modules(db.model):
    module_id = db.Column(db.Integer, primary_key=True)
    module_type = db.Column(db.String(10))
    module_author = db.Column(db.String(64))
    module_priority = db.Column(db.Integer(3))
    module_filename = db.Column(db.String(64), unique=True)
    module_name = db.Column(db.String(64), unique=True)
    module_enabled = db.Column(db.Boolean, default=True)

class Users(db.model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_fname= db.Column(db.String(64))
    user_lname = db.Column(db.String(64))
    user_login = db.Column(db.String(64))
    user_password = db.Column(db.String(64))
    user_zipcode = db.Column(db.Integer(5))
    user_gender = db.Column(db.Integer(1))



    ### End of Methods ###