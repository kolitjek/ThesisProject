from aiThesis import game_state_node
import random
from fireplace import card
import itertools
from aiThesis import printController
from .partial_action import Partial_action
from hearthstone import enums
import random
from collections import Counter
import copy
from .simulate import simulate_game
import numpy as np


def expand_game_node(_node):
	# Steps:
	# Get partial actions
	# Combine different partial actions
	# return a new game state

	if _node.game_state.state is enums.State.RUNNING:  # Just a failsafe check
		# print("**** Starting expansion phase ****")
		# print("Expanding turn: " + str(_node.game_state.turn) + " (Node:" + str(_node.id)+")" + ", acting player: " + _node.game_state.current_player.hero.data.name)

		if _node.action_space is None:  # Maybe this has to change?
			_node.action_space = permute_action_space(_node)


		if len(_node.action_space) == 0:
			print("Trying to expand an action space of length 0...")
			return

		#action_space_index = random.randint(0, len(_node.action_space) - 1)
		action_space_index = 0
		chosen_action_space = _node.action_space[action_space_index]
		node_to_simulate = game_state_node.GameStateNode(generate_new_state(_node.game_state, chosen_action_space),
														 _node)
		node_to_simulate.performed_action_space = chosen_action_space

		_node.explored_nodes.append(node_to_simulate)
		_node.action_space.pop(action_space_index)
		simulate_game(node_to_simulate, 0)
		# for action_sequence in _node.action_space:
		#	_node.explored_nodes.append(game_state_node.GameStateNode(generate_new_state(_node.game_state,action_sequence), _node))

		# _node.print_local_relations()
		node_to_simulate.game_state.end_turn()  # ends the turn of the current player
	# return _node

	else:
		_node.leaf = True  # Maybe this is not necessary...
		print("The node selected for expansion is terminal...")
		return None


def permute_action_space(_node):
	player = _node.game_state.current_player
	list_of_sequential_actions_hand = player.hand[:]  # The total possible actions from the given space in perspective from the hand
	list_of_sequential_actions_hand.append(
		player.hero.power)  # The total possible actions from the given space in perspective from the board
	list_of_sequential_actions_board = player.characters  # The total possible actions from the given space in perspective from the board

	'''
	for _card in _node.game_state.current_player.actionable_entities:
		if type(_card) is not card.Hero:  # A hero (on its own) cannot act
			if _card.zone is enums.Zone.HAND or type(_card) is card.HeroPower and player.can_pay_cost(_card):  # Actions taken from the hand (IMPORTANT!: this only consider cards it can play in its given state)

				partial_actions_hand.append(_card)
			elif _card.zone is enums.Zone.PLAY and type(_card) is not card.HeroPower:  # Actions from the board
				partial_actions_board.append(_card)
	'''

	# Dividing action between hand and board, is based on the idea that player cards first is optima
	# partial_actions_hand = set(itertools.permutations(partial_actions_hand))  # Permuting every action
	list_of_sequential_actions_hand = retrieve_valid_sequence(list_of_sequential_actions_hand,
															  player.mana)  # Permuting every action
	list_of_sequential_actions_hand_permuted = []
	for action_sequence in list_of_sequential_actions_hand:
		list_of_sequential_actions_hand_permuted += set(itertools.permutations(action_sequence))

	# partial_actions_hand = list({x for x in partial_actions_hand if partial_actions_hand.count(x) >= 1})  # Remove repeating actions sequences
	# partial_actions_hand = evaluate_hand_to_board_sequence(partial_actions_hand, player.mana)  # This returns a squence that the player can afford
	#middle_index = len(list_of_sequential_actions_hand_permuted) // 2
	return list(set(list_of_sequential_actions_hand_permuted))
	list_of_sequential_actions_board = set(itertools.permutations(list_of_sequential_actions_board))  # Permuting every action
	# partial_actions_board = list({x for x in partial_actions_board if partial_actions_board.count(x) >= 1})  # Remove repeating actions sequences

	# if len(partial_actions_hand) is 0:  # Failsafe for no cards in hand
	#	action_sequences = partial_actions_board
	# elif len(partial_actions_board) is 0:  # Failsafe for no cards on board
	#	action_sequences = partial_actions_hand
	# else:
	action_sequences = list(
		itertools.product(list_of_sequential_actions_hand_permuted, list_of_sequential_actions_board))
	for i in range(0, len(action_sequences)):  # Just to convert to a single tuple (not that good...)
		if action_sequences[i][0] is not None and action_sequences[i][1] is not None:
			action_sequences[i] = action_sequences[i][0] + action_sequences[i][1]


	# copy_game_state = copy.deepcopy(_node.game_state)
	return action_sequences


def retrieve_valid_sequence(_action_sequence, player_mana):
	return [seq for i in range(len(_action_sequence), 0, -1) for seq in itertools.combinations(_action_sequence, i) if
			return_mana_sum(seq) <= player_mana]


def return_mana_sum(actions):
	accumulated_mana = 0
	for action in actions:
		accumulated_mana += action.cost
	return accumulated_mana


def transfer_action_sequence(_action_sequence,
							 _game_state):  # This insures that the actions are not applied on the base node
	adapted_action_sequence = []
	player_actions = list(_game_state.current_player.actionable_entities)
	for action in _action_sequence:
		for i in range(0, len(player_actions)):
			if action.id == player_actions[i]:
				adapted_action_sequence.append(player_actions.pop(i))
				break

	return adapted_action_sequence


'''
def evaluate_hand_to_board_sequence(_action_sequence, _player_mana):  # This is the time consumer...
	playable_action_sequences = []
	for _actions in _action_sequence:
		mana_used = 0
		playable_actions = []
		for _card in _actions:
			accumulated_mana = mana_used + _card.cost
			if accumulated_mana <= _player_mana:
				playable_actions.append(_card)
				mana_used += _card.cost

				if accumulated_mana == _player_mana:
					continue

		if len(playable_actions) is not 0:
			playable_action_sequences.append(tuple(playable_actions))

	playable_action_sequences = set(playable_action_sequences)
	#partial_actions_hand = list({x for x in playable_action_sequences if playable_action_sequences.count(x) > 1})  # Remove repeating actions sequences
	return playable_action_sequences
'''


def generate_new_state(_base_game_state, _action_sequence):  # IMPORTANT!: this is based on randm targets
	new_game_state = copy.deepcopy(_base_game_state)
	new_game_state.is_simulation = True
	player = new_game_state.current_player
	printController.disable_print()
	_action_sequence = transfer_action_sequence(_action_sequence, new_game_state)
	for action in _action_sequence:
		target = None
		if type(action) is card.HeroPower:
			if action.is_usable():
				if action.requires_target():
					action.use(target=random.choice(player.opponent.characters))#target = random.choice(action.targets)
				else:
					action.use()

		elif action.zone is enums.Zone.HAND:  # does this covers enough...?
			if action.is_playable():
				if action.must_choose_one:
					action = random.choice(action.choose_cards)
				if action.requires_target():
					if type(action) is card.Spell:
						target = random.choice(action.enemy_targets if action.enemy_targets != [] else action.targets)
						#target = evaluate_spell_targets(action,action.targets)
					# changed this from action.targets
					else:
						target = random.choice(action.targets)
				# print("Playing %r on %r" % (action, targ	et))
				action.play(target=target)

				if player.choice:
					choice = random.choice(player.choice.cards)
					player.choice.choose(choice)
			else:
				if player.choice:
					choice = random.choice(player.choice.cards)
					player.choice.choose(choice)

	for character in player.characters:  # This ignores the action sequence
		if character.can_attack():
			#character.attack(random.choice(character.targets))
			character.attack(evaluate_character_targets(character,character.targets))

	return new_game_state

	'''
	adapted_action_sequence = []
	for action in _action_sequence:
		adapted_action_sequence.append(next(x for x in _game_state.current_player.actionable_entities if x.id == action.id)) #FIXME maybe the same problem I had in select_actions with having two of same minions means that the id is shared...

	return adapted_action_sequence
	'''
def evaluate_character_targets(character, targets):
	if targets[0].health <= character.atk:
		return targets[0]

	for i in range(1, len(targets)):
		if targets[i].health <= character.atk:
			return targets[i]

	if len(targets) > 1:
		return targets[1]
	else:
		return targets[0]

def evaluate_spell_targets(_spell, targets):
	base_game = _spell.game
	#printController.enable_print()
	#print("player: " +  str(base_game.current_player.hero.health))
	#print("opponent: " +  str(base_game.current_player.opponent.hero.health))
	state_metric = -1000
	chosen_target = None
	for target in targets:
		state_outcome = copy.deepcopy(base_game)
		player = state_outcome.current_player
		spell = [x for x in list(player.actionable_entities) if x.entity_id == _spell.entity_id][0]
		target_copy = [x for x in spell.targets if x.entity_id == target.entity_id][0]
		'''
		print(spell.game == _spell.game)
		print(id(_spell.game))
		print(id(spell.game))
		print(id(target.game))
		'''
		spell.play(target=target_copy)

		cp_health_delta = base_game.current_player.hero.health - player.hero.health  #TODO is this a problem with life gain?
		op_health_delta = base_game.current_player.opponent.hero.health - player.opponent.hero.health

		cp_minions_health_delta = sum(c.health for c in base_game.current_player.field) - sum(c.health for c in player.field)
		op_minions_health_delta = sum(c.health for c in base_game.current_player.opponent.field) - sum(c.health for c in player.opponent.field)

		cp_minions_power_delta = sum(c.atk for c in base_game.current_player.field) - sum(c.atk for c in player.field)
		op_minions_power_delta = sum(c.atk for c in base_game.current_player.opponent.field) - sum(c.atk for c in player.opponent.field)

		current_state_metric = cp_health_delta + op_health_delta + cp_minions_health_delta + op_minions_health_delta + cp_minions_power_delta + op_minions_power_delta
		if state_metric < current_state_metric:
			state_metric = current_state_metric
			chosen_target = target

	return chosen_target
		#print("Spell played")
	'''
	if targets[0].health <= character.atk:
		return targets[0]

	for i in range(1, len(targets)):
		if targets[i].health <= character.atk:
			return targets[i]

	if len(targets) > 1:
		return targets[1]
	else:
		return targets[0]
	'''
	pass
