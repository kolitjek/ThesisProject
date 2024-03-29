import sys
import argparse

import subprocess

from aiThesis.graphs import create_line_graph, create_displot
from fireplace import cards
from aiThesis.printController import *
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft
# Import math library
import math
import os.path
import random
from bisect import bisect
from importlib import import_module
from pkgutil import iter_modules
from typing import List
from xml.etree import ElementTree
from Agents.play_all_agent import PlayAllAgent
from Agents.mcts_sequence_agent import MCTSSequentialAgent
import matplotlib.pyplot as plt
from hearthstone.enums import CardClass, CardType

from aiThesis.utils import CMDInterface
from aiThesis.scenario import Scenario
import pandas as pd
import numpy as np
import pathlib
import seaborn as sns
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
	folder_path = "./data/"
	classes = ["druid", "hunter", "priest", "warrior"]
	classes_des = ["Combo", "Mid-range", "Control", "Aggro"]
	'''result = pd.DataFrame()
	class_counter = 0
	for c in classes:
		df = pd.data_imp = pd.read_csv(str(pathlib.Path(__file__).parent.absolute()) + "\\data\\max_turns_" + c + ".csv")
		df = df.replace(np.nan, 0)
		#print(df.head(10))
		df = df.iloc[9].tolist()
		df.pop(0)
		df_new = [[math.floor(x / 2),classes_des[class_counter]] for x in df]

		temp_df = pd.DataFrame(df_new)
		temp_df.columns = ["Max Turns", "Class"]
		class_counter += 1
		result = result.append(temp_df)

	#print("afl,æøl,æfasl,æafd")

	#print(result.size)
	#print(len(result))
	#data = pd.DataFrame( {'Type': classes_des, 'Values': result})
	data = pd.DataFrame([])

	count = 0

	#print(data.head())

	#print(sns.load_dataset("penguins").head())
	data = data.T

	#create_displot(result[0],name="x variable", folder_path + "/last_turn_800_all_classes" + ".PNG")
	sns.histplot(result, x="Max Turns",hue = 'Class',binrange=(0,25),alpha = .2,kde = True)
	plt.ylabel('Frequency', size=20)
	plt.xlabel('Max Turn', size=20)

	plt.show()

	print("done")
		#for i in range(0,upper_limit-1):'''

	'''	sum_data = 0
			none_counter = 0
			for t in df[["turn " + str(i)]].values.tolist():
				if t[0] == 0:
					none_counter += 1
				else:
					sum_data += float(t[0])
			print(sum_data / (len(df[["turn " + str(i)]].values.tolist())-none_counter))
			result[-1].append(sum_data / (len(df[["turn " + str(i)]].values.tolist())-none_counter))
	x = list(([(range(0, len(i)) for i in result)])[0])
	print(x)
	print(result)
	folder_path = "./data/"
	create_line_graph(x, result, ["Turn", "Action space"], classes_des, folder_path + "/initial_action_space_800_all_classes" + ".PNG", 250)'''


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
