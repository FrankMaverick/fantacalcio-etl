import pandas as pd

def get_players_info(players_list):
    players_info_list = []
    for player_entry in players_list:
        players_info_list.append(get_player_info(player_entry))
    return players_info_list
    

def get_player_info(player_obj):
    player = player_obj['player']
    for stat in player_obj['statistics']:
        player_info = {
            'player_id': player['id'],
            'player_name': player['name'],
            'player_firstname': player['firstname'],
            'player_lastname': player['lastname'],
            'player_age': player['age'],
            'player_birth_date': player['birth']['date'],
            'player_birth_place': player['birth']['place'],
            'player_birth_country': player['birth']['country'],
            'player_nationality': player['nationality'],
            'player_height': player['height'],
            'player_weight': player['weight'],
            'player_injured': player['injured'],
            'player_photo': player['photo'],
            # 'team_id': stat['team']['id'],
            # 'team_name': stat['team']['name'],
            # 'team_logo': stat['team']['logo'],
            # 'league_id': stat['league']['id'],
            # 'league_name': stat['league']['name'],
            # 'league_country': stat['league']['country'],
            # 'league_logo': stat['league']['logo'],
            # 'league_flag': stat['league']['flag'],
            # 'season': stat['league']['season'],
            # 'games_appearences': stat['games']['appearences'],
            # 'games_lineups': stat['games']['lineups'],
            # 'games_minutes': stat['games']['minutes'],
            # 'games_number': stat['games']['number'],
            'games_position': stat['games']['position'],
            # 'games_rating': stat['games']['rating'],
            # 'games_captain': stat['games']['captain'],
            # 'substitutes_in': stat['substitutes']['in'],
            # 'substitutes_out': stat['substitutes']['out'],
            # 'substitutes_bench': stat['substitutes']['bench'],
            # 'shots_total': stat['shots']['total'],
            # 'shots_on': stat['shots']['on'],
            # 'goals_total': stat['goals']['total'],
            # 'goals_conceded': stat['goals']['conceded'],
            # 'goals_assists': stat['goals']['assists'],
            # 'goals_saves': stat['goals']['saves'],
            # 'passes_total': stat['passes']['total'],
            # 'passes_key': stat['passes']['key'],
            # 'passes_accuracy': stat['passes']['accuracy'],
            # 'tackles_total': stat['tackles']['total'],
            # 'tackles_blocks': stat['tackles']['blocks'],
            # 'tackles_interceptions': stat['tackles']['interceptions'],
            # 'duels_total': stat['duels']['total'],
            # 'duels_won': stat['duels']['won'],
            # 'dribbles_attempts': stat['dribbles']['attempts'],
            # 'dribbles_success': stat['dribbles']['success'],
            # 'dribbles_past': stat['dribbles']['past'],
            # 'fouls_drawn': stat['fouls']['drawn'],
            # 'fouls_committed': stat['fouls']['committed'],
            # 'cards_yellow': stat['cards']['yellow'],
            # 'cards_yellowred': stat['cards']['yellowred'],
            # 'cards_red': stat['cards']['red'],
            # 'penalty_won': stat['penalty']['won'],
            # 'penalty_commited': stat['penalty']['commited'],
            # 'penalty_scored': stat['penalty']['scored'],
            # 'penalty_missed': stat['penalty']['missed'],
            # 'penalty_saved': stat['penalty']['saved']
        }
    return player_info


def players_to_dataframe(players_list):
    return pd.DataFrame(get_players_info(players_list))