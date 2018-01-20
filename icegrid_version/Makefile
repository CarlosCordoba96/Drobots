#!/usr/bin/make -f
# -*- mode:makefile -*-

.PHONY: all dir opennodes clean
NODES=$(basename $(shell ls node*.config | sort -r))
ADMIN = icegridadmin --Ice.Config=locator.config -u user -p pass

all:
	make dir
	make opennodes
	make ice
	icegridgui &

dir:
	mkdir -p grid
	mkdir -p grid/registry
	mkdir -p grid/node1
	mkdir -p grid/node2
	mkdir -p grid/node3

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
ice:
	$(ADMIN) -e "application add 'drobots.xml'" &
	$(ADMIN) -e "application update 'drobots.xml'"
	
stop-grid:
	@for node in $(NODES); do \
	    $(ADMIN) -e "node shutdown $$node"; \
	    echo -- $$node finished; \
	done

	@killall icegridnode
	@echo -- ok

clean:
	make closegrid
	sudo rm -r grid/
