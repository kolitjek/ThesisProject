from hearthstone.enums import CardClass
from fireplace.player import Player
from Agents.randomAgent import RandomAgent
from Agents.mcts_agent import MCTSAgent
from fireplace.utils import random_draft
from .setup_players import create_players
from fireplace.exceptions import GameOver
from .scenario import Scenario
from .printController import *
import random
from .game_data import GameData

class GameSession:
	def __init__(self, scenario_name, iterations, p1name, p2name, p1Class, p2Class, p1Deck, p2Deck, p1_deck_type, p2_deck_type,  p1Agent, p2Agent):
		self.scenario = scenario_name
		self.iterations = iterations
		self.game = None
		self.record_session = True
		self.player1_name = p1name
		self.player2_name = p2name
		self.player1_class = p1Class
		self.player2_class = p2Class
		self.player1_deck = p1Deck
		self.player2_deck = p2Deck
		self.player1_deck_type = p1_deck_type
		self.player2_deck_type = p2_deck_type
		self.player1_agent = p1Agent
		self.player2_agent = p2Agent
		self.session_data = []
		self. iteration_number = -1


	def start_session(self):
		for i in range(self.iterations):
			print("\n\n\n\n\n\n\n\n")
			print("New Game")
			print("*********************************************************************************************")
			print("Iteration: " + str(i+1))
			self.iteration_number = str(i+1)
			if self.scenario != None:
				self.test_scenario(Scenario(self.scenario))
			else:
				players = create_players(self.player1_name, self.player2_name, self.player1_class, self.player2_class, self.player1_deck, self.player2_deck, self.player1_agent, self.player2_agent)
				self.test_full_game(players[0], players[1])

	def test_full_game(self, player1, player2):
		try:
			self.play_full_game(player1, player2)
		except GameOver:
			print("Game completed normally.")
			self.append_last_turn_of_game()

	def test_scenario(self, scenario):
		try:
			self.play_scenario(scenario)
		except GameOver:
			print("Game completed normally. _1")
			self.append_last_turn_of_game()

	def setup_game(self,player1=None, player2=None, scenario=None):
		from fireplace.game import Game

		if self.record_session:
			self.session_data.append(GameData(self.iteration_number))

		game = Game(players=(player1, player2), scenario=scenario)
		game.start()

		return game

	def play_turn(self, game):
		currPlayer = game.current_player

		print("******PLAYER INFO********")
		print(str(currPlayer.name))
		print("Hero: " + str(currPlayer.hero))
		print("Turn: " + str(game.turn))
		print("Health: " + str(currPlayer.hero.health))
		print("Deck size: " + str(len(currPlayer.deck)))
		print("Hand size: " + str(len(currPlayer.hand)))
		print("Field size :" + str(len(currPlayer.field)))
		enable_print()
		currPlayer.agent.play_turn()

		if self.record_session:
			self.session_data[-1].append_turn_data(game.turn, currPlayer.name, game.players[0].hero.health, game.players[1].hero.health, len(game.players[0].field), len(game.players[1].field), len(game.players[0].hand), len(game.players[1].hand), len(game.players[0].deck), len(game.players[1].deck))
		game.end_turn()
		return game

	def play_scenario(self, scenario=None):
		self.game = self.setup_game(scenario.player1, scenario.player2, scenario)
		for player in self.game.players:
			mull_count = random.randint(0, len(player.choice.cards))
			cards_to_mulligan = random.sample(player.choice.cards, mull_count)

			player.choice.choose(*cards_to_mulligan)

		while self.game.turn < scenario.start_at_turn:
			scenario.skip_to_next_turn(self.game)

		scenario.setup_scenario(self.game)

		enable_print()
		while True:
			self.play_turn(self.game)

		return self.game

	def play_full_game(self, player1=None, player2=None):
		self.game = self.setup_game(player1, player2)

		for player in self.game.players:
			mull_count = random.randint(0, len(player.choice.cards))
			cards_to_mulligan = random.sample(player.choice.cards, mull_count)

			player.choice.choose(*cards_to_mulligan)

		while True:
			self.play_turn(self.game)

		return game

	def append_last_turn_of_game(self):
		game = self.game
		currPlayer = game.current_player
		self.session_data[-1].append_turn_data(game.turn, currPlayer.name, game.players[0].hero.health,
											   game.players[1].hero.health, len(game.players[0].field),
											   len(game.players[1].field), len(game.players[0].hand),
											   len(game.players[1].hand), len(game.players[0].deck),
											   len(game.players[1].deck))

		for turn in self.session_data[-1].game_data:
			print("**********************************************")
			print("Turn number: " + str(turn.turn_number))
			print("player 1 health: " + str(turn.player1_health))
			print("player 2 health: " + str(turn.player2_health))
			print("player 1 hand: " + str(turn.player1_hand_size))
			print("player 2 hand: " + str(turn.player2_hand_size))
			print("player 1 field: " + str(turn.player1_field_size))
			print("player 2 field: " + str(turn.player2_field_size))
			print("player 1 deck: " + str(turn.player1_deck_size))
			print("player 2 deck: " + str(turn.player2_deck_size))

			print("**********************************************")





