import copy
from .back_propagate import back_propagate
from hearthstone import enums


def simulate_game(node, depth=-1):
	simulated_game = copy.deepcopy(node.game_state)
	#simulated_turns = 0
	while simulated_game.state is enums.State.RUNNING:
		simulated_game = simulate_turn(simulated_game)
		#simulated_turns += 1

	back_propagate(node, True if node.game_state.current_player.hero.health > 0 else False)


def simulate_turn(game):
	game.current_player.agent.play_turn()
	game.end_turn()
	return game

def evaluate_simulated_state(game, simulated_game, currplayer):
	return len(game.players[currplayer].field) - len(game.players[currplayer].opponent.field) + len(simulated_game.players[currplayer].field) - len(simulated_game.players[currplayer].opponent.field)
