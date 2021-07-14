import matplotlib.pyplot as plt
import networkx as nx
import pydot
import graphviz
from networkx.drawing.nx_pydot import graphviz_layout
from hearthstone.enums import BlockType, CardType, PlayState, State, Step, Zone
def generate_tree(_root, play_path, single_turn = True):

	if single_turn:
		tree_nodes = retrieve_nodes_single_turn(_root)
	if not single_turn:
		tree_nodes = retreive_nodes_all(_root)

	g = nx.DiGraph()
	graph_nodes = [(_root.id, {"color": "#A4D8F3"})]
	graph_edges = []
	for node in tree_nodes:
		edge_color = 'black'
		mcts_win = False
		if node.isLeaf and node.game_state.state == State.COMPLETE:
			for player in node.game_state.players:
				if player.name == _root.game_state.current_player.name:
					mcts_win = player.playstate == PlayState.WON
			graph_nodes.append((node.id, {"color": "#A5F2B3" if mcts_win else '#F2EEA5'}))
			for action_node in play_path:
				if action_node.id is node.id:
					edge_color = '#E15BF4'
			graph_edges.append((node.parent.id, node.id, {"entity": str(node.performed_action_space), "color": edge_color}))
		else:
			graph_nodes.append((node.id, {
				"color": "#A4D8F3" if node.game_state.current_player.name == _root.game_state.current_player.name else '#F7BABA'}))
			#for action_node in play_path:
			#	if action_node.id is node.id:
			#		edge_color = '#E15BF4'

			graph_edges.append(
				(node.parent.id, node.id, {"entity": str(node.performed_action_space), "color": edge_color}))

	g.add_nodes_from(graph_nodes)
	g.add_edges_from(graph_edges)

	pos = graphviz_layout(g, prog="dot")
	node_colors = list(nx.get_node_attributes(g,"color").values())
	edge_labels = nx.get_edge_attributes(g, 'entity')
	edge_color = nx.get_edge_attributes(g, 'color').values()
	#p = nx.drawing.nx_pydot.to_pydot(g)
	nx.draw(g, pos,with_labels=True, node_color=node_colors, edge_color= edge_color)
	nx.draw_networkx_edge_labels(g, pos, edge_labels)
	plt.show()
	#plt.savefig("tree_plots/path.png")

def retrieve_nodes_single_turn(_root_node):
	action_spaces = []
	for child in _root_node.explored_nodes:
		if child.performed_action_space is None:
			continue
		else:
			action_spaces.append(child)
			one_layer_deeper = retrieve_nodes_single_turn(child)
			if one_layer_deeper != []:
				for item in one_layer_deeper:
					action_spaces.append(item)

	return action_spaces

def retreive_nodes_all(_root_node):
	action_spaces = []
	for child in _root_node.explored_nodes:

		action_spaces.append(child)
		one_layer_deeper = retreive_nodes_all(child)

		for item in one_layer_deeper:
			action_spaces.append(item)
	return action_spaces


	child1 = _root.explored_nodes[0]
	child2 = _root.explored_nodes[1]
	child3 = _root.explored_nodes[2]

	g.add_nodes_from([
		(_root.id, {"color": "blue" if child1.game_state.current_player == child1.game_state.current_player else 'red'}),
		(child1.id, {"color": "blue" if child1.game_state.current_player == child1.game_state.current_player else 'red'}),
		(child2.id, {"color": "red"}),
		(child3.id, {"color": "red"}),
	])
	g.add_edges_from([
		(child1.parent.id, child1.id, {"entity":str(child1.performed_action_space)}),
		(child2.parent.id,child2.id,  {"entity":str(child2.performed_action_space)}),
		(child3.parent.id, child3.id, {"entity":str(child3.performed_action_space)})
	])

