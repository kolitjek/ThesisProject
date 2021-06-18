from fireplace import card
class mcts_card_play_order:
	def __init__(self):                             #normal_minion / battlecry / combo
		self.order_values = {"<class 'fireplace.card.Minion'>": [0, 4, 5, 7], "<class 'fireplace.card.Secret'>": 1, "<class 'fireplace.card.Weapon'>": 2, "<class 'fireplace.card.HeroPower'>": 3,   "<class 'fireplace.card.Spell'>": 6}
		self.special_card_values = {"The Coin": 0}


		#fixme maybe introduce a reevaluate handcost card?
		#fixme maybe add types of spells AOE, heal, burn, buff ect
	def filter_action(self, node, curr_action):

		if(node.parent is None or node.performed_action_space is None):
			return True
		parent_action = node.performed_action_space


		print("******")
		print(curr_action)
		print(curr_action.controller)
		print(parent_action)
		print(parent_action.controller)
		print("******")
		'''print("parent:")
		node.parent.print_local_relations()
		print("Child:")
		node.print_local_relations()
		print("current action: ", curr_action)'''

		if self.get_order_value(parent_action) > self.get_order_value(curr_action):
			'''print("****** BRANCH SKIPPED ******")
			print("Parent action performed: " + str(parent_action))
			print("Curr action: " + str(curr_action))'''
			return False
		else:
			return True

	def get_order_value(self, _card):
		if self.check_for_special_card(_card) is not None:
			print("found THE COIN returning " + str(self.check_for_special_card(_card)) + " as value")
			return self.check_for_special_card(_card)
		if type(_card) is card.Minion: # så den henter ikke fra dictionarien?
			return 7 if _card.has_combo else (4 if _card.has_battlecry else (5 if _card.has_choose_one else 0))
		else:
			return self.order_values[str(type(_card))]

	def check_for_special_card(self, _card):
		if str(_card) in self.special_card_values.keys():
			return self.special_card_values[str(_card)]
		else:
			return None


