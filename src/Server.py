##############################################
# Module: Server
# Author: Jacob Calvert
# Description: The server module implements
# the connection handlers for the WebSocket
# transport layer. It also houses the entry point
# for the application.
# Dependencies: Tornado.py, User.py, Utils.py
##############################################

import tornado.websocket
from Utils import *
import User

class WS_Handler(tornado.websocket.WebSocketHandler):
    # open          - instantiate user, await authentication
    # on_message    - check user auth, parse message
    # on_close      - safely exit user session
    def open(self):
        Logging.instance().log("SERVER: Websocket connection opened.")

    def on_message(self, message):
        pass
    def on_close(self):
        Logging.instance().log("SERVER: Websocket connection closed.")





def main():
    Logging.create_instance("PME.log")
if __name__ == "__main__":
    main()