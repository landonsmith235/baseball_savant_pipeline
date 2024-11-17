import pandas as pd
import sqlite3
import argparse

#Set up arguement parser
parser = argparse.ArgumentParser(description="Display SQL queries.")
parser.add_argument("db", type=str, help="The filepath to the database.")
parser.add_argument('-v', '--verbose', action='store_true', help='Show SQL query.')

# Parse arguments
args = parser.parse_args()
 
# Accessing the database filepath
db_path = args.db

#Accessing verbose toggle
verbose = args.verbose

#Connect to database using filepath
conn = sqlite3.connect(db_path)

#Create Cursor Object
cursor = conn.cursor()

### Execute demonstration queries
# Which pitchers threw the most pitches in a game? How many pitches did they throw? How many batters did they face?
query = """
WITH top_pitch_counts AS (SELECT game_pk, pitcher_name, MAX(player_total_pitches) AS top_pitch_counts 
FROM pitch
GROUP BY 1,2
ORDER BY 3 DESC
LIMIT 5),
ab_count AS (SELECT p.game_pk, p.pitcher_name, batter_name, COUNT(*) AS ab_count
FROM pitch p
JOIN top_pitch_counts c ON c.game_pk = p.game_pk
WHERE pitch_number = 1
GROUP BY 1,2,3),
batters_faced AS (SELECT game_pk, pitcher_name, SUM(ab_count) AS batters_faced
FROM ab_count
WHERE pitcher_name IN (SELECT pitcher_name FROM top_pitch_counts)
GROUP BY 1, 2
ORDER BY 3 DESC)
SELECT RANK() OVER(ORDER BY top_pitch_counts DESC) AS rank, tc.pitcher_name, top_pitch_counts, batters_faced
FROM top_pitch_counts tc
JOIN batters_faced bf ON tc.pitcher_name = bf.pitcher_name
"""
df = pd.read_sql_query(query, conn)
print()
# Print the question
print('Which pitchers threw the most pitches in a game? How many pitches did they throw? How many batters did they face?')
print()
# If verbose is True, print the SQL query use to achieve results
if verbose == True:
    print(query)
    print()
# Print resulting dataframe
print(df)

# Who are the top batters by average exit velocity on balls in play, split by both pitcher handedness and batter handedness? What is their average exit velocity? How many balls in play did they have?
query = '''
WITH unranked AS (SELECT batter_name, p_throws AS pitcher_side, stand AS batter_side, ROUND(AVG(hit_speed), 2) AS avg_exit_velo, COUNT(*) AS balls_in_play
FROM pitch
WHERE hit_speed NOT NULL AND call_name = 'In Play'
GROUP BY 1,2,3
ORDER BY 4 DESC
LIMIT 5)
SELECT RANK() OVER(ORDER BY avg_exit_velo DESC) AS rank, *
FROM unranked
'''
df = pd.read_sql_query(query, conn)
print()
# Print the question
print('Who are the top batters by average exit velocity on balls in play, split by both pitcher handedness and batter handedness? What is their average exit velocity? How many balls in play did they have?')
print()
# If verbose is True, print the SQL query use to achieve results
if verbose == True:
    print(query)
    print()
# Print resulting dataframe
print(df)

# What are the average pitch speed, spin rate, horizontal break, and induced vertical break for each pitch type?
query = '''
SELECT pitch_name, ROUND(AVG(start_speed),2) AS avg_speed, ROUND(AVG(spin_rate),2) AS avg_spin, ROUND(AVG(breakX),2) AS avg_breakX, ROUND(AVG(breakZ),2) AS avg_breakZ
FROM pitch
GROUP BY 1
'''
df = pd.read_sql_query(query, conn)
print()
# Print the question
print('What are the average pitch speed, spin rate, horizontal break, and induced vertical break for each pitch type?')
print()
# If verbose is True, print the SQL query use to achieve results
if verbose == True:
    print(query)
    print()
# Print resulting dataframe
print(df)