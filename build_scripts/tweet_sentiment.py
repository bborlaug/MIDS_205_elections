#Script that grabs 8 tweets containing each of the 5 remaining political candidate's
#names every 30 min from ~12:00 - 24:00 PST. Mention rate is calculated for each
#candidate as well as sentiment for the tweets grabbed. Results are saved to postgreSQL db

import twitter
import time
from datetime import datetime
import psycopg2
import json
import requests
from pytz import timezone
import pytz

##Twitter credentials - Enter your own
CONSUMER_KEY = 'Insert consumer key here'
CONSUMER_SECRET ='Insert consumer secret here'
OAUTH_TOKEN = 'Insert Oauth token here'
OAUTH_TOKEN_SECRET = 'Insert token secret here'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

#url for tweet sentiment processing
url = 'http://text-processing.com/api/sentiment/'

#Insert postgres info
postgres_username = 'postgres' #Enter postgres username
postgres_password = 'postgres' #Enter postgres password
        
# Query terms
q = ['Trump', 'Cruz', 'Kasich', 'Hillary, Clinton', 'Bernie, Bern']

while True:
    
    for cand in q:
        print 'Filtering the public timeline for track="%s"' % (cand,)
        twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
        stream = twitter_stream.statuses.filter(track=cand)
        
        then = time.time()
        count=0
        tweets = []        
        
        ##Grab tweets
        for tweet in stream:
            count += 1
            print count
            tweets.append(tweet['text'])
            
            if count >= 8:
                break
            
        now = time.time()
        rate = count/(now-then)
        sentiments = []
        #Retrieve sentiments
        for t in tweets:
            payload = {'text': t}
            r = requests.post(url, data=payload)
            sen = json.loads(r.text)
            sentiments.append(sen["label"])
        
        #Sentiment counts
        pos = sentiments.count('pos')
        neg = sentiments.count('neg')
        neut = sentiments.count('neutral')
        
        #Assign party variable
        if cand in ('Trump', 'Cruz', 'Kasich'):
            party = 'gop'
        else:
            party ='dem'
            
        #Recode candidate names
        if cand == 'Trump':
            lowcand = 'trump'
            
        if cand == 'Cruz':
            lowcand = 'cruz'
            
        if cand == 'Kasich':
            lowcand = 'kasich'
            
        if cand == 'Hillary, Clinton':
            lowcand = 'clinton'
            
        if cand == 'Bernie, Bern':
            lowcand = 'sanders'
        
        #Save results to postgres db
        try:
            conn = psycopg2.connect(dbname='elections', user=postgres_username, password=postgres_password)
        except:
            print "Unable to connect to elections database"
        
        cur = conn.cursor()
        cur.execute('commit')
    
        print '\n'
        print 'Inserting results into postgres db'
        print '\n'
        
        fmt = '%Y-%m-%d %H:%M:%S'
        now_utc = datetime.now(timezone('UTC'))
        now_pacific = now_utc.astimezone(timezone('US/Pacific'))
        pacific_date = now_pacific.strftime(fmt)
        pacific_date = pacific_date.split(' ')[0]
        pacific_time = now_pacific.strftime(fmt)
        pacific_time = pacific_time.split(' ')[1]
        insert_query = """INSERT INTO data.twitter
                          VALUES ('%s','%s','%s','%s',%f,%d,%d,%d);""" %(str(pacific_date),str(pacific_time),lowcand,party,float(rate),int(pos),int(neg),int(neut))
        
        cur.execute(insert_query)
        cur.close()
        conn.close()
        print 'waiting 30 sec...'
        time.sleep(30) #Wait 30 sec to prevent exceeding Twitter Streaming limits
            
    ##Stop for 12 hrs 12 AM PST
    ##Prevents making too many sentiment requests
    now_utc = datetime.now(timezone('UTC'))
    now_pacific = now_utc.astimezone(timezone('US/Pacific'))
    pacific_time = now_pacific.strftime(fmt)
    pacific_time = pacific_time.split(' ')[1]
    
    
    if '12:00:00' > pacific_time:
        print '\n'
        print 'Sleeping...Zzz..'
        print '\n'
        time.sleep(60*60*12) #wait 12 hrs
      
    print '\n'    
    print 'Waiting for next batch...'
    print '\n'
    time.sleep(60*30) #wait 30 min
    
