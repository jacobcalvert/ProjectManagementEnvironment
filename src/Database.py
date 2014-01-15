##############################################
# Module: Database
# Author: Jacob Calvert
# Description: The Database component is an
# abstraction layer for the functionality that
# will be needed later. The final implementation
# WILL be different. Just plain text for now.
# Dependencies: Utils.py
##############################################
import Utils
class UserDB:
    __INST__ = None
    def __init__(self):
        UserDB.__INST__ = self
        self.__fp = open("users.db","r")
        self.reload()
        Utils.Logging.instance().log("USERDB: userdb initialized.")
    @staticmethod
    def create_instance():
        UserDB()
    @staticmethod
    def instance():
        return UserDB.__INST__
    def reload(self):
        content = self.__fp.read()
        content = content.split("\n")
        content = content[:-1]
        self.__entries = {}
        for c in content:
            r = c.split(",")
            self.__entries[r[0]] = r[1]


    def find_user(self,username, passhash):
        self.reload()
        if(username in self.__entries):
            if(self.__entries[username] == passhash):
                return True

class DataDB:
    pass