from Agents.agent import Agent
from aiThesis.game_state_node import GameStateNode
#from aiThesis.game_session import GameSession
from .mcts_scripts.select_node import select_node
import random
from fireplace import utils
import copy
from aiThesis.game_state_node import GameStateNode
from Agents.mcts_scripts.select_actions import select_and_perform_actions


class MCTSAgent(Agent):
	currentGameState = None  # only for quick test

	def __init__(self, _player):
		self.player = _player
		self.gameTree = []
		self.rootNode = None

	def play_turn(self):
		GameStateNode.nodeCount = 0

		rootNode = GameStateNode(copy.deepcopy(self.player.game))
		#rootNode.print_local_relations()
		#rootNode = expand_game_node(rootNode)

		for i in range(0, 50):
			#print("ITERATIONS: " +str(i))
			select_node(rootNode)

		select_and_perform_actions(rootNode, self.player)

		#rootNode.explored_nodes[0].print_local_relations()
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
