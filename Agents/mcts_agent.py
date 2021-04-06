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
		GameStateNode.max_level_depth = 0

		rootNode = GameStateNode(copy.deepcopy(self.player.game))
		#rootNode.print_local_relations()
		#rootNode = expand_game_node(rootNode)

		#while  GameStateNode.max_level_depth <= 3:
		for i in range(0, 50):

			#print("ITERATIONS: " +str(i))
			select_node(rootNode)
			if len(rootNode.explored_nodes) is 0 and len(rootNode.action_space) is 0:
				break

		if len(rootNode.explored_nodes) is not 0:
			select_and_perform_actions(rootNode, self.player)
		else:
			print("No actions available, skipping turn...")
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
