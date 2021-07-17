## Master thesis project 2021 (Games Technology Track, ITU)
This repository contains the code used in the  master thesis project: Sequential pruning in Hearthstone. The code is an extension to the Fireplace simulator found at: https://github.com/jleclanche/fireplace. The project revolves around experimenting with different data structures and pruning methods for a Monte Carlo tree search (MCTS) agent. 

Contributors: Anton Sandberg and Sune Klem.

## Main scripts
* `start.py`: this script starts up the simulator and runs the desired game.
* `data_analysis.py`: this script contains the whole data analysis detailed in the report 

## Cmd interface 
This project contains a command line interface, which allows you to initialize the simulator with a set of parameters. The different possible parrameter keywords can be found in `utils.py`, here a some of the exist onces:
* -s: scenario name (if you want to run a given game preset)
* -n: Total number of games to run
* -name1: name of player one
* -name2: Name of player two
* -p1Class: class of player one
* -p2Class: class of player two
* -p1Deck: deck of player one
* -p2Deck: deck of player two
* -p1Agent: agent of player one
* -p2Agent: agent of player two
* -mctsIterations: number of MCTS iterations 
* -plotTree: enable of disable a tree visualizer 

## Requirements

* Python 3.8+


## Installation

* `pip install .` (run this from the root folder)
* Additional libraries need to be installed: Numpy, seaborn, matlibplot, networkx and graphviz 


## Community

Fireplace is a [HearthSim](http://hearthsim.info/) project.
Join the community: <https://hearthsim.info/join/>
