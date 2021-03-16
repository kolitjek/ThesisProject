
class GameStateNode:
	nodeCount = 0
	depth = 0

	def __init__(self, _game_state, _parent=None):
		self.id = GameStateNode.nodeCount
		GameStateNode.nodeCount += 1

		if _parent is not None:
			self.depth_level = _parent.depth_level + 1
		else:
			self.depth_level = 0

		self.game_state = _game_state
		self.parent = _parent
		self.action_space = []
		self.explored_nodes = []
		self.leaf = False
		self.number_of_visits = 0
		self.number_of_wins = 0

	def print_local_relations(self):
		print("------- Node relations -------")
		print("Node id: " + str(self.id) + ", depth level: " + str(self.depth_level) + ", action space:" + str(len(self.action_space)) + ", explored nodes: " + str(len(self.explored_nodes)))

		if self.parent is not None:
			print("Parent id: " + str(self.parent.id) + ", parent depth level: " + str(self.parent.depthLevel))
		else:
			print("Root Node")

		print("** Explored children Nodes **")

		for node in self.explored_nodes:
			print("child id: " + str(node.id) + ", depth level: " + str(node.depth_level) + ", action space:" +
				str(len(node.action_space)) + ", explored nodes: " + str(len(node.explored_nodes)))

		print("-------------------------------")

	def update_node(self, did_win):
		self.number_of_visits += 1
		if did_win:
			self.number_of_wins += 1
