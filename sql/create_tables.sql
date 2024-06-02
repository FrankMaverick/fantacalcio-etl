-- Tabella giocatori
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    display_name TEXT UNIQUE NOT NULL,
    first_name TEXT,
    last_name TEXT,
    primary_role_id INTEGER,
    team_id INTEGER,
    serie_a_player BOOLEAN,
    FOREIGN KEY (primary_role_id) REFERENCES roles(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- Tabella dettagli_giocatori
CREATE TABLE IF NOT EXISTS player_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    player_id INTEGER,
    height DECIMAL(5,2),
    weight DECIMAL(5,2),
    birth_date DATE,
    nationality TEXT,
    img_url TEXT,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Tabella ruoli
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    role_principal TEXT,
    role_specific TEXT,
    role_abbreviation TEXT
);

-- Tabella mapping nomi ruoli
CREATE TABLE IF NOT EXISTS role_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER,
    source_id INTEGER,
    role_name TEXT,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- Tabella valori giocatori
CREATE TABLE IF NOT EXISTS player_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    player_id INTEGER,
    eurocent_value INTEGER,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Tabella squadre
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    team_name TEXT,
    team_code TEXT,
    team_country TEXT,
    team_founded INTEGER,
    team_national BOOLEAN,
    team_logo_url TEXT,
    current_in_serie_a BOOLEAN
);

-- Tabella dettagli squadre
CREATE TABLE IF NOT EXISTS team_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    team_id INTEGER,
    stadium_name TEXT,
    stadium_city TEXT,
    stadium_capacity INTEGER,
    stadium_image_url TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- Tabella mapping nomi squadre
CREATE TABLE IF NOT EXISTS team_name_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,
    source_id INTEGER,
    team_name TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- Tabella statistiche partite squadra
CREATE TABLE IF NOT EXISTS team_match_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,
    game_schedule_id INTEGER,
    season INTEGER,
    goals_scored INTEGER,
    goals_conceded INTEGER,
    possession DECIMAL(5,2),
    shots INTEGER,
    shots_on_target INTEGER,
    corners INTEGER,
    fouls INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (game_schedule_id) REFERENCES game_schedule(id)
);

-- Tabella statistiche stagione squadra
CREATE TABLE IF NOT EXISTS team_season_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER,
    season INTEGER,
    matches_played INTEGER,
    wins INTEGER,
    draws INTEGER,
    losses INTEGER,
    goals_scored INTEGER,
    goals_conceded INTEGER,
    possession_avg DECIMAL(5,2),
    shots INTEGER,
    shots_on_target INTEGER,
    corners INTEGER,
    fouls INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- Tabella classifiche
CREATE TABLE IF NOT EXISTS standings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    season INTEGER,
    team_id INTEGER,
    position INTEGER,
    points INTEGER,
    matches_played INTEGER,
    wins INTEGER,
    draws INTEGER,
    losses INTEGER,
    goals_scored INTEGER,
    goals_conceded INTEGER,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- Tabella mapping nomi giocatori
CREATE TABLE IF NOT EXISTS player_name_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    source_id INTEGER,
    name TEXT,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (source_id) REFERENCES sources(id)
);

-- Tabella trasferimenti
CREATE TABLE IF NOT EXISTS transfers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    from_team_id INTEGER,
    to_team_id INTEGER,
    transfer_date DATE,
    transfer_fee DECIMAL(15,2),
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (from_team_id) REFERENCES teams(id),
    FOREIGN KEY (to_team_id) REFERENCES teams(id)
);

-- Tabella statistiche partite giocatore
CREATE TABLE IF NOT EXISTS player_match_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    game_schedule_id INTEGER,
    season INTEGER,
    goals INTEGER,
    assists INTEGER,
    minutes_played INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    shots INTEGER,
    passes INTEGER,
    tackles INTEGER,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (game_schedule_id) REFERENCES game_schedule(id)
);

-- Tabella statistiche stagione giocatore
CREATE TABLE IF NOT EXISTS player_season_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    season INTEGER,
    goals INTEGER,
    assists INTEGER,
    minutes_played INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    shots INTEGER,
    passes INTEGER,
    tackles INTEGER,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Tabella ruoli dei giocatori
CREATE TABLE IF NOT EXISTS player_roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    role_id INTEGER,
    is_primary BOOLEAN,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

-- Tabella responsabilità giocatori
CREATE TABLE IF NOT EXISTS player_responsibilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    team_id INTEGER,
    season INTEGER,
    responsibility_type TEXT,
    priority INTEGER,
    FOREIGN KEY (player_id) REFERENCES players(id),
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- Tabella infortuni
CREATE TABLE IF NOT EXISTS injuries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    injury_date DATE,
    injury_type TEXT,
    expected_return DATE,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Tabella squalifiche
CREATE TABLE IF NOT EXISTS suspensions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    suspension_date DATE,
    reason TEXT,
    return_date DATE,
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Tabella formazione
CREATE TABLE IF NOT EXISTS lineups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date DATE,
    team_id INTEGER,
    player_id INTEGER,
    confirmed BOOLEAN,
    FOREIGN KEY (team_id) REFERENCES teams(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);

-- Tabella programma partite
CREATE TABLE IF NOT EXISTS game_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_date DATE,
    match_time TIME,
    home_team_id INTEGER,
    away_team_id INTEGER,
    referee_name TEXT,
    FOREIGN KEY (home_team_id) REFERENCES teams(id),
    FOREIGN KEY (away_team_id) REFERENCES teams(id)
);

-- Tabella allenatori
CREATE TABLE IF NOT EXISTS coaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid TEXT UNIQUE NOT NULL,
    team_id INTEGER,
    coach_name TEXT,
    coach_nationality TEXT,
    coach_birth_date DATE,
    coach_image_url TEXT,
    FOREIGN KEY (team_id) REFERENCES teams(id)
);

-- Tabella sorgenti
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT
);
