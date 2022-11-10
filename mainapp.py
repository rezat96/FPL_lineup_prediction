import pandas as pd
import numpy as np
import sqlite3
## use pylint for code rate: PEP8 Standard!

## read the db
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

#pre_process the data!
players_stats = players_stats.sort_values('value_season',ascending=False)

### Lets sort players based on their position
goal_df = players_stats.loc[players_stats.position == 'Goalkeepers'].reset_index(drop=True)
def_df = players_stats.loc[players_stats.position == 'Defenders'].reset_index(drop=True)
mid_df = players_stats.loc[players_stats.position == 'Midfielders'].reset_index(drop=True)
fwd_df = players_stats.loc[players_stats.position == 'Forwards'].reset_index(drop=True)

# # Now lets find the best team consisting: 2GKs, 5 DEFS, 5Mids, 3Fwds: So lets pick our team
# print(players_stats.sort_values(by=["total_points"],ascending = False).head(15).reset_index(drop = True))     

############################################################### our application
position_limit = 3

def team_total_cost(df):
    return df['now_cost'].sum()

def check_budget(df):
    return True if team_total_cost(df) <= 1000 else False

def check_team_limit(df, position_limit):
    if np.any(np.unique(df['teams'], return_counts= True)[1]) <= position_limit:
        return True
    else:
        return False

## initial teams
def make_initial_team_list(slim_teams_df):
    all_teams = list(slim_teams_df.name)
    zero_init = np.zeros(20, dtype='int32')
    return dict(zip(all_teams, zero_init))

#pick with constraint
def pick_with_constraint(out_df, pos_df, teams_dict, number_of_players):
    cnt = 0
    i = 0
    while(cnt < number_of_players):
        i += 1
        if teams_dict[pos_df.iloc[i].teams] < position_limit:
            teams_dict[pos_df.iloc[i].teams] +=1
            out_df = pd.concat([out_df, pos_df.iloc[i: i+1]]).reset_index(drop= True)
            cnt += 1
    return out_df, teams_dict

# startegy to pick 2gks
def pick_goalies(goal_df, teams_dict, number_of_players=2):
    for i in range(number_of_players):
        teams_dict[goal_df.iloc[i].teams] +=1
    return goal_df[:number_of_players], teams_dict

# finally merge and come up with the teem sheet
def best_fifteen_by_position(goal_df, def_df, mid_df, fwd_df, teams_dict):
    out_df, teams_dict = pick_goalies(goal_df, teams_dict, number_of_players = 2)
    out_df, teams_dict = pick_with_constraint(out_df, def_df, teams_dict, number_of_players=5)
    out_df, teams_dict = pick_with_constraint(out_df, mid_df, teams_dict, number_of_players=5)
    return pick_with_constraint(out_df, fwd_df, teams_dict, number_of_players=3)[0]

def main():
    teams_dict = make_initial_team_list(slim_teams_df)
    team_sheet = best_fifteen_by_position(goal_df, def_df, mid_df, fwd_df, teams_dict)
    print(len(team_sheet))
    # print("the total cost is:", team_total_cost(team_sheet))
    return team_sheet


if __name__ =='__main__':
    main()
# can we come up with a idea for the captain? we can also add that to the unittesting?
