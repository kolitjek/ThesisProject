from Agents.agent import Agent
from aiThesis.game_state_node import GameStateNode
#from aiThesis.game_session import GameSession
import random
from fireplace import utils
class MCTSAgent(Agent):
	currentGameState = None  # only for quick test
	nodeCount = 0

	def __init__(self, _player):
		self.player = _player
		self.gameTree = []
		self.rootNode = None

	def play_turn(self):
		rootNode = GameStateNode(MCTSAgent.nodeCount)
		rootNode.print_local_relations()

		print("___________________________________")

		print("Playing with MCTS agent")
		if MCTSAgent.currentGameState is not None:
			print("Game turn: " + str(MCTSAgent.currentGameState.turn))
		print("___________________________________")
		print("Actionable entities: ")
		for entety in self.player.actionable_entities:
			print(entety)


	def construct_tree(self, game):
		pass

	def select_node(self):
		pass

	def expand(self):
		pass

	def simulate(self):
		pass

	def backpropergate(self):
		pass
