from Agents.agent import Agent
from aiThesis.morph_node import MorphNode,NodeType
from Agents.mcts_single_action.selection import select_node, player_ref
import copy
from Agents.mcts_single_action.select_actions import select_and_perform_actions
from aiThesis.game_state_node import GameStateNode
import matplotlib.pyplot as plt
from aiThesis.tree_plot import generate_tree
from aiThesis.utils import CMDInterface
class MCTSSingleAgent(Agent):

	PLAYER_REF = None
	def __init__(self, _player, _print_tree):
		self.player = _player
		player_ref.ROOT_PLAYER = self.player
		self.action_spaces = []
		self.avg_times_visited_children = []
		self.unexplored_children = []
		self.tree_depths = []
		self.initial_action_space_length = []
		self.improved_action_space_in_percentage = []
		self.print_tree = _print_tree
		self.iterations = None

	def play_turn(self):

		GameStateNode.nodeCount = 0
		GameStateNode.max_level_depth = 0
		root_node = MorphNode(copy.deepcopy(self.player.game),NodeType.action_node)

		print("starting hand!")
		player_status(self.player)

		#player_status(self.player.game.player2)

		#root_node.print_local_relations()

		for i in range(self.iterations):
			select_node(root_node)
			if len(root_node.explored_nodes) is 0 and len(root_node.action_space) is 0:
				break

		#root_node.print_local_relations()
		print("MCTS Done")

		if self.print_tree != None:
			only_single_turn = True if self.print_tree == "single" else False
			generate_tree(root_node, single_turn=only_single_turn)
		performed_actions = select_and_perform_actions(root_node,self.player)

		print("Actions performed: ", performed_actions)
		player_status(self.player)
		player_status(self.player.game.player2)
		print("switch")

		self.action_spaces.append(len(root_node.explored_nodes) + len(root_node.action_space))
		if len(root_node.action_space) > 0:
			self.avg_times_visited_children.append(
				(len(root_node.explored_nodes) / (len(root_node.explored_nodes) + len(root_node.action_space))))
		else:
			visits = 0
			for child in root_node.explored_nodes:
				visits += child.number_of_visits
			self.avg_times_visited_children.append(visits / len(root_node.explored_nodes))
		self.unexplored_children.append(len(root_node.action_space))
		self.tree_depths.append(root_node.max_level_depth)
		self.improved_action_space_in_percentage.append(root_node.improved_action_space_in_percentage)
		self.initial_action_space_length.append(root_node.initial_action_space_length)
		print("THE ACTION SPACE IS: ")
		print(count_action_space(root_node)+1)


		'''
		print("MCTS FINISHED...")

		print("...")
		print("___________________________________")
		print("i wanna play")
		print(self.player.hero.health)
		print(self.player.hand)
		print("Playing with MCTS agent")

		print("___________________________________")
		print("Actionable entities: ")
		print(self.player.actionable_entities)
		print("live entities: ")
		print(self.player.field)
		print("-")
		'''

def player_status (player):
	print("-------STATUS-------")
	print(player.name)
	print("health: ", player.characters[0].health)
	print("mana: ", player.mana)
	print("Hand: ", player.hand)
	print("field: ", player.field)
	print("graveyard: ", player.graveyard)
	print("--------------")
#break

def count_action_space(_node):
	action_space = 0
	for child in _node.explored_nodes:
		if child.performed_action_space is None:
			continue
		else:
			action_space += 1
			action_space += count_action_space(child)

	return action_space

