###############################################################################
##
##  Copyright 2011 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import sys

if sys.platform in ['freebsd8']:
   from twisted.internet import kqreactor
   kqreactor.install()

if sys.platform in ['win32']:
   from twisted.application.reactors import installReactor
   installReactor("iocp")

import sys
from twisted.python import log
from twisted.internet import reactor, ssl
from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS


class WebSocketTestServerProtocol(WebSocketServerProtocol):

   def onMessage(self, msg, binary):
      self.sendMessage(msg, binary)


if __name__ == '__main__':

   log.startLogging(sys.stdout)

   ## SSL server context: load server key and certificate
   ##
   contextFactory = ssl.DefaultOpenSSLContextFactory('keys/server.key', 'keys/server.crt')

   ## create a WS server factory with our protocol
   ##
   factory = WebSocketServerFactory("wss://localhost:9000", debug = False)
   factory.setProtocolOptions(failByDrop = False)
   factory.protocol = WebSocketTestServerProtocol

   ## Listen for incoming WebSocket connections: wss://localhost:9000
   ##
   listenWS(factory, contextFactory)

   log.msg("Using Twisted reactor class %s" % str(reactor.__class__))
   reactor.run()
