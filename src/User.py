##############################################
# Module: User
# Author: Jacob Calvert
# Description: The User module defines an object
# for user auth and account tracking
# Dependencies: Utils.py, time,Enums
##############################################
from Utils import Logging
import time
import Enums
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
    def needs_reauth(self):
        if(self.__authenticated and self.__expiry - time.time() < Enums.AuthToken.renew_window_in_seconds and not self.is_expired()):
            return True
    def is_expired(self):
        if(time.time() > self.__expiry):
            self.__authenticated = False
            self.__auth_token = None
            self.__expiry = None
            return True
    def is_authenticated(self):
        return self.__authenticated
    def auth_token(self):
        return self.__auth_token
    def user(self):
        return self.__username
    def passhash(self):
        return self.__passhash
    def ws(self):
        return self.__ws
    def __str__(self):
        s = ""
        s+= "USER"
        s+= "  username: %-30s\n" %(self.__username)
        s+= "  passhash: %-30s\n" %(self.__passhash)
        s+= "  auth_tok: %-30s\n" %(self.__auth_token)
        s+= "  expiry:   %-30s\n" %(self.__expiry)
        s+= "  current:  %-30s\n" %(time.time())
        s+= "  exp_diff: %-30s\n" %(self.__expiry - time.time())
        s+= "  auth'd:   %-30s\n" %(self.__authenticated)
        return s


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
