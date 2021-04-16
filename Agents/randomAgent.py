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

				c = self.player.hand[card_index - played_cards]  #FIXME this seems to break (out of range)?
				if c.is_playable(): # removed 50% chance to skip // and random.random() < 0.5
					target = None
					played_cards += 1
					if c.must_choose_one:
						if (c.choose_cards[0].is_playable):
							c = c.choose_cards[0]
						else:
							c = c.choose_cards[1]
					if c.requires_target():
						if type(c) is card.Spell:
							target = random.choice(c.enemy_targets if c.enemy_targets != [] else c.targets)#target = c._enemy_targets if c.predefined_enemy_target != [] else c.predefined_target
						else:
							target =  random.choice(c.targets)# c.predefined_target
					#print("Playing %r on %r" % (card, target))
					c.play(target=target)

					if self.player.choice:
						choice = random.choice(self.player.choice.cards)
						self.player.choice.choose(choice)
					#continue
			heropower = self.player.hero.power
			if heropower.is_usable(): #and random.random() < 0.1:
				if heropower.requires_target():
					heropower.use(target=random.choice(self.player.opponent.characters))#target=self.player.hero_power_predefined_enemy_target)
				else:
					heropower.use()

			# Randomly attack with whatever can attack

			for character in self.player.characters:

				if character.can_attack():
					character.attack(random.choice(character.targets))

			break
