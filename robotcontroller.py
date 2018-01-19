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

    def __init__(self, bot, container, mines, key):

        self.bot = bot
        self.container = container
        self.state = State.MOVING

        self.key = key
        self.mines = mines

        self.vel = 0
        #self.energia = 0
        self.x = 100
        self.y = 100
        self.angle = 0
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
        location = self.bot.location()
        print("Turn of {} at location {},{}".format(id(self), location.x, location.y))

    def play(self):
        my_location = self.bot.location()

        for i in range(0,3):
            attacker_prx = self.container.getElementAt(i)
            attacker = robots.RobotControllerAttackerPrx.uncheckedCast(attacker_prx)
            attacker.allies(my_location, i)
        self.state = State.SCANNING


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
        return True

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

    def robotDestroyed(self, current):

        print('Defender was destroyed')
        pass

class ControllerAttackerI(robots.RobotControllerAttacker):

    def __init__(self, bot, container, mines, key): 

        self.bot = bot
        self.container = container
        self.state = State.MOVING

        self.key = key
        self.mines = mines

        self.vel = 0
        self.x = 100
        self.y = 100
        self.angle = 0
        self.allies_pos = dict()
        self.enemies_pos = []

        self.handlers = {
            State.MOVING : self.move,
            State.SHOOTING : self.shoot,
            State.PLAYING : self.play
        }



    def allies(self, point, id_bot, current=None):
        self.allies_pos[id_bot] = point

    def enemies(self, point, current=None):
        for key, value in self.allies_pos.items():
             if (point.x != self.allies_pos[key].x and point.y != self.allies_pos[key].y):
                 if not(point in self.enemies_pos):
                     self.enemies_pos.append(point)

    def turn(self, current):
        try:
            self.handlers[self.state]()
        except drobots.NoEnoughEnergy:
            pass
        location = self.bot.location()
        print("Turn of {} at location {},{}".format(id(self), location.x, location.y))

    def play(self):
        my_location = self.bot.location()

        for i in range(0,3):
            defender_prx = self.container.getElementAt(i)
            defender = robots.RobotControllerDefenderPrx.uncheckedCast(defender_prx)
            defender.allies(my_location, i)
            self.state = State.SHOOTING


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
        return True

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
            if not self.enemies_pos:
                angle = self.angle + random.randint(0, 360)
                distance = random.randint(60,100)
            else:
                location = self.bot.location()
                aim = self.enemies_pos[random.randint(0, len(self.enemies_pos)-1)]
                new_x = aim.x - location.x
                new_y = aim.y - location.y
                angle = int(round(self.recalculate_angle(new_x, new_y), 0))
                distance = math.hypot(new_x, new_y)
                if (distance > 100):
                     distance = 100
            if(self.avoidAlly(angle,distance) == True):
                self.bot.cannon(angle,distance)
                self.state = State.SHOOTING
                print("Shooting towards {}º , {}m of distance".format(angle, distance))

        except drobots.NoEnoughEnergy:
            self.state = State.MOVING
            pass

    def avoidAlly(self, angle, distance):
        avoided = True
        location = self.bot.location()
        new_x = (distance * math.sin(angle)) + location.x
        new_y = (distance * math.cos(angle)) + location.y
        #Setting the square where the explossion reaches
        min_x = new_x - 50
        min_y = new_y - 50
        max_x = new_x + 50
        max_y = new_y + 50
        for key, value in self.allies_pos.items():
            if (self.allies_pos[key].x > min_x and self.allies_pos[key].y > min_y and self.allies_pos[key].x < max_x and self.allies_pos[key].y < max_y):
                print("Attacker robot avoided shooting his ally {}.".format(key))
                avoided = False
        return avoided

    #def (SEARCH & REGISTER FOR DEFF ALLIES) NO SE PUEDE HACER TAL CUAL PORQUE DEVUELVE NUMERO EN UN ANGULO, NO POSICIONES

    def robotDestroyed(self, current):

        print('Attacker was destroyed')
        pass
