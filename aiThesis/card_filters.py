from fireplace import card


def get_enemy_targets(targets, current_player):
	enemy_targets = []
	for card in targets:
		if card.controller is not current_player:
			enemy_targets.append(card)
	return enemy_targets


def get_left_most_enemy_target(targets, current_player):
	enemy_targets = get_enemy_targets(targets, current_player)
	#print("ENEMY TARGETS: ")
	#print(enemy_targets)
	#print("CHOOSE: ")
	if len(enemy_targets) > 0:
		if len(enemy_targets) > 1:
			if type(enemy_targets[0]) is card.Hero:
				#print("card is hero")
				#print(enemy_targets[1])
				return enemy_targets[1]
			else:
				#print("card is not hero but can attack minion")
				#print(enemy_targets[0])
				return enemy_targets[0]
		else:
			#print("only one target")
			#print(enemy_targets[0])
			return enemy_targets[0]
	else:
		#print("got to the end")
		#print(enemy_targets)
		return enemy_targets  # should be empty set by now

