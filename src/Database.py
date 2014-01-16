##############################################
# Module: Database
# Author: Jacob Calvert
# Description: The Database component is an
# abstraction layer for the functionality that
# will be needed later. The final implementation
# WILL be different. Just plain text for now.
# Dependencies: Utils.py,sqlite3,os,Enums,hashlib
##############################################
import Utils
import sqlite3
import Enums
import os
import hashlib
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
            self.__cursor.execute(Enums.DatabaseInsertions.new_user_login % (username,passhash))
            self.__cursor.execute(Enums.DatabaseInsertions.new_user_data % (username,new_table))
            self.__db_con.commit()
            DataDB.instance().new_user(new_table)
    def username_exists(self,username):
        results = self.__cursor.execute(Enums.DatabaseQueries.find_username % ("login",username))
        rows = [res for res in results]
        if(len(rows) != 0):
            return True
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
        self.__cursor.execute(Enums.DatabaseTableDefs.user_data_table % (table_name))
        self.__db_con.commit()
    def get_node(self,table,node_id):
        results = self.__cursor.execute(Enums.DatabaseQueries.get_node % (table,node_id))
        rows = [row for row in results]
        return rows
