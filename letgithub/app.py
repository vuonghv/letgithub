import sys
import os
import readline

import utils
import repos
import users
import issues
from config import config, load_config
from colors import cyan, magenta, red, yellow, color


COMMANDS = {
    'whois': users.show_user,
    'whoami': users.show_user,
    'login': users.login,
    'repos': repos.display_repos,
    'issue': issues.view_issue,
    'mi': issues.my_issues,
    'c': utils.clear_screen,
    'q': utils.quit
}

EXIT_SUCCESS = 0
EXIT_FAILED = -1

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_conf_file = os.path.join(current_dir, 'config.json')
    theme_file = os.path.join(current_dir, 'themes', 'dracula.json')
    obj = load_config(default_conf_file)
    config.update(obj)
    theme = load_config(theme_file)
    config.update({'THEME': theme})
    users.authenticate_user()
    while True:
        try:
            promt = color(config['THEME']['PROMT'])(config['PROMT_MSG'])
            data = input(promt).strip()
        except EOFError:
            print()
            continue
        except KeyboardInterrupt:
            sys.exit(yellow('\nGoodbye, see you. :)'))
        except Exception:
            continue

        if data == 'q':
            utils.quit(yellow('Bye, see you. :)'), EXIT_SUCCESS)

        try:
            args = data.split()
            cmd = args[0]
            COMMANDS[cmd](*args[1:])
        except (KeyError, ValueError):
            print(red('Command `{}` not found!'.format(data)))
        except (IndexError, KeyboardInterrupt):
            pass
        except TypeError:
            print(red('Sorry, I can\'t understand.'))
        except Exception as err:
            utils.perr(red(err))

if __name__ == '__main__':
    main()

