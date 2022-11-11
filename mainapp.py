'''
this module has the main coding for reading from our local database and to define nessecary
functions to get our best 15-men pl fantasy team-sheet
'''
import sqlite3
import pandas as pd
import numpy as np
## Connect to the db and read it.
con = sqlite3.connect("fpl_final.db")
c = con.cursor()
slim_elements_df= pd.read_sql("SELECT * FROM players",con)
slim_teams_df = pd.read_sql("SELECT * FROM teams",con)
positions_df = pd.read_sql("SELECT * FROM positions",con)
#main Query
players_stats = pd.read_sql('''SELECT players.id,second_name, selected_by_percent,
chance_of_playing_next_round, value_season, now_cost,
minutes, total_points, plural_name as position, teams.name as teams FROM
players INNER JOIN positions on players.element_type=positions.id
INNER JOIN teams on players.team=teams.id ''', con)
c.close()
#pre_process the data: sort by value_season
players_stats = players_stats.sort_values('value_season',ascending=False)
### Lets sort players based on their position
goal_df = players_stats.loc[players_stats.position == 'Goalkeepers'].reset_index(drop=True)
defender_df = players_stats.loc[players_stats.position == 'Defenders'].reset_index(drop=True)
midfielder = players_stats.loc[players_stats.position == 'Midfielders'].reset_index(drop=True)
forward_df = players_stats.loc[players_stats.position == 'Forwards'].reset_index(drop=True)
## Now lets find the best team consisting: 2GKs, 5 DEFS, 5Mids, 3Fwds
######################## our main application
TEAMS_LIMIT = 3
TEAM_BUDGET = 1000
def team_total_cost(team_df):
    '''get how much our team costs'''
    return team_df['now_cost'].sum()

def check_budget(team_df):
    '''check to see if we are well within our budget'''
    return team_total_cost(team_df) <= TEAM_BUDGET

def check_team_limit(team_df, team_limit = TEAMS_LIMIT):
    '''check to see if we are fine with team_limit constraint'''
    return np.any(np.unique(team_df['teams'], return_counts= True)[1]) <= team_limit
## initial teams
def make_initial_team_list(teams):
    '''make a list of all preimer league teams,
    and set the default number of players selected from each team to zero
    '''
    all_teams = list(teams.name)
    zero_init = np.zeros(20, dtype='int32')
    return dict(zip(all_teams, zero_init))
#pick with constraint
def pick_with_constraint(out_df, pos_df, teams_dict, number_of_players):
    '''pick each position by checking team_limit constraint when choosing players
    retruns out our team and the team_dictionary'''
    cnt = 0
    i = 0
    while cnt < number_of_players:
        i += 1
        if teams_dict[pos_df.iloc[i].teams] < TEAMS_LIMIT:
            teams_dict[pos_df.iloc[i].teams] +=1
            out_df = pd.concat([out_df, pos_df.iloc[i: i+1]]).reset_index(drop= True)
            cnt += 1
    return out_df, teams_dict

# startegy to pick 2gks
def pick_goalies(gk_df, teams_dict, number_of_players=2):
    '''start from Gks(our analyze shows they are the most important)'''
    for i in range(number_of_players):
        teams_dict[gk_df.iloc[i].teams] +=1
    return gk_df[:number_of_players], teams_dict

# finally merge and come up with the teem sheet
def best_fifteen_by_position(gk_df, def_df, mid_df, fwd_df, teams_dict):
    '''pick the final 15-Men shortlist by position-order[2 gks, 5 defs, 5 mids, 5 fwds]'''
    out_df, teams_dict = pick_goalies(gk_df, teams_dict, number_of_players = 2)
    out_df, teams_dict = pick_with_constraint(out_df, def_df, teams_dict, number_of_players=5)
    out_df, teams_dict = pick_with_constraint(out_df, mid_df, teams_dict, number_of_players=5)
    return pick_with_constraint(out_df, fwd_df, teams_dict, number_of_players=3)[0]

def main():
    '''run the main application and return the 15-Men team_sheet'''
    teams_dict = make_initial_team_list(slim_teams_df)
    team_sheet = best_fifteen_by_position(goal_df, defender_df, midfielder, forward_df, teams_dict)
    # print(len(team_sheet))
    # print("the total cost is:", team_total_cost(team_sheet))
    return team_sheet


if __name__ =='__main__':
    main()
