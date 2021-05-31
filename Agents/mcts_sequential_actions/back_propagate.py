def back_propagate(node, is_win):
	#node.game_state.end_turn()
	curr_node = node
	while curr_node is not None:
		if is_win:
			curr_node.number_of_wins += 1

		curr_node.number_of_visits += 1
		curr_node = curr_node.parent




