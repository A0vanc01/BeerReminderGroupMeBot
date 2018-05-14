import os
import requests


class Poll:
    def __init__(self, id, subject, owner_id, conversation_id, created_at, expiration, status, options):
        self.id = id
        self.subject = subject
        self.owner_id = owner_id
        self.conversation_id = conversation_id
        self.created_at = created_at
        self.expiration = expiration
        self.status = status
        self.options = options


class PollOption:
    def __init__(self, id, title, votes):
        self.id = id
        self.title = title
        self.votes = votes


class PollHelper:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_poll(self, conversation_id, poll_id):
        url = f'https://api.groupme.com/v3/poll/{conversation_id}/{poll_id}'
        headers = {'X-Access-Token': self.access_token}
        r = requests.get(url, headers=headers)
        data = r.json()
        poll_json = data['response']['poll']['data']
        options = []
        for opt in poll_json['options']:
            options.append(PollOption(opt['id'], opt['title'], opt.get('votes', 0)))
        poll = Poll(poll_json['id'], poll_json['subject'], poll_json['owner_id'],
            poll_json['conversation_id'], poll_json['created_at'], poll_json['expiration'],
            poll_json['status'], options)
        return poll

    def vote(self, conversation_id, poll, option):
        url = f'https://api.groupme.com/v3/poll/{conversation_id}/{poll.id}/{option.id}'
        headers = {'X-Access-Token': self.access_token}
        r = requests.post(url, data={}, headers=headers)
        return r
