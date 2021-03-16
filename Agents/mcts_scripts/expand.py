from aiThesis import game_state_node
from hearthstone.enums import CardType
from fireplace import card
import itertools
from Agents import mcts_agent
from .partial_action import Partial_action
from hearthstone import enums
import random
from collections import Counter
import copy

def expand_game_node (_node):

	# Steps:
	# Get partial actions
	# Combine different partial actions
	# return a new game state

	if _node.game_state.state is enums.State.RUNNING:  # Just a failsafe check
		print("**** Starting expansion phase ****")
		print("Expanding turn: " + str(_node.game_state.turn) + ", acting player: " + _node.game_state.current_player.hero.data.name)

		if len(_node.action_space) is 0:  # Maybe this has to change?
			_node.action_space = permute_action_space(_node)

		for action_sequence in _node.action_space:
			pass
	else:
		_node.leaf = True  # Maybe this is not necessary...
		print("The node selected for expansion is terminal...")
		return None

def permute_action_space(_node):
	partial_actions_hand = []  # The total possible actions from the given space in perspective from the hand
	partial_actions_board = []  # The total possible actions from the given space in perspective from the board
	player = _node.game_state.current_player
	print(player.hero.power)
	for _card in _node.game_state.current_player.actionable_entities:
		if type(_card) is not card.Hero:  # A hero (on its own) can not act
			if _card.zone is enums.Zone.HAND or _card is player.hero.power and player.can_pay_cost(_card):  # Actions taken from the hand (IMPORTANT!: this only consider cards it can play in its given state)
				partial_actions_hand.append(_card)
			elif _card.zone is enums.Zone.PLAY:  # Actions from the board
				partial_actions_board.append(_card)

	# Dividing action between hand and board, is based on the idea that player cards first is optimal
	partial_actions_hand = list(itertools.permutations(partial_actions_hand))  # Permuting every action
	partial_actions_hand = list({x for x in partial_actions_hand if partial_actions_hand.count(x) >= 1})  # Remove repeating actions sequences
	partial_actions_hand = evaluate_hand_to_board_sequence(partial_actions_hand, player.mana)  # This returns a squence that the player can afford

	partial_actions_board = list(itertools.permutations(partial_actions_board))  # Permuting every action
	partial_actions_board = list({x for x in partial_actions_board if partial_actions_board.count(x) >= 1})  # Remove repeating actions sequences

	if len(partial_actions_hand) is 0:  # Failsafe for no cards in hand
		action_sequences = partial_actions_board
	elif len(partial_actions_board) is 0:  # Failsafe for no cards on board
		action_sequences = partial_actions_hand
	else:
		action_sequences = list(itertools.product(partial_actions_hand, partial_actions_board))
		for i in range(0, len(action_sequences)):  # Just to convert to a single tuple
			if action_sequences[i][0] is not None and action_sequences[i][1] is not None:
				action_sequences[i] = action_sequences[i][0] + action_sequences[i][1]

	copy_game_state = copy.deepcopy(_node.game_state)
	return action_sequences

def evaluate_hand_to_board_sequence(_action_sequence, _player_mana):  # This only takes into account what the can play right now
	playable_action_sequences = []
	for _actions in _action_sequence:
		mana_used = 0
		playable_actions = []
		for _card in _actions:
			if mana_used + _card.cost <= _player_mana:
				playable_actions.append(_card)
				mana_used += _card.cost
		if len(playable_actions) is not 0:
			playable_action_sequences.append(tuple(playable_actions))

	playable_action_sequences = tuple(playable_action_sequences)
	partial_actions_hand = list({x for x in playable_action_sequences if playable_action_sequences.count(x) > 1})  # Remove repeating actions sequences
	return partial_actions_hand

