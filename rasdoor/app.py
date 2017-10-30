#! /usr/bin/env python3

import os

from flask import Flask, abort, request
app = Flask(__name__)

FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
FACEBOOK_VERIFICATION_TOKEN = os.getenv('FACEBOOK_VERIFICATION_TOKEN')

FACEBOOK_AUTHORIZED_SENDER_IDS = set([
    '1552580134821661',  # Szeto
    '1588200337910270',  # Peter
    '1346686395457291',  # Shana
])

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/privacy')
def privacy_policy():
    return 'You should not be using this site if you don\'t know Szeto. ' \
        'If you do, the privacy policy is that there is a log of who ' \
        'opens this door. This is a private residence, so we want to ' \
        'know who unlocks and locks our door.'

@app.route('/webhook/facebook_messenger', methods=['GET', 'POST'])
def facebook_webhook():
    if request.method == 'POST':
        raw_data = request.get_data()
        print('raw_data =', raw_data)
        print('X-Hub-Signature =', request.headers.get('X-Hub-Signature'))
        body = request.get_json()
        if body['object'] == 'page':
            for entry in body['entry']:
                # facebook docs say that one entry will always have only one message
                message = entry['messaging'][0]
                if message['sender']['id'] in FACEBOOK_AUTHORIZED_SENDER_IDS:
                    if message['message']['text'] == 'lock':
                        lock_august()
                    elif message['message']['text'] == 'unlock':
                        unlock_august()
                        unlock_front()
                print(message)
            return 'EVENT_RECEIVED'
        abort(404)
    else:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == FACEBOOK_VERIFICATION_TOKEN:
            return challenge
        abort(403)

def _run_command_on_pi(cmd):
    os.system(f'ssh -o StrictHostKeyChecking=no -i /sshkeys/mountedpi/ssh-privatekey pi@mountedpi "{cmd}"')

def lock_august():
    _run_command_on_pi('python3 august.py lock')

def unlock_august():
    _run_command_on_pi('python3 august.py unlock')

def unlock_front():
    _run_command_on_pi('python opendoor.py')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
