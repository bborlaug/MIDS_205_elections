#Script grabs wk of Google search traffic data for 2016 Democratic
#candidates Hillary Clinton & Bernie Sanders, cleans it, 
#& dumps it into a PostgreSQL database

#Run script on night of election & specify states variable
from pytrends.pyGTrends import pyGTrends
import time
import datetime as dt
import pandas as pd
import os
import psycopg2

#Insert Google info 
google_username = "" #Enter google username
google_password = "" #Enter google password
path = "C:\Users\Brennan\Desktop\w205_data\google_traffic"
#Change path ^ to wherever you feel comportable temporarily storing files

os.chdir(path)

dem = "Hillary Clinton, Bernie Sanders"
states = ["US-PA", "US-CT", "US-DE", "US-MD", "US-RI"] #enter states or string of states

#Insert postgres info
postgres_username = 'postgres'
postgres_password = 'postgres'

for state in states:
    connector = pyGTrends(google_username, google_password)
    connector.request_report(dem, geo = state, date = "today 7-d")
    time.sleep(5)
    
    file = ''.join([str(dt.date.today()),'_', state, '_dem', '_messy'])
    connector.save_csv('', file)
    
    #Now for some cleaning...
    print '\n'
    print 'cleaning...'
    print '\n'
    
    df = pd.read_csv(''.join([file, '.csv']), skiprows = 4)
    df = df[:151]
    df2 = pd.read_csv(''.join([file, '.csv']), skiprows = 4)
    df2 = df2[:151]
    df['candidate'] = 'clinton'
    df2['candidate'] = 'sanders'
    df = df.drop('bernie sanders', 1)
    df2 = df2.drop('hillary clinton', 1)
    df = df.rename(columns={'hillary clinton': 'traffic'})
    df2 = df2.rename(columns={'bernie sanders': 'traffic'})
    df = df.append(df2)
    df['state'] = state.split("-")[1]
    df['party'] = 'dem'
    
    df = df.dropna()
    
    dates= []
    times=[]
    for t in df['Time']:
        split1 = t.split(' ')
        split1 = split1[0]
        split2 = split1.split('-')
        date = '-'.join(split2[:3])
        time = '-'.join(split2[3:])
        dates.append(date)
        times.append(time)
    df['date'] = dates
    df['time'] = times
    df = df.drop('Time', 1)
    
    #Drop csv
    os.remove(''.join([file, '.csv']))
    print '\n'
    print 'csv dropped'
    
    #Save results to postgres db
    try:
        conn = psycopg2.connect(dbname='elections', user=postgres_username, password=postgres_password)
    except:
        print "Unable to connect to elections database"
        
    cur = conn.cursor()
    cur.execute('commit')
    
    print '\n'
    print 'Inserting results into postgres db'
    
    for i,j,k,l,m,n in zip(df['date'], df['time'], df['state'], df['candidate'], df['party'], df['traffic']):
        insert_query = """INSERT INTO data.google
                          VALUES ('%s','%s','%s','%s','%s',%d);""" %(i,j,k,l,m,int(n))
        cur.execute(insert_query)
    cur.close()
    conn.close()
    
    
