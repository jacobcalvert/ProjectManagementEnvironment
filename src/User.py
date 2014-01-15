##############################################
# Module: User
# Author: Jacob Calvert
# Description: The User module defines an object
# for user auth and account tracking
# Dependencies: Utils.py, time
##############################################
from Utils import Logging
import time
class User:
    TYPE = "User"
    def __init__(self):
        Logging.instance().log("USER: User instantiated.")
        self.__username = None
        self.__passhash = None
        self.__auth_token = None
        self.__expiry = None
        self.__authenticated = False
    def authenticated(self,token,expires,user_name,passhash):
        self.__auth_token = token
        self.__expiry = expires
        self.__username = user_name
        self.__passhash = passhash
        self.__authenticated = True
    def expired(self):
        if(self.__expiry == None or self.__expiry < time.time()):
            return True
    def is_authenticated(self):
        return self.__authenticated


