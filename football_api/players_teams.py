import pandas as pd

def get_players_team_info(players_team_obj):
    rows = []
    team_id = players_team_obj['team']['id']
    team_name = players_team_obj['team']['name']
    team_logo = players_team_obj['team']['logo']
    for player in players_team_obj['players']:
        row = {
            'player_id': player['id'],
            #'player_name': player['name'],
            #'player_age': player['age'],
            'player_number': player['number'],
            'player_position': player['position'],
            #'player_photo': player['photo'],
            'team_id': team_id,
            'team_name': team_name,
            'team_logo': team_logo
        }
        rows.append(row)
    return rows


def get_players_teams_info(players_teams_list):
    players_teams_info_list = []
    for team_entry in players_teams_list:
        players_teams_info_list.extend(get_players_team_info(team_entry))
    return players_teams_info_list

def players_teams_to_dataframe(players_teams_list):
    return pd.DataFrame(get_players_teams_info(players_teams_list))