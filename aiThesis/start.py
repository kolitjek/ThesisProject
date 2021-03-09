import sys
import argparse

import subprocess
from fireplace import cards
from aiThesis.printController import *
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft

import os.path
import random
from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List
from xml.etree import ElementTree
from Agents.randomAgent import RandomAgent
from Agents.mcts_agent import MCTSAgent

from hearthstone.enums import CardClass, CardType

from aiThesis.utils import CMDInterface
from aiThesis.scenario import Scenario

from aiThesis.game_session import GameSession
#best decks from witchwood which is the latest expansion we have got
#https://www.metabomb.net/hearthstone/gameplay-guides/hearthstone-the-best-witchwood-decks-6
#os.system("cd .. && pip install .")
sys.path.append("")

def main():

	cmdU = CMDInterface()
	args = cmdU.parse_date()
	cards.db.initialize()
	gameSession = GameSession(args.s, args.n, args.name1, args.name2, args.p1Class, args.p2Class, args.p1Deck, args.p2Deck, args.p1DeckType, args.p2DeckType,
							  args.p1Agent, args.p2Agent)

	gameSession.start_session()

if __name__ == "__main__":
	main()
