from team import team
from position import position

class player:
	#static attribute to keep track of number of created teams
	numberOfPlayers = 0
	#parameterized constructor
	def __init__(self, second_name, team, position, selected_by_percent,
       chance_of_playing_next_round, value_season, now_cost, minutes,
       total_points):
		#increment the static variable to keep track of the number of players
		player.numberOfPlayers += 1
		#non-static attributes
		self.id = player.numberOfPlayers
		self.second_name = second_name
		self.team = team
		self.position = position
		self.selected_by_percent = selected_by_percent
		self.chance_of_playing_next_round = chance_of_playing_next_round
		self.value_season = value_season
		self.now_cost = now_cost
		self.minutes = minutes
		self.total_points = total_points

	# def get_name_position():
	# 	self.position.plural_name

# t1 = team('Arsenal', 'ars', 20, 10, 8, 15)	
# pos1 = position('DEF', 1, 4, 12)	
# player1 = player('Reza', t1, pos1, 100, 100, 100, 6, 90, 50)
# print(player1.team.name)