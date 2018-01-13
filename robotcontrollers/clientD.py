#!/usr/bin/env python3

"""
Implementation of a simple client that is able to accomplish the following:

- Retrieve a GamePrx from a configuration file and connect to it
- Serve a Player servant
- Receive the invocations to create robot controllers
- Receive the win, lose or gameAbort invocation at the end of a match
- The 4 robot controllers behave in the same way

This implementation lacks:

- The RobotController servants are in the same process as the Player, so
  it breaks a practice requisite
- No detector controllers are created
- No mine positions are returned to the game
- There is no communication between the robot controllers
"""

import sys

import Ice

Ice.loadSlice('drobots.ice')
import drobots
import random
from robotState import *


class ControllerI(drobots.RobotController):
    """
    RobotController interface implementation.

    The implementation only retrieve and print the location of the assigned
    robot
    """
    def __init__(self, bot, container): #mines, x, y):	#, key):
        """
        ControllerI constructor. Accepts only a "bot" argument, that should be
        a RobotPrx object, usually sent by the game server.
        """
        self.bot = bot
        self.container = container
        self.state = State.MOVING

        #self.key = key
        #self.mines = mines

        self.vel = 0
        self.energia = 0
        self.x = 100
        self.y = 100
        self.angle = 0
        #self.damage_taken = 0
        self.allies_pos = dict()
        self.handlers = {
            State.MOVING : self.move,
            State.SCANNING : self.scan,
            State.PLAYING : self.play
        }

    def setContainer(self, container, current=None):
        self.container = container

    def allies(self, point, id_bot, current=None):
        self.allies_pos[id_bot]= point

    def turn(self, current):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass
        #location = self.bot.location()
        #print("Turn of {} at location {},{}".format(id(self), location.x, location.y))
        #except(drobots.NoEnoughEnergy):
        #   pass

    def play(self):
        my_location = self.bot.location()

        #for i in range(0,3):
        #    attacker_prx = self.container.getElementAt(i)
        #    attacker = drobots.RobotControllerAttackerPrx.uncheckedCast(attacker_prx)
        #    attacker.friendPosition(my_location, i)
        self.state = State.SCANNING	#Quitar esto luego


    #MOVING

    def move(self):
        location = self.bot.location()
        new_x = self.x - location.x
        new_y = self.y - location.y
        direction = int(round(self.recalculate_angle(new_x, new_y), 0))

        #Se mueve random si está parado, y se aparta de los extremos en lo posible
        if (self.vel == 0):
             self.bot.drive(random.randint(0,360),100)
             self.vel = 100
        elif (location.x > 350):
             self.bot.drive(225, 50) #100
             self.vel = 100
        elif (location.x < 50):
             self.bot.drive(45, 50) #100
             self.vel = 100
        elif (location.y > 350):
             self.bot.drive(315, 50) #100
             self.vel = 100
        elif (location.y < 50):
             self.bot.drive(135, 50) #100
             self.vel = 100
        #El bloque if/elif de arriba podria sobrar en ambos

        print("Move of {} at location {},{}, angle {}º".format(id(self), location.x, location.y,direction))
        self.bot.drive(direction,100)
        self.state = State.PLAYING      


    def recalculate_angle(self, x, y, current=None):
        if x == 0:
            if y > 0:
                return 90
            else:
                return 270
        if y == 0:
            if x > 0:
                return 0
            else:
                return 180
        elif y > 0:
            return 90 - math.degrees(math.atan(float(x)/float(y)))
        else:
            return 270 - math.degrees(math.atan(float(x)/float(y)))

    #SHOOTING

    def scan(self):
        #try:
        angle = random.randint(0, 360)
        #except IndexError:
            #self.angles_left_to_scan = self.Allangles[:]
            #random.shuffle(self.angles_left_to_scan)
            #current_angle = self.angles_left_to_scan.pop()
        try:
            enemies = self.bot.scan(angle, 20)
            print("Found {} enemies in {}º direction.".format(enemies, angle))
        except drobots.NoEnoughEnergy:
            self.state = State.MOVING
            pass

    #def (SEARCH & REGISTER FOR DEFF ALLIES)

    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        print('Defender was destroyed')
        pass


class DetectorControllerI(drobots.DetectorController):
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


class PlayerI(drobots.Player):
    """
    Player interface implementation.

    It responds correctly to makeController, win, lose or gameAbort.
    """
    def __init__(self):
        self.detector_controller = None
        self.mine_index = 0
        self.mines = [
            drobots.Point(x=100, y=100),
            drobots.Point(x=100, y=300),
            drobots.Point(x=300, y=100),
            drobots.Point(x=300, y=300),
        ]

    def makeController(self, bot, current):
        """
        makeController is invoked by the game server. The method receives a
        "bot", instance of RobotPrx.

        It is mandatory to return a direct proxy, in case that you are using
        IceGrid
        """

        print("Make controller received bot {}".format(bot))
        controller = ControllerI(bot, self.mines)
        object_prx = current.adapter.addWithUUID(controller)
        controller_prx = drobots.RobotControllerPrx.checkedCast(object_prx)
        return controller_prx

    def makeDetectorController(self, current):
        """
        Pending implementation:
        DetectorController* makeDetectorController();
        """
        print("Make detector controller.")

        if self.detector_controller is not None:
            return self.detector_controller

        controller = DetectorControllerI()
        object_prx = current.adapter.addWithUUID(controller)
        self.detector_controller = \
            drobots.DetectorControllerPrx.checkedCast(object_prx)
        return self.detector_controller

    def getMinePosition(self, current):
        """
        Pending implementation:
         Point getMinePosition();
        """
        pos = self.mines[self.mine_index]
        self.mine_index += 1
        return pos

    def win(self, current):
        """
        Received when we win the match
        """
        print("You win")
        current.adapter.getCommunicator().shutdown()

    def lose(self, current):
        """
        Received when we lose the match
        """
        print("You lose :-(")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current):
        """
        Received when the match is aborted (when there are not enough players
        to start a game, for example)
        """
        print("The game was aborted")
        current.adapter.getCommunicator().shutdown()


class ClientApp(Ice.Application):
    """
    Ice.Application specialization
    """
    def run(self, argv):
        """
        Entry-point method for every Ice.Application object.
        """

        broker = self.communicator()

        # Using PlayerAdapter object adapter forces to define a config file
        # where, at least, the property "PlayerAdapter.Endpoints" is defined
        adapter = broker.createObjectAdapter("PlayerAdapter")

        # Using "propertyToProxy" forces to define the property "GameProxy"
        game_prx = broker.propertyToProxy("GameProxy")
        game_prx = drobots.GamePrx.checkedCast(game_prx)

        # Using "getProperty" forces to define the property "PlayerName"
        name = broker.getProperties().getProperty("PlayerName")

        servant = PlayerI()
        player_prx = adapter.addWithUUID(servant)
        player_prx = drobots.PlayerPrx.uncheckedCast(player_prx)
        adapter.activate()

        print("Connecting to game {} with nickname {}".format(game_prx, name))

        try:
            game_prx.login(player_prx, name)

            self.shutdownOnInterrupt()
            self.communicator().waitForShutdown()

        except Exception as ex:
            print("An error has occurred: {}".format(ex))
            return 1

        return 0


if __name__ == '__main__':
    client = ClientApp()
    retval = client.main(sys.argv)
    sys.exit(retval)
