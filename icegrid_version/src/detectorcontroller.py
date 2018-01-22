#!/usr/bin/env python3
#/------------------------------------------------------------------------/

#	Authors: Carlos Córdoba Ruiz & Álvaro Ángel-Moreno Pinilla

#/------------------------------------------------------------------------/

import sys

import Ice

Ice.loadSlice('aux.ice --all -I .')
import aux
import drobots

class DetectorControllerI(drobots.DetectorController):
    def __init__(self,Container):
        self.container=Container

    def alert(self, pos, robots_detected, current):

        print("Alert: {} robots detected at {},{}".format(
            robots_detected, pos.x, pos.y))
        list=self.container.getAttackers()
        for i in list :
            attacker_prx = self.container.getElementAt(i)
            attacker = aux.RobotControllerAttackerPrx.uncheckedCast(attacker_prx)
            attacker.enemies(pos)



class DetectorControllerFactoryI(aux.DetectorControllerfactory):
    def __init__(self):
        self.proxy=None
    def make(self, Container, current = None):
        if self.proxy is None:
            servant = DetectorControllerI(Container)
            proxy = current.adapter.addWithUUID(servant)
            proxy = current.adapter.createDirectProxy(proxy.ice_getIdentity())
            proxy = drobots.DetectorControllerPrx.checkedCast(proxy)
            self.proxy=proxy

        return self.proxy

class DetectorControllerFactoryServer(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = DetectorControllerFactoryI()
        adapter = broker.createObjectAdapter("DetectorAdapter")
        proxy = adapter.add(servant,broker.stringToIdentity(broker.getProperties().getProperty("Identity")))
        print(proxy)
        adapter.activate()
        sys.stdout.flush()


        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == '__main__':
	server = DetectorControllerFactoryServer()
	sys.exit(server.main(sys.argv))
