from itertools import chain

from .graphs import *
import itertools
import operator
import numpy as np
import datetime
import os


deck_ran = "this should be the name of the deck kappa"

def health_distribution_graph(session_data,heroes):
	player1_health =[]
	player2_health =[]
	for game_data in session_data:
		player1_health.append(game_data.game_data[-1].player1_health)
		player2_health.append(game_data.game_data[-1].player2_health)

	print(player1_health)
	print(player2_health)

	player = ["player: " + str(x) for x in range(1,3)]
	col = ["game: " + str(x) for x in range(0, len(player1_health))]
	folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
	df1 = pd.DataFrame([player1_health, player2_health], index=player, columns=col)
	save_DF(df1, folder_path, "health_distribution")

	create_graph([player1_health, player2_health], ["Player 1", "Player 2"], ["Health", "Frequency"],  folder_path + "/_health_distribution" + ".PNG")

def line_graph(session_data, mcts_iterations, heroes):
	number_of_different_iterations = len(mcts_iterations)
	player2_health = []
	for game_data in session_data:
		player2_health.append(game_data.game_data[-1].player2_health)
	n_split = np.array_split(player2_health, number_of_different_iterations)
	y =[0.0]
	x = mcts_iterations[:]
	x.insert(0, '0')
	x = [int(i) for i in x]
	for iterations in n_split:
		point = 0
		for iteration in iterations:
			if iteration > 0:
				point += 1
		y.append(point*100 / len(iterations))

	itr_no = ["Iterations: " + str(x) for x in mcts_iterations]
	#col = ['turn ' + str(i) for i in range(0, len(max(y, key=len)))]
	folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
	df1 = pd.DataFrame(y[1:], index=itr_no, columns=["win rate"])
	save_DF(df1, folder_path, "win_percentage")

	create_line_graph([x], [y],  ["Iterations", "Win percentage"], ["Line"], folder_path + "/_win_rate" + ".PNG")

def avg_max_turn_box_plot(session_data, mcts_iterations,heroes):
	number_of_different_iterations = len(mcts_iterations)
	max_turn = []
	for game_data in session_data:
		max_turn.append(game_data.game_data[-1].turn_number)
	n_split = np.array_split(max_turn, number_of_different_iterations)
	x = [["0"]]
	itr_no = []
	y = [np.array([0.0])]
	for i in mcts_iterations[:]:
		x.append([i])
		itr_no.append('itr: ' + str(i))
	for iterations in n_split:
		y.append(iterations)
	print("avg_max_turn X: " +str(x))
	print("avg_max_turn Y: " + str(y))

	col = ['game ' + str(i) for i in range(0, len(max(y, key=len)))]

	folder_path = "./data/"+heroes["p1"] + "_vs_" + heroes["p2"]
	df1 = pd.DataFrame(y[1:], index=[itr_no],columns=[col])

	save_DF(df1,folder_path, "max_turns")

	create_box_plot(x, y, ["Iterations", "Max_turn"],  folder_path + "/_avg_max_turn" + ".PNG")


def avg_max_turn_number(session_data, mcts_iterations):
	number_of_different_iterations = len(mcts_iterations)
	max_turns = []
	for game_data in session_data:
		max_turns.append(game_data.game_data[-1].turn_number)
	n_split = np.array_split(max_turns, number_of_different_iterations)
	y =[0.0]
	x = mcts_iterations[:]
	x.insert(0, '0')
	x = [int(i) for i in x]
	for iterations in n_split:
		avg_value = 0
		for iteration in iterations:
				avg_value += iteration
		y.append(avg_value / len(iterations))
	print("mcts_iterations: " + str(x))
	print("avg_max_turn: " + str(y))



def avg_mcts_action_space_pr_turn(session_data, mcts_iterations,heroes): #session_data_lists, mcts_iterations, text_x, text_y
	number_of_different_iterations = len(mcts_iterations)
	to_be_split = []
	for game_data in session_data:
		to_be_split.append(game_data.action_spaces)
	n_split = (np.array_split(to_be_split, number_of_different_iterations))
	n_split = [x.tolist() for x in n_split]
	print(n_split)
	result =[]
	index = 0
	for action_spaces in n_split:
		print("\n")
		print("Action space: " + str(action_spaces))

		itr_no = ["game: " + str(x) for x in range(0,len(action_spaces))]
		col = ['turn ' + str(i) for i in range(0, len(max(action_spaces, key=len)))]
		folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
		df1 = pd.DataFrame(action_spaces, index=itr_no, columns=col)
		save_DF(df1, folder_path, "raw_action_space_itr_" + str(mcts_iterations[index] + "_"))

		index += 1
		lists = list(map(list,itertools.zip_longest(*action_spaces)))
		result.append( [sum([i for i in x if i is not None]) / len([i for i in x if i is not None]) for x in lists])
		print("Action space split list: " + str(lists))
		print("Action space result: " + str (result))
	x = list(([(range(0, len(i)) for i in result)])[0])

	itr_no = ["Iterations: " + str(x) for x in mcts_iterations]
	col = ['turn ' + str(i) for i in range(0, len(max(result, key=len)))]
	folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
	df1 = pd.DataFrame(result, index=itr_no, columns=col)
	save_DF(df1, folder_path, "avg_as_per_turn")

	create_line_graph(x, result, ["Turn", "Action space"], itr_no, folder_path + "/_action_space" + ".PNG")


def avg_mcts_avg_times_visited_children_pr_turn(session_data, mcts_iterations, heroes): #session_data_lists, mcts_iterations, text_x, text_y
	number_of_different_iterations = len(mcts_iterations)
	to_be_split = []
	for game_data in session_data:
		to_be_split.append(game_data.avg_times_visited_children)
	n_split = (np.array_split(to_be_split, number_of_different_iterations))
	n_split = [x.tolist() for x in n_split]
	result =[]
	index = 0
	for avg_times_visited_children in n_split:

		itr_no = ["game: " + str(x) for x in range(0, len(avg_times_visited_children))]
		col = ['turn ' + str(i) for i in range(0, len(max(avg_times_visited_children, key=len)))]
		folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
		df1 = pd.DataFrame(avg_times_visited_children, index=itr_no, columns=col)
		save_DF(df1, folder_path, "raw_times_visited_itr_" + str(mcts_iterations[index] + "_"))
		index += 1
		print("\n")
		print("avg_times_visited_children : " + str(avg_times_visited_children))
		lists = list(map(list,itertools.zip_longest(*avg_times_visited_children)))
		print("avg_times_visited_children split list: " + str(lists))
		result.append( [sum([i for i in x if i is not None]) / len([i for i in x if i is not None]) for x in lists])
		print("avg_times_visited_children result: " + str(result))
	x = list(([(range(0, len(i)) for i in result)])[0])


	itr_no = ["Iterations: " + str(x) for x in mcts_iterations]
	col = ['turn ' + str(i) for i in range(0, len(max(result, key=len)))]
	folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
	df1 = pd.DataFrame(result, index=itr_no, columns=col)
	save_DF(df1, folder_path, "avg_times_visited_children")
	create_line_graph(x, result, ["Turn", "avg_times_visited_children"], itr_no, folder_path + "/_avg_times_visited_children" + ".PNG")

def avg_mcts_unexplored_children_pr_turn(session_data, mcts_iterations, heroes): #session_data_lists, mcts_iterations, text_x, text_y
	number_of_different_iterations = len(mcts_iterations)
	to_be_split = []
	for game_data in session_data:
		to_be_split.append(game_data.unexplored_children)
	n_split = (np.array_split(to_be_split, number_of_different_iterations))
	n_split = [x.tolist() for x in n_split]
	result =[]
	index = 0
	for unexplored_children in n_split:

		itr_no = ["game: " + str(x) for x in range(0, len(unexplored_children))]
		col = ['turn ' + str(i) for i in range(0, len(max(unexplored_children, key=len)))]
		folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
		df1 = pd.DataFrame(unexplored_children, index=itr_no, columns=col)
		save_DF(df1, folder_path, "raw_unexplored_children_itr_" + str(mcts_iterations[index] + "_"))
		index += 1
		print("\n")
		print("\n")
		print("Unexplored_children: " + str(unexplored_children))
		lists = list(map(list, itertools.zip_longest(*unexplored_children)))
		print("unexplored_children split list: " + str(lists))
		print([len([i for i in x if i is not None]) for x in lists])
		result.append([sum([i for i in x if i is not None]) / len([i for i in x if i is not None]) for x in lists])
		print("unexplored_children result: " + str(result))
	x = list(([(range(0, len(i)) for i in result)])[0])

	itr_no = ["Iterations: " + str(x) for x in mcts_iterations]
	col = ['turn ' + str(i) for i in range(0, len(max(result, key=len)))]
	folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
	df1 = pd.DataFrame(result, index=itr_no, columns=col)
	save_DF(df1, folder_path, "avg_unexplored_children")
	create_line_graph(x, result, ["Turn", "unexplored_children"],itr_no, folder_path + "/_unexplored_children" + ".PNG")


def avg_mcts_tree_depths_pr_turn(session_data, mcts_iterations, heroes): #session_data_lists, mcts_iterations, text_x, text_y
	number_of_different_iterations = len(mcts_iterations)
	to_be_split = []
	for game_data in session_data:
		to_be_split.append(game_data.tree_depths)
	n_split = (np.array_split(to_be_split, number_of_different_iterations))
	n_split = [x.tolist() for x in n_split]
	result =[]
	index = 0
	for tree_depths in n_split:

		itr_no = ["game: " + str(x) for x in range(0, len(tree_depths))]
		col = ['turn ' + str(i) for i in range(0, len(max(tree_depths, key=len)))]
		folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
		df1 = pd.DataFrame(tree_depths, index=itr_no, columns=col)
		save_DF(df1, folder_path, "raw_tree_depth_itr_" + str(mcts_iterations[index] + "_"))
		index += 1

		print("\n")
		print("Tree_depts: " + str(tree_depths))
		lists = list(map(list,itertools.zip_longest(*tree_depths)))
		print("tree_depths split list: " + str(lists))
		print([len([i for i in x if i is not None]) for x in lists])
		result.append([sum([i for i in x if i is not None]) / len([i for i in x if i is not None]) for x in lists])
		print("tree_depths result: " + str(result))
	x = list(([(range(0, len(i)) for i in result)])[0])

	itr_no = ["Iterations: " + str(x) for x in mcts_iterations]
	col = ['turn ' + str(i) for i in range(0, len(max(result, key=len)))]
	folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
	df1 = pd.DataFrame(result, index=itr_no, columns=col)
	save_DF(df1, folder_path, "tree_depths")

	create_line_graph(x, result, ["Turn", "tree_depths"], itr_no, folder_path + "/_tree_depths" + ".PNG")

def avg_computation_time(session_data, mcts_iterations, heroes):

	itr_no = ["Iterations: " + str(x) for x in mcts_iterations]
	col = ['game ' + str(i) for i in range(0,len(session_data[0]))]
	folder_path = "./data/" + heroes["p1"] + "_vs_" + heroes["p2"]
	df1 = pd.DataFrame(session_data, index=itr_no, columns=col)
	save_DF(df1, folder_path, "avg_computation_time")
	pass

def save_DF(data_frame, path, data_type):
	if not os.path.exists(path):
		os.makedirs(path)
	date = datetime.datetime.now()
	data_frame.to_csv(path+"/" + data_type+"_" + str(date.strftime("%x")).replace("/","_")+".csv")

