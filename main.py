import sqlite3
import pandas as pd
from team import Team
from position import Position
from player import Player

con = sqlite3.connect("fpl_final.db")
c = con.cursor()
slim_elements_df = pd.read_sql("SELECT * FROM players",con)
slim_teams_df = pd.read_sql("SELECT * FROM teams",con)
slim_elements_types_df = pd.read_sql("SELECT * FROM positions",con)
c.close()

def main():
	#list teams hold all team objects
	teams = []
	for _, row in slim_teams_df.iterrows():
	    teams.append(Team(row[1], row[2], row[3], row[4], row[5], row[8]))
	    #teams.append(team(tuple(row[1:].tolist())))

	#list positions hold all position objects
	positions = []
	for _, row in slim_elements_types_df.iterrows():
		positions.append(Position(row[2], row[4], row[5], row[6]))

	#list players hold all Player objects
	players = []
	for _, row in slim_elements_df.iterrows():
		players.append(Player(row[1], teams[row[2]-1], positions[row[3]-1], row[4], row[5], row[6], row[7], row[8], row[9]))
	
	for i in players:
		i.high_value_occurance()

	for key in Player.highValuePlayers_teams_occurance_:
		print(key, ': ', Player.highValuePlayers_teams_occurance_[key])
	print('==========')	
	for key in Player.highValuePlayers_position_occurance_:
		print(key, ': ', Player.highValuePlayers_position_occurance_[key])

if __name__ =='__main__':
	main()