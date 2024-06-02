PRAGMA foreign_keys = OFF;

DELETE FROM players;
DELETE FROM player_details;
DELETE FROM roles;
DELETE FROM role_mappings;
DELETE FROM player_values;
DELETE FROM teams;
DELETE FROM team_details;
DELETE FROM team_name_mappings;
DELETE FROM team_match_stats;
DELETE FROM team_season_stats;
DELETE FROM standings;
DELETE FROM player_name_mappings;
DELETE FROM transfers;
DELETE FROM player_match_stats;
DELETE FROM player_season_stats;
DELETE FROM player_roles;
DELETE FROM player_responsibilities;
DELETE FROM injuries;
DELETE FROM suspensions;
DELETE FROM lineups;
DELETE FROM game_schedule;
DELETE FROM coaches;
DELETE FROM sources;

PRAGMA foreign_keys = ON;
