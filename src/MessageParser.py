##############################################
# Module: MessageParser
# Author: Jacob Calvert
# Description: The MessageParser module provides
# methods to parse and process incoming messages.
# Dependencies: Utils.py,json
##############################################
from Utils import Logging
import json
class MessageParser:
    _INST__ = None
    def __init__(self):
        MessageParser.__INST__ = self
        Logging.instance().log("PARSER: messageparser initialized.")
    @staticmethod
    def create_instance():
        MessageParser()
    @staticmethod
    def instance():
        return MessageParser.__INST__
    def parse(self,raw_message,user_obj):
        jObj = None
        try:
            jObj = json.loads(raw_message)
        except Exception, err:
            Logging.instance().log("PARSER: Invalid json object with message (%s)" % (raw_message))
        if(jObj):
            #message parsed ok
            ok = True
            ok &= self._ph_is_object_formatted(jObj)\

    def _ph_is_object_formatted(self,jObj):
        if("req_type" in jObj):
            if("req_type" == "login"):
                if("username" in jObj and "passhash" in jObj):
                    return True
            else:
                if("auth_token" in jObj):
                    return True
