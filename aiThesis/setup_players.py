from hearthstone.enums import CardClass
from fireplace.player import Player
from Agents.randomAgent import RandomAgent
from Agents.mcts_agent import MCTSAgent
from fireplace.utils import random_draft


def setup_player(name, deck, hero, agent):
	player = Player(name, deck, hero)
	player.agent = get_agent_from_string(agent, player)
	return player


def create_players(name1, name2, p1Class, p2Class, p1Deck, p2Deck, p1Agent, p2Agent):
	players = [setup_player(name1, p1Deck if p1Deck != [] else create_deck(p1Class),
									  get_class_from_string(p1Class).default_hero, p1Agent),
					setup_player(name2, p2Deck if p2Deck != [] else create_deck(p2Class),
									  get_class_from_string(p2Class).default_hero, p2Agent)]
	return players


def get_agent_from_string(agentString, player):
	if agentString == "RANDOMAGENT":
		return RandomAgent(player)
	elif (agentString == "BASEMCTS"):
		# TODO make a baseMCTS class
		return MCTSAgent(player)
	# return None
	else:
		print("DID NOT FIND AN AGENT MATCHING THE SPECIFIED INPUT, CHOOSING DEFAULT AGENT (RANDOM AGENT)")
		return RandomAgent(player)


def create_deck(strClass):
	deck = random_draft(get_class_from_string(strClass))  # Random deck with a given hero
	return deck


def get_class_from_string(strClass):
	if strClass == "DRUID":
		return CardClass.DRUID.default_hero
	elif strClass == "HUNTER":
		return CardClass.HUNTER
	elif strClass == "MAGE":
		return CardClass.MAGE
	elif strClass == "PALADIN":
		return CardClass.PALADIN
	elif strClass == "PRIEST":
		return CardClass.PRIEST
	elif strClass == "ROGUE":
		return CardClass.ROGUE
	elif strClass == "SHAMAN":
		return CardClass.SHAMAN
	elif strClass == "WARLOCK":
		return CardClass.WARLOCK
	elif strClass == "WARRIOR":
		return CardClass.WARRIOR
	else:
		print("STR INPUT FOR CLASS DID NOT MATCH ANY TYPE, RETURNING PRIEST CLASS AS DEFAULT. PRINTED IN start.py")
		return CardClass.PRIEST.default_hero
