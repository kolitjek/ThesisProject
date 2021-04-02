import random
from Agents.agent import Agent
from fireplace import card

import copy


class RandomAgent(Agent):

	def __init__(self, _player):
		self.player = _player

	def play_turn(self):
		while True:
			# iterate over our hand and play whatever is playable
			played_cards = 0
			for card_index in range(0, len(self.player.hand)):
				if card_index - played_cards < len(self.player.hand): #FIXME just to stop the break, temp solution
					c = self.player.hand[card_index - played_cards]  #FIXME this seems to break (out of range)?
					if c.is_playable():
						target = None
						played_cards += 1
						if c.must_choose_one:
							c = random.choice(c.choose_cards)
						if c.requires_target():
							if type(c) is card.Spell:
								target = random.choice(c.enemy_targets if c.enemy_targets != [] else c.targets)
							else:
								target = random.choice(c.targets)
						#print("Playing %r on %r" % (card, target))
						c.play(target=target)

						if self.player.choice:
							choice = random.choice(self.player.choice.cards)
							self.player.choice.choose(choice)
						#continue

			heropower = self.player.hero.power
			if heropower.is_usable() :
				if heropower.requires_target():
					heropower.use(target=random.choice(self.player.opponent.characters))
				else:
					heropower.use()
			# Randomly attack with whatever can attack

			for character in self.player.characters:
				if character.can_attack():
					character.attack(random.choice(character.targets))

			break
