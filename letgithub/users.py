import os
import requests
import json
from getpass import getpass

from github import Github, UnknownObjectException
from config import config
from utils import perr
from colors import red, color

GITHUB_API = 'https://api.github.com'

def _color_field(field_name, value):
    return color(config['THEME']['USER'][field_name])(value)

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
    try:
        user = g.get_user(username) if username else g.get_user()
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
        for attr in attrs:
            val = getattr(user, attr, None)
            print('  {}: {}'.format(attr, val if val is not None else ''))
        login = _color_field('login', user.login)
        name = _color_field('name', user.name)
        email = _color_field('email', '{} {}'.format(u'\U00002709', user.email))
        company = _color_field('company', '{} {}'.format(u'\U0001F3E2', user.company))
        blog = _color_field('blog', '{} {}'.format(u'\U0001F30E', user.blog))
        location = _color_field('location', '{} {}'.format(u'\U0001F3E0', user.location))
        bio = _color_field('bio', user.bio)
        public_repos = _color_field('public_repos', '{} repositories'.format(user.public_repos))
        public_gists = _color_field('public_gists', '{} gists'.format(user.public_gists))
        followers = _color_field('followers', '{} followers'.format(user.followers))
        following = _color_field('following', '{} following'.format(user.following))
        joined_at = _color_field('created', 'joined at {}'.format(user.created_at))
    except UnknownObjectException:
        perr(red('user `{}` not found!'.format(username)))

