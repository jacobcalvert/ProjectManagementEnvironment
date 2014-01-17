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
class DatabaseTableDefs:
    user_data_table = "CREATE TABLE %s (id TEXT(1000),parent TEXT(1000) ,content TEXT(1000));"
    user_data_map = "CREATE TABLE user_data(username TEXT(1000),table_name TEXT(1000));"
    login = "CREATE TABLE login(username TEXT(1000),passhash TEXT(1000));"

class DatabaseQueries:
    find_user = "SELECT * FROM %s WHERE username='%s' AND passhash='%s'"
    find_username = "SELECT * FROM %s WHERE username='%s'"
    get_user_table_name = "SELECT * FROM user_data WHERE username='%s'"
    get_node = "SELECT * FROM '%s' WHERE parent='%s'"
class DatabaseInsertions:
    new_user_login = "INSERT INTO login VALUES('%s','%s')"
    new_user_data = "INSERT INTO user_data VALUES('%s','%s');"
class AuthToken:
    valid_interval_in_minutes = 0.5
    renew_window_in_seconds = 15