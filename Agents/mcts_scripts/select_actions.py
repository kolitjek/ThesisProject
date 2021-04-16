from aiThesis import printController
from fireplace import card
from hearthstone import enums
import random
from aiThesis import card_filters


from fireplace.targeting import is_valid_target


def select_and_perform_actions(root_node, player):

	perform_action_sequence(select_best_node(root_node).performed_action_space, player)
	pass

def select_best_node(root_node):
	best_node = None
	for n in root_node.explored_nodes:
		if n.isLeaf and n.number_of_wins is 1:
			print("i'm gonna win!")
			print_tree(root_node, n)
			return n

		if best_node is None or (n.number_of_visits >= best_node.number_of_visits and best_node.number_of_wins < n.number_of_wins):
			best_node = n
	print_tree(root_node, best_node)
	return best_node


def print_tree(root_node, best_node):
	root_node.print_local_relations()

	if(best_node != None):
		print("Chosen node: " + str(best_node.id))


def transfer_action_sequence(_action_sequence, _player):  # This insures that the actions are not applied on the base node
	adapted_action_sequence = []
	player_actions = _player.hand + [_player.hero.power] + _player.characters # list(_player.actionable_entities)
	print("ACTIONS")
	print(_action_sequence)
	for action in _action_sequence:
		for i in range(0, len(player_actions)):
			if action.id == player_actions[i]:
				adapted_action_sequence.append(player_actions.pop(i))
				break


	return adapted_action_sequence


def perform_action_sequence(_action_sequence, player):  # IMPORTANT!: this is based on randm targets

	_action_sequence = transfer_action_sequence(_action_sequence, player)
	printController.disable_print()


	print("Actions to perfrom")
	print(_action_sequence)

	for action in _action_sequence:
		target = None

		if type(action) is card.HeroPower:
			print("ACtion useable")
			print(action.is_usable())
			if action.is_usable():
				if action.requires_target():
					action.use(target=card_filters.get_left_most_enemy_target(action.enemy_targets, action.controller) )#random.choice(player.opponent.characters)) #changed this from action.targets
				else:
					action.use()
				continue  # need this because hero is a special card type

		elif action.zone is enums.Zone.HAND:  # does this covers enough...?
			if action.is_playable():
				if action.must_choose_one:
					action = action.choose_cards[0]
				if action.requires_target():
					spell_target = player.card_details[action.id]["target"]

					if (spell_target == "opponent"):
						target = card_filters.get_left_most_enemy_target(action.enemy_targets,
																		 action.controller) if card_filters.get_left_most_enemy_target(
							action.enemy_targets, action.controller) != [] else random.choice(
							action.targets)  # random.choice(action.enemy_targets if action.enemy_targets != [] else action.targets)
					else:
						target = card_filters.get_left_most_friendly_target(action.targets,
																			action.controller) if card_filters.get_left_most_friendly_target(
							action.enemy_targets, action.controller) != [] else random.choice(action.targets)
					'''
					if type(action) is card.Spell:
						target = card_filters.get_left_most_enemy_target(action.enemy_targets, action.controller) if card_filters.get_left_most_enemy_target(action.enemy_targets, action.controller) != [] else random.choice(action.targets) #random.choice(action.enemy_targets if action.enemy_targets != [] else action.targets)
						#changed this from action.targets
					else:
						target = random.choice(action.targets)
					'''
				#print("Playing %r on %r" % (action, targ	et))
				try:
					action.play(target=target)
				except NameError:
					print(NameError)
			#else: I think this causes the "can't end with open action..."
				if player.choice:
					choice = random.choice(player.choice.cards)
					player.choice.choose(choice)

	for character in player.characters:
				if character.can_attack():
					character.attack(card_filters.get_left_most_enemy_target(character.targets, player))#random.choice(character.targets))






