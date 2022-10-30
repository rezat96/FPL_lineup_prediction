import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import sqlite3
## use pylint for code rate: PEP8 Standard!

## read the db
con = sqlite3.connect("fpl_db.db")
c = con.cursor()
slim_teams_df = pd.read_sql("SELECT * FROM players",con)
slim_elements_df = pd.read_sql("SELECT * FROM teams",con)
slim_elements_types_df = pd.read_sql("SELECT * FROM positions",con)

# Result = pd.read_sql('''SELECT players.id,second_name, element_type, selected_by_percent,
# chance_of_playing_next_round, value_season, now_cost,
# minutes, total_points, teams.name as teams FROM players INNER JOIN teams on players.team=teams.id Inner JOIN element_type= ''', con)

players_stats = pd.read_sql('''SELECT players.id,second_name, selected_by_percent,
chance_of_playing_next_round, value_season, now_cost,
minutes, total_points, plural_name as position, teams.name as teams FROM players INNER JOIN positions on players.element_type=positions.id
INNER JOIN teams on players.team=teams.id ''', con)

c.close()
#pre_process the data!
players_stats['value'] = players_stats.value_season.astype(float)
players_stats = players_stats.drop('value_season', axis=1)
players_stats = players_stats.sort_values('value',ascending=False)
#Now we would like to delete all of the players who have zero minutes of playing.
players_stats = players_stats.loc[players_stats.value > 0]
print(players_stats)
## Lets check each position stats
pivot=players_stats.pivot_table(index='position',values='value',aggfunc=np.mean).reset_index()
print(pivot.sort_values('value',ascending=False))
## Lets check each teams stats
pivot=players_stats.pivot_table(index='teams',values='value',aggfunc=np.mean).reset_index()
print(pivot.sort_values('value',ascending=False).head(7))

### Lets sort players based on their position
fwd_df = players_stats.loc[players_stats.position == 'Forwards']
mid_df = players_stats.loc[players_stats.position == 'Midfielders']
def_df = players_stats.loc[players_stats.position == 'Defenders']
goal_df = players_stats.loc[players_stats.position == 'Goalkeepers']

print(goal_df.sort_values('value',ascending=False).head(10))


# Now lets find the best team consisting: 2GKs, 5 DEFS, 5Mids, 3Fwds: So lets pick our team
print(slim_elements_types_df)