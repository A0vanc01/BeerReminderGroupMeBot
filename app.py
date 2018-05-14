import os
import sys
import json
import datetime
import time
import os
import random

from datetime import date
from groupme.polls import Poll, PollOption, PollHelper
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request


from urllib.parse import urlencode
from urllib.request import Request, urlopen

application = Flask(__name__)

GROUPME_API_URL = 'https://api.groupme.com/v3/bots/post'
GROUPME_BOT_ID = os.getenv('GROUPME_BOT_ID')
GROUPME_ACCESS_TOKEN = os.getenv('GROUPME_ACCESS_TOKEN')

poll_helper = PollHelper(GROUPME_ACCESS_TOKEN)


@application.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if (handle_message(data)):
        return "ok poll response", 200

    if data['sender_type'] == 'bot' or "beer" not in data['text']:# != "/beer":
       return "ok not beer response", 200

    log('Received {}'.format(data))
    
    #Database check
    DATABASE_URL = os.environ['DATABASE_URL']

    d = datetime.datetime.now()

    next_Sunday = next_weekday(d, 6)

    msg = '{}, you volunteered to get beer on the {}.  I will try to remind you.'.format(data['name'], next_Sunday.date())
    send_message(msg)
    

    testMessage = "\nShow me the databases:\n"

    msg = 'here is what the db has in it: {},'.format(testMessage)
    send_message

    return "ok", 200

def handle_message(message) -> bool:

    pollFound = False
    
    for attachment in message['attachments']:
        if attachment['type'] == 'poll':
            group_id = message['group_id']
            app.logger.debug('I found a poll')
            poll: Poll = poll_helper.get_poll(group_id, attachment['poll_id'])
            send_message(f"That poll's title is {poll.subject}")
            my_vote: PollOption = random.choice(poll.options)
            resp = poll_helper.vote(group_id, poll, my_vote)
            send_message(f'I pick "{my_vote.title}"')
            app.logger.debug(resp)
            pollFound = True
    send_message('Hello, ' + message['name'])
    return pollFound

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def log(msg):
    print(str(msg))
    sys.stdout.flush()

def send_message(message):
    data = {
        'bot_id' : GROUPME_BOT_ID,
        'text' : message,
    }
    #app.logger.debug('Sending: ' + str(data))
    request = Request(GROUPME_API_URL, urlencode(data).encode())
    urlopen(request).read().decode()

if __name__=="__main__":
    application.run()