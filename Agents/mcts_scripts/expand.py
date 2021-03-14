from aiThesis import game_state_node
from hearthstone.enums import CardType
from fireplace import card
import itertools
from .partial_action import Partial_action
from hearthstone import enums
import copy

def expand_game_node (acting_player):

	print("Looking action space...")
	#print(type(acting_player.actionable_entities))
	cards_in_hand = []  # Should be played first and shuffled
	current_game_state = copy.deepcopy(acting_player.game)  # I need to act this copy of the game state
	partial_actions = []
	action_space_sequences = []
	for _card in acting_player.actionable_entities:
		if type(_card) is not card.Hero:
			action_space_sequences.append(_card)
			partial_actions.append(Partial_action(_card))
	print(len(list(itertools.permutations(action_space_sequences))))
	playable_card_sequences(partial_actions, acting_player)
	pass

def playable_card_sequences (partial_actions, acting_player):
	for partial_action in partial_actions:
		if not acting_player.can_pay_cost(partial_action.card) or partial_action.card.zone is not enums.Zone.HAND:
			continue

		temp_partial_actions = partial_actions.copy()
		temp_partial_actions.remove(partial_action)
		for remaining_partial_actions in temp_partial_actions:
			print("hell ya " + remaining_partial_actions.card.id)

			pass

	pass
