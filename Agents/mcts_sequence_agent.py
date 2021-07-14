from Agents.agent import Agent
from aiThesis.game_state_node import GameStateNode
#from aiThesis.game_session import GameSession
from .mcts_sequential_actions.select_node import select_node, create_actionSpace_for_root_node
import random
from fireplace import utils
import multiprocessing
from multiprocessing.pool import ThreadPool as Pool
import numpy as np
import copy
import time
import math
from aiThesis.game_state_node import GameStateNode
from Agents.mcts_sequential_actions.select_actions import select_and_perform_actions
from aiThesis.tree_plot import generate_tree
class MCTSSequentialAgent(Agent):
	currentGameState = None  # only for quick test

	def __init__(self, _player,_print_tree):
		self.player = _player
		self.gameTree = []
		self.rootNode = None
		self.iterations = 10
		self.action_spaces = []
		self.avg_times_visited_children = []
		self.unexplored_children = []
		self.tree_depths = []
		self.turn_times = []
		self.initial_action_space_length = []
		self.improved_action_space_in_percentage = []
		self.print_tree = _print_tree

	def play_turn(self):
		GameStateNode.nodeCount = 0
		GameStateNode.max_level_depth = 0

		rootNode = GameStateNode(copy.deepcopy(self.player.game))
		#rootNode = expand_game_node(rootNode)

		#while  GameStateNode.max_level_depth <= 3:

		#rootNode = create_actionSpace_for_root_node(rootNode)
		#print("here")
		#print(rootNode.action_space)

		#rootNode.print_local_relations()
		#rootNode = expand_game_node(rootNode)
		#t0 = time.time()
		#delegate_processors(rootNode.action_space, self.player.game)
		#t1 = time.time()
		#print("first timer: " + str(t1-t0))
		t2 = time.time()

		for i in range(self.iterations):
			#print("ITERATIONS: " +str(i))
			select_node(rootNode)
			if len(rootNode.explored_nodes) is 0 and len(rootNode.action_space) is 0:
				break




		self.action_spaces.append(len(rootNode.explored_nodes) + len(rootNode.action_space))
		print("ACTION SPACE: " + str(len(rootNode.explored_nodes)))
		if len(rootNode.action_space) > 0:
			self.avg_times_visited_children.append((len(rootNode.explored_nodes) / (len(rootNode.explored_nodes) + len(rootNode.action_space))))
		else:
			visits = 0
			for child in rootNode.explored_nodes:
				visits += child.number_of_visits
			self.avg_times_visited_children.append(visits / len(rootNode.explored_nodes))
		self.unexplored_children.append(len(rootNode.action_space))
		self.tree_depths.append(rootNode.max_level_depth)
		self.improved_action_space_in_percentage.append(rootNode.improved_action_space_in_percentage)
		self.initial_action_space_length.append(rootNode.initial_action_space_length)
		if len(rootNode.explored_nodes) is not 0:
			play_path = select_and_perform_actions(rootNode, self.player) #fixme should be added to else aswell..
		else:
			print("No actions available, skipping turn...")
		t3 = time.time()
		print("second timer: " + str(t3-t2))
		self.turn_times.append(t3-t2)
		#select_and_perform_actions(rootNode, self.player)

		if self.print_tree != None:
			only_single_turn = True if self.print_tree == "single" else False
			generate_tree(rootNode,play_path, single_turn=only_single_turn)

		#rootNode.explored_nodes[0].print_local_relations()
		print("Tree info:")
		print(" No. of nodes: " + str(GameStateNode.nodeCount))
		print(" Max level depth: " + str(GameStateNode.max_level_depth))

		print("******************************")
		#print(rootNode.number_of_visits)
		#print(rootNode.number_of_wins)

		print(self.player.hand)

		print("Performed optimal action")
		pass
	'''
		print("___________________________________")
		print(self.player.hero.health)
		print("Playing with MCTS agent")
		if MCTSSequentialAgent.currentGameState is not None:
			print("Game turn: " + str(MCTSSequentialAgent.currentGameState.turn))
		print("___________________________________")
		print("Actionable entities: ")
		print(self.player.actionable_entities)
		print("live entities: ")

		print(self.player.field)
	'''




	def construct_tree(self, game):
		pass

	def select_node(self):
		pass

	def expand(self):
		pass

	def simulate(self):
		pass

	def back_propergate(self):
		pass

def delegate_processors(action_space, game_state):
	available_processors = multiprocessing.cpu_count() #fixme handle not enough processors

	action_space_sets = np.array_split(action_space, (len(action_space) if available_processors >= len(action_space) else available_processors))
	tasks = []
	for ass in action_space_sets:
		node = GameStateNode(copy.deepcopy(game_state))
		node.action_space = ass.tolist()
		tasks.append([node])

	pool(tasks)

def run_branch(action_space, game_state):
	print("starting branch: ")
	node = GameStateNode(copy.deepcopy(game_state))

	node.action_space = action_space
	for i in range(100):
		select_node(node)
	print("finished branch: " + str(id))
	return node

def pool(tasks):
	p = Pool(3)
	print(tasks)
	p.map(task_exec, tasks)


def task_exec(data):
	print(data)
	for i in range(0, 100):
		select_node(data[0])
	for node in data[0].explored_nodes:
		action_space_length = str(len(node.action_space)) if node.action_space is not None else "?"
		print("child id: " + str(node.id) + ", depth level: " + str(node.depth_level) + ', p(s): ' + str(
			node.game_state.current_player) + ", action space: " +
			  action_space_length + ", explored nodes: " + str(len(node.explored_nodes)) + ", W/V: " + str(
			node.number_of_wins) + "/" + str(node.number_of_visits))

	print("-------------------------------")

