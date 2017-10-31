#! /usr/bin/env python3

import hashlib
import hmac
import os

from flask import Flask, abort, request
import requests

app = Flask(__name__)

FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
FACEBOOK_VERIFICATION_TOKEN = os.getenv('FACEBOOK_VERIFICATION_TOKEN')

FACEBOOK_MESSAGE_URL = 'https://graph.facebook.com/v2.6/me/messages'

FACEBOOK_AUTHORIZED_SENDER_IDS = set([
    '1552580134821661',  # Szeto
    '1588200337910270',  # Peter
    '1346686395457291',  # Shana
    '1155732571195547',  # Shawn
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
        try:
            if not verify_facebook_signature(request.get_data(), request.headers.get('X-Hub-Signature')):
                abort(403)
        except:
            abort(403)
        body = request.get_json()
        if body['object'] == 'page':
            for entry in body['entry']:
                # facebook docs say that one entry will always have only one message
                message = entry['messaging'][0]
                print(message)
                sender_id = message['sender']['id']
                message_text = message['message']['text'].lower()
                if message_text == 'lock':
                    if sender_id in FACEBOOK_AUTHORIZED_SENDER_IDS:
                        lock_august()
                    send_facebook_message(sender_id, 'Door locked.')
                elif message_text == 'unlock':
                    if sender_id in FACEBOOK_AUTHORIZED_SENDER_IDS:
                        unlock_august()
                        unlock_front()
                    send_facebook_message(sender_id, 'Door unlocked.')
                else:
                    send_facebook_message(sender_id, 'Unrecognized command.')
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

def verify_facebook_signature(payload, expected_signature):
    key = bytes(FACEBOOK_APP_SECRET, 'utf-8')
    calculated_signature = hmac.new(key, payload, hashlib.sha1).hexdigest()
    return f'sha1={calculated_signature}' == expected_signature

def send_facebook_message(recipient_id, message):
    params = {
        'access_token': FACEBOOK_PAGE_ACCESS_TOKEN,
    }
    payload = {
        'recipient': {
            'id': recipient_id,
        },
        'message': {
            'text': message,
        },
    }
    requests.post(FACEBOOK_MESSAGE_URL, params=params, json=payload)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
