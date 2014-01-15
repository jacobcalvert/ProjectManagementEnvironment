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
    def __init__(self,ws_handle):
        Logging.instance().log("USER: User instantiated.")
        self.__username = None
        self.__passhash = None
        self.__auth_token = None
        self.__expiry = None
        self.__authenticated = False
        self.__ws = ws_handle
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


class UserComponent:
    __INST__ = None
    def __init__(self):
        UserComponent.__INST__ = self
        Logging.instance().log("USERCOMP: usercomp initialized.")
        self.__users = {}
    @staticmethod
    def create_instance():
        UserComponent()
    @staticmethod
    def instance():
        return UserComponent.__INST__
    def find(self, ws_handle):
        if ws_handle in self.__users:
            return self.__users[ws_handle]
        else:
            return False
    def add_user(self,ws_handle,user_obj):
        self.__users[ws_handle] = user_obj
    def del_user(self,ws_handle):
        if ws_handle in self.__users:
            del self.__users[ws_handle]
