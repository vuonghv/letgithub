import os
import requests
import json
from getpass import getpass

from github import Github, UnknownObjectException
from config import config
from utils import perr, align_text
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
        login = _color_field('login', '{} {}'.format(u'\U0001F608', user.login))
        name = _color_field('name', user.name)
        email = _color_field('email', 'Email: {}'.format(user.email))
        company = _color_field('company', 'Company: {}'.format(user.company))
        location = _color_field('location', 'Location: {}'.format(user.location))
        blog = _color_field('blog', 'Blog: {}'.format(user.blog))
        bio = _color_field('bio', 'bio: {}'.format(user.bio))
        public_repos = _color_field('public_repos', '{} repositories'.format(user.public_repos))
        public_gists = _color_field('public_gists', '{} gists'.format(user.public_gists))
        followers = _color_field('followers', '{} followers'.format(user.followers))
        following = _color_field('following', '{} following'.format(user.following))
        joined_at = _color_field('created', 'joined at {}'.format(user.created_at))

        template = ('{login} ({name})\n'
                    '{email}\n'
                    '{company}  {location}\n'
                    '{blog}\n'
                    '{bio}\n'
                    '{public_repos}  {public_gists}\n'
                    '{followers}  {following}\n'
                    '{joined_at}')
        info = template.format(login=login, name=name, email=email,
                                company=company, location=location,
                                blog=blog, bio=bio, public_repos=public_repos,
                                public_gists=public_gists, followers=followers,
                                following=following, joined_at=joined_at)
        info = align_text(info, left_margin=2, max_width=100)
        print(info)
    except UnknownObjectException:
        perr(red('user `{}` not found!'.format(username)))

