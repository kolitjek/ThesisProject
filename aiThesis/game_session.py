from hearthstone.enums import CardClass
from fireplace.player import Player
from fireplace.utils import random_draft
from .setup_players import create_players
from fireplace.exceptions import GameOver
from .scenario import Scenario
from .game_session_data_handler import *
from .printController import *
from Agents import randomAgent
import Agents
import random
from .game_data import GameData
from aiThesis import printController
import Agents
class GameSession:
	def __init__(self, scenario_name, iterations, p1name, p2name, p1Class, p2Class, p1Deck, p2Deck, p1_deck_type, p2_deck_type, p1Agent, p2Agent ,mctsIterations):
		self.scenario = scenario_name
		self.iterations = iterations
		self.mcts_iterations = mctsIterations #lsit of different
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
		self. iteration_number = 0
		self.number_of_wins_pr_player = [0, 0] #first index = player1, second index = player 2


	def start_session(self):
		mcts_iteration_index = 0
		#self.iterations = self.iterations - (self.iterations % len(self.mcts_iterations))
		for i in range(self.iterations):
			print("\n\n\n\n\n\n\n\n")
			print("New Game")
			print("*********************************************************************************************")
			print("Game number: " + str(i+1))
			self.iteration_number += 1
			if i is not 0 and i % int((self.iterations / len(self.mcts_iterations))) is 0:
				mcts_iteration_index += 1
				print("Gets here")
				print(mcts_iteration_index)
			if self.scenario != None:
				scenario = Scenario(self.scenario)
				if self.mcts_iterations != None:
					print(self.iterations)
					print(self.mcts_iterations)
					print(len(self.mcts_iterations))
					print(i)
					print((self.iterations / len(self.mcts_iterations)))
					print(i % (self.iterations / len(self.mcts_iterations)))

					print("mcts iterations: " + str(self.mcts_iterations[mcts_iteration_index]))

					print(self.mcts_iterations)


					self.set_mcts_agent_iterations(scenario.player1, self.mcts_iterations[mcts_iteration_index])
					self.set_mcts_agent_iterations(scenario.player2, self.mcts_iterations[mcts_iteration_index])
					print("here")

				self.test_scenario(scenario)
			else:
				players = create_players(self.player1_name, self.player2_name, self.player1_class, self.player2_class, self.player1_deck, self.player2_deck, self.player1_agent, self.player2_agent)
				self.set_mcts_agent_iterations(players[0], self.mcts_iterations[mcts_iteration_index])
				self.set_mcts_agent_iterations(players[1], self.mcts_iterations[mcts_iteration_index])

				self.test_full_game(players[0], players[1])

		self.print_game_session_data()
		health_distribution_graph(self.session_data)
		if(self.mcts_iterations is not None):
			line_graph(self.session_data, self.mcts_iterations)

	def set_mcts_agent_iterations(self, player, iterations):
		print(type(player.agent))
		if Agents.randomAgent.RandomAgent is not type(player.agent):
			print("here2")
			print(type(player.agent))
			player.agent.iterations = int(iterations)
			print(player.agent.iterations)

	def test_full_game(self, player1, player2):
		try:
			printController.enable_print()


			self.play_full_game(player1, player2)
		except GameOver:
			print("Game completed normally.")
			self.append_last_turn_of_game()

	def test_scenario(self, scenario):
		try:
			self.play_scenario(scenario)
		except GameOver:
			print("Game completed normally. _1")
			print(self.game.players[0].hero.health)
			print(self.game.players[1].hero.health)
			self.append_last_turn_of_game()

	def setup_game(self, player1=None, player2=None, scenario=None):
		from fireplace.game import Game

		if self.record_session:
			self.session_data.append(GameData(self.iteration_number))

		game = Game(players=(player1, player2), scenario=scenario)
		game.start(int(self.iteration_number))

		return game

	def play_turn(self, game):
		currPlayer = game.current_player

		print("******PLAYER INFO********")
		print(str(currPlayer.name))
		print("Hero: " + str(currPlayer.hero))
		print("Turn: " + str(game.turn))
		print("Health: " + str(currPlayer.hero.health))
		print("Mana: " + str(currPlayer.mana))
		print("Deck size: " + str(len(currPlayer.deck)))
		print("Hand size: " + str(currPlayer.hand))
		print("Field size :" + str(currPlayer.field))
		disable_print()
		currPlayer.agent.play_turn()
		print("******PLAYER INfFO******** After")
		print(str(currPlayer.name))
		print("Hero: " + str(currPlayer.hero))
		print("Turn: " + str(game.turn))
		print("Health: " + str(currPlayer.hero.health))
		print("Mana: " + str(currPlayer.mana))
		print("Deck size: " + str(len(currPlayer.deck)))
		print("Hand size: " + str(currPlayer.hand))
		print("Field size :" + str(currPlayer.field))

		if self.record_session:
			self.session_data[-1].append_turn_data(game.turn, currPlayer.name, game.players[0].hero.health, game.players[1].hero.health, len(game.players[0].field), len(game.players[1].field), len(game.players[0].hand), len(game.players[1].hand), len(game.players[0].deck), len(game.players[1].deck))
		game.end_turn()
		return game

	def play_scenario(self, scenario=None):
		self.game = self.setup_game(scenario.player1, scenario.player2, scenario)
		self.player1_class = scenario.player1_hero #FIXME only hero is sat for gamesessions self variables the rest is sat to default
		self.player2_class = scenario.player2_hero

		for player in self.game.players:
			mull_count = random.randint(0, len(player.choice.cards))
			cards_to_mulligan = random.sample(player.choice.cards, mull_count)

			player.choice.choose(*cards_to_mulligan)

		while self.game.turn < scenario.start_at_turn:
			scenario.skip_to_next_turn(self.game)

		scenario.setup_scenario(self.game)

		disable_print()
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
		if game.players[0].hero.health > 0:
			self.number_of_wins_pr_player[0] += 1
			self.session_data[-1].winning_player = "player1"
		elif game.players[1].hero.health > 0:
			self.number_of_wins_pr_player[1]  += 1
			self.session_data[-1].winning_player = "player2"
		else:
			print("GAME ENDED WITHOUT A PLAYER BEING AT 0 HEALTh, CANT DECLARE A WINNER FOR THIS GAME")

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

	def print_game_session_data(self):
		print("\n\nGAME SESSION OVER\n\n")
		print("Played " + str(self.iterations) + " number of games")
		print("Player1 (" + self.player1_class + ") won " + str(self.number_of_wins_pr_player[0]) + "/" + str(self.iterations))
		print("Player2 (" + self.player2_class + ") won " + str(self.number_of_wins_pr_player[1]) + "/" + str(self.iterations))




