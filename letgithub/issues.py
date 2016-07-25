from config import config
from github import UnknownObjectException


def my_issues(*args, **kwagrs):
    g = config.get('GITHUB')
    for issue in g.get_user().get_issues():
        print('{} ({}): {}'.format(issue.number, issue.state, issue.title))

def view_issue(data: str, *args, **kwargs):
    try:
        param = data.split('/')
        if len(param) == 3:
            view_detail_issue(param[0], param[1], int(param[2]))
        else:
            view_list_issues(param[0], param[1])
    except IndexError:
        print('Useage: `issue username/repos/[number]`')

def view_detail_issue(username: str, repos: str, number: int):
    try:
        g = config.get('GITHUB')
        issue = g.get_user(username).get_repo(repos).get_issue(number)
        print('#{number} ({state}) {title} {comments} comments'.format(
              number=issue.number,
              state=issue.state,
              title=issue.title,
              comments=issue.comments))
        assignee = issue.assignee.login if issue.assignee else ''
        print('user: {}\tassignee: {}\tcreated: {}'.format(
              issue.user.login, assignee, issue.created_at))
        print('--- {body}'.format(body=issue.body))

        print('{}comments{}'.format('_'*8, '_'*8))
        for c in issue.get_comments():
            print('{user} {updated}'.format(
                  user=c.user.login, updated=c.updated_at))
            print('\t{body}'.format(body=c.body))
    except KeyError as err:
        print(err)
    except UnknownObjectException:
        print('Issue {}/{}/{} not found!'.format(username, repos, number))

def view_list_issues(username: str, repos: str):
    try:
        g = config.get('GITHUB')
        issues = g.get_user(username).get_repo(repos).get_issues()
        for i in issues:
            print('#{number} ({state}) {title}'.format(
                  number=i.number, state=i.state, title=i.title))
            print('-- {created}\t{comments} comments'.format(
                  created=i.created_at, comments=i.comments))
    except KeyError as err:
        print(err)
    except UnknownObjectException:
        print('Can\'t get issues for {}/{}'.format(username, repos))

