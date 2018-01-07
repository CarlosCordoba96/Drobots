#!/usr/bin/env python3

import sys

import Ice

Ice.loadSlice('drobots.ice')
import drobots
Ice.loadSlice('robots.ice --all -I .')
import robots



class ControllerAttackerI(drobots.RobotController):
    """
    RobotController interface implementation.

    The implementation only retrieve and print the location of the assigned
    robot
    """
    def __init__(self, bot, container, key, mines):
        """
        ControllerI constructor. Accepts only a "bot" argument, that should be
        a RobotPrx object, usually sent by the game server.
        """
        self.bot = bot
        self.container = container
        self.key = key
        self.mines = mines

    def turn(self, current):
        """
        Method that will be invoked remotely by the server. In this method we
        should communicate with out Robot
        """
        location = self.bot.location()
        print("Turn of {} at location {},{}".format(
            id(self), location.x, location.y))

    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        pass
