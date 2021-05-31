import argparse
import matplotlib.pyplot as plt

class CMDInterface:
	def __init__(self):
		self.parser = argparse.ArgumentParser(description="Setting up game")
		self.parser.add_argument("-s", metavar='s', type=str, default=None)
		self.parser.add_argument("-n", metavar='n', type=int, default=1)
		self.parser.add_argument("-name1", metavar='name1', type=str, default="player1")
		self.parser.add_argument("-name2", metavar='name2', type=str, default="player2")
		self.parser.add_argument("-p1Class", metavar='p1Class', type=str, default="DRUID")
		self.parser.add_argument("-p2Class", metavar='p2Class', type=str, default="DRUID")
		self.parser.add_argument("-p1Deck", nargs='*', default=[])
		self.parser.add_argument("-p2Deck", nargs='*', default=[])
		self.parser.add_argument("-p1DeckType", metavar='p1DeckType', type=str, default="RANDOM")
		self.parser.add_argument("-p2DeckType", metavar='p2DeckType', type=str, default="RANDOM")
		self.parser.add_argument("-p1Agent", metavar='p1Agent', type=str, default="BASEMCTS")
		self.parser.add_argument("-p2Agent", metavar='p2Agent', type=str, default="BASEMCTS")
		self.parser.add_argument("-mctsIterations",  nargs='*', default=[1])


	def parse_date(self):
		return self.parser.parse_args()

def player_stat_graph(_player, _turns):
	plt.plot(_player, _turns, label=_player.hero)
	pass







