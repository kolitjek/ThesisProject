from .game_state_node import GameStateNode
from enum import Enum

0
class NodeType(Enum):
	undefined = 0
	end_node = 1
	action_node = 2


class MorphNode(GameStateNode):
	nodeCount = 0
	max_level_depth = 0
	depth = 0
	def __init__(self, _game_state, _node_type, _parent=None):
		super().__init__(_game_state, _parent)
		self.node_type = _node_type

