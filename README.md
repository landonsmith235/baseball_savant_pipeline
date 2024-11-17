# **Baseball Savant Data Pipeline**
#### Landon Smith

### **Problem Statement**

Baseball Savant provides a rich interface and visualizations for baseball fans to view detailed Statcast data through various features, including a tool called the "Game Feed". The Game Feed updates an interactive dashboard throughout the duration of a baseball game with play-by-play data by polling a JSON API, and additionally stores the data from completed games to be viewed in the same interface. The task addressed by this project is to efficiently capture and store the data from past games into our own custom database to enable further insights and analysis.

### **Project Objectives**

The primary objectives of this project include:

1. **Database Design**: Design and implement a SQLite database tailored for storing and analyzing Baseball Savant game feed data.

2. **Data Ingestion**: Develop a Python program to extract data from the Baseball Savant game feed and load it into the SQLite database. The program should handle game primary keys (`game_pk`) as inputs and ensure data consistency and atomicity in ingestion processes.

3. **SQL Queries**: Utilize the designed database and ingested data to perform complex queries and extract meaningful insights.

### **Deliverables**

- This README file in Markdown and PDF format.
- Source code (4 Python scripts, requirements.txt file)
- An Entity Relationship Diagram (ERD) displaying the structure of the database.

### **Setup**

#### **Install Required Dependencies**
In order for us to successfully run the program, we need to have all of the proper dependencies installed. To do this, we can utilize `pip`, the package installer for Python. On your `bash` command line interface, use the following code to install project dependencies that aren't found natively within Python:

`pip install -r requirements.txt`

### **Pipeline Execution**
Once our dependencies are installed, we can run our program on our `bash` command line interface using the following syntax:

`python pipeline_execution.py {game_pks or game_pks.txt} --db {database filepath}`

In the above syntax, `python` is the command that specifies we want to run the Python interpreter, while `pipeline_execution.py` is the script we want to execute. The first and only required argument that we pass to our script is the unique `game_pk` identifier of games where we wish to access data. The game_pks can be passed to the script as a single value, a space-delimited list, or a .txt file containing the desired game_pk values as shown below:

`python pipeline_execution.py 635907`

`python pipeline_execution.py 635907 635910 635913`

`python pipeline_execution.py game_pks.txt`

The final argument that can be passed to our script is optional. The `--db` argument allows the user to name the resulting database file and specify a location for the database file to be written. If no input is passed in, the database file will be created inside the current working directory and be named `baseballsavant.db` by default. Additionally, if there is a pre-existing database file you would like to write to, you can specify the path of this file in order to ingest game data from further game_pks. Here is an example:

`python pipeline_execution.py 635907 --db /Desktop/Pipeline/baseball.db`

### **Pipeline Outputs**

Upon the script completing the process of creating the database, necessary tables, and ingesting the game data for each game_pk from the Baseball Savant API, the program will provide varying outputs depending on the success of the process. The following examples represent the range of potential outputs:

If all game_pks were successfully ingested:
- "Data ingestion for all {# of total game_pks} game_pks complete!"

If certain game_pks were excluded to prevent the duplication of data:
- "Data ingestion for {# of successful game_pks} game_pks has been completed."
- "The following game_pks were excluded to avoid duplication of data: 635907 635910 635913"

If certain game_pks were unable to be retrieved from the Baseball Savant API:
- "The following game_pks were unable to be retrieved from the Baseball Savant API:"
- game_pk, Error Code
- 635907, 404

If certain game_pks experienced errors during the ingestion process and suffered a rollback:
- "The following errors occurred while ingesting the data for each game_pk:"
- game_pk, Error
- 635907, KeyError

### **SQL Query Execution**

Once our database has been created and we have ingested game data from the Baseball Savant API, we can query the database in order to craft meaningful insights. The following questions are examples of insights that are able to be derived from our newly created database:

1. Which pitchers threw the most pitches in a game? How many pitches did they throw? How many batters did they face?
2. Who are the top batters by average exit velocity on balls in play, split by both pitcher handedness and batter handedness? What is their average exit velocity? How many balls in play did they have?
3. What are the average pitch speed, spin rate, horizontal break, and induced vertical break for each pitch type?

In order to see the results of these queries on the database, we can execute the `sql_queries.py` script using the following `bash` syntax:

`python sql_queries.py {database filepath} -v`

In the above syntax, we can use the `-v` or `--verbose` option to specify whether or not the SQL query used to achieve the result should be returned. If omitted, the question and resulting dataframe are all that will be returned for each question. When either option name is specified, the question, SQL query, and dataframe will all be returned.

Additionally, if the user seeks to write their own queries against the database from the command line, they can use the `sqlite3` command on a `bash` command line:

`sqlite3 {database filepath}`

After connecting to the database, a user can simply input a SQL query and obtain the results of their query from the command line.

