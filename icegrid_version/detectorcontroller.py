#!/usr/bin/env python3


import sys

import Ice

Ice.loadSlice('robots.ice --all -I .')
import robots
import drobots

class DetectorControllerI(drobots.DetectorController):
    def __init__(self,Container):
        self.container=Container

    def alert(self, pos, robots_detected, current):

        print("Alert: {} robots detected at {},{}".format(
            robots_detected, pos.x, pos.y))
        list=self.container.getAttackers()
        print(list)
        for i in range(0,3):
            attacker_prx = self.container.getElementAt(i)
            attacker = robots.RobotControllerAttackerPrx.uncheckedCast(attacker_prx)
            attacker.enemies(pos)


class DetectorControllerFactoryI(robots.DetectorControllerfactory):
    def __init__(self):
        self.proxy=None
    def make(self, Container, current = None):
        if self.proxy is None:
            servant = DetectorControllerI(Container)
            proxy = current.adapter.addWithUUID(servant)
            proxy = drobots.DetectorControllerPrx.checkedCast(proxy)
            self.proxy=proxy

        return self.proxy

class DetectorControllerFactoryServer(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = DetectorControllerFactoryI()
        adapter = broker.createObjectAdapter("DetectorAdapter")
        proxy = adapter.add(servant,broker.stringToIdentity("Detector"))
        print(proxy)
        adapter.activate()
        sys.stdout.flush()


        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


server = DetectorControllerFactoryServer()
sys.exit(server.main(sys.argv))
