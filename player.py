'''module docstring'''

class Player:
	''' A class which represents the players '''
	#static attribute to keep track of number of created teams
	numberOfPlayers = 0
	#following dict contains the name of the teams and occurence of having players
	#which have the value season more than 10
	highValuePlayers_teams_occurance_ = {}
	highValuePlayers_position_occurance_ = {}
	#parameterized constructor
	def __init__(self, second_name, team, position, selected_by_percent,
       chance_of_playing_next_round, value_season, now_cost, minutes,
       total_points):
		'''parametrized constructor'''
		#increment the static variable to keep track of the number of players
		Player.numberOfPlayers += 1
		#non-static attributes
		self.id_ = Player.numberOfPlayers
		self.second_name = second_name
		self.team = team
		self.position = position
		self.selected_by_percent = selected_by_percent
		self.chance_of_playing_next_round = chance_of_playing_next_round
		self.value_season = value_season
		self.now_cost = now_cost
		self.minutes = minutes
		self.total_points = total_points

	#find the teams which have the players with value season of more than 10 and their occurence
	def high_value_occurance(self):
		''' high value players occurance '''
		if self.value_season >= 10:
			if self.team.name in Player.highValuePlayers_teams_occurance_:
				Player.highValuePlayers_teams_occurance_[self.team.name] += 1
			else:
				Player.highValuePlayers_teams_occurance_[self.team.name] = 1

			if 	self.position.plural_name in Player.highValuePlayers_position_occurance_:
				Player.highValuePlayers_position_occurance_[self.position.plural_name] += 1
			else:
				Player.highValuePlayers_position_occurance_[self.position.plural_name] = 1
