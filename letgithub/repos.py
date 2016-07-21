from core import config 


def display_repos(username: str, repo_name: str=None, *arg):
    gh = config.get('github')
    if repo_name:
        attrs = [
            'name',
            'full_name',
            'description',
            'url',
            'clone_url',
            'homepage',
            'language',
            'forks_count',
            'stargazers_count',
            'watchers_count',
            'size',
            'open_issues_count',
            'subscribers_count',
            'has_downloads',
            'pushed_at',
            'created_at',
            'updated_at'
        ]
        try:
            repo = gh.get_user(username).get_repo(repo_name)
            for attr in attrs:
                val = getattr(repo, attr, None)
                print('  {}: {}'.format(attr, val if val is not None else ''))
        except Exception:
            print('Repository {}/{} not found!')
        finally:
            return

    for repo in gh.get_user(username).get_repos():
        print('{} [stars: {}, forks: {}] - {}'.format(
                repo.name, repo.stargazers_count,
                repo.forks_count, repo.description))

