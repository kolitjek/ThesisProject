from .turn_data import TurnData


class GameData:
	def __init__(self, iteration_number):
		self.iteration_number = iteration_number
		self.game_data = []
		self.winning_player = None
		self.action_spaces = []
		self.avg_times_visited_children = []
		self.unexplored_children = []
		self.tree_depths = []

	def append_turn_data(self, turn_number, player_name_turn, player1_health, player2_health, player1_field_size, player2_field_size, player1_hand_size, player2_hand_size, player1_deck_size, player2_deck_size):
		self.game_data.append(TurnData(turn_number, player_name_turn, player1_health, player2_health, player1_field_size, player2_field_size, player1_hand_size, player2_hand_size, player1_deck_size, player2_deck_size))

	def append_mcts_data(self, mcts_agent):
		self.action_spaces = mcts_agent.action_spaces
		self.avg_times_visited_children = mcts_agent.avg_times_visited_children
		self.unexplored_children = mcts_agent.unexplored_children
		self.tree_depths = mcts_agent.tree_depths
