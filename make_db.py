import requests
import pandas as pd
import numpy as np
import sqlite3
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json = r.json()
elements_df = pd.DataFrame(json['elements'])
elements_types_df = pd.DataFrame(json['element_types'])
teams_df = pd.DataFrame(json['teams'])
event_df = pd.DataFrame(json['events'])
phases_df = pd.DataFrame(json['phases'])
#total_players_df = pd.DataFrame(json['total_players'])
element_stats_df = pd.DataFrame(json['element_stats'])

#lets pick useful columns!
slim_elements_types_df = elements_types_df[['id', 'plural_name', 'singular_name_short','squad_select', 'squad_min_play', 'squad_max_play', 'element_count']]
slim_elements_df = elements_df[['id','second_name','team','element_type',
                                'selected_by_percent','chance_of_playing_next_round','value_season', 'now_cost','minutes','total_points']]

slim_teams_df = teams_df[['id','name','short_name','loss','draw','win','played','points','position']]

#resolving value season issue!
slim_elements_df = slim_elements_df.astype({"value_season": float})
#Now we would like to delete all of the players who have zero minutes of playing.
slim_elements_df = slim_elements_df.loc[slim_elements_df.value_season > 0]
# slim_elements_df = slim_elements_df.drop('value_season', axis=1)
# slim_elements_df = slim_elements_df.sort_values('value',ascending=False)


#Create connection to sql
conn = sqlite3.connect('fpl_final.db')
cursor = conn.cursor()

command1 = """CREATE TABLE IF NOT EXISTS
positions(id INTEGER PRIMARY KEY, plural_name TEXT, singular_name_short TEXT, squad_select INTEGER, squad_min_play INTEGER, squad_max_play INTEGER, element_count INTEGER)"""
cursor.execute(command1)

command2 = """CREATE TABLE IF NOT EXISTS
teams(id INTEGER PRIMARY KEY, name TEXT, short_name TEXT, loss INTEGER, draw INTEGER, win INTEGER, played INTEGER, points INTEGER, position INTEGER)"""
cursor.execute(command2)

command3 = """CREATE TABLE IF NOT EXISTS
players(id INTEGER PRIMARY KEY, second_name TEXT, team TEXT, element_type INTEGER, selected_by_percent REAL,
chance_of_playing_next_round INETGER, value_season REAL, now_cost INTEGER, minutes INTEGER, total_points INTEGER, FOREIGN KEY(element_type) REFERENCES positions(id))"""
cursor.execute(command3)

slim_elements_df.to_sql(name= 'players', con= conn, if_exists= 'replace', index=False)
slim_teams_df.to_sql(name= 'teams', con= conn, if_exists= 'replace', index=False)
slim_elements_types_df.to_sql(name= 'positions', con= conn, if_exists= 'replace', index=False)
conn.commit()


print(slim_elements_df)
