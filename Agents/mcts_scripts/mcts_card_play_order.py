from fireplace import card
class mcts_card_play_order:
	def __init__(self):                             #normal_minion / battlecry / combo
		self.order_values = {"<class 'fireplace.card.Minion'>": [0, 3, 5], "<class 'fireplace.card.Weapon'>": 1, "<class 'fireplace.card.HeroPower'>": 2,  "<class 'fireplace.card.Spell'>": 4}

		#fixme maybe introduce a reevaluate handcost card?
		#fixme maybe add types of spells AOE, heal, burn, buff ect
	def filter_sequences(self, sequences):
		filtered_sequence = []
		for sequence in sequences:
			biggest_value = None

	def get_order_value(self, _card):
		if type(_card) is card.Minion:
			return 5 if _card.has_combo else (3 if _card.has_battlecry else 0)
		else:
			return self.order_values[str(type(_card))]

