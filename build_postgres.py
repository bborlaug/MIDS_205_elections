#Script that builds out a postgreSQL db for web & social media analysis during the U.S.
#presidential primary election cycle

import psycopg2

username = 'postgres' #Enter postgres username
password = 'N1!dakota' #Enter postgres password

try:
    conn = psycopg2.connect(dbname='postgres', user=username, password=password)
except:
    print "Unable to connect to postgres database"

cur = conn.cursor()

cur.execute('commit')
drop_db = """DROP DATABASE elections;"""
cur.execute(drop_db)
create_db = """CREATE DATABASE elections;"""
cur.execute(create_db)

#Now that elections db is created, close connection & connect to this
#db directly
cur.close()
conn.close()

#Connect to elections db
try:
    conn = psycopg2.connect(dbname='elections', user=username, password=password)
except:
    print "Unable to connect to elections database"

cur = conn.cursor()
cur.execute('commit')

create_schema = """CREATE SCHEMA data;"""
cur.execute(create_schema)

results_table = """CREATE TABLE data.results (
                            date text,
                            state text,
                            candidate text,
                            party text,
                            poll double precision,
                            results double precision
);"""
cur.execute(results_table)

google_table = """CREATE TABLE data.google (
                            date text,
                            time text,
                            state text,
                            candidate text,
                            party text,
                            traffic integer
);"""
cur.execute(google_table)

twitter_table = """CREATE TABLE data.twitter (
                            date text,
                            time text,
                            candidate text,
                            party text,
                            mention_rate double precision,
                            pos_tweets integer,
                            neg_tweets integer,
                            neut_tweets integer
);"""
cur.execute(twitter_table)

cur.close()
conn.close()
