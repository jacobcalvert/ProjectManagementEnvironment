##############################################
# Module: Utils
# Author: Jacob Calvert
# Description: The Utils module defines objects
# for logging and other utilities.
# Dependencies: Enums.py, time, datetime
##############################################
import Enums
import time
import datetime
class Logging:
    # This class is sort of a singleton, we don't need 10 Logging
    # objects running around. It is created with 'create_instance'
    # and the instance is retrieved with 'instance()'. 
    __INST__ = None
    def __init__(self,file_name,log_lev):
        self.__INST__ = self
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
