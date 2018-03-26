import os
import sys
import json
import datetime
import time
import os
import psycopg2


from datetime import date
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

application = Flask(__name__)

@application.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    if data['sender_type'] == 'bot' or data['text'] != "/beer":
       return "ok", 200

    log('Received {}'.format(data))
    
    #Database check
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS VOLUNTEER
       (ID SERIAL PRIMARY KEY  NOT NULL,
       NAME            TEXT    NOT NULL,
       DATE_ENTERED    TIMESTAMP DEFAULT NULL,
       DATE_REQUIRED   DATE    NOT NULL;''')

    d = datetime.datetime.now()
    #d = date.today.isoformat()

    next_Sunday = next_weekday(d, 6) # 0 = Monday, 1=Tuesday, 2=Wednesday...

    conn.execute('''INSERT INTO VOLUNTEER (NAME, DATE_ENTERED, DATE_REQUIRED)
                 VALUES ({}, {}, {})'''.format(data['name'],d , next_Sunday.date()))
    

    msg = '{}, you volunteered to get beer on the {}.  I will try to remind you.'.format(data['name'], next_Sunday.date())
    send_message(msg)
    
    #getting all the stuff in the DB
    rows = cur.fetchall()
    testMessage = "\nShow me the databases:\n"
    for row in rows:
        testMessage += "   ", row[0]
    msg = 'here is what the db has in it: {},'.format(testMessage)
    send_message


    return "ok", 200

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def send_message(msg):
    url  = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id' : os.getenv('GROUPME_BOT_ID'),
        'text'   : msg,
        }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()
  
def log(msg):
    print(str(msg))
    sys.stdout.flush()

if __name__=="__main__":
    application.run()