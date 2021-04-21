from itertools import chain

from .graphs import *
import itertools
import operator
import numpy as np

def health_distribution_graph(session_data):
	player1_health =[]
	player2_health =[]
	for game_data in session_data:
		player1_health.append(game_data.game_data[-1].player1_health)
		player2_health.append(game_data.game_data[-1].player2_health)

	print(player1_health)
	print(player2_health)


	create_graph([player1_health, player2_health], ["Player 1", "Player 2"], ["Health", "Frequency"])

def line_graph(session_data, mcts_iterations):
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

	create_line_graph([x], [y],  ["Iterations", "Win percentage"], ["Line"])

def avg_max_turn_box_plot(session_data, mcts_iterations):
	number_of_different_iterations = len(mcts_iterations)
	max_turn = []
	for game_data in session_data:
		max_turn.append(game_data.game_data[-1].turn_number)
	n_split = np.array_split(max_turn, number_of_different_iterations)
	x = [["0"]]
	y = [np.array([0.0])]
	for i in mcts_iterations[:]:
		x.append([i])
	for iterations in n_split:
		y.append(iterations)
	print("avg_max_turn X: " +str(x))
	print("avg_max_turn Y: " + str(y))

	create_box_plot(x, y, ["Iterations", "Max_turn"])


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


def avg_mcts_action_space_pr_turn(session_data, mcts_iterations): #session_data_lists, mcts_iterations, text_x, text_y
	number_of_different_iterations = len(mcts_iterations)
	to_be_split = []
	for game_data in session_data:
		to_be_split.append(game_data.action_spaces)
	n_split = (np.array_split(to_be_split, number_of_different_iterations))
	n_split = [x.tolist() for x in n_split]
	print(n_split)
	result =[]
	for action_spaces in n_split:
		print("\n")
		print("Action space: " + str(action_spaces))
		lists = list(map(list,itertools.zip_longest(*action_spaces)))
		result.append( [sum([i for i in x if i is not None]) / len([i for i in x if i is not None]) for x in lists])
		print("Action space split list: " + str(lists))
		print("Action space result: " + str (result))
	x = list(([(range(0, len(i)) for i in result)])[0])
	create_line_graph(x, result, ["Turn", "Action space"], label=["Iterations: " + str(x) for x in mcts_iterations])


def avg_mcts_avg_times_visited_children_pr_turn(session_data, mcts_iterations): #session_data_lists, mcts_iterations, text_x, text_y
	number_of_different_iterations = len(mcts_iterations)
	to_be_split = []
	for game_data in session_data:
		to_be_split.append(game_data.avg_times_visited_children)
	n_split = (np.array_split(to_be_split, number_of_different_iterations))
	n_split = [x.tolist() for x in n_split]
	result =[]
	for avg_times_visited_children in n_split:
		print("\n")
		print("avg_times_visited_children : " + str(avg_times_visited_children))
		lists = list(map(list,itertools.zip_longest(*avg_times_visited_children)))
		print("avg_times_visited_children split list: " + str(lists))
		result.append( [sum([i for i in x if i is not None]) / len([i for i in x if i is not None]) for x in lists])
		print("avg_times_visited_children result: " + str(result))
	x = list(([(range(0, len(i)) for i in result)])[0])
	create_line_graph(x, result, ["Turn", "avg_times_visited_children"], label=["Iterations: " + str(x) for x in mcts_iterations])


def avg_mcts_unexplored_children_pr_turn(session_data, mcts_iterations): #session_data_lists, mcts_iterations, text_x, text_y
	number_of_different_iterations = len(mcts_iterations)
	to_be_split = []
	for game_data in session_data:
		to_be_split.append(game_data.unexplored_children)
	n_split = (np.array_split(to_be_split, number_of_different_iterations))
	n_split = [x.tolist() for x in n_split]
	result =[]
	for unexplored_children in n_split:
		print("\n")
		print("Unexplored_children: " + str(unexplored_children))
		lists = list(map(list, itertools.zip_longest(*unexplored_children)))
		print("unexplored_children split list: " + str(lists))
		print([len([i for i in x if i is not None]) for x in lists])
		result.append([sum([i for i in x if i is not None]) / len([i for i in x if i is not None]) for x in lists])
		print("unexplored_children result: " + str(result))
	x = list(([(range(0, len(i)) for i in result)])[0])
	create_line_graph(x, result, ["Turn", "unexplored_children"], label=["Iterations: " + str(x) for x in mcts_iterations])


def avg_mcts_tree_depths_pr_turn(session_data, mcts_iterations): #session_data_lists, mcts_iterations, text_x, text_y
	number_of_different_iterations = len(mcts_iterations)
	to_be_split = []
	for game_data in session_data:
		to_be_split.append(game_data.tree_depths)
	n_split = (np.array_split(to_be_split, number_of_different_iterations))
	n_split = [x.tolist() for x in n_split]
	result =[]
	for tree_depths in n_split:
		print("\n")
		print("Tree_depts: " + str(tree_depths))
		lists = list(map(list,itertools.zip_longest(*tree_depths)))
		print("tree_depths split list: " + str(lists))
		print([len([i for i in x if i is not None]) for x in lists])
		result.append([sum([i for i in x if i is not None]) / len([i for i in x if i is not None]) for x in lists])
		print("tree_depths result: " + str(result))
	x = list(([(range(0, len(i)) for i in result)])[0])

	create_line_graph(x, result, ["Turn", "tree_depths"], label=["Iterations: " + str(x) for x in mcts_iterations])
