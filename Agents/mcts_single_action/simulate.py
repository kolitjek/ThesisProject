import copy
from Agents.play_all_agent import PlayAllAgent
from aiThesis import printController
from .backpropagation import back_propagate
from ..filtered_play_all_agent_single_action_mcts import FilteredPlayAllAgent


def simulate_game(_node):
	simulated_game = copy.deepcopy(_node.game_state)
	simulated_game.is_simulation = True
	root_node = _node
	while root_node.parent is not None:
		root_node = root_node.parent

	printController.disable_print()

	simulated_root_player = simulated_game.players[0] if root_node.game_state.current_player is root_node.game_state.players[0] else simulated_game.players[1]
	simulated_game.players[0].agent = get_simulator_agent(simulated_game.players[0], _node)
	simulated_game.players[1].agent = get_simulator_agent(simulated_game.players[1], _node)
	while not simulated_game.simulation_finished:
		simulate_turn(simulated_game)
	back_propagate(_node, True if simulated_root_player.hero.health > 0 else False) #FIXME need to be the right player every step

def get_simulator_agent(player, _node):
	if player.simulator_agent == "PLAYALLAGENT":
		return PlayAllAgent(player)
	elif player.simulator_agent == "FILTEREDPLAYALLAGENT":
		return FilteredPlayAllAgent(player, _node)
	else:
		raise Exception("No simulator string maches any agent type")


def simulate_turn(game):
	game.current_player.agent.play_turn()
	game.end_turn()

