import os
import sys
import json
import datetime

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



    d = datetime.date(datetime.datetime.now())
    next_Sunday = next_day(d, 6) # 0 = Monday, 1=Tuesday, 2=Wednesday...
    print(next_Sunday)
   

    msg = '{}, you volunteered to get beer on the "{}".'.format(data['name'], next_Sunday)
    send_message(msg)

    return "ok", 200

def next_day(d, day):
    days_ahead = day - d.day()
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