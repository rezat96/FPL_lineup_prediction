'''this module read from fpl api and then save the required table and their relations
to our local RDB(Relational DataBase)'''
import sqlite3
import requests
import pandas as pd
URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(URL)
json = r.json()
elements_df = pd.DataFrame(json['elements'])
elements_types_df = pd.DataFrame(json['element_types'])
teams_df = pd.DataFrame(json['teams'])
event_df = pd.DataFrame(json['events'])
phases_df = pd.DataFrame(json['phases'])
element_stats_df = pd.DataFrame(json['element_stats'])

#lets pick useful columns!
#position dataframe
slim_elements_types_df = elements_types_df[['id', 'plural_name', 'singular_name_short',
'squad_select', 'squad_min_play', 'squad_max_play', 'element_count']]
## players dataframe
slim_elements_df = elements_df[['id','second_name','team','element_type',
'selected_by_percent','chance_of_playing_next_round',
'value_season', 'now_cost','minutes','total_points']]
## teams dataframe
slim_teams_df = teams_df[['id', 'name', 'short_name', 'loss', 'draw', 'win',
'played','points','position']]
#resolving value season issue!
slim_elements_df = slim_elements_df.astype({"value_season": float})
#Now we would like to delete all of the players who have zero minutes of playing.
slim_elements_df = slim_elements_df.loc[slim_elements_df.value_season > 0]
#Create connection to sql
conn = sqlite3.connect('fpl_final.db')
cursor = conn.cursor()
## create position teble
COMMAND1 = """CREATE TABLE IF NOT EXISTS
positions(id INTEGER PRIMARY KEY, plural_name TEXT, singular_name_short TEXT,
squad_select INTEGER, squad_min_play INTEGER, squad_max_play INTEGER, element_count INTEGER)"""
cursor.execute(COMMAND1)
## create team teble
COMMAND2 = """CREATE TABLE IF NOT EXISTS
teams(id INTEGER PRIMARY KEY, name TEXT, short_name TEXT, loss INTEGER,
draw INTEGER, win INTEGER, played INTEGER, points INTEGER, position INTEGER)"""
cursor.execute(COMMAND2)
## create players table
COMMAND3 = """CREATE TABLE IF NOT EXISTS
players(id INTEGER PRIMARY KEY, second_name TEXT, team TEXT, element_type INTEGER, selected_by_percent REAL,
chance_of_playing_next_round INETGER, value_season REAL, now_cost INTEGER,
minutes INTEGER, total_points INTEGER, FOREIGN KEY(element_type) REFERENCES positions(id))"""
cursor.execute(COMMAND3)
## make tables and commit
slim_elements_df.to_sql(name= 'players', con= conn, if_exists= 'replace', index=False)
slim_teams_df.to_sql(name= 'teams', con= conn, if_exists= 'replace', index=False)
slim_elements_types_df.to_sql(name= 'positions', con= conn, if_exists= 'replace', index=False)
conn.commit()
