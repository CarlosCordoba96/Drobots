#!/usr/bin/env python3

import sys
import Ice
import os

Ice.loadSlice('robots.ice --all -I .')
import robots
import drobots
#import drobots
#Ice.loadSlice('drobots.ice')

from robotcontroller import *


class Factory(robots.ControllerFactory):
    def __init__(self):
	    pass

    def make(self, robot, container_robots, key, current = None):
#          if robot.ice_isA():
           rc_servant = ControllerAttackerI(robot, container_robots, key, mines)
           rc_proxy = current.adapter.addWithUUID(rc_servant)
           #print rc_proxy
           rc_proxy = current.adapter.createDirectProxy(rc_proxy.ice_getIdentity())
           container_robots.link(key, rc_proxy)
           rc = robots.RobotControllerAttackerPrx.checkedCast(rc_proxy)

           rc.setContainer(container_robots)
           return rc

class ServerFactory(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        
        servant = Factory()

	adapter = broker.createObjectAdapter("FactoryAdapter")
        proxy = adapter.add(servant,
                            broker.stringToIdentity("printerFactory1"))
       
	
        print(proxy) #'factory1 -t -e 1.1:tcp -h ' +my ip +' -p 9091 -t 60000'
#pero... 8727385C-A64E-44C5-8888-8ED6F14B16EC -t -e 1.1:tcp -h 192.168.1.41 -p 9090 -t 60000:tcp -h 161.67.172.84 -p 9090 -t 60000

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


factory = ServerFactory()
sys.exit(factory.main(sys.argv))


