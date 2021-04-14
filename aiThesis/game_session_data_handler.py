from .graphs import *
import numpy as np
def health_distribution_graph(session_data):
	player1_health =[]
	player2_health =[]
	for game_data in session_data:
		player1_health.append(game_data.game_data[-1].player1_health)
		player2_health.append(game_data.game_data[-1].player2_health)

	print(player1_health)
	print(player2_health)


	create_graph([player1_health, player2_health], ["Player 1", "Player 2"], ["Health", "Frequency"])

def line_graph(session_data, mcts_iterations):
	number_of_different_iterations = len(mcts_iterations)
	player2_health = []
	for game_data in session_data:
		player2_health.append(game_data.game_data[-1].player2_health)
	three_split = np.array_split(player2_health, number_of_different_iterations)
	y =[0.0]
	x = mcts_iterations[:]
	x.insert(0, '0')
	x = [int(i) for i in x]
	for iterations in three_split:
		point = 0
		for iteration in iterations:
			if iteration > 0:
				point += 1
		y.append(point*100 / len(iterations))
	print(x)
	print(y)

	create_line_graph(x, y,  ["Iterations", "Win percentage"])



