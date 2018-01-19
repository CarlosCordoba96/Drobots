#!/usr/bin/make -f
# -*- mode:makefile -*-

ADMIN = icegridadmin --Ice.Config=locator.config -u user -p pass

all:
	make dir
	make opennodes
	icegrid-gui

dir:
	mkdir -p grid
	mkdir -p grid/registry
	mkdir -p grid/node1
	mkdir -p grid/node2
	mkdir -p grid/node3

opennodes:
	icegridnode --Ice.Config = node1.config
	icegridnode --Ice.Config = node2.config
	icegridnode --Ice.Config = node3.config

#closegrid:
#	killall icegridnode

clean:
	make closegrid
	sudo rm -r grid/
