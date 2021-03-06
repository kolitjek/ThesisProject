import copy
from .back_propagate import back_propagate
from Agents.play_all_agent import PlayAllAgent
from aiThesis import printController
from fireplace.exceptions import GameOver
from hearthstone import enums


def simulate_game(node, depth=-1):



	simulated_game = copy.deepcopy(node.game_state)
	simulated_game.is_simulation = True

	root_node = node
	while root_node.parent is not None:
		root_node = root_node.parent


	simulated_root_player = simulated_game.players[0] if root_node.game_state.current_player is root_node.game_state.players[0] else simulated_game.players[1]

	simulated_game.players[0].agent = get_simulator_agent(simulated_game.players[0])
	simulated_game.players[1].agent = get_simulator_agent(simulated_game.players[1])

	#simulated_turns = 0
	printController.disable_print()

	#printController.enable_print()
	while not simulated_game.simulation_finished:
		#print("simulating")

		simulate_turn(simulated_game)


	#print("Player1 health: " + str(simulated_game.players[0].hero.health))
	#print("Player2 health: " + str(simulated_game.players[1].hero.health))
	#print("Currplayer health: " + str(simulated_root_player.hero.health))

	back_propagate(node, True if simulated_root_player.hero.health > 0 else False) #FIXME need to be the right player every step
	#raise GameOver("test")
	#raise GameOver("TEST")


def simulate_turn(game):
	game.current_player.agent.play_turn()
	game.end_turn()


def get_simulator_agent(player):
	return PlayAllAgent(player)


def evaluate_simulated_state(game, simulated_game, currplayer):
	return len(game.players[currplayer].field) - len(game.players[currplayer].opponent.field) + len(simulated_game.players[currplayer].field) - len(simulated_game.players[currplayer].opponent.field)
