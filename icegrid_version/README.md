# drobots: Steps to execute
To execute our drobots application, it is only needed to execute 'make' in a terminal in the currently directory. With this command, all the three nodes will get configurated and icegrid-gui will start running.

After that, it is only needed to press 'Log into an IceGrid Registry' and select 'IceGrid:tcp -p 4061' (create it if it is needed). Then press Tools>Application>PatchDistribution. Select Drobots, press 'OK' and 'Yes' in the next opened window.

Open 'node1' in 'Live Deployment', rightclick Player and select 'Start'. If you want to check the execution of the program or the flow of events within the game, you can rightclick 'RCFactory' and press 'Retrieve stdout' in each one of the nodes, to see how the corresponding robot controllers act in each case.
