
class GameStateNode:
	nodeCount = 0
	max_level_depth = 0
	depth = 0

	def __init__(self, _game_state, _parent=None):
		self.id = GameStateNode.nodeCount
		GameStateNode.nodeCount += 1

		if _parent is not None:
			self.depth_level = _parent.depth_level + 1

			if GameStateNode.max_level_depth < self.depth_level:
				GameStateNode.max_level_depth = self.depth_level
		else:
			self.depth_level = 0


		self.game_state = _game_state
		self.parent = _parent
		self.performed_action_space = None
		self.action_space = None
		self.explored_nodes = []
		self.isLeaf = False
		self.number_of_visits = 0
		self.number_of_wins = 0
		self.initial_action_space_length = 0
		self.improved_action_space_in_percentage = 0

	def print_local_relations(self):

		print("------- Node relations -------")
		action_space_length = str(len(self.action_space)) if self.action_space is not None else "?"

		print("Node id: " + str(self.id) + ", depth level: " + str(self.depth_level) + ', p(s): ' + str(self.game_state.current_player) + ", action space: " + action_space_length + ", explored nodes: "
			  + str(len(self.explored_nodes)) + ", W/V: " + str(self.number_of_wins) + "/" + str(self.number_of_visits))

		if self.parent is not None:
			print("Parent id: " + str(self.parent.id) + ", parent depth level: " + str(self.parent.depth_level) + ", W/V: " + str(self.parent.number_of_wins) + "/" + str(self.parent.number_of_visits))
		else:
			print("Root Node")

		print("** Explored children Nodes **")

		for node in self.explored_nodes:
			action_space_length = str(len(node.action_space)) if node.action_space is not None else "?"
			print("child id: " + str(node.id) + ", depth level: " + str(node.depth_level) + ', p(s): ' + str(node.game_state.current_player) +", performed actions: "+ str(node.performed_action_space) + ", action space: " +
				action_space_length + ", explored nodes: " + str(len(node.explored_nodes)) + ", W/V: " + str(node.number_of_wins) + "/" + str(node.number_of_visits))

		print("-------------------------------")

	def update_node(self, did_win):
		self.number_of_visits += 1
		if did_win:
			self.number_of_wins += 1
