from .turn_data import TurnData


class GameData:
	def __init__(self, iteration_number):
		self.iteration_number = iteration_number
		self.game_data = []
		self.winning_player = None

	def append_turn_data(self, turn_number, player_name_turn, player1_health, player2_health, player1_field_size, player2_field_size, player1_hand_size, player2_hand_size, player1_deck_size, player2_deck_size):
		self.game_data.append(TurnData(turn_number, player_name_turn, player1_health, player2_health, player1_field_size, player2_field_size, player1_hand_size, player2_hand_size, player1_deck_size, player2_deck_size))


