##############################################
# Module: User
# Author: Jacob Calvert
# Description: The User module defines an object
# for user auth and account tracking
# Dependencies: Utils.py
##############################################
from Utils import Logging
class User:
    def __init__(self):
        Logging.instance().log("USER: User instantiated.")
