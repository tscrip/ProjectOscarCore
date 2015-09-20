import sqlite3 as sqlite
import sys
import datetime

### Data Access Class ###
class Database():
    def __init__(self):
        self.aiml_file = "app/db/aiml/Custom.aiml"
        self.sql_file = "app/db/sqlite/ProjectOscar.db"
    
    ############################
    ## Module Related Methods ##
    ############################

    #Get ALL enabled modules
    def GetEnabledModules(self):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()
        conn.text_factory = str

        #Modules array values
        #0 - module_id
        #1 - module_name
        #2 - module_type
        #3 - module_filename
        #4 - module_priority
        #5 - module_enabled

        query = "SELECT `Modules`.`module_id`,`Modules`.`module_name`,`Modules`.`module_type`,`Modules`.`module_filename`,`Modules`.`module_priority`,`Modules`.`module_enabled` FROM `Modules` WHERE `Modules`.`module_enabled` = '1' ORDER BY `Modules`.`module_priority`"
        cur.execute(query)
        modules = cur.fetchall()
        conn.close()
        return modules

    #Getting ALL modules
    def GetAllModules(self):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()
        conn.text_factory = str

        #Modules array values
        #0 - module_id
        #1 - module_name
        #2 - module_type
        #3 - module_filename
        #4 - module_priority
        #5 - module_enabled

        query = "SELECT `Modules`.`module_id`,`Modules`.`module_name`,`Modules`.`module_type`,`Modules`.`module_filename`,`Modules`.`module_priority`,`Modules`.`module_enabled` FROM `Modules` ORDER BY `Modules`.`module_priority`"
        cur.execute(query)
        modules = cur.fetchall()
        conn.close()
        return modules

    #Get module by id
    def GetModule(self,module_id):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()
        conn.text_factory = str

        #Modules array values
        #0 - module_id
        #1 - module_name
        #2 - module_type
        #3 - module_filename
        #4 - module_priority
        #5 - module_enabled
        #6 - module_author

        query = "SELECT `Modules`.`module_id`,`Modules`.`module_name`,`Modules`.`module_type`,`Modules`.`module_filename`,`Modules`.`module_priority`,`Modules`.`module_enabled`, `Modules`.`module_enabled` FROM `Modules` WHERE `module_id` = ?"
        cur.execute(query, (module_id,))
        module = cur.fetchone()
        conn.close()
        return module

    #Toggle module status
    def ToggleModuleStatus(self,module_id):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        #Getting Status of module
        select_query = "SELECT `module_enabled` FROM `Modules` WHERE `module_id` = ?"
        cur.execute(select_query, (module_id,))
        current_status = cur.fetchone()

        print str(current_status[0])

        #Changing status
        if int(current_status[0]) == 0:
            #Enabling module
            update_query = "UPDATE `Modules` SET `module_enabled` = '1' WHERE `module_id` = ?"
            status = "Enabled"
        
        elif int(current_status[0]) == 1:
            #Disable module
            update_query = "UPDATE `Modules` SET `module_enabled` = '0' WHERE `module_id` = ?"
            status = "Disabled"

        print status
        cur.execute(update_query, (module_id,))
        conn.commit()
        conn.close()
        return status

    #Create Module in SQLite
    def CreateModule(self,name,author,filename,status,priority):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "INSERT INTO `Modules` (`module_enabled`, `module_type`, `module_author`, `module_priority`, `module_filename`, `module_name`) VALUES(?,'user',?,?,?,?)"
        cur.execute(query, (status,author,priority,filename,name))
        conn.commit()
        conn.close()
        return True

    #Update Module in SQLite
    def UpdateModule(self,module_id,name,author,filename,status,priority):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "UPDATE `Modules` SET `module_enabled`=?, `module_type`='user', `module_author`=?, `module_priority`=?, `module_filename`=?, `module_name`=? WHERE `module_id` = ?"
        cur.execute(query, (status,author,priority,filename,name,module_id))
        conn.commit()
        conn.close()
        return True

    ############################
    ## End Module Methods ##
    ############################

    ###############################
    ## Knowledge Related Methods ##
    ###############################
    #Add knowledge to SQLite DB
    def AddKnowledge(self,phrase,answer,apikey):
        now = datetime.datetime.now()
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "INSERT INTO `Knowledge` (`question`,`answer`,`author`,`creation_date`,`committed`) VALUES (?,?,(SELECT `key_id` FROM `API_Keys` WHERE `key_value` = ?),?,?)"
        cur.execute(query, (phrase,answer,apikey,now.strftime("%Y-%m-%d"),"0"))
        conn.commit()
        conn.close()
        return True

    #Remove knowledge from SQLite DB
    def RemoveLastKnowledge(self,apikey):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        #Creating variables
        select_query = "SELECT * FROM `Knowledge` WHERE `committed` = '0'"
        delete_query = "DELETE FROM `Knowledge` WHERE `committed` = '0' AND `author` = (SELECT `key_id` FROM `API_Keys` WHERE `key_value` = ?)"

        #Checking for non-committed records
        cur.execute(select_query)

        if len(cur.fetchall()) > 0:
            #Records found

            #Deleting last record
            cur.execute(delete_query, (apikey,))
            conn.commit()

            #Closing connection
            conn.close()

            #Returning status of True
            return True

        else:
            #No records

            #Closing connection
            conn.close()

            #Returning status of False
            return False

    #Mark last knowledge as "Committed" in SQLite DB
    def CommitLastKnowledge(self,apikey):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "UPDATE `Knowledge` SET `committed`='1' WHERE `author` = (SELECT `key_id` FROM `API_Keys` WHERE `key_value` = ?) AND `id` = (SELECT `id` FROM `Knowledge` WHERE `committed` = '0'  ORDER BY `id` DESC LIMIT 1)"
        cur.execute(query, (apikey,))
        conn.commit()
        conn.close()
        return True

    #Get last knowledge from SQLite DB
    def GetLastKnowledge(self,apikey):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()
        conn.text_factory = str

        query = "SELECT `question`, `answer` FROM `Knowledge` WHERE `committed` = '0' AND `author` = (SELECT `key_id` FROM `API_Keys` WHERE `key_value` = ?) ORDER BY `id` DESC LIMIT 1"
        cur.execute(query, (apikey,))
        knowledge = cur.fetchone()
        conn.close()
        return knowledge

    ###########################
    ## End Knowledge Methods ##
    ###########################


    ##########################
    ## AIML Related Methods ##
    ##########################
    #Write last SQLite entry to AIML DB
    def WriteLastToAIML(self,apikey):
        import aiml
        from xml.dom.minidom import parse

        #Creating object
        DatabaseObj = Database()


        returnval = DatabaseObj.GetLastKnowledge(apikey)
        commitval = DatabaseObj.CommitLastKnowledge(apikey)
        
        #Checking to see if there is a LastKnowledge
        if returnval != None:
            #There is a LastKnowledge

            #Getting phrase and answer
            phrase = str(returnval[0])
            answer = str(returnval[1])
            
            #Opening AIML file
            dom = parse(aiml_file)

            #Creating elements
            category = dom.createElement("category")
            pattern = dom.createElement("pattern")
            template = dom.createElement("template")

            #Creating nodes
            pattern_text = dom.createTextNode(phrase.upper())
            template_text = dom.createTextNode(answer)

            #Building XML string
            pattern.appendChild(pattern_text)
            template.appendChild(template_text)
            category.appendChild(pattern)
            category.appendChild(template)
            dom.childNodes[0].appendChild(category)

            #Writing XML string to file
            with open(self.aiml_file, "wb") as f:
                #dom.writexml(f)
                f.write(dom.toprettyxml(indent='  ', newl='\r', encoding="utf-8"))

            #Returning True
            return True
        else:
            #There is no LastKnowledge

            return False


    #NEED TO BUILD!
    #Clean up AIML XML
    def CleanUpXML(self):
        print "Here"

    ######################
    ## End AIML Methods ##
    ######################

    ##########################
    ## User Related Methods ##
    ##########################
     #Get ALL users
    def GetAllUsers(self,apikey):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()
        conn.text_factory = str

        query = "SELECT `user_fname` AS `fname`,`user_lname` AS `lname`, `user_login` AS `login`, `user_password` AS `pass`, `user_zipcode` AS `zip`, `user_gender` AS `gender` FROM `Users` WHERE `user_id` = (SELECT `key_user_id` FROM `API_Keys` WHERE `key_value` = ?)"
        cur.execute(query, (apikey,))
        userinfo = cur.fetchone()
        conn.close()
        return userinfo

    #Get user by API key
    def GetUserbyAPIKey(self,apikey):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()
        conn.text_factory = str

        query = "SELECT `user_fname` AS `fname`,`user_lname` AS `lname`, `user_login` AS `login`, `user_password` AS `pass`, `user_zipcode` AS `zip`, `user_gender` AS `gender` FROM `Users` WHERE `user_id` = (SELECT `key_user_id` FROM `API_Keys` WHERE `key_value` = ?)"
        cur.execute(query, (apikey,))
        userinfo = cur.fetchone()
        conn.close()
        return userinfo

    #Create user
    def CreateUser(self,fname,lname,login,password,zipcode,gender):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "INSERT INTO `Users` (`user_fname`,`users_lname`,`user_login`,`user_password`,`user_zipcode`,`user_gender`) VALUES (?,?,?,?,?,?)"
        cur.execute(query, (fname,lname,login,password,zipcode,gender))
        conn.commit()
        conn.close()
        return True
        
    #Deleting User
    def DeleteUser(self,uid):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "DELETE FROM `Users` WHERE `user_id` = '?'"
        cur.execute(query, (uid))
        conn.commit()
        conn.close()

    #Update User by username
    def UpdateUser(self,fname,lname,login,password,zipcode,gender):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "UPDATE `Users` SET `user_fname`='?', `users_lname`='?', `user_password`='?', `user_zipcode`='?', `user_gender`='?' WHERE `user_login`='?'"
        cur.execute(query, (fname,lname,password,zipcode,gender,login))
        conn.commit()
        conn.close()
        return True
   
    ######################
    ## End User Methods ##
    ######################

    #########################
    ## API Related Methods ##
    #########################
    #Get Enabled API Keys
    def GetAPIKeys(self):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()
        conn.text_factory = str

        query = "SELECT `key_value` FROM `API_Keys` WHERE `key_enabled` = 1"
        cur.execute(query)
        apikeys = cur.fetchall()
        conn.close()

        return apikeys

    #Create API Key
    def CreateAPIKey(self,fname,lname,login,password,zipcode,gender):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "INSERT INTO `Users` (`user_fname`,`users_lname`,`user_login`,`user_password`,`user_zipcode`,`user_gender`) VALUES (?,?,?,?,?,?)"
        cur.execute(self.query, (fname,lname,login,password,zipcode,gender))
        conn.commit()
        conn.close()
        return True
        
    #Delete API Key
    def DeleteAPIKey(self,uid):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "DELETE FROM `Users` WHERE `user_id` = '?'"
        cur.execute(query, (uid))
        conn.commit()
        conn.close()

    #Update API Key
    def UpdateAPIKey(self,fname,lname,login,password,zipcode,gender):
        conn = sqlite.connect(self.sql_file)
        cur = conn.cursor()

        query = "UPDATE `Users` SET `user_fname`='?', `users_lname`='?', `user_login`='?',`user_password`='?',`user_zipcode`='?',`user_gender`='?'"
        cur.execute(query, (fname,lname,login,password,zipcode,gender))
        conn.commit()
        conn.close()
        return True
    #####################
    ## End API Methods ##
    #####################