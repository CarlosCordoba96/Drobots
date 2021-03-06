#!/usr/bin/env python3
#/------------------------------------------------------------------------/

#	Authors: Carlos Córdoba Ruiz & Álvaro Ángel-Moreno Pinilla

#/------------------------------------------------------------------------/

import sys
import Ice
import os

Ice.loadSlice('aux.ice --all -I .')
import aux
import drobots
#Ice.loadSlice('drobots.ice')

from robotcontroller import *


class Factory(aux.ControllerFactory):

    def make(self, bot, container_robots, key,minas,nattackers, current = None):
        if bot.ice_isA("::drobots::Attacker") and nattackers<2:
           rc_servant = ControllerAttackerI(bot, container_robots,minas, key)
           rc_proxy = current.adapter.addWithUUID(rc_servant)
           print (rc_proxy)
           print ("Robot attacker")
           rc_proxy = current.adapter.createDirectProxy(rc_proxy.ice_getIdentity())
           rc = aux.RobotControllerAttackerPrx.uncheckedCast(rc_proxy)
        else:
            rc_servant = ControllerDefenderI(bot, container_robots,minas, key)
            rc_proxy = current.adapter.addWithUUID(rc_servant)
            print (rc_proxy)
            print ("Robot defender")
            rc_proxy = current.adapter.createDirectProxy(rc_proxy.ice_getIdentity())
            rc = aux.RobotControllerDefenderPrx.uncheckedCast(rc_proxy)

        return rc



class ServerFactory(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = Factory()
        adapter=broker.createObjectAdapter("FactoryAdapter")
        proxy = adapter.add(servant,broker.stringToIdentity(broker.getProperties().getProperty("Identity")))


        print(proxy) #'factory1 -t -e 1.1:tcp -h ' +my ip +' -p 9091 -t 60000'
#pero... 8727385C-A64E-44C5-8888-8ED6F14B16EC -t -e 1.1:tcp -h 192.168.1.41 -p 9090 -t 60000:tcp -h 161.67.172.84 -p 9090 -t 60000

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
	factory = ServerFactory()
	sys.exit(factory.main(sys.argv))
