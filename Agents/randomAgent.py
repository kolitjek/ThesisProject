import random
from Agents.agent import Agent
import copy


class RandomAgent(Agent):

	def __init__(self, _player):
		self.player = _player

	def play_turn(self):
		while True:
			heropower = self.player.hero.power
			if heropower.is_usable() and random.random() < 0.1:
				if heropower.requires_target():
					heropower.use(target=random.choice(heropower.targets))
				else:
					heropower.use()
				continue

			# iterate over our hand and play whatever is playable
			played_cards = 0
			for card_index in range(0, len(self.player.hand)):
				card = self.player.hand[card_index - played_cards]
				if card.is_playable() and random.random() < 0.5:
					target = None
					played_cards += 1
					if card.must_choose_one:
						card = random.choice(card.choose_cards)
					if card.requires_target():
						target = random.choice(card.targets)
					print("Playing %r on %r" % (card, target))
					card.play(target=target)

					if self.player.choice:
						choice = random.choice(self.player.choice.cards)
						self.player.choice.choose(choice)
					#continue
			# Randomly attack with whatever can attack
			for character in self.player.characters:
				if character.can_attack():
					character.attack(random.choice(character.targets))

			break
