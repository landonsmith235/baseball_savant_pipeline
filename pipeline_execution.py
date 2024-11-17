import requests
import sqlite3
import time
import os
import argparse
import schema
import data_ingestion

# Set up command line argument parsing for this script
parser = argparse.ArgumentParser(description="Process game data.")
parser.add_argument("inputs", nargs='+', help="The game primary key(s) or a .txt file containing the game_pks.")
parser.add_argument("--db", type=str, default="baseballsavant.db", help="The filepath to the database.")

# Parse arguments
args = parser.parse_args()

# Store the provided game_pk list or file as a variable 
inputs = args.inputs

# Store the provided database filepath as a variable 
db_filepath = args.db

# Store game_pks from file if needed
game_pks = []

# Check whether or not first arguemnt is a list of game_pks or a filepath
if len(inputs) == 1 and os.path.isfile(inputs[0]):
    with open(inputs[0], 'r') as file:
        for line in file:
            game_pk = line.strip() 
            if game_pk.isdigit():
                game_pks.append(game_pk)
else:
    game_pks = inputs
                
#Check whether the provided database file exists yet 
if os.path.isfile(db_filepath):
# If file exists, print we are accessing a previous db filepath
    if '/' in db_filepath:
        print(f'Accessing local database file with the following location: {db_filepath}')
    else:
        fullpath = os.getcwd() + '/' + db_filepath
        print(f'Accessing local database file with the following location: {fullpath}')
# If file doesn't exist, print we are creating a new db filepath
else:
    if '/' in db_filepath:
        print(f'Creating new database file with the following location: {db_filepath}')
    else:
        fullpath = os.getcwd() + '/' + db_filepath
        print(f'Creating new database file with the following location: {fullpath}')
    
# Connect to or create the database using filepath
conn = sqlite3.connect(db_filepath)
# Create cursor object
cursor = conn.cursor()

# Store ingestion start time
start_time = time.time()
print('Initializing ingestion of ' + str(len(game_pks)) + ' game_pks...')

# Store succesfully ingested game_pks, already seen game_pks, failed API requests, and ingestion exceptions for summarization purposes
successful_game_pks = []
already_seen_game_pks = []
failed_to_retrieve = {}
ingestion_exception = {}

# Loop through all provided game_pks
for pk in game_pks:
    try:
        # Grab all existing table names 
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cursor.fetchall()
        table_names = [n[0] for n in table_names]
        # If the games table already exists due to prior executions, check game_pk column to avoid retrieving data for games we already possess
        # If the games table doesn't exist due to no prior executions, move on to creating endpoint URL and pulling game_pk data from API
        if 'games' in table_names:
            game_pk_check = 'SELECT EXISTS(SELECT 1 FROM games WHERE game_pk = ? LIMIT 1)'
            cursor.execute(game_pk_check, (int(pk),))
            result = cursor.fetchone()[0]
            if result == 1:
                already_seen_game_pks.append(str(pk))
                continue

        # Create endpoint URL
        url = 'https://baseballsavant.mlb.com/gf?game_pk=' + str(pk)

        # Make a GET request to the API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Store JSON data into variable
            data = response.json()
        else:
            # Store failed retrievals inside a dictionary with the key being game_pk and value being status code
            failed_to_retrieve[pk] = reponse.status_code

        # Create list of SQL table creation statements (imported from schema.py)
        table_statement_list = [schema.fielding_season_stats, schema.batter_season_stats, schema.pitcher_season_stats, schema.player_descriptions, schema.team_data, schema.games, schema.pitch, schema.linescore, schema.officials, schema.game_wpa]

        # Create list of the table names (same order as prior list)
        table_name_list = ['fielding_season_stats', 'batter_season_stats', 'pitcher_season_stats', 'player_descriptions', 'team_data', 'games', 'pitch', 'linescore', 'officials', 'game_wpa']

        # Iterate through the prior two lists at the same time
        for statement, name in zip(table_statement_list, table_name_list):
            # If the current iteration of the table names is not present within the database, the respective table creation statement will be executed
            if name not in table_names:
                cursor.execute(statement)
            
            # Define team splits
            home_away = ['home', 'away']

            # For each iteration of the table names, the respective ingestion functions will be run against the home and away teams when nessesary 
            # (imported from data_ingestion.py)
            if name == 'fielding_season_stats':
                [data_ingestion.ingest_fielding_season_stats(data, team, cursor) for team in home_away]
            if name == 'batter_season_stats':
                [data_ingestion.ingest_batter_season_stats(data, team, cursor) for team in home_away]
            if name == 'pitcher_season_stats':
                [data_ingestion.ingest_pitcher_season_stats(data, team, cursor) for team in home_away]
            if name == 'player_descriptions':
                [data_ingestion.ingest_player_descriptions(data, team, cursor) for team in home_away]
            if name == 'team_data':
                [data_ingestion.ingest_team_data(data, team, cursor) for team in home_away]
            if name == 'games':
                data_ingestion.ingest_games(data, cursor)
            if name == 'pitch':
                [data_ingestion.ingest_pitch(data, team, cursor) for team in home_away]
            if name == 'linescore':
                [data_ingestion.ingest_linescore(data, team, cursor) for team in home_away]
            if name == 'officials':
                data_ingestion.ingest_officials(data, cursor)
            if name == 'game_wpa':
                data_ingestion.ingest_game_wpa(data, cursor)
        
        #Commit changes to database for each game_pk ingested
        conn.commit()
        
        #Add game_pk to succesfully ingested list
        successful_game_pks.append(pk)
    
    except Exception as e:
        #If there is an error, revert all changes to the database for the current game_pk, record the error, and continue to next game_pk
        conn.rollback()
        ingestion_exception[pk] = e
        continue
        
#Record end ingestion time
end_time = time.time()
    
#Print Summary Information
if len(successful_game_pks) == len(game_pks):
    print('Data ingestion for all ' + str(len(successful_game_pks)) + ' game_pks complete!')
if len(successful_game_pks) < len(game_pks):
    print('Data ingestion for ' + str(len(successful_game_pks)) + ' game_pks has been completed.')
    if len(already_seen_game_pks) > 0:
        print('The following game_pks were excluded to avoid duplication of data: ' + ' '.join(already_seen_game_pks))
    if len(failed_to_retrieve.keys()) > 0:
        print('The following game_pks were unable to be retrieved from the Baseball Savant API:')
        print('game_pk', 'Error Code')
        for key, value in failed_to_retrieve.items():
            print(key, value)
    if len(ingestion_exception.keys()) > 0:
        print('The following errors occured while ingesting the data for each game_pk:')
        print('game_pk', 'Error')
        for key, value in ingestion_exception.items():
            print(key, value)
print('Duration: ' + str(round(end_time - start_time, 3)) + ' seconds')
            
#Close connection to database after ingestion process is complete
conn.close()
