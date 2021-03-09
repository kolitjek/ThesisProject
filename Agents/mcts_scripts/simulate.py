import copy

class Simulate:

	def simulate_game(self, game, depth):
		currplayer = 0 if (game.current_player == game.players[0]) else 1
		simulated_game = copy.deepcopy(game)
		simulated_turns = 0
		while simulated_turns < depth:
			simulated_game = self.simulate_turn(simulated_game)
			simulated_turns += 1

		return self.evaluate_simulated_state(game, simulated_game, currplayer)


	def simulate_turn(self, game):
		game.current_player.agent.play_turn()
		game.end_turn()
		return game

	def evaluate_simulated_state(self, game, simulated_game, currplayer):
		return len(game.players[currplayer].field) - len(game.players[currplayer].opponent.field) + len(simulated_game.players[currplayer].field) - len(simulated_game.players[currplayer].opponent.field)
