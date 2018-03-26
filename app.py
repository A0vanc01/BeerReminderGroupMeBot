import os
import sys
import json
import time
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

   #d = datetime.datetime.now()
    d = date.today#.isoformat()
    next_Sunday = next_weekday(d, 6) # 0 = Monday, 1=Tuesday, 2=Wednesday...

    msg = '{}, you volunteered to get beer on the {}.  I will try to remind you.'.format(data['name'], next_Sunday)
    send_message(msg)
    #add fireBase, or just save and read from the Herokuserver here for a remind at 12:30 on next_Suday
    #then figure out how to read in once every .5 minutes and check if it matches the date and time, but only to YY:MM:DD:HH:MM


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