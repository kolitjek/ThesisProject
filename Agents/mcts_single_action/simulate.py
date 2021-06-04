import copy
from Agents.play_all_agent import PlayAllAgent
from aiThesis import printController
from .backpropagation import back_propagate
def simulate_game(_node):
	simulated_game = copy.deepcopy(_node.game_state)
	simulated_game.is_simulation = True
	root_node = _node

	while root_node.parent is not None:
		root_node = root_node.parent

	printController.disable_print()

	simulated_root_player = simulated_game.players[0] if root_node.game_state.current_player is root_node.game_state.players[0] else simulated_game.players[1]
	simulated_game.players[0].agent = simulate_random_actions(simulated_game.players[0])
	simulated_game.players[1].agent = simulate_random_actions(simulated_game.players[1])
	while not simulated_game.simulation_finished:
		simulate_turn(simulated_game)

	back_propagate(_node, True if simulated_root_player.hero.health > 0 else False) #FIXME need to be the right player every step

def simulate_random_actions(player):
	return PlayAllAgent(player)

def simulate_turn(game):
	game.current_player.agent.play_turn()
	game.end_turn()

