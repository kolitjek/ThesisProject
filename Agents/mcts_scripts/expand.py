from aiThesis import game_state_node
from hearthstone.enums import CardType
from fireplace import card
import itertools
from .partial_action import Partial_action
from hearthstone import enums
import random

import copy

def expand_game_node (_node):

	# Steps:
	# Get partial actions
	# Combine different partial actions
	# return a new game state

	if _node.game_state.state is enums.State.RUNNING:  # Just a failsafe check
		print("**** Starting expansion phase ****")
		print("Expanding turn: " + str(_node.game_state.turn) + ", acting player: " + _node.game_state.current_player.hero.data.name)

		if len(_node.action_space) is 0:
			_node.action_space = permute_action_space(_node)

		apply_action_sequence(_node.action_space)

		pass
	else:
		_node.leaf = True  # Maybe this is not necessary...
		print("The node selected for expansion is terminal...")
		return None

def permute_action_space(_node):
	partial_actions_hand = []  # The total possible actions from the given space in perspective from the hand
	partial_actions_board = []  # The total possible actions from the given space in perspective from the board

	for _card in _node.game_state.current_player.actionable_entities:
		if type(_card) is not card.Hero:  # A hero (on its own) can not act
			if _card.zone is enums.Zone.HAND:  # Actions taken from the hand
				partial_actions_hand.append(_card)
			elif _card.zone is enums.Zone.PLAY:  # Actions from the board
				partial_actions_board.append(_card)

	# Dividing action between hand and board, is based on the idea that player cards first is optimal
	partial_actions_hand = list(itertools.permutations(partial_actions_hand))
	partial_actions_board = list(itertools.permutations(partial_actions_board))
	action_sequences = list(itertools.product(partial_actions_hand, partial_actions_board))

	for i in range(0, len(action_sequences)):  # Just to convert to a single tuple
		if action_sequences[i][0] is not None and action_sequences[i][1] is not None:
			action_sequences[i] = action_sequences[i][0] + action_sequences[i][1]

	copy_game_state = copy.deepcopy(_node.game_state)
	action_sequences = evaluate_sequences(action_sequences, copy_game_state)
	return action_sequences

def evaluate_sequences (_action_sequences, _game_state):  # Only returns "valid"/possible action sequences
	valid_action_sequences = []
	current_player = _game_state.current_player
	for _card in _action_sequences[0]:  # Only for testing
		if _card.zone is enums.Zone.HAND and _card.is_playable():
			target = None
			if _card.must_choose_one:
				_card = random.choice(_card.choose_cards)
			if _card.requires_target():
				target = random.choice(_card.targets)
			print("Playing %r on %r" % (_card, target))
			_card.play(target=target)

			if current_player.choice:
				choice = random.choice(current_player.choice.cards)
				current_player.choice.choose(choice)
			pass
		else:
			pass

	return valid_action_sequences


def apply_action_sequence (_action_sequence):


	pass

