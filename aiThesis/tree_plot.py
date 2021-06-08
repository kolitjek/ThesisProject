import matplotlib.pyplot as plt
import networkx as nx
import pydot
import graphviz
from networkx.drawing.nx_pydot import graphviz_layout

def generate_tree(_root, single_turn = True):

	if single_turn:
		tree_nodes = retrieve_nodes_single_turn(_root)
	if not single_turn:
		tree_nodes = retreive_nodes_all()


	g = nx.DiGraph()
	graph_nodes = [(_root.id, {"color": "blue"})]
	graph_edges = []
	for node in tree_nodes:
		graph_nodes.append((node.id, {"color": "blue" if node.game_state.current_player.name == _root.game_state.current_player.name else 'red'}))
		graph_edges.append((node.parent.id, node.id, {"entity": str(node.performed_action_space)}))

	g.add_nodes_from(graph_nodes)
	g.add_edges_from(graph_edges)
	'''
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
	'''


	pos = graphviz_layout(g, prog="dot")
	node_colors = list(nx.get_node_attributes(g,"color").values())
	edge_labels = nx.get_edge_attributes(g, 'entity')
	#p = nx.drawing.nx_pydot.to_pydot(g)
	nx.draw(g, pos,with_labels=True, node_color=node_colors)
	nx.draw_networkx_edge_labels(g, pos, edge_labels);
	plt.show()
	print("asd")
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

def retreive_nodes_all():
	pass

