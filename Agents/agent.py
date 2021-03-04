class Agent(object):
	def __init__(self):
		self.player = None

	def play_turn(self):
		raise Exception("PARENT CLASS OF AGENT 'play_turn' is called instead of child!!!! In agent.py ")
