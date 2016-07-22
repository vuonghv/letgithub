import os
import requests
import json
from getpass import getpass

from config import config
from github import Github

GITHUB_API = 'https://api.github.com'

def authenticate_user():
    token_file = os.path.expanduser('~/.letgithub/token.txt')
    while True:
        try:
            with open(token_file, 'r') as f:
                token = f.read()
                g = Github(token)
                config.update(GITHUB=g)
                config.update(PROMT_MSG='[{}]> '.format(g.get_user().login))
                return
        except FileNotFoundError:
            username = input('Github username: ')
            password = getpass('Github password: ')

            url = '{}/{}'.format(GITHUB_API, 'authorizations')
            payload = {
                'note': 'token for letgithub',
                'scopes': ['repo']
            }
            res = requests.post(url,
                                auth=(username, password),
                                data=json.dumps(payload))
            data = json.loads(res.text)
            if res.status_code != 201:
                msg = data.get('message', res.status_code)
                print('ERROR: {}'.format(msg))
                continue

            config.update(GITHUB=Github(data['token']))
            config.update(PROMT_MSG='[{}]> '.format(username))
            os.makedirs(os.path.dirname(token_file), exist_ok=True)
            with open(token_file, 'w') as f:
                f.write(data['token'])
            return

def login(username: str, *arg, **kwagrs):
    password = getpass('Enter password for user `{}`: '.format(username))
    config.update(GITHUB=Github(username, password))
    config.update(PROMT_MSG='[{}]> '.format(username))

def show_user(username: str=None, *args, **kwagrs):
    g = config.get('GITHUB')
    if username:
        user = g.get_user(username)
    else:
        user = g.get_user()
    attrs = [
        'login',
        'name',
        'email',
        'company',
        'blog',
        'bio',
        'public_repos',
        'public_gists',
        'followers',
        'following',
        'created_at',
        'updated_at',
    ]
    try:
        for attr in attrs:
            val = getattr(user, attr, None)
            print('  {}: {}'.format(attr, val if val is not None else ''))
    except Exception:
        print('user `{}` not found!'.format(username))

