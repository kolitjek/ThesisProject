from hearthstone import enums

from aiThesis.printController import disable_print
from fireplace import card
from aiThesis import game_state_node, printController
from aiThesis.morph_node import MorphNode, NodeType
from aiThesis.single_action_edge import SingleActionEdge, EdgeType
from .simulate import simulate_game
from aiThesis import card_filters
import random
import copy
from .mcts_card_play_order import mcts_card_play_order

INCLUDE_ATTACK = False
TEST = True


play_order = mcts_card_play_order()

def expand_node(_node):

	current_player = _node.game_state.current_player
	id_list = []
	if _node.game_state.state is enums.State.RUNNING:
		if _node.action_space is None:
			_node.action_space = []
			for entity in current_player.actionable_entities:
				if entity.zone is enums.Zone.HAND:
					if entity.is_playable() and entity.cost <= current_player.mana and entity.id not in id_list:
						#print(entity)
						#print(_node.print_local_relations())
						if play_order.filter_action(_node, entity):
							_node.action_space.append(SingleActionEdge(copy.deepcopy(entity), EdgeType.card_play))
							id_list.append(entity.id)
					# print("card in hand: ", entity)
					else:
						pass
				if type(entity) is card.HeroPower and entity.cost <= current_player.mana:
					if not entity.exhausted:
						if play_order.filter_action(_node, entity):
							_node.action_space.append(SingleActionEdge(copy.deepcopy(entity), EdgeType.card_play))


				#						print("can't play card: ", entity)
				elif INCLUDE_ATTACK and entity.zone is enums.Zone.PLAY and type(
					entity) is not card.HeroPower:  # For when attack is included!!!!
					# print("Minion in play: ", entity)
					if type(entity) is card.Hero and entity.atk > 0:
						# _node.action_space.append(entity)
						_node.action_space.append(SingleActionEdge(entity, EdgeType.character_attack))
						# print("Hero can attack")
						break
					elif type(entity) is card.Minion and entity.can_attack():
						# _node.action_space.append(entity)
						_node.action_space.append(SingleActionEdge(entity, EdgeType.character_attack))

			_node.action_space.append(SingleActionEdge(None, EdgeType.empty))

	# print("--------------")
	if len(_node.action_space) == 0:
		print("no more actions to take, ending turn...")

		end_game_state = copy.deepcopy(_node.game_state)
		end_game_state.end_turn()

		end_node = MorphNode(end_game_state, NodeType.end_node, _node)
		end_node.performed_action_space = "end turn"
		_node.explored_nodes.append(end_node)
		expand_node(end_node)
		return

	action_space_index = 0
	chosen_action_space = _node.action_space[action_space_index]

	if chosen_action_space.edge_type == EdgeType.empty:
		node_to_simulate = MorphNode(generate_new_state(_node.game_state, chosen_action_space), NodeType.end_node,
									 _node)
		attack(node_to_simulate.game_state.current_player)
		node_to_simulate.game_state.end_turn()
	else:
		node_to_simulate = MorphNode(generate_new_state(_node.game_state, chosen_action_space), NodeType.action_node,
									 _node)

	node_to_simulate.performed_action_space = chosen_action_space.card
	_node.explored_nodes.append(node_to_simulate)
	_node.action_space.pop(action_space_index)

	simulate_game(node_to_simulate)


# _node.print_local_relations()
# node_to_simulate.print_local_relations()

def return_target(action, player):
	spell_target = player.card_details[action.id]["target"]
	if (spell_target == "opponent"):
		target = card_filters.get_left_most_enemy_target(action.enemy_targets,
														 action.controller) if card_filters.get_left_most_enemy_target(
			action.enemy_targets, action.controller) != [] else random.choice(
			action.targets)  # random.choice(action.enemy_targets if action.enemy_targets != [] else action.targets)
	else:
		target = card_filters.get_left_most_friendly_target(action.targets,
															action.controller) if card_filters.get_left_most_friendly_target(
			action.targets, action.controller) != [] else random.choice(action.targets)

	return target


def transfer_action_sequence(action,
							 _game_state):  # This insures that the actions are not applied on the base node

	if action.card == None:
		return []

	adapted_action_sequence = []
	player_actions = list(_game_state.current_player.actionable_entities)
	for i in range(0, len(player_actions)):
		if action.card.uuid == player_actions[i].uuid:
			adapted_action_sequence.append(player_actions.pop(i))
			break

	return adapted_action_sequence


def generate_new_state(_base_game_state, _action_sequence):  # IMPORTANT!: this is based on randm targets
	new_game_state = copy.deepcopy(_base_game_state)
	new_game_state.is_simulation = True
	player = new_game_state.current_player
	disable_print()
	action_sequence = transfer_action_sequence(_action_sequence, new_game_state)



	for action in action_sequence:
		target = None
		base_card_action = None
		if type(action) is card.HeroPower:
			if action.is_usable():
				if action.requires_target():
					action.use(target=card_filters.get_left_most_enemy_target(player.opponent.characters,
																			  action.controller))  # target = random.choice(action.targets)
				else:
					action.use()

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
					if type(action) is card.Spell:
						target = return_target(action, player)
					# changed this from action.targets
					else:
						target = random.choice(action.targets)
				# print("Playing %r on %r" % (action, targ	et))
				try:
					if action.is_playable():
						if base_card_action is None:
							action.play(target=target)
						else:
							base_card_action.play(target=target, choose=action)
				except NameError:
					print(NameError)

				if player.choice:
					choice = random.choice(player.choice.cards)
					player.choice.choose(choice)
			else:
				if player.choice:
					choice = random.choice(player.choice.cards)
					player.choice.choose(choice)

	'''for character in player.characters:
		if character.can_attack():
			character.attack(
				card_filters.get_left_most_enemy_target(character.targets, player))  # random.choice(character.targets))'''

	return new_game_state


def attack(player):
	for character in player.characters:
		if character.can_attack():
			character.attack(
				card_filters.get_left_most_enemy_target(character.targets, player))  # random.choice(character.targets))


'''
if(_node.performed_action_space is not None and entity.id == _node.performed_action_space.id):
							print("parent had same id, running up")
							temp = copy.deepcopy(_node)
							print("child hand")
							print(temp.game_state.current_player.hand)
							temp.print_local_relations()

							print(entity.id)

							count = 0
							while temp.parent != None and temp.performed_action_space is not None and temp.performed_action_space.id == entity.id:


								count += 1
								print("same: ", count)

								temp = temp.parent
								print("parent hand")
								print(temp.game_state.current_player.hand)
								#print(entity.uuid == temp.performed_action_space.uuid)
								temp.print_local_relations()
							print("end....")
'''
