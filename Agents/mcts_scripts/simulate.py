import copy
from .back_propagate import back_propagate
from Agents.randomAgent import RandomAgent
from aiThesis import printController
from hearthstone import enums

def simulate_game(node, depth=-1):




	simulated_game = copy.deepcopy(node.game_state)



	simulated_game.is_simulation = True
	simulated_game.players[0].agent = simulate_random_actions(simulated_game)
	simulated_game.players[1].agent = simulate_random_actions(simulated_game)


	#simulated_turns = 0
	print(simulated_game.simulation_finished)
	printController.disable_print()
	while not simulated_game.simulation_finished:
		simulate_turn(simulated_game)
		print("sim health")
		print(simulated_game.players[0].hero.health)
		print(simulated_game.players[1].hero.health)
		print(simulated_game.simulation_finished)
		#simulated_turns += 1

	printController.disable_print()
	print("Ran Simulation")
	print(simulated_game.mcts_agent.hero.health)
	back_propagate(node, True if simulated_game.mcts_agent.hero.health > 0 else False) #FIXME need to be the right player every step


def simulate_turn(game):
	game.current_player.agent.play_turn()
	game.end_turn()


def simulate_random_actions(game):
	curr_player = game.current_player
	return RandomAgent(curr_player)


def evaluate_simulated_state(game, simulated_game, currplayer):
	return len(game.players[currplayer].field) - len(game.players[currplayer].opponent.field) + len(simulated_game.players[currplayer].field) - len(simulated_game.players[currplayer].opponent.field)
