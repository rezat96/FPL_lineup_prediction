class team:
	#static attribute to keep track of number of created teams
	numberOfTeams = 0
	#parameterized constructor
	def __init__(self, name, short_name, loss, draw, win, position):
		#increment the static variable to keep track of number of teams
		team.numberOfTeams += 1
		#non-static attribute
		self.id = team.numberOfTeams
		self.name = name
		self.short_name = short_name
		self.loss = loss
		self.draw = draw
		self.win = win
		self.set_played()
		self.set_point()
		self.position = position
		
		
	# advanced version of setter for decreasing number of inputs
	def set_played(self):
		self.played = self.win + self.loss + self.draw	

	def set_point(self):
		#calculation of points is as follows
		self.set_point = (3 * self.win) + (1 * self.draw)
