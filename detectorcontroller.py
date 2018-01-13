#!/usr/bin/env python3


import sys

import Ice

Ice.loadSlice('robots.ice --all -I .')
import robots
import drobots
class DetectorControllerI(drobots.DetectorController):
    def __init__(self,Container):
	self.container=Container
    """
    DetectorController interface implementation.

    It implements the alert method.

    Remember: every alert call will include de position, so there is no need
    to create a DetectorControllerI servant for every detector, you can re-use
    the same servant (and its proxy) to every "makeDetectorController" petition
    on the PlayerI
    """
    def alert(self, pos, robots_detected, current):
        """
        Method that receives a Point with the coordinates where the detector is
        placed and the number of robots around it. This method is only invoked
        when at least 1 robot is near to the detector. If there is no robots
        around it, this method will never be called.
        """
        print("Alert: {} robots detected at {},{}".format(
            robots_detected, pos.x, pos.y))


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
