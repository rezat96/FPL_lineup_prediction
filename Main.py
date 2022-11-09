from team import team
from position import position
from player import player
import sqlite3
import requests
import pandas as pd
import numpy as np

con = sqlite3.connect("fpl_final.db")
c = con.cursor()
slim_elements_df = pd.read_sql("SELECT * FROM players",con)
slim_teams_df = pd.read_sql("SELECT * FROM teams",con)
slim_elements_types_df = pd.read_sql("SELECT * FROM positions",con)
c.close()

def main():
	#list teams hold all team objects
	teams = []
	for index, row in slim_teams_df.iterrows():
	    teams.append(team(row[1], row[2], row[3], row[4], row[5], row[8]))
	    #teams.append(team(tuple(row[1:].tolist())))

	#list positions hold all position objects
	positions = []
	for _, row in slim_elements_types_df.iterrows():
		positions.append(position(row[2], row[4], row[5], row[6]))

	#list players hold all player objects
	players = []
	for _, row in slim_elements_df.iterrows():
		players.append(player(row[1], teams[row[2]-1], positions[row[3]-1], row[4], row[5], row[6], row[7], row[8], row[9]))
	
	for i in players:
		i.highValuePlayers_teams_occurance()

	for key in player.highValuePlayers_teams_occurance_:
		print(key, ' ', player.highValuePlayers_teams_occurance_[key])
	print('==========')		
	for key in player.highValuePlayers_position_occurance_:
		print(key, ' ', player.highValuePlayers_position_occurance_[key])

if __name__ =='__main__':
	main()