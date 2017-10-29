#! /usr/bin/env python3

import os

from flask import Flask, abort, request
app = Flask(__name__)

FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
FACEBOOK_VERIFICATION_TOKEN = os.getenv('FACEBOOK_VERIFICATION_TOKEN')

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/webhook/facebook_messenger', methods=['GET', 'POST'])
def facebook_webhook():
    if request.method == 'POST':
        body = request.get_json()
        if body['object'] == 'page':
            for entry in body['entry']:
                message = entry['messaging'][0]
                if message['sender']['id'] == '1552580134821661':
                    if message['message']['text'] == 'lock':
                        print('Locking the August lock!')
                        os.system('ssh -i /sshkeys/mountedpi/ssh-privatekey pi@mountedpi "python3 august.py lock"')
                    elif message['message']['text'] == 'unlock':
                        print('Unlocking the August lock!')
                        os.system('ssh -i /sshkeys/mountedpi/ssh-privatekey pi@mountedpi "python3 august.py unlock"')
                print(entry['messaging'][0])
            return 'EVENT_RECEIVED'
        abort(404)
    else:
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == FACEBOOK_VERIFICATION_TOKEN:
            return challenge
        abort(403)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
