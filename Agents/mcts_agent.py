from Agents.agent import Agent
from aiThesis.game_state_node import GameStateNode
#from aiThesis.game_session import GameSession
from .mcts_scripts.select_node import select_node
import random
from fireplace import utils
import copy

class MCTSAgent(Agent):
	currentGameState = None  # only for quick test


	def __init__(self, _player):
		self.player = _player
		self.gameTree = []
		self.rootNode = None

	def play_turn(self):
		rootNode = GameStateNode(copy.deepcopy(self.player.game))
		rootNode.print_local_relations()
		#rootNode = expand_game_node(rootNode)
		print("blaaaah")

		for i in range(0, 3):
			select_node(rootNode)
		best_node_visits = -1
		best_node = None
		for n in rootNode.explored_nodes:
			if n.number_of_visits > best_node_visits:
				best_node = n
				best_node_visits = n.number_of_visits
		rootNode.explored_nodes[0].print_local_relations()
		print("******************************")
		print(rootNode.number_of_visits)
		print(rootNode.number_of_wins)


		print("s")
	'''
		print("___________________________________")
		print(self.player.hero.health)
		print("Playing with MCTS agent")
		if MCTSAgent.currentGameState is not None:
			print("Game turn: " + str(MCTSAgent.currentGameState.turn))
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
