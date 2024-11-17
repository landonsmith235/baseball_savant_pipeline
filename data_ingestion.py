#Define fielding_season_stats ingestion function
def ingest_fielding_season_stats(data, home_away, cursor):
    #Parse the JSON keys returned for each player to find all unique keys
    unique_keys = set()

    for player_id in data['boxscore']['teams'][home_away]['players']:
        unique_keys.update(data['boxscore']['teams'][home_away]['players'][player_id]['seasonStats']['fielding'].keys())

    #Convert unique keys to list, order alphabetically, and insert id + fullName keys
    unique_keys = sorted(unique_keys)
    unique_keys.insert(0, 'id')
    unique_keys.insert(1, 'fullName')

    #Create dictionary of all expected fields based off of unique keys
    expected_schema = {key: None for key in unique_keys}

    for player_id in data['boxscore']['teams'][home_away]['players']:
        player_stats = data['boxscore']['teams'][home_away]['players'][player_id]['seasonStats']['fielding']

        #Merge data pulled from the API with the expected fields, fields that are missing in the data will be replaced by None
        complete_data = {key: player_stats.get(key, expected_schema[key]) for key in expected_schema}

        #Insert seperate values for player id and fullName
        complete_data['id'] = data['boxscore']['teams'][home_away]['players'][player_id]['person']['id']
        complete_data['fullName'] = data['boxscore']['teams'][home_away]['players'][player_id]['person']['fullName']

        #Create dynamic SQL insert statement
        columns = ', '.join(complete_data.keys())
        placeholders = ', '.join(['?' for _ in complete_data])
        insert_statement = f'INSERT OR IGNORE INTO fielding_season_stats ({columns}) VALUES ({placeholders})'
        values_to_insert = list(complete_data.values())

        #Insert data for each player 
        cursor.execute(insert_statement, values_to_insert)
        
#Define pitching_season_stats ingestion function
def ingest_pitcher_season_stats(data, home_away, cursor):
    #Parse the JSON keys returned for each player to find all unique keys
    unique_keys = set()

    for player_id in data['boxscore']['teams'][home_away]['players']:
        unique_keys.update(data['boxscore']['teams'][home_away]['players'][player_id]['seasonStats']['pitching'].keys())

    #Convert unique keys to list, order alphabetically, and insert id + fullName keys
    unique_keys = sorted(unique_keys)
    unique_keys.insert(0, 'id')
    unique_keys.insert(1, 'fullName')

    #Create dictionary of all expected fields based off of unique keys
    expected_schema = {key: None for key in unique_keys}

    for player_id in data['boxscore']['teams'][home_away]['players']:
        player_stats = data['boxscore']['teams'][home_away]['players'][player_id]['seasonStats']['pitching']

        #Merge data pulled from the API with the expected fields, fields that are missing in the data will be replaced by None
        complete_data = {key: player_stats.get(key, expected_schema[key]) for key in expected_schema}

        #Insert seperate values for player id and fullName
        complete_data['id'] = data['boxscore']['teams'][home_away]['players'][player_id]['person']['id']
        complete_data['fullName'] = data['boxscore']['teams'][home_away]['players'][player_id]['person']['fullName']

        #Create dynamic SQL insert statement
        columns = ', '.join(complete_data.keys())
        placeholders = ', '.join(['?' for _ in complete_data])
        insert_statement = f'INSERT OR IGNORE INTO pitcher_season_stats ({columns}) VALUES ({placeholders})'
        values_to_insert = list(complete_data.values())

        #Insert data for each player 
        cursor.execute(insert_statement, values_to_insert)
        
#Define batter_season_stats ingestion function
def ingest_batter_season_stats(data, home_away, cursor):
    #Parse the JSON keys returned for each player to find all unique keys
    unique_keys = set()

    for player_id in data['boxscore']['teams'][home_away]['players']:
        unique_keys.update(data['boxscore']['teams'][home_away]['players'][player_id]['seasonStats']['batting'].keys())

    #Convert unique keys to list, order alphabetically, and insert id + fullName keys
    unique_keys = sorted(unique_keys)
    unique_keys.insert(0, 'id')
    unique_keys.insert(1, 'fullName')

    #Create dictionary of all expected fields based off of unique keys
    expected_schema = {key: None for key in unique_keys}

    for player_id in data['boxscore']['teams'][home_away]['players']:
        player_stats = data['boxscore']['teams'][home_away]['players'][player_id]['seasonStats']['batting']

        #Merge the data from the API with the expected schema, fields missing in the data will be replaced by None
        complete_data = {key: player_stats.get(key, expected_schema[key]) for key in expected_schema}

        #Insert Player Id and FullName
        complete_data['id'] = data['boxscore']['teams'][home_away]['players'][player_id]['person']['id']
        complete_data['fullName'] = data['boxscore']['teams'][home_away]['players'][player_id]['person']['fullName']

        #Create dynamic SQL insert statement
        columns = ', '.join(complete_data.keys())
        placeholders = ', '.join(['?' for _ in complete_data])
        insert_statement = f'INSERT OR IGNORE INTO batter_season_stats ({columns}) VALUES ({placeholders})'
        values_to_insert = list(complete_data.values())

        #Insert data for each player 
        cursor.execute(insert_statement, values_to_insert)
        
#Define player_descriptions ingestion function
def ingest_player_descriptions(data, home_away, cursor):
    #Loop through players
    for player_id in data['boxscore']['teams'][home_away]['players']:
        #Create list to track insertion values
        values_to_insert = []
        #Collect id
        values_to_insert.append(data['boxscore']['teams'][home_away]['players'][player_id]['person']['id'])
        #Collect fullName
        values_to_insert.append(data['boxscore']['teams'][home_away]['players'][player_id]['person']['fullName'])
        #Collect jerseyNumber (sometimes null)
        values_to_insert.append(data['boxscore']['teams'][home_away]['players'][player_id].get('jerseyNumber', None))
        #Collect position_code
        values_to_insert.append(data['boxscore']['teams'][home_away]['players'][player_id]['position']['code'])
        #Collect position_abbrev
        values_to_insert.append(data['boxscore']['teams'][home_away]['players'][player_id]['position']['abbreviation'])
        #Collect position
        values_to_insert.append(data['boxscore']['teams'][home_away]['players'][player_id]['position']['name'])
        #Collect teamId (sometimes null)
        values_to_insert.append(data['boxscore']['teams'][home_away]['players'][player_id].get('parentTeamId', None))

        #Define insert statement
        insert_statement = '''INSERT OR IGNORE INTO player_descriptions (id, fullName, jerseyNumber, position_code, position_abbrev, position, teamId)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        #Insert data for each player
        cursor.execute(insert_statement, values_to_insert)
        
#Define team_data ingestion function
def ingest_team_data(data, home_away, cursor):
    #Standardize inputs
    if home_away == 'home':
        home_away = 'home_team_data'
    if home_away == 'away':
        home_away = 'away_team_data'
        
    #Create list to track insertion values
    values_to_insert = []
    #Collect springleagueid
    values_to_insert.append(data[home_away]['springLeague']['id'])
    #Collect springleaguename
    values_to_insert.append(data[home_away]['springLeague']['name'])
    #Collect springleagueabbrev
    values_to_insert.append(data[home_away]['springLeague']['abbreviation'])
    #Collect id
    values_to_insert.append(data[home_away]['id'])
    #Collect name
    values_to_insert.append(data[home_away]['name'])
    #Collect season
    values_to_insert.append(data[home_away]['season'])
    #Collect venueid
    values_to_insert.append(data[home_away]['venue']['id'])
    #Collect venuename
    values_to_insert.append(data[home_away]['venue']['name'])
    #Collect springvenueid
    values_to_insert.append(data[home_away]['springVenue']['id'])
    #Collect teamcode
    values_to_insert.append(data[home_away]['teamCode'])
    #Collect filecode
    values_to_insert.append(data[home_away]['fileCode'])
    #Collect abbrev
    values_to_insert.append(data[home_away]['abbreviation'])
    #Collect teamname
    values_to_insert.append(data[home_away]['teamName'])
    #Collect locationname
    values_to_insert.append(data[home_away]['locationName'])
    #Collect firstyearofplay
    values_to_insert.append(data[home_away]['firstYearOfPlay'])
    #Collect leagueid
    values_to_insert.append(data[home_away]['league']['id'])
    #Collect leaguename
    values_to_insert.append(data[home_away]['league']['name'])
    #Collect divisionid
    values_to_insert.append(data[home_away]['division']['id'])
    #Collect divisionname
    values_to_insert.append(data[home_away]['division']['name'])
    #Collect shortname
    values_to_insert.append(data[home_away]['shortName'])
    #Collect gamesplayed
    values_to_insert.append(data[home_away]['record']['gamesPlayed'])
    #Collect wins
    values_to_insert.append(data[home_away]['record']['leagueRecord']['wins'])
    #Collect losses 
    values_to_insert.append(data[home_away]['record']['leagueRecord']['losses'])
    #Collect ties
    values_to_insert.append(data[home_away]['record']['leagueRecord']['ties'])
    #Collect winningpercentage
    values_to_insert.append(data[home_away]['record']['winningPercentage'])
    #Collect franchisename
    values_to_insert.append(data[home_away]['franchiseName'])
    #Collect clubhouse
    values_to_insert.append(data[home_away]['clubName'])
    #Collect active
    values_to_insert.append(data[home_away]['active'])
    
    #Define insert statement
    insert_statement = '''
    INSERT OR IGNORE INTO team_data (
    springleagueuid,
    springleaguename,
    springleagueabbrev,
    id,
    name,
    season,
    venueid,
    venuename,
    springvenueid,
    teamcode,
    filecode,
    abbrev,
    teamname,
    locationname,
    firstyearofplay,
    leagueuid,
    leaguename,
    divisionid,
    divisionname,
    shortname,
    gamesplayed,
    wins,
    losses,
    ties,
    winningpercentage,
    franchisename,
    clubhouse,
    active
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    #Insert data for each player
    cursor.execute(insert_statement, values_to_insert)
    
#Define games ingestion function
def ingest_games(data, cursor):
    #Create list to track insertion values
    values_to_insert = []
    #Collect game_pk
    values_to_insert.append(data['scoreboard']['gamePk'])
    #Collect homeTeamId
    values_to_insert.append(data['boxscore']['teams']['home']['team']['id'])
    #Collect awayTeahId
    values_to_insert.append(data['boxscore']['teams']['away']['team']['id'])
    #Collect gameStatusCode
    values_to_insert.append(data['game_status_code'])
    #Collect gameStatus
    values_to_insert.append(data['game_status'])
    #Collect gamedayType
    values_to_insert.append(data['gamedayType'])
    #Collect dateTime
    values_to_insert.append(data['scoreboard']['datetime']['dateTime'])
    #Collect originalDate
    values_to_insert.append(data['scoreboard']['datetime']['originalDate'])
    #Collect officialDate
    values_to_insert.append(data['scoreboard']['datetime']['officialDate'])
    #Collect dayNight
    values_to_insert.append(data['scoreboard']['datetime']['dayNight'])
    #Collect time
    values_to_insert.append(data['scoreboard']['datetime']['time'])
    #Collect ampm
    values_to_insert.append(data['scoreboard']['datetime']['ampm'])
    #Collect venueId
    values_to_insert.append(data['venue_id'])
    
    #Define insert statement
    insert_statement = '''INSERT OR IGNORE INTO games (
        game_pk,
        homeTeamId,
        awayTeamId,
        gameStatusCode,
        gameStatus,
        gamedayType,
        dateTime,
        originalDate,
        officialDate,
        dayNight,
        time,
        ampm,
        venueID
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    #Insert data
    cursor.execute(insert_statement, values_to_insert)
    
#Define linescore Ingestion Function
def ingest_linescore(data, home_away, cursor):
    #Iterate through each inning of a game
    for inning in range(len(data['scoreboard']['linescore']['innings'])):
        #Create list to track insertion values
        values_to_insert = []
        #Collect game_pk
        values_to_insert.append(data['scoreboard']['gamePk'])
        #Collect inning
        values_to_insert.append(data['scoreboard']['linescore']['innings'][inning]['num'])
        #Collect inning_ordinal 
        values_to_insert.append(data['scoreboard']['linescore']['innings'][inning]['ordinalNum'])
        #Insert top or bottom string
        if home_away == 'home':
            values_to_insert.append('bottom')
        else:
            values_to_insert.append('top')
        #Collect runs (home)
        values_to_insert.append(data['scoreboard']['linescore']['innings'][inning][home_away].get('runs', None))
        #Collect hits (home)
        values_to_insert.append(data['scoreboard']['linescore']['innings'][inning][home_away].get('hits', None))
        #Collect errors (home)
        values_to_insert.append(data['scoreboard']['linescore']['innings'][inning][home_away].get('errors', None))
        #Collect leftOnBase (home)
        values_to_insert.append(data['scoreboard']['linescore']['innings'][inning][home_away].get('leftOnBase', None))
        
        #Define insert statement
        insert_statement = '''INSERT OR IGNORE INTO linescore (
        game_pk,
        inning,
        inning_ordinal,
        topBottom,
        runs,
        hits,
        errors,
        left_on_base
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        #Insert data for each inning
        cursor.execute(insert_statement, values_to_insert)
        
#Define "officials" ingestion function
def ingest_officials(data, cursor):
    #Iterate through each official
    for official in range(len(data['boxscore']['officials'])):
        #Create list to track insertion values
        values_to_insert = []
        #Collect game_pk
        values_to_insert.append(data['scoreboard']['gamePk'])
        #Collect id
        values_to_insert.append(data['boxscore']['officials'][official]['official']['id'])
        #Collect fullName
        values_to_insert.append(data['boxscore']['officials'][official]['official']['fullName'])
        #Collect officialType
        values_to_insert.append(data['boxscore']['officials'][official]['officialType'])
        
        #Define insert statement
        insert_statement = '''INSERT OR IGNORE INTO officials (
            game_pk,
            id,
            fullName,
            officialType
            ) VALUES (?, ?, ?, ?)
            '''
        #Insert data for each official
        cursor.execute(insert_statement, values_to_insert)
        
#Define "game_wpa" ingestion function
def ingest_game_wpa(data, cursor):
    for wpa in range(len(data['scoreboard']['stats']['wpa']['gameWpa'])):
        #Collect all data
        complete_data = data['scoreboard']['stats']['wpa']['gameWpa'][wpa]
        #Insert game_pk as first key in dictionary
        new_dict = {'game_pk': data['scoreboard']['gamePk']}
        complete_data = {**new_dict, **complete_data}
        
        #Define insert statement
        insert_statement = '''INSERT OR IGNORE INTO game_wpa (
        game_pk,
        homeTeamWinProb,
        awayTeamWinProb,
        homeTeamWinProbAdded,
        hwp,
        awp,
        atBatIndex,
        inning,
        capIndex
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        #Define values to insert
        values_to_insert = list(complete_data.values())
        #Insert data
        cursor.execute(insert_statement, values_to_insert)
        
#Define "pitch" ingestion function
def ingest_pitch(data, home_away, cursor):
    #Standardize inputs
    if home_away == 'home':
        split = 'team_home'
    else:
        split = 'team_away'
    
    #Define list of required keys 
    keys_list = ['game_pk', 'play_id', 'inning', 'ab_number', 'cap_index', 'outs', 'batter', 'stand', 'batter_name', 'pitcher', 'p_throws', 'pitcher_name', 'team_batting', 'team_fielding', 'team_batting_id', 'team_fielding_id', 'runnerOn1B', 'runnerOn2B', 'runnerOn3B', 'result', 'des', 'events', 'strikes', 'balls', 'pre_strikes', 'pre_balls', 'call', 'call_name', 'pitch_type', 'pitch_name', 'description', 'result_code', 'pitch_call', 'is_strike_swinging', 'balls_and_strikes', 'start_speed', 'end_speed', 'sz_top', 'sz_bot', 'extension', 'plateTime', 'zone', 'spin_rate', 'px', 'pz', 'x0', 'y0', 'z0', 'ax', 'ay', 'az', 'vx0', 'vy0', 'vz0', 'pfxX', 'pfxZ', 'pfxZWithGravity', 'pfxZWithGravityNice', 'pfxZDirection', 'pfxXWithGravity', 'pfxXNoAbs', 'pfxXDirection', 'breakX', 'breakZ', 'inducedBreakZ', 'hit_speed_round', 'hit_speed', 'hit_distance', 'xba', 'hit_angle', 'is_barrel', 'hc_x', 'hc_x_ft', 'hc_y', 'hc_y_ft', 'is_bip_out', 'pitch_number', 'player_total_pitches', 'player_total_pitches_pitch_types', 'game_total_pitches']
    
    #Create dictionary of all expected fields
    expected_schema = {key: None for key in keys_list}

    for play in data[split]:
        #Merge the data from the API with the expected schema, fields missing in the data will be replaced by None
        complete_data = {key: play.get(key, expected_schema[key]) for key in expected_schema}

        #Create dynamic SQL insert statement
        columns = ', '.join(complete_data.keys())
        placeholders = ', '.join(['?' for _ in complete_data])
        insert_statement = f'INSERT INTO pitch ({columns}) VALUES ({placeholders})'
        values_to_insert = list(complete_data.values())

        #Insert data for each play
        cursor.execute(insert_statement, values_to_insert)