import pandas as pd

def get_team_info(team_obj):
    team_info = {
        'team_id': team_obj['team']['id'],
        'team_name': team_obj['team']['name'],
        'team_code': team_obj['team']['code'],
        'team_country': team_obj['team']['country'],
        'team_founded': team_obj['team']['founded'],
        'team_national': team_obj['team']['national'],
        'team_logo': team_obj['team']['logo'],
        'venue_id': team_obj['venue']['id'],
        'venue_name': team_obj['venue']['name'],
        'venue_address': team_obj['venue']['address'],
        'venue_city': team_obj['venue']['city'],
        'venue_capacity': team_obj['venue']['capacity'],
        'venue_surface': team_obj['venue']['surface'],
        'venue_image': team_obj['venue']['image']
    }
    return team_info


def get_teams_info(teams_list):
    teams_info_list = []
    for team_entry in teams_list:
        teams_info_list.append(get_team_info(team_entry))
    return teams_info_list

def teams_to_dataframe(teams_list):
    return pd.DataFrame(get_teams_info(teams_list))