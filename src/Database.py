##############################################
# Module: Database
# Author: Jacob Calvert
# Description: The Database component is an
# abstraction layer for the functionality that
# will be needed later. The final implementation
# WILL be different. Just plain text for now.
# Dependencies: Utils.py,sqlite3,os,Enums,json,random
##############################################
import Utils
import sqlite3
import Enums
import os
import hashlib
import json
import random
class UserDB:
    __INST__ = None
    def __init__(self):
        UserDB.__INST__ = self
        if(not os.path.isfile("users.db")):
            self.__create_db()
        else:
            self.__db_con = sqlite3.connect("users.db")
            self.__cursor = self.__db_con.cursor()
        Utils.Logging.instance().log("USERDB: userdb initialized.")
    @staticmethod
    def create_instance():
        UserDB()
    @staticmethod
    def instance():
        return UserDB.__INST__
    def __create_db(self):
        self.__db_con = sqlite3.connect("users.db")
        self.__cursor = self.__db_con.cursor()
        self.__cursor.execute(Enums.DatabaseTableDefs.login)
        self.__cursor.execute(Enums.DatabaseTableDefs.user_data_map)
        self.__db_con.commit()
    def find_user(self,username, passhash):
        results = self.__cursor.execute(Enums.DatabaseQueries.find_user % ("login",username,passhash))
        rows = [res for res in results]
        if(len(rows) == 1):
            return True
    def new_user(self,username,passhash):
        if(not self.username_exists(username)):
            new_table = hashlib.sha256(username+passhash).hexdigest()
            new_table_sanitized = self.__sanitize_table(str(new_table))  # HACK: SQL doesn't like table names beginning
                                                                         # with a digit.
            self.__cursor.execute(Enums.DatabaseInsertions.new_user_login % (username,passhash))
            self.__cursor.execute(Enums.DatabaseInsertions.new_user_data % (username,new_table_sanitized))
            self.__db_con.commit()
            DataDB.instance().new_user(new_table_sanitized)

    def username_exists(self,username):
        results = self.__cursor.execute(Enums.DatabaseQueries.find_username % ("login",username))
        rows = [res for res in results]
        if(len(rows) != 0):
            return True
    def __sanitize_table(self,table):
        i = 0
        char_found = False
        while(True):
            if(table[i].isalpha()):
                break
            else:
                i+=1
        return table[i:]
    def get_user_table(self,username):
        results = self.__cursor.execute(Enums.DatabaseQueries.get_user_table_name % (username))
        rows = [res for res in results]
        if(len(rows)==1):
            return rows[0][1]
class DataDB:
    __INST__ = None
    def __init__(self):
        DataDB.__INST__ = self
        if(not os.path.isfile("data.db")):
            self.__create_db()
        else:
            self.__db_con = sqlite3.connect("data.db")
            self.__cursor = self.__db_con.cursor()
        Utils.Logging.instance().log("DATADB: datadb initialized.")
    @staticmethod
    def create_instance():
        DataDB()
    @staticmethod
    def instance():
        return DataDB.__INST__
    def __create_db(self):
        self.__db_con = sqlite3.connect("data.db")
        self.__cursor = self.__db_con.cursor()
        self.__db_con.commit()

    def new_user(self,table_name):
        sql = Enums.DatabaseTableDefs.user_data_table % (table_name)
        print sql
        sql = str(sql)
        self.__cursor.execute(sql)
        self.__db_con.commit()
    def get_node(self,table,node_id):
        results = self.__cursor.execute(Enums.DatabaseQueries.get_node % (table,node_id))
        rows = [row for row in results]
        result = []
        for i in range(len(rows)):
            result.append({"id":rows[i][0],"parent":rows[i][1],"content":rows[i][2]})
        return result
    def delete_node(self,table_name,node_id):
        pass # we'll need to recursively search down the tree and find every node under the node being deleted and then
             # delete them all.
    def insert_node(self,table,node_id,parent_node,content):
        content = json.dumps(content)
        self.__cursor.execute(Enums.DatabaseInsertions.new_node % (table,node_id,parent_node,content))
        self.__db_con.commit()