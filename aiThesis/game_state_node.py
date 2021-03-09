class GameStateNode:
	def __init__(self, _id, _parent=None):
		self.id = _id
		self.depthLevel = _id
		self.game = None
		self.parent = _parent
		self.actionSpace = []
		self.exploredNodes = []
		self.leaf = False
		self.numberOfVisits = 0
		self.numberOfWins = 0

	def print_local_relations(self):
		print("------- Node relations -------")
		print("Node id: " + str(self.id) + ", depth level: " + str(self.depthLevel) + ", action space:" + str(len(self.actionSpace)) + ", explored nodes: " + str(len(self.exploredNodes)))

		if self.parent is not None:
			print("Parent id: " + str(self.parent.id) + ", parent depth level: " + str(self.parent.depthLevel))
		else:
			print("Root Node")

		print("** Explored children Nodes **")

		for node in self.exploredNodes:
			print("child id: " + str(node.id) + ", depth level: " + str(node.depthLevel) + ", action space:" +
				str(len(self.actionSpace)) + ", explored nodes: " + str(len(self.exploredNodes)))

		print("-------------------------------")

	def update_node(self, did_win):
		self.numberOfVisits += 1
		if did_win:
			self.numberOfWins += 1
