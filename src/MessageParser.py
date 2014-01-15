##############################################
# Module: MessageParser
# Author: Jacob Calvert
# Description: The MessageParser module provides
# methods to parse and process incoming messages.
# Dependencies: Utils.py,json,Enums.py
##############################################
from Utils import Logging
import json
import Enums
class MessageParser:
    __INST__ = None
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

            ok = self._ph_is_object_formatted(jObj)
            if(ok):
                message_obj = self._ph_do_parse(jObj)
                if(message_obj.valid):
                    self._ph_process_message(message_obj,user_obj)

    def _ph_is_object_formatted(self,jObj):
        if("req_type" in jObj):
            if(jObj["req_type"] == "login"):
                if("username" in jObj and "passhash" in jObj):
                    return True
            else:
                if("auth_token" in jObj):
                    return True
    def _ph_do_parse(self,jObj):
        msg = Message()
        if(jObj["req_type"] == "login"):
            msg.set_req_type(Enums.MessageReqType.LOGIN)
            msg.username = jObj["username"]
            msg.passhass = jObj["passhash"]
        elif(jObj["req_type"] == "logout"):
            msg.set_req_type(Enums.MessageReqType.LOGOUT)
            msg.auth_token = jObj["auth_token"]
        elif(jObj["req_type"] == "get_node"):
            msg.set_req_type(Enums.MessageReqType.GET_NODE)
            msg.auth_token = jObj["auth_token"]
            msg.node_id = jObj["node_id"]
        else:
            msg.valid = False
        return msg
    def _ph_process_message(self,message,user):
        if(message.get_req_type() != Enums.MessageReqType.LOGIN and message.auth_token == user.auth_token()):
            #auth'd
            pass


class Message:
    def __init__(self):
        self.__req_type = None
        self.valid = True
    def set_req_type(self,req_type):
        self.__req_type = req_type
    def get_req_type(self):
        return self.__req_type
