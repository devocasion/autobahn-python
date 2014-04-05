###############################################################################
##
##  Copyright (C) 2014 Tavendo GmbH
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

import datetime

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession

from calculator import Calculator


## WAMP application component with our app code.
##
class Component1(ApplicationSession):

   def __init__(self, config):
      ApplicationSession.__init__(self)
      self.config = config

   def onConnect(self):
      self.join(self.config.realm)

   @inlineCallbacks
   def onJoin(self, details):

      ## register a function that can be called remotely
      ##
      def utcnow():
         now = datetime.datetime.utcnow()
         return now.strftime("%Y-%m-%dT%H:%M:%SZ")

      reg = yield self.register(utcnow, 'com.timeservice.now')
      print("Procedure registered with ID {}".format(reg.id))

      ## create an application object that exposes methods for remoting
      ##
      self.calculator = Calculator()

      ## register all methods on the "calculator" decorated with "@wamp.procedure"
      ##
      results = yield self.register(self.calculator)
      for success, res in results:
         if success:
            print("Ok, registered procedure with registration ID {}".format(res.id))
         else:
            print("Failed to register procedure: {}".format(res.value))

   def onLeave(self, details):
      self.disconnect()

   def onDisconnect(self):
      reactor.stop()



def make(config):
   ##
   ## This component factory creates instances of the
   ## application component to run.
   ## 
   ## The function will get called either during development
   ## using the ApplicationRunner below, or as  a plugin running
   ## hosted in a WAMPlet container such as a Crossbar.io worker.
   ##
   if config:
      return Component1(config)
   else:
      return {'label': 'Awesome WAMPlet 1',
              'description': 'This is just a test WAMPlet that provides some procedures to call.'}



if __name__ == '__main__':
   from autobahn.twisted.wamp import ApplicationRunner

   config = {
      "router": {
         "type": "websocket",
         "endpoint": {
            "type": "tcp",
            "host": "localhost",
            "port": 8080
         },
         "url": "ws://localhost:8080/ws",
         "realm": "realm1"
      }
   }

   ## test drive the component during development ..
   runner = ApplicationRunner(config)
   runner.run(make)