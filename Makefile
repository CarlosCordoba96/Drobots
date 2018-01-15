#!/usr/bin/make -f
# -*- mode:makefile -*-

.PHONY: all run-player run-player2 run-container clean run-all-factories

SERVER = factory

all:
	gnome-terminal -e "make run-all-factories"
	gnome-terminal -e "make run-container"
	make run-player

run-player:
	python3 player.py --Ice.Config=player.config 

run-player2:
	gnome-terminal -e "python3 player.py --Ice.Config=player2.config" 

run-factory1:
	gnome-terminal -e "python3 factory.py --Ice.Config=Factory1.config"

run-factory2:
	gnome-terminal -e "python3 factory.py --Ice.Config=Factory2.config"

run-factory3:
	gnome-terminal -e "python3 factory.py --Ice.Config=Factory3.config"

run-detector:
	gnome-terminal -e "python3 detectorcontroller.py --Ice.Config=Detector.config"

run-all-factories:
	make -j run-factory1 run-factory2 run-factory3 run-detector

run-container:
	python container.py --Ice.Config=Container.config

run-game-factory:
	firefox http://atclab.esi.uclm.es/drobots/canvas.html?p=FactoryRobots &

clean:
	sudo rm -f code/*.pyc
	sudo killall -q -9 python
