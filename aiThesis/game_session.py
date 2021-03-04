from hearthstone.enums import CardClass
from fireplace.player import Player
from Agents.randomAgent import RandomAgent
from Agents.mcts_agent import MCTSAgent
from fireplace.utils import random_draft
from .setup_players import create_players
from fireplace.exceptions import GameOver
from .scenario import Scenario
import random

class GameSession:
	def __init__(self, scenario_name, iterations, name1, name2, p1Class, p2Class, p1Deck, p2Deck, p1Agent, p2Agent):
		self.scenario = scenario_name
		self.iterations = iterations
		self.game = None
		self.player1_name = name1
		self.player2_name = name2
		self.player1_class = p1Class
		self.player2_class = p2Class
		self.player1_deck = p1Deck
		self.player2_deck = p2Deck
		self.player1_agent = p1Agent
		self.player2_agent = p2Agent



	def start_session(self):


		for i in range(self.iterations):
			print("\n\n\n\n\n\n\n\n")
			print("New Game")
			print("*********************************************************************************************")
			print("Iteration: " + str(i+1))
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

	def test_scenario(self, scenario):
		try:
			self.play_scenario(scenario)
		except GameOver:
			print("Game completed normally.")


	def setup_game(self,player1=None, player2=None, scenario=None):
		from fireplace.game import Game

		game = Game(players=(player1, player2), scenario=scenario)
		game.start()

		return game

	def play_turn(self, game):
		player = game.current_player

		player.agent.play_turn()

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

		while True:
			self.play_turn(self.game)

		return self.game

	def play_full_game(self, player1=None, player2=None):
		game = self.setup_game(player1, player2)

		for player in game.players:
			mull_count = random.randint(0, len(player.choice.cards))
			cards_to_mulligan = random.sample(player.choice.cards, mull_count)

			player.choice.choose(*cards_to_mulligan)

		while True:
			self.play_turn(game)

		return game






