from hearthstone.enums import CardClass
from fireplace.player import Player
from Agents.randomAgent import RandomAgent
from Agents.mcts_agent import MCTSAgent
from fireplace.utils import random_draft
from .Path import BASE_PATH
import json
from hearthstone.enums import Zone

HUNTER_FACE = "HUNTER_FACE"
HUNTER_MID = "HUNTER_MID"
MAGE = "MAGE"
DRUID = "DRUID"
ROGUE = "ROGUE"
PRIEST = "PRIEST"
WARRIOR = "WARRIOR"


def setup_player(name, deck, hero, agent):
	player = Player(name, deck[0], hero)
	player.agent = get_agent_from_string(agent, player)
	player.card_details = deck[1]

	return player


def create_players(name1, name2, p1Class, p2Class, p1Deck, p2Deck, p1Agent, p2Agent):
	players = [setup_player(name1, p1Deck if p1Deck != [] else retrive_hero_deck(p1Class),
									  get_class_from_string(p1Class).default_hero, p1Agent),
					setup_player(name2, p2Deck if p2Deck != [] else retrive_hero_deck(p2Class),
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

def retrive_hero_deck(here_type):

	deck_details_path = ""

	if here_type == DRUID:
		hero_type_path = "classic_combo_druid"
	elif here_type == HUNTER_FACE:
		hero_type_path = "gvg_face_hunter"
	elif here_type == HUNTER_MID:
		hero_type_path = "classic_midrange_hunter"
	elif here_type == MAGE:
		hero_type_path = "gvg_mech_mage"
	elif here_type == ROGUE:
		hero_type_path = "gvg_oil_rogue"
	elif here_type == PRIEST:
		hero_type_path = "classic_control_priest"
	elif here_type == WARRIOR:
		hero_type_path = "classic_aggro_warrior"
	else:
		hero_type_path = "gvg_mech_mage"

	path_string = BASE_PATH + "\\decks\\" + hero_type_path + ".json"

	with open(path_string) as f:
		data = json.load(f)

	return [data["deck"], data["card_details"]]

def get_class_from_string(strClass):
	if strClass == DRUID:
		return CardClass.DRUID
	elif strClass == HUNTER_FACE or strClass == HUNTER_MID:
		return CardClass.HUNTER
	elif strClass == MAGE:
		return CardClass.MAGE
	elif strClass == "PALADIN":
		return CardClass.PALADIN
	elif strClass == "PRIEST":
		return CardClass.PRIEST
	elif strClass == ROGUE:
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

