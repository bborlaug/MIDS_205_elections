#Step-by-Step Instructions
...for replicating this project yourself:
  
1) Download PostgreSQL (http://www.postgresql.org/download/)
  
2) Install Python 2.7 (https://www.python.org/downloads/)
  
3) Run build.postgres.py -> This will build out the "elections" database in PostgresSQL (Note: If you lack some of the python libraries used in this or other scripts, install them separately with 'pip' or from your browser).
  
4) Run load_data.sql (from MIDS_205_elections/data) -> This will load the previous data that I have collected into the 'elections' database (election results & google traffic only; Twitter data not included due to its dynamic nature).
  
5) Run tweet_sentiment.py -> Script that connects to Twitter's public streaming API & collects 16 tweets/candidate/hr from 12 pm PST -> 12 am PST to measure "mention rate" & tweet sentiment statistics. Results are stored in 'elections' database. This script runs continuously & should be left on in the background.
  
6) On the night of a primary election (or anytime you are interested in obtaining a week's worth of Google search traffic data) run the google_trends_dem.py & google_trends_gop.py scripts. Make sure you alter the script to search only the states that you are interested in. Results will be dumped into 'elections' database.
  
7) Open a live PostgreSQL connection in Tableau desktop with the following connection details:
  
Tableau-PostgreSQL Connection Details:  
  
Server: (Server where your postgreSQL db lives)  
Port: 5432  
Database: elections  
  
Authentication: "Username and Password"  
Username: postgres  
Password: postgres  
  
You should now have a streamlined flow of new twitter data for your Tableau workbooks. You must add election results as they come in separately by running the google_trends_dem.py & google_trends_gop.py scripts anytime you want to obtain a new week's worth of search traffic data for a given state. Have fun! For reference, here's a snapshot of some of the workbooks I created (up to date as of 4/28/16):
  
**A comprehensive dashboard will ultimately be created for simple election summary analyses.

