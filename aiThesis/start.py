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
from Agents.play_all_agent import PlayAllAgent
from Agents.mcts_sequence_agent import MCTSSequentialAgent

from hearthstone.enums import CardClass, CardType

from aiThesis.utils import CMDInterface
from aiThesis.scenario import Scenario
import pandas as pd
import pathlib
from scipy import stats
from scipy.stats import levene
from scipy.stats import chisquare

#from .ttest import *
#from .load_data import *
from aiThesis.game_session import GameSession
#best decks from witchwood which is the latest expansion we have got
#https://www.metabomb.net/hearthstone/gameplay-guides/hearthstone-the-best-witchwood-decks-6
#os.system("cd .. && pip install .")
sys.path.append("")

def main():

	cmdU = CMDInterface()
	args = cmdU.parse_date()
	cards.db.initialize()
	gameSession = GameSession(args.s, args.n, args.name1, args.name2, args.p1Class, args.p2Class, args.p1Deck, args.p2Deck, args.p1DeckType, args.p2DeckType, args.p1Agent, args.p2Agent, args.p1SimulatorAgent, args.p2SimulatorAgent, args.mctsIterations, args.plotTree)


	gameSession.start_session()
	'''curr_class = "druid"
	print(str(pathlib.Path(__file__).parent.absolute()) + "\\data\\DRUID_vs_DRUID\\win_percentage_05_04_21.csv")
	data_init = pd.read_csv(str(pathlib.Path(__file__).parent.absolute()) + "\\data\\evaluation\\raw_initial_action_space_itr_500_"+curr_class+".csv") #DRUID_vs_DRUID\\win_percentage_05_04_21.csv")
	data_imp = pd.read_csv(str(pathlib.Path(__file__).parent.absolute()) + "\\data\\evaluation\\raw_action_space_itr_500_"+curr_class+".csv")

	data_init = data_init.drop('Unnamed: 0', 1)
	data_imp = data_imp.drop('Unnamed: 0', 1)

	data_init = data_init['turn 9']
	data_imp = data_imp['turn 9']

	data_init = [x for x in data_init if str(x) != 'nan']
	data_imp = [x for x in data_imp if str(x) != 'nan']

	print(data_init)
	print(data_imp)

	print("Levene test ")
	stat, p3 = levene(data_init, data_imp)
	print("p-value levene test: %d" % p3)
	print(p3)

	flat_list = [item for sublist in data.values.tolist() for item in sublist]
	cleanedList = [x for x in flat_list if str(x) != 'nan']
	print(cleanedList)
	print(len(cleanedList))

	k2, p = stats.normaltest(data_imp)
	alpha = 0.05
	print("normal Distribution ("+curr_class+", 500 itr, improved action space ")
	# print("p = {:g}".format(p))

	if p < alpha:  # null hypothesis: x comes from a normal distribution
		print("The null hypothesis can be rejected, x does not come from the same distribution")
	else:
		print("The null hypothesis cannot be rejected, x comes from the same distribution")
	print("P: " + str(p))

	k2, p = stats.normaltest(data_init)
	alpha = 0.05
	print("normal Distribution ("+curr_class+", 500 itr, initial action space ")
	# print("p = {:g}".format(p))

	if p < alpha:  # null hypothesis: x comes from a normal distribution
		print("The null hypothesis can be rejected, x does not come from the same distribution")
	else:
		print("The null hypothesis cannot be rejected, x comes from the same distribution")
	print("P: " + str(p))'''



if __name__ == "__main__":
	main()
