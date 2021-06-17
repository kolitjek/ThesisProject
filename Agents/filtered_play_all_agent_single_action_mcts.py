import random
from Agents.agent import Agent
from Agents.mcts_single_action.mcts_card_play_order import mcts_card_play_order
from fireplace import card

import copy


class FilteredPlayAllAgent(Agent):

	def __init__(self, _player, _node):
		self.player = _player
		self.node = _node
		self.first_turn_in_simulation = True
		self.filter = mcts_card_play_order()

	def play_turn(self):
		while True:
			# iterate over our hand and play whatever is playable
			played_cards = 0
			for card_index in range(0, len(self.player.hand)):

				c = self.player.hand[card_index - played_cards]  #FIXME this seems to break (out of range)?
				if self.first_turn_in_simulation and not self.filter.filter_action(self.node, c):
					#print("SKIPPED CARD IN FILTERED PLAY ALL AGENT")
					#print("Performed Action: "  + str(self.node.performed_action_space) + ", card skipped: " + str(c))
					continue
				if c.is_playable(): # removed 50% chance to skip // and random.random() < 0.5
					target = None
					base_card_action = None
					played_cards += 1
					if c.must_choose_one:
						random_spell_index = random.randint(0,1)
						alternative_spell_index = 0 if random_spell_index == 1 else 1

						if c.choose_cards[random_spell_index].is_playable():
							base_card_action = c
							c = c.choose_cards[random_spell_index]
						elif c.choose_cards[alternative_spell_index].is_playable():
							base_card_action = c
							c = c.choose_cards[alternative_spell_index]

					if c.requires_target():
						if type(c) is card.Spell:
							if c.targets == []:
								print("cant hit anything")
							target = random.choice(c.enemy_targets if c.enemy_targets != [] else c.targets)#target = c._enemy_targets if c.predefined_enemy_target != [] else c.predefined_target
						else:
							target = random.choice(c.targets)# c.predefined_target
					#print("Playing %r on %r" % (card, target))'

					#if c.requirements != None and c.requirements["PlayReq.REQ_NUM_MINION_SLOTS"] is not None and 7 - self.player.field <= 0:
					#	print("wanna player an animal, but there is not space...")

					if c.is_playable():
						if base_card_action is None:
							c.play(target=target)
						else:
							base_card_action.play(target=target, choose = c)

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
		self.first_turn_in_simulation = False
