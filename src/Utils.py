##############################################
# Module: Utils
# Author: Jacob Calvert
# Description: The Utils module defines objects
# for logging,authentication, and other utilities.
# Dependencies: Enums.py, Database.py,time, datetime,hashlib
##############################################
import Enums
import Database
import time
import datetime
import hashlib
class Logging:
    # This class is sort of a singleton, we don't need 10 Logging
    # objects running around. It is created with 'create_instance'
    # and the instance is retrieved with 'instance()'.
    __INST__ = None
    def __init__(self,file_name,log_lev):
        Logging.__INST__ = self
        self.__fn = file_name
        self.__fp = open(file_name,"a",0)
        self.__log_lev = log_lev
        self.log("LOGGER: Logging initialized.")
    @staticmethod
    def create_instance(file_name, logging_level = Enums.LoggingLevel.Info):
        Logging(file_name,logging_level)
    @staticmethod
    def instance():
        return Logging.__INST__
    def log(self,event_line,level = Enums.LoggingLevel._DEFAULT_LOG_LEVEL):
        if(level<= self.__log_lev):
            if(self.__fp.closed):
                self.__fp = open(self.__fn,"a",0)
            self.__fp.write(self._timestamp()+" - " +str(event_line)+"\n")

    def _timestamp(self):
        t = time.time()
        return datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
class CredentialSet:
    TYPE = "Cred"
    def __init__(self,username,passhash):
        self.__un = username
        self.__ph = passhash
    def user(self):
        return self.__un
    def passhash(self):
        return self.__ph
class Authenticator:
    # This class is sort of a singleton, we don't need 10 Auth
    # objects running around. It is created with 'create_instance'
    # and the instance is retrieved with 'instance()'. Its purpose
    # is to provide authentication methods for users.
    __INST__ = None
    def __init__(self):
        Authenticator.__INST__ = self
        Logging.instance().log("AUTH: auth initialized.")
    @staticmethod
    def create_instance():
        Authenticator()
    @staticmethod
    def instance():
        return Authenticator.__INST__
    def authenticate(self,user_obj,credential_obj):
        result = Database.UserDB.instance().find_user(credential_obj.user(),credential_obj.passhash())
        if(result == True):
            #authenticate
            hash = hashlib.sha512(str(time.time())+credential_obj.user).hexdigest()
            user_obj.authenticated(hash,time.time()+(15*60),credential_obj.user(),credential_obj.passhash())


