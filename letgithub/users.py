from core import config
from github import Github
from getpass import getpass


def login(username: str, *arg, **kwagrs):
    gh = config.get('github')
    password = getpass('Enter password for user `{}`: '.format(username))
    config.update(github=Github(login_or_token=username, password=password))
    config.update(promt_msg='[{}]> '.format(username))

def get_user(username: str=None, *args, **kwagrs):
    gh = config.get('github')
    if username:
        user = gh.get_user(username)
    else:
        user = gh.get_user()
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

