##############################################
# Module: Server
# Author: Jacob Calvert
# Description: The server module implements
# the connection handlers for the WebSocket
# transport layer. It also houses the entry point
# for the application.
# Dependencies: Tornado.py, User.py, Utils.py, Database.py, MessageParser.py, threading
##############################################

import tornado.websocket
import tornado.web
from Utils import Logging
import Database
from User import *
from MessageParser import *
class WS_Handler(tornado.websocket.WebSocketHandler):
    # open          - instantiate user, await authentication
    # on_message    - check user auth, parse message
    # on_close      - safely exit user session
    def open(self):
        Logging.instance().log("SERVER: Websocket connection opened.")
        user = User(self)
        UserComponent.instance().add_user(self,user)

    def on_message(self, message):
        user = UserComponent.instance().find(self)
        if(user):
            MessageParser.instance().parse(message,user)
        else:
            Logging.instance().log("SERVER: rx'd message from unknown client location!!") # this is bad.
    def on_close(self):
        Logging.instance().log("SERVER: Websocket connection closed.")
        UserComponent.instance().del_user(self)
class NewUserHandler(tornado.web.RequestHandler):
    def post(self):
        username = self.get_argument("username")
        passhash = self.get_argument("passhash")
        if(not Database.UserDB.instance().username_exists(username)):
            Database.UserDB.instance().new_user(username,passhash)
            self.write("True")
        else:
            self.write("False")



def main():
    Logging.create_instance("PME.log")
    Authenticator.create_instance()
    Database.UserDB.create_instance()
    Database.DataDB.create_instance()
    UserComponent.create_instance()
    MessageParser.create_instance()
    #tornado config
    app = tornado.web.Application([
        (r"/ws", WS_Handler),
        (r"/new_user", NewUserHandler),
        ])
    app.listen(8022)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()