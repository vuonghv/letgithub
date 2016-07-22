from config import config

def my_issues(*args, **kwagrs):
    g = config.get('GITHUB')
    for issue in g.get_user().get_issues():
        print('{} ({}): {}'.format(issue.number, issue.state, issue.title))

