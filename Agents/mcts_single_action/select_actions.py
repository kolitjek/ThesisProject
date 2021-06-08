from aiThesis import printController
from fireplace import card
from hearthstone import enums
import random
import copy
from aiThesis import card_filters
from .selection import action_traversal
from aiThesis.morph_node import NodeType


def select_and_perform_actions(root_node, player):

	selected_actions = select_best_node(root_node)
	perform_action_sequence(selected_actions, player)
	return selected_actions



def select_best_node(root_node):
	best_node = None
	for n in root_node.explored_nodes:
		if n.isLeaf and n.number_of_wins is 1:
			print("i'm gonna win!")
			return [n.performed_action_space]

	frontier_node = copy.deepcopy(root_node)

	#frontier_node.print_local_relations()
	action_list = []
	while len(frontier_node.explored_nodes) > 0 and frontier_node.node_type is not NodeType.end_node:
		temp_action_id = frontier_node.performed_action_space
		frontier_node = copy.deepcopy(action_traversal(frontier_node))
		#print("Action performed of the selected node (not added yet): ", frontier_node.performed_action_space)
		#frontier_node.print_local_relations()

		if temp_action_id is not None and temp_action_id == frontier_node.performed_action_space:
			print("SAME CARD")

		if root_node.game_state.current_player.name == frontier_node.game_state.current_player.name:
			print("I can take this action...")
		else:
			print("this is my opponent....")

		if frontier_node.node_type is not NodeType.end_node:
			action_list.append(frontier_node.performed_action_space)
	return action_list


def transfer_action_sequence(_action_sequence, _player):  # This insures that the actions are not applied on the base node
	adapted_action_sequence = []
	player_actions = _player.hand + [_player.hero.power] + _player.characters # list(_player.actionable_entities)
	#print("ACTIONS")
	#print(_action_sequence)
	saved_actions = []
	for action in _action_sequence:

		if(action == "end turn" or action == None):
			continue

		for i in range(0, len(player_actions)):
			if action.uuid == player_actions[i].uuid and action.uuid not in adapted_action_sequence:
				#print("action match")
				adapted_action_sequence.append(player_actions[i])



	return adapted_action_sequence


def perform_action_sequence(_action_sequence, player):  # IMPORTANT!: this is based on randm targets


	_action_sequence = transfer_action_sequence(_action_sequence, player)
	printController.disable_print()
	#printController.enable_print()



	#print("Actions to perfrom")
	#print(_action_sequence)

	for action in _action_sequence:
		target = None
		base_card_action = None
		if type(action) is card.HeroPower:
			#print("ACtion useable")
			#print(action.is_usable())
			if action.is_usable():
				if action.requires_target():
					action.use(target=card_filters.get_left_most_enemy_target(action.enemy_targets, action.controller) )#random.choice(player.opponent.characters)) #changed this from action.targets
				else:
					action.use()
				continue  # need this because hero is a special card type

		elif action.zone is enums.Zone.HAND:  # does this covers enough...?
			if action.is_playable():
				if action.must_choose_one:
					chosen_spell = player.card_details[action.id]["choose_0"]
					alternative_spell = player.card_details[action.id]["choose_1"]

					if action.choose_cards.filter(id=chosen_spell)[0].is_playable():
						base_card_action = action
						action = action.choose_cards.filter(id=chosen_spell)[0]
					elif action.choose_cards.filter(id=alternative_spell)[0].is_playable():
						base_card_action = action
						action = action.choose_cards.filter(id=alternative_spell)[0]

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
					if action.is_playable():
						if base_card_action is None:
							action.play(target=target)
						else:
							base_card_action.play(target=target, choose = action)
				except NameError:
					print(NameError)
			#else: I think this causes the "can't end with open action..."
				if player.choice:
					choice = random.choice(player.choice.cards)
					player.choice.choose(choice)

	for character in player.characters:
				if character.can_attack():
					character.attack(card_filters.get_left_most_enemy_target(character.targets, player))#random.choice(character.targets))






