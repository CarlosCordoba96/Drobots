#!/usr/bin/env python3
#/------------------------------------------------------------------------/

#	Authors: Carlos Córdoba Ruiz & Álvaro Ángel-Moreno Pinilla

#/------------------------------------------------------------------------/

import sys
import Ice
Ice.loadSlice('aux.ice --all -I .')
import aux

class Container(aux.Container):

     def __init__(self, current=None):
         self.proxies = dict()
         self.attackers=[]
         self.defenders=[]

     def link(self, key, proxy,type, current=None):
         self.proxies[key] = proxy
         if type == "a":
             self.attackers.append(key)
         else:
             self.defenders.append(key)

     def getAttackers(self,current=None):
         return self.attackers

     def getDefenders(self,current=None):
         return self.defenders

     def unlink(self, key, current=None):
         print("{0}: unlink: {1}".format(self.type, key))
         del self.proxies[key]

     def list(self,current=None):
         return self.proxies

     def getElementAt(self, key, current=None):
         return self.proxies[key]

     def getType(self, current=None):
         return self.type

class ContainerApp (Ice.Application):

     def run (self, argv):
         broker = self.communicator()
         adapter = broker.createObjectAdapter('ContainerAdapter')
         servant = Container()
         proxy = adapter.add(servant,broker.stringToIdentity("container1"))
         print (proxy)
         adapter.activate()
         self.shutdownOnInterrupt()
         broker.waitForShutdown()

         return 0

if __name__ == '__main__':
     sys.exit(ContainerApp().main(sys.argv))
