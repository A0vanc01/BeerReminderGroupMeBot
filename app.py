import logging
import os
import random
import sys

from flask import Flask, request

from groupme.polls import Poll, PollOption, PollHelper

from urllib.parse import urlencode
from urllib.request import Request, urlopen

application = Flask(__name__)
application.logger.addHandler(logging.StreamHandler(sys.stdout))
application.logger.setLevel(logging.DEBUG)

GROUPME_API_URL = 'https://api.groupme.com/v3/bots/post'
GROUPME_BOT_ID = os.getenv('GROUPME_BOT_ID')
GROUPME_ACCESS_TOKEN = os.getenv('GROUPME_ACCESS_TOKEN')

poll_helper = PollHelper(GROUPME_ACCESS_TOKEN)

@app.route('/')
def hello_world():
    application.logger.debug('Hello, World!')
    return 'Hello, World!'


@app.route('/webhook/', methods=['POST'])
def webhook():
    data = request.get_json()
    application.logger.debug('Received: ' + str(data))
    return handle_message(data)

def handle_message(message):
    if message['sender_type'] != 'user':
        # Don't process bot messages for now
        return 'OK', 200
    
    for attachment in message['attachments']:
        if attachment['type'] == 'poll':
            group_id = message['group_id']
            application.logger.debug('I found a poll')
            poll: Poll = poll_helper.get_poll(group_id, attachment['poll_id'])
            send_message(f"That poll's title is {poll.subject}")
            my_vote: PollOption = random.choice(poll.options)
            resp = poll_helper.vote(group_id, poll, my_vote)
            send_message(f'I pick "{my_vote.title}"')
            application.logger.debug(resp)
            return 'OK', 200

    send_message('Hello, ' + message['name'])

    return 'OK', 200

def send_message(message):
    data = {
        'bot_id' : GROUPME_BOT_ID,
        'text' : message,
    }
    application.logger.debug('Sending: ' + str(data))
    request = Request(GROUPME_API_URL, urlencode(data).encode())
    urlopen(request).read().decode()


if __name__ == '__main__':  
    application.run()