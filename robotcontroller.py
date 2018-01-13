#!/usr/bin/env python3

import sys
import Ice
Ice.loadSlice('robots.ice --all -I .')
import drobots
import robots
from robotState import State
import math
import random

class ControllerDefenderI(robots.RobotControllerDefender):
    """
    RobotController interface implementation.

    The implementation only retrieve and print the location of the assigned
    robot
    """
    def __init__(self, bot, container,key): #mines, x, y):	#, key):
        """
        ControllerI constructor. Accepts only a "bot" argument, that should be
        a RobotPrx object, usually sent by the game server.
        """
        self.bot = bot
        self.container = container
        self.state = State.MOVING

        self.key = key
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

        #Se mueve random si esta parado, y se aparta de los extremos en lo posible
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

        print("Move of {} at location {},{}, angle {}".format(id(self), location.x, location.y,direction))
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
        try:
            angle = random.randint(0, 360)
        except IndexError:
            self.angles_left_to_scan = self.Allangles[:]
            random.shuffle(self.angles_left_to_scan)
            current_angle = self.angles_left_to_scan.pop()
        try:
            enemies = self.bot.scan(angle, 20)
            print("Found {} enemies in {}  direction.".format(enemies, angle))
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

class ControllerAttackerI(robots.RobotControllerAttacker):
    """
    RobotController interface implementation.

    The implementation only retrieve and print the location of the assigned
    robot
    """
    def __init__(self, bot, container,key): #mines, x, y):	#, key):
        """
        ControllerI constructor. Accepts only a "bot" argument, that should be
        a RobotPrx object, usually sent by the game server.
        """
        self.bot = bot
        self.container = container
        self.state = State.MOVING

        self.key = key
        #self.mines = mines

        self.vel = 0
        self.energia = 0
        self.x = 100
        self.y = 100
        self.angle = 0
        self.damage_taken = 0
        self.allies_pos = dict()
        self.handlers = {
            State.MOVING : self.move,
            State.SHOOTING : self.shoot,
            State.PLAYING : self.play
        }



    def allies(self, point, id_bot, current=None):
        self.allies_pos[id_bot]= point

    def turn(self, current):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass
        location = self.bot.location()
        print("Turn of {} at location {},{}".format(id(self), location.x, location.y))

    def play(self):
        my_location = self.bot.location()

        #for i in range(0,3):
        #    defender_prx = self.container.getElementAt(i)
        #    defender = drobots.RobotControllerAttackerPrx.uncheckedCast(defender_prx)
        #    defender.allies(my_location, i)
        self.state = State.SHOOTING	#Quitar esta linea luego


    #MOVING

    def move(self):
        location = self.bot.location()
        new_x = self.x - location.x
        new_y = self.y - location.y
        direction = int(round(self.recalculate_angle(new_x, new_y), 0))

        #Se mueve random si esta parado, y se aparta de los extremos en lo posible
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

        print("Move of {} at location {},{}, angle {}".format(id(self), location.x, location.y,direction))
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

    def shoot(self):
        try:
            angle = self.angle + random.randint(0, 360)
            distance = random.randint(20,100)
            self.bot.cannon(angle,distance)
            self.state = State.SHOOTING
            print("Shooting towards {} , {}m of distance".format(angle, distance))
        except drobots.NoEnoughEnergy:
            self.state = State.MOVING
            pass

    #def (SEARCH & REGISTER FOR DEFF ALLIES)

    def robotDestroyed(self, current):
        """
        Pending implementation:
        void robotDestroyed();
        """
        print('Attacker was destroyed')
        pass