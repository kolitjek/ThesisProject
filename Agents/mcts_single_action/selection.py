from .expand import expand_node
import math
from .expand import expand_node
from hearthstone import enums

class player_ref:
	ROOT_PLAYER = None

def select_node (node):
	return uct(node)

def uct(node, traversal = False):
	c = 1.41421 # math.sqrt(2), C is a constant to adjust the amount of exploration and incorporates the sqrt(2) from the UCB1 formula
							#Ved ikke lige med den C her
	arg_max_n = -1.0
	node_to_select = node
	if node.action_space is None or len(node.action_space) is not 0:
		expand_node(node)
		return

	for n in node.explored_nodes:
		#print(n.number_of_visits)
		#print(n.parent.number_of_visits)

		#min_max_wins = n.number_of_wins if node.depth_level % 2 is 0 else n.number_of_visits - n.number_of_wins #FIXME check if the switch is working
		min_max_wins = n.number_of_wins if player_ref.ROOT_PLAYER.uuid == node.game_state.current_player.uuid else n.number_of_visits - n.number_of_wins

		x = min_max_wins / n.number_of_visits
		uct = x + c * math.sqrt((math.log2(n.parent.number_of_visits)/n.number_of_visits))
		if uct > arg_max_n and not n.isLeaf:
			arg_max_n = uct
			node_to_select = n


	if node_to_select.game_state.state is not enums.State.RUNNING or node_to_select.id == node.id:
		node_to_select.isLeaf = True
		if node_to_select.parent is not None:
			select_node(node_to_select.parent)
		return

	if node_to_select.action_space is None or len(node.action_space) is not 0:
		#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		#print("Player: " + str(node_to_select.game_state.current_player))
		#print("Node ID if: " + str(node_to_select.id))
		#node_to_select.parent.print_local_relations()
		#node_to_select.print_local_relations()
		expand_node(node_to_select)
		#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	else:
		select_node(node_to_select)
		#print("Node ID else: " + str(node_to_select.id))

	#print("Node ID: " + str(node_to_select.id))
'''
def create_actionSpace_for_root_node(node):
	node.action_space = permute_action_space(node)
	return node
'''
def action_traversal (node):
	c = 1.41421  # math.sqrt(2), C is a constant to adjust the amount of exploration and incorporates the sqrt(2) from the UCB1 formula
	# Ved ikke lige med den C her
	arg_max_n = -1.0
	node_to_select = node
	best_node = None

	for n in node.explored_nodes:
		#print(n.number_of_visits)
		#print(n.parent.number_of_visits)

		#min_max_wins = n.number_of_wins if node.depth_level % 2 is 0 else n.number_of_visits - n.number_of_wins #FIXME check if the switch is working

		if best_node is None or (n.number_of_visits >= best_node.number_of_visits and best_node.number_of_wins < n.number_of_wins):
			best_node = n
		'''
		min_max_wins = n.number_of_wins

		x = min_max_wins / n.number_of_visits
		uct = x
		if uct > arg_max_n:
			arg_max_n = uct
			node_to_select = n
		'''
	return best_node
