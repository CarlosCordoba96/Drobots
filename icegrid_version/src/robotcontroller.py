#!/usr/bin/env python3
#/------------------------------------------------------------------------/

#	Authors: Carlos Córdoba Ruiz & Álvaro Ángel-Moreno Pinilla

#/------------------------------------------------------------------------/

import sys
import Ice
Ice.loadSlice('aux.ice --all -I .')
import drobots
import aux
from robotState import State
import math
import random

class ControllerDefenderI(aux.RobotControllerDefender):

    def __init__(self, bot, container, mines, key):

        self.bot = bot
        self.container = container
        self.state = State.MOVING

        self.key = key
        self.mines = mines

        self.vel = 0
        self.x = 100
        self.y = 100
        self.nscans = 0
        self.angle = 0
        self.allies_pos = dict()
        self.handlers = {
            State.MOVING : self.move,
            State.SCANNING : self.scan,
            State.PLAYING : self.play
        }

    def allies(self, point, id_bot, current=None):
        self.allies_pos[id_bot]= point
        print("Ally {} is in position {}, {}".format(id_bot, point.x, point.y))
        sys.stdout.flush()

    def turn(self, current):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass
        location = self.bot.location()
        print("Turn of {} at location {},{}".format(id(self), location.x, location.y))

	#PLAYING

    def play(self):
        my_location = self.bot.location()

        for i in self.container.getDefenders():
            defender_prx = self.container.getElementAt(i)
            defender = aux.RobotControllerDefenderPrx.uncheckedCast(defender_prx)
            defender.allies(my_location, self.key)
        for i in self.container.getAttackers():
            attacker_prx = self.container.getElementAt(i)
            attacker = aux.RobotControllerAttackerPrx.uncheckedCast(attacker_prx)
            attacker.allies(my_location, self.key)
        self.state = State.SCANNING


    #MOVING

    def move(self):
        self.x = random.randint(0,400)
        self.y = random.randint(0,400)
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

        if (self.avoidCollision(direction,self. vel)==True):
             #Si la velocidad no es 0, se mueve con la definida.
             print("Move of {} from location {},{}, angle {}º".format(id(self), location.x, location.y,direction))
             self.bot.drive(direction,100)
             self.vel = 100
        self.state = State.PLAYING

    def avoidCollision(self, direction, vel):
        avoid = True
        for distance in range (1, vel):
             new_x = (distance * math.sin(direction)) + self.x
             new_y = (distance * math.cos(direction)) + self.y
             for mine in self.mines:
                  if (new_x == mine.x and new_y == mine.y):
                       print("Not moving to avoid a mine")
                       return False
             for key, value in self.allies_pos.items():
                  if (new_x == self.allies_pos[key].x and new_y == self.allies_pos[key].y):
                       print("Not moving to avoid colliding an ally")
                       return False
        return avoid

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

    #SCANNING

    def scan(self):
        if (self.nscans == 5):
            self.nscans = 0
            self.state = State.MOVING
        else:
            angle = random.randint(0, 360)
            try:
                enemies = self.bot.scan(angle, 20)
                print("Found {} enemies in {}  direction.".format(enemies, angle))
                self.nscans += 1
            except drobots.NoEnoughEnergy:
                self.state = State.MOVING
                pass

    def robotDestroyed(self, current):

        print('Defender was destroyed')
        pass

class ControllerAttackerI(aux.RobotControllerAttacker):

    def __init__(self, bot, container, mines, key): 

        self.bot = bot
        self.container = container
        self.state = State.MOVING

        self.key = key
        self.mines = mines

        self.vel = 0
        self.x = 100
        self.y = 100
        self.nshoots = 0
        self.angle = 0
        self.allies_pos = dict()
        self.enemies_pos = []

        self.handlers = {
            State.MOVING : self.move,
            State.SHOOTING : self.shoot,
            State.PLAYING : self.play
        }

    def allies(self, point, id_bot, current=None):
        self.allies_pos[id_bot]= point
        print("Ally {} is in position {}, {}".format(id_bot, point.x, point.y))
        sys.stdout.flush()

    def enemies(self, point, current=None):
        min_x = point.x - 80
        min_y = point.y - 80
        max_x = point.x + 80
        max_y = point.y + 80
        for key, value in self.allies_pos.items():
             if ((self.allies_pos[key].x < min_x or self.allies_pos[key].x > max_x) and (self.allies_pos[key].y < min_y or self.allies_pos[key].y > max_y)):
                 if not(point in self.enemies_pos):
                     self.enemies_pos.append(point)

    def turn(self, current):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass
        location = self.bot.location()
        print("Turn of {} at location {},{}".format(id(self), location.x, location.y))

    #PLAYING

    def play(self):
        my_location = self.bot.location()

        for i in self.container.getDefenders():
            defender_prx = self.container.getElementAt(i)
            defender = aux.RobotControllerDefenderPrx.uncheckedCast(defender_prx)
            defender.allies(my_location, self.key)
        for i in self.container.getAttackers():
            attacker_prx = self.container.getElementAt(i)
            attacker = aux.RobotControllerAttackerPrx.uncheckedCast(attacker_prx)
            attacker.allies(my_location, self.key)
        self.state = State.SHOOTING


    #MOVING

    def move(self):
        self.x = random.randint(0,400)
        self.y = random.randint(0,400)
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

        if (self.avoidCollision(direction,self.vel)==True):
             #Si la velocidad no es 0, se mueve con la definida.
             print("Move of {} from location {},{}, angle {}º".format(id(self), location.x, location.y,direction))
             self.bot.drive(direction,100)
             self.vel = 100
        self.state = State.PLAYING

    def avoidCollision(self, direction, vel):
        avoid = True
        for distance in range (1, vel):
             new_x = (distance * math.sin(direction)) + self.x
             new_y = (distance * math.cos(direction)) + self.y
             for mine in self.mines:
                  if (new_x == mine.x and new_y == mine.y):
                       print("Not moving to avoid a mine")
                       return False
             for key, value in self.allies_pos.items():
                  if (new_x == self.allies_pos[key].x and new_y == self.allies_pos[key].y):
                       print("Not moving to avoid colliding an ally")
                       return False
        return avoid

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
        if (self.nshoots == 5):
            self.nshoots = 0
            self.state = State.MOVING
        else:
            try:
                if not self.enemies_pos:
                    angle = self.angle + random.randint(0, 360)
                    distance = random.randint(81,100)
                else:
                    location = self.bot.location()
                    aim = self.enemies_pos[random.randint(0, len(self.enemies_pos)-1)]
                    new_x = aim.x - location.x
                    new_y = aim.y - location.y
                    angle = int(round(self.recalculate_angle(new_x, new_y), 0))
                    distance = math.hypot(new_x, new_y)
                    if (distance > 100):
                        distance = 100
                    elif (distance <= 80):  #The objective is to not shoot yourself
                        distance = 81
                if(self.avoidAlly(angle,distance) == True):
                    self.bot.cannon(angle,distance)
                    self.state = State.SHOOTING
                    print("Shooting towards {}º , {}m of distance".format(angle, distance))
                    self.nshoots += 1

            except drobots.NoEnoughEnergy:
                self.state = State.MOVING
                pass

    def avoidAlly(self, angle, distance):
        avoided = True
        location = self.bot.location()
        new_x = (distance * math.sin(angle)) + location.x
        new_y = (distance * math.cos(angle)) + location.y
        #Setting the square where the explossion reaches
        min_x = new_x - 80
        min_y = new_y - 80
        max_x = new_x + 80
        max_y = new_y + 80
        for key, value in self.allies_pos.items():
            if (self.allies_pos[key].x > min_x and self.allies_pos[key].y > min_y and self.allies_pos[key].x < max_x and self.allies_pos[key].y < max_y):
                print("Attacker robot avoided shooting his ally {}.".format(key))
                avoided = False
        return avoided

    def robotDestroyed(self, current):

        print('Attacker was destroyed')
        pass
