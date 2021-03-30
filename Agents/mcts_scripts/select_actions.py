from aiThesis import printController
from fireplace import card
from hearthstone import enums
import random


def select_and_perform_actions(root_node, player):

	perform_action_sequence(select_best_node(root_node).performed_action_space, player)
	pass

def select_best_node(root_node):
	best_node = None
	for n in root_node.explored_nodes:
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
	printController.enable_print()

	print("Actions to perfrom")
	print(_action_sequence)
	for action in _action_sequence:
		target = None
		if type(action) is card.HeroPower:
			print("ACtion useable")
			print(action.is_usable())
			if action.is_usable():
				if action.requires_target():
					action.use(target=random.choice(action.targets))
				else:
					action.use()
				continue  # need this because hero is a special card type

		elif action.zone is enums.Zone.HAND:  # does this covers enough...?
			if action.is_playable():
				if action.must_choose_one:
					action = random.choice(action.choose_cards)
				if action.requires_target():
					target = random.choice(action.targets)
				#print("Playing %r on %r" % (action, targ	et))
				action.play(target=target)
			else:
				if player.choice:
					choice = random.choice(player.choice.cards)
					player.choice.choose(choice)
		'''else:
			if action.can_attack():
				action.attack(random.choice(action.targets))'''

	for character in player.characters:
				if character.can_attack():
					character.attack(random.choice(character.targets))




