import random
from Agents.agent import Agent


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
			print(self.player.hand)
			print("mana: " + str(self.player._max_mana))
			print("used_mana: " + str(self.player.used_mana))
			for card in self.player.hand:
				print("John_cena")
				print(self.player.hand)
				print("mana: " + str(self.player._max_mana))
				print("used_mana: " + str(self.player.used_mana))
				if card.is_playable(): # and random.random() < 0.5:
					target = None
					if card.must_choose_one:
						card = random.choice(card.choose_cards)
					if card.requires_target():
						target = random.choice(card.targets)
					print("Playing %r on %r" % (card, target))
					card.play(target=target)

					if self.player.choice:
						choice = random.choice(self.player.choice.cards)
						print("Choosing card %r" % (choice))
						self.player.choice.choose(choice)
					print(self.player.hand)
					print("mana: " + str(self.player._max_mana))
					print("used_mana: " + str(self.player.used_mana))
					#continue

			# Randomly attack with whatever can attack
			for character in self.player.characters:
				if character.can_attack():
					character.attack(random.choice(character.targets))

			break
