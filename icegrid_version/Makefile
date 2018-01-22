#!/usr/bin/make -f
# -*- mode:makefile -*-

.PHONY: all dir opennodes iceconfig icepatch stop-grid clean
NODES=$(basename $(shell ls node*.config | sort -r))
ADMIN = icegridadmin --Ice.Config=locator.config -u user -p pass

all:
	cp -R ../icegrid_version /tmp/
	chmod u+x /tmp/icegrid_version/*
	make dir
	make opennodes
	make icepatch
	cd /tmp/icegrid_version/
	make iceconfig
	icegridgui &

dir:
	mkdir -p /tmp/icegrid_version/grid
	mkdir -p /tmp/icegrid_version/grid/registry
	mkdir -p /tmp/icegrid_version/grid/node1
	mkdir -p /tmp/icegrid_version/grid/node2
	mkdir -p /tmp/icegrid_version/grid/node3

opennodes:
	icegridnode --Ice.Config=node1.config &

	@echo -- waiting registry to start...
	@while ! netstat -lptn 2> /dev/null | grep ":4061" > /dev/null; do \
	    sleep 1; \
	done

	@for node in $(filter-out node1, $(NODES)); do \
	    icegridnode --Ice.Config=$$node.config & \
	    echo -- $$node started; \
	done

	@echo -- ok

iceconfig:
	$(ADMIN) -e "application add 'drobots.xml'" &
	
icepatch:
	icepatch2calc /tmp/icegrid_version/src/

stop-grid:
	@for node in $(NODES); do \
	    $(ADMIN) -e "node shutdown $$node"; \
	    echo -- $$node finished; \
	done

	@killall icegridnode
	@echo -- ok

clean:
	make stop-grid
	sudo rm -r /tmp/icegrid_version/grid/
	rm /tmp/icegrid_version/src/*.bz2
	rm /tmp/icegrid_version/src/*.sum
	rm *.txt
