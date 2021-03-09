from aiThesis import game_state_node
def expand_game_node (acting_player):

	print("Looking action space...")
	for card in acting_player.actionable_entities:
		print(card)
		print(acting_player.can_pay_cost(card))

	pass
