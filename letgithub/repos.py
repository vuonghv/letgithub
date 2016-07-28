from github import UnknownObjectException
from config import config
from utils import perr, align_text
from colors import red, color

LEFT_MARGIN = 2
MAX_WIDTH = 100

def _color_field(field_name, value):
    return color(config['THEME']['REPOS'][field_name])(value)

def view_repos(username: str, repo_name: str=None, *args, **kwargs):
    if repo_name:
        return view_detail_repo(username, repo_name)
    return view_list_repos(username)

def view_detail_repo(username: str, repo_name: str):
    raise NotImplementedError

def view_list_repos(username: str):
    g = config['GITHUB']
    try:
        repositories = g.get_user(username).get_repos()
        for repo in repositories:
            name = repo.name
            name = _color_field('name', name)

            desc = repo.description if repo.description else ''
            desc = _color_field('description', desc) if desc else ''

            stars = '{} {}'.format(u'\U00002B50', repo.stargazers_count)
            stars = _color_field('stargazers_count', stars)

            forks = '{} {}'.format(u'\U0001F433', repo.forks_count)
            forks = _color_field('forks_count', forks)

            upd_at = repo.updated_at
            upd_at = _color_field('updated_at', upd_at)

            parent = repo.parent.full_name if repo.parent else ''
            parent = _color_field('parent', parent) if parent else ''
 
            template = ('{name}  ({stars_count}  {forks_count})\n',
                        'forked from {parent}\n' if parent else '{parent}',
                        '{description}\n' if desc else '{description}',
                        'Updated on {updated_at}',)
            template = ''.join(template)
            info = template.format(name=name, stars_count=stars,
                                    forks_count=forks, parent=parent,
                                    description=desc, updated_at=upd_at)
            info = align_text(info, LEFT_MARGIN, MAX_WIDTH)
            print(info, '\n')
    except UnknownObjectException as err:
        perr(red(err))

