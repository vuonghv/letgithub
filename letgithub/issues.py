from github import UnknownObjectException
from config import config as c
from utils import perr
from colors import color, default, color_256, get_contrast
from colortrans import rgb2short


def color_field(field_name, value):
    return color(c['THEME']['ISSUE'][field_name])(value)

def my_issues(*args, **kwagrs):
    g = c.get('GITHUB')
    for issue in g.get_user().get_issues():
        state_icon = u'\U0001F3C3'
        if issue.state == 'open':
            state = color_field('state_open', state_icon)
        elif issue.state == 'closed':
            state = color_field('state_closed', state_icon)
        else:
            state = default(state_icon)

        repos = color_field('repos', issue.repository.full_name)
        title = color_field('title', issue.title)
        if int(issue.comments) > 0:
            comments = color_field('comments',
                                '{} {}'.format(u'\U0001F4AC', issue.comments))
        else:
            comments = ''
        number = color_field('number', '#{}'.format(issue.number))
        created = color_field('created', issue.created_at)
        user = color_field('user', issue.user.login)

        list_labels = []
        for l in issue.labels:
            term_color = rgb2short(l.color)[0]
            text_color = get_contrast(l.color)
            label = color_256(term_color, bg=True)(text_color(l.name))
            list_labels.append(label)
        labels = ' '.join(list_labels)

        template = ('{state} {repos} {title} {labels}  {comments}\n'
                    '  {number} opened {created} by {user}')
        info = template.format(state=state, repos=repos, title=title,
                                comments=comments, number=number,
                                created=created, user=user, labels=labels)
        print(info, '\n')

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
        g = c.get('GITHUB')
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
        for cmt in issue.get_comments():
            print('{user} {updated}'.format(
                  user=cmt.user.login, updated=cmt.updated_at))
            print('\t{body}'.format(body=cmt.body))
    except KeyError as err:
        perr(err)
    except UnknownObjectException:
        perr('Issue {}/{}/{} not found!'.format(username, repos, number))

def view_list_issues(username: str, repos: str):
    try:
        g = c.get('GITHUB')
        issues = g.get_user(username).get_repo(repos).get_issues()
        for issue in issues:
            state_icon = u'\U0001F3C3'
            if issue.state == 'open':
                state = color_field('state_open', state_icon)
            elif issue.state == 'closed':
                state = color_field('state_closed', state_icon)
            else:
                state = default(state_icon)

            title = color_field('title', issue.title)
            if int(issue.comments) > 0:
                comments = color_field('comments',
                                    '{} {}'.format(u'\U0001F4AC', issue.comments))
            else:
                comments = ''
            number = color_field('number', '#{}'.format(issue.number))
            created = color_field('created', issue.created_at)
            user = color_field('user', issue.user.login)
            if issue.assignee:
                assignee = '{} {}'.format(u'\U0001F647', issue.assignee.login)
                assignee = color_field('assignee', assignee)
            else:
                assignee = ''

            list_labels = []
            for l in issue.labels:
                term_color = rgb2short(l.color)[0]
                text_color = get_contrast(l.color)
                label = color_256(term_color, bg=True)(text_color(l.name))
                list_labels.append(label)
            labels = ' '.join(list_labels)

            template = ('{state} {title} {labels}  {assignee}  {comments}\n'
                        '  {number} opened {created} by {user}')
            info = template.format(state=state, title=title, labels=labels,
                                    comments=comments, number=number,
                                    created=created, user=user,
                                    assignee=assignee)
            print(info, '\n')
    except KeyError as err:
        print(err)
    except UnknownObjectException:
        print('Can\'t get issues for {}/{}'.format(username, repos))

