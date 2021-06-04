from enum import Enum


class EdgeType(Enum):
	empty = 0
	character_attack = 1
	card_play = 2


class SingleActionEdge:
	def __init__(self, _card, _edge_type, _target = None):
		self.edge_type = _edge_type
		self.card = _card
		if _edge_type is EdgeType.character_attack:
			if _target is not None:
				self.target = _target
			else:
				raise Exception("ERROR! minion attack edge created WITHOUT target")


