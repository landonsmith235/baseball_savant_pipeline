#Create fielding_season_stats table
fielding_season_stats = '''CREATE TABLE IF NOT EXISTS fielding_season_stats (
    id INT NOT NULL,
    fullName VARCHAR(30) NOT NULL,
    gamesStarted INT,
    caughtStealing INT NOT NULL,
    stolenBases INT NOT NULL,
    stolenBasePercentage VARCHAR(10) NOT NULL,
    assists INT NOT NULL,
    putOuts INT NOT NULL,
    errors INT NOT NULL,
    chances INT NOT NULL,
    fielding VARCHAR(10) NOT NULL,
    passedBall INT NOT NULL,
    pickoffs INT NOT NULL, 
    FOREIGN KEY (id) REFERENCES player_descriptions(id),
    UNIQUE (id)
);
'''

#Create batter_season_stats table
batter_season_stats = '''CREATE TABLE IF NOT EXISTS batter_season_stats (
    id INT NOT NULL,
    fullName VARCHAR(30) NOT NULL,
    gamesPlayed INT NOT NULL,
    flyOuts INT NOT NULL,
    groundOuts INT NOT NULL,
    runs INT NOT NULL,
    doubles INT NOT NULL,
    triples INT NOT NULL,
    homeRuns INT NOT NULL,
    strikeOuts INT NOT NULL,
    baseOnBalls INT NOT NULL,
    intentionalWalks INT NOT NULL,
    hits INT NOT NULL,
    hitByPitch INT NOT NULL,
    avg VARCHAR(10) NOT NULL,
    atBats INT NOT NULL,
    obp VARCHAR(10) NOT NULL,
    slg VARCHAR(10) NOT NULL,
    ops VARCHAR(10) NOT NULL,
    caughtStealing INT NOT NULL,
    stolenBases INT NOT NULL,
    stolenBasePercentage VARCHAR(10) NOT NULL,
    groundIntoDoublePlay INT NOT NULL,
    groundIntoTriplePlay INT NOT NULL,
    plateAppearances INT NOT NULL,
    totalBases INT NOT NULL,
    rbi INT NOT NULL,
    leftOnBase INT NOT NULL,
    sacBunts INT NOT NULL,
    sacFlies INT NOT NULL,
    babip VARCHAR(10) NOT NULL,
    catchersInterference INT NOT NULL,
    pickoffs INT NOT NULL,
    atBatsPerHomeRun VARCHAR(10) NOT NULL,
    FOREIGN KEY (id) REFERENCES player_descriptions(id),
    UNIQUE (id)
);
'''

#Create player_descriptions table
player_descriptions = '''CREATE TABLE IF NOT EXISTS player_descriptions (
    id INT PRIMARY KEY,
    fullName VARCHAR(30),
    jerseyNumber INT,
    position_code VARCHAR(5),
    position_abbrev VARCHAR(5),
    position VARCHAR(15),
    teamId INT,
    FOREIGN KEY (teamId) REFERENCES team_data(id)
);
'''

#Create pitcher_season stats
pitcher_season_stats = '''CREATE TABLE IF NOT EXISTS pitcher_season_stats (
    id INT,
    fullName VARCHAR(30),
    gamesStarted INT,
    gamesPlayed INT,
    flyOuts INT,
    groundOuts INT,
    airOuts INT,
    runs INT,
    doubles INT,
    triples INT,
    homeRuns INT,
    strikeOuts INT,
    baseOnBalls INT,
    intentionalWalks INT,
    hits INT,
    hitByPitch INT,
    atBats INT,
    obp VARCHAR(10),
    caughtStealing INT,
    stolenBases INT,
    stolenBasePercentage VARCHAR(10),
    numberOfPitches INT,
    era VARCHAR(30),
    inningsPitched VARCHAR(10),
    wins INT,
    losses INT,
    saves INT,
    saveOpportunities INT,
    holds INT,
    blownSaves INT,
    earnedRuns INT,
    whip VARCHAR(10),
    battersFaced INT,
    outs INT,
    gamesPitched INT,
    completeGames INT,
    shutouts INT,
    pitchesThrown INT,
    balls INT,
    strikes INT,
    strikePercentage VARCHAR(10),
    hitBatsmen INT,
    balks INT,
    wildPitches INT,
    pickoffs INT,
    groundOutsToAirouts VARCHAR(10),
    rbi INT,
    winPercentage VARCHAR(10),
    pitchesPerInning VARCHAR(10),
    gamesFinished INT,
    strikeoutWalkRatio VARCHAR(10),
    strikeoutsPer9Inn VARCHAR(10),
    walksPer9Inn VARCHAR(10),
    hitsPer9Inn VARCHAR(10),
    runsScoredPer9 VARCHAR(10),
    homeRunsPer9 VARCHAR(10),
    inheritedRunners INT,
    inheritedRunnersScored INT,
    catchersInterference INT,
    sacBunts INT,
    sacFlies INT,
    passedBall INT,
    FOREIGN KEY (id) REFERENCES player_descriptions(id),
    UNIQUE (id)
);
'''

#Create team_data table
team_data = '''CREATE TABLE IF NOT EXISTS team_data (
    springleagueuid INT NOT NULL,
    springleaguename VARCHAR(30) NOT NULL,
    springleagueabbrev VARCHAR(5) NOT NULL,
    id INT PRIMARY KEY,
    name VARCHAR(75) NOT NULL,
    season INT NOT NULL,
    venueid INT NOT NULL,
    venuename VARCHAR(75) NOT NULL,
    springvenueid INT NOT NULL,
    teamcode VARCHAR(10) NOT NULL,
    filecode VARCHAR(10) NOT NULL,
    abbrev VARCHAR(5) NOT NULL,
    teamname VARCHAR(20) NOT NULL,
    locationname VARCHAR(20) NOT NULL,
    firstyearofplay VARCHAR(5) NOT NULL,
    leagueuid INT NOT NULL,
    leaguename VARCHAR(30) NOT NULL,
    divisionid INT NOT NULL,
    divisionname VARCHAR(50) NOT NULL,
    shortname VARCHAR(30) NOT NULL,
    gamesplayed INT NOT NULL,
    wins INT NOT NULL,
    losses INT NOT NULL,
    ties INT NOT NULL,
    winningpercentage FLOAT NOT NULL,
    franchisename VARCHAR(30) NOT NULL,
    clubhouse VARCHAR(30) NOT NULL,
    active BOOLEAN NOT NULL
);
'''

#Create games table
games = '''CREATE TABLE IF NOT EXISTS games (
  game_pk INT PRIMARY KEY,
  homeTeamId INT NOT NULL,
  awayTeamId INT NOT NULL,
  gameStatusCode VARCHAR(5) NOT NULL,
  gameStatus VARCHAR(5) NOT NULL,
  gamedayType VARCHAR(5) NOT NULL,
  dateTime TIMESTAMPTZ NOT NULL,
  originalDate VARCHAR(30) NOT NULL,
  officialDate VARCHAR(30) NOT NULL,
  dayNight VARCHAR(15) NOT NULL,
  time VARCHAR(15) NOT NULL,
  ampm VARCHAR(5) NOT NULL,
  venueID INT NOT NULL,
  FOREIGN KEY (homeTeamId) REFERENCES team_data(id),
  FOREIGN KEY (awayTeamId) REFERENCES team_data(id)
);
'''

#Create pitch table
pitch = '''CREATE TABLE IF NOT EXISTS pitch (
  game_pk INT,
  play_id VARCHAR(100),
  inning INT,
  ab_number INT,
  cap_index INT,
  outs INT,
  batter INT,
  stand VARCHAR(5),
  batter_name VARCHAR(75),
  pitcher INT,
  p_throws VARCHAR(5),
  pitcher_name VARCHAR(75),
  team_batting VARCHAR(5),
  team_fielding VARCHAR(5),
  team_batting_id INT,
  team_fielding_id INT,
  runnerOn1B BOOLEAN,
  runnerOn2B BOOLEAN,
  runnerOn3B BOOLEAN,
  result VARCHAR(100),
  des VARCHAR(255),
  events VARCHAR(100),
  strikes INT,
  balls INT,
  pre_strikes INT,
  pre_balls INT,
  call VARCHAR(5),
  call_name VARCHAR(30),
  pitch_type VARCHAR(5),
  pitch_name VARCHAR(30),
  description VARCHAR(255),
  result_code VARCHAR(5),
  pitch_call VARCHAR(30),
  is_strike_swinging BOOLEAN,
  balls_and_strikes VARCHAR(5),
  start_speed FLOAT,
  end_speed FLOAT,
  sz_top FLOAT,
  sz_bot FLOAT,
  extension DOUBLE,
  plateTime DOUBLE,
  zone INT,
  spin_rate INT,
  px DOUBLE,
  pz DOUBLE,
  x0 DOUBLE,
  y0 DOUBLE,
  z0 DOUBLE,
  ax DOUBLE,
  ay DOUBLE,
  az DOUBLE,
  vx0 DOUBLE,
  vy0 DOUBLE,
  vz0 DOUBLE,
  pfxX DOUBLE,
  pfxZ DOUBLE,
  pfxZWithGravity DOUBLE,
  pfxZWithGravityNice INT,
  pfxZDirection VARCHAR(5),
  pfxXWithGravity INT,
  pfxXNoAbs VARCHAR(5),
  pfxXDirection VARCHAR(5),
  breakX INT,
  breakZ INT,
  inducedbreakZ INT,
  hit_speed_round FLOAT,
  hit_speed FLOAT,
  hit_distance FLOAT,
  xba VARCHAR(10),
  hit_angle FLOAT,
  is_barrel INT,
  hc_x FLOAT,
  hc_x_ft DOUBLE,
  hc_y FLOAT,
  hc_y_ft DOUBLE,
  is_bip_out VARCHAR(5),
  pitch_number INT,
  player_total_pitches INT,
  player_total_pitches_pitch_types INT,
  game_total_pitches INT,
  FOREIGN KEY (game_pk) REFERENCES games(game_pk)
);
'''

#Create linescore table
linescore = '''CREATE TABLE IF NOT EXISTS linescore (
  game_pk INT NOT NULL,
  inning INT NOT NULL,
  inning_ordinal VARCHAR(5) NOT NULL,
  topBottom VARCHAR(10) NOT NULL,
  runs INT,
  hits INT,
  errors INT,
  left_on_base INT,
  FOREIGN KEY (game_pk) REFERENCES games(game_pk)
);
'''

#Create officials table
officials = '''CREATE TABLE IF NOT EXISTS officials (
  game_pk INT NOT NULL,
  id INT NOT NULL,
  fullName VARCHAR(30) NOT NULL,
  officialType VARCHAR(30) NOT NULL,
  FOREIGN KEY (game_pk) REFERENCES games(game_pk)
);
'''

#Create win_probability_added table
game_wpa = '''CREATE TABLE IF NOT EXISTS game_wpa (
  game_pk INT NOT NULL,
  homeTeamWinProb DOUBLE NOT NULL,
  awayTeamWinProb DOUBLE NOT NULL,
  homeTeamWinProbAdded DOUBLE NOT NULL,
  hwp DOUBLE NOT NULL,
  awp DOUBLE NOT NULL,
  atBatIndex INT NOT NULL,
  inning VARCHAR(5) NOT NULL,
  capIndex INT NOT NULL,
  FOREIGN KEY (game_pk) REFERENCES games(game_pk)
);
'''