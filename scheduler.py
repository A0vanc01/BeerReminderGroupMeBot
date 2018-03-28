from logging import log, DEBUG
import sys
import psycopg2
import os
import sys
import json
import datetime
import time


from datetime import date
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request



if __name__=='__main__':
    print("I'm still awake")
    sys.stdout.flush()

 #Database check
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    onlyHasOneRow = False
    cur = conn.cursor()
    cur.execute('''SELECT * FROM VOLUNTEER''')
    rows = cur.fetchall()
    rowsize = 0
    print("\nShow me the databases:\n")
    for row in rows:
        print("   ", row[0])
        rowsize+=1

    if(rowsize == 1):
        onlyHasOneRow = True
   
    d = datetime.datetime.now()
    if(onlyHasOneRow & d.date() >= rows[0]["DATE_REQUIRED"]):
       print('return reminder for volunteer to bring beer')# return "ok", 200

    if(rowsize>3):
        msg = 'Holy crap you guys are dicks all volunteering to try to screw over this bot I wrote.'
        send_message(msg)
        cur.execute('''SELECT * FROM VOLUNTEER ORDER BY ID DESC LIMIT 1''')
        row = cur.fetchone()
        msg = 'Well @{} was the last person to spam the bot, so I guess he''s bringing beer!!!!\n=P'.format(row['name'])
        send_message(msg)

def send_message(msg):
    url  = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id' : os.getenv('GROUPME_BOT_ID'),
        'text'   : msg,
        }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()
  
