from .graphs import *

def health_distribution_graph(session_data):
	player1_health =[]
	player2_health =[]
	for game_data in session_data:
		player1_health.append(game_data.game_data[-1].player1_health)
		player2_health.append(game_data.game_data[-1].player2_health)

	print(player1_health)
	print(player2_health)


	create_graph([player1_health, player2_health], ["Player 1", "Player 2"], ["Health", "Frequency"])
