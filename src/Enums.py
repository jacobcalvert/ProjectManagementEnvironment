##############################################
# Module: Enums
# Author: Jacob Calvert
# Description: The Enums module defines
# application wide enums.
# Dependencies: None
##############################################

class LoggingLevel:
    Info = 1
    Warning = 2
    Error = 3
    Severe = 4
    Fatal = 5
    _DEFAULT_LOG_LEVEL = Info
class MessageReqType:
    LOGIN = 1
    LOGOUT = 2
    GET_NODE = 3
    GET_TREE = 4
