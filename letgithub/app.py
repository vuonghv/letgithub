import sys
import os

import utils
import repos
import users
import issues
from config import config, load_config


COMMANDS = {
    'whois': users.show_user,
    'whoami': users.show_user,
    'login': users.login,
    'repos': repos.display_repos,
    'issue': None,
    'mi': issues.my_issues,
    'c': utils.clear_screen,
    'q': utils.quit
}

EXIT_SUCCESS = 0
EXIT_FAILED = -1

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    default_conf_file = os.path.join(current_dir, 'config.json')
    load_config(default_conf_file)
    users.authenticate_user()
    while True:
        try:
            data = input(config.get('PROMT_MSG')).strip()
        except EOFError:
            print()
            continue
        except KeyboardInterrupt:
            sys.exit('\nGoodbye, see you. :)')
        except Exception:
            continue

        if data == 'q':
            utils.quit('Bye, see you. :)', EXIT_SUCCESS)

        try:
            args = data.split()
            cmd = args[0]
            COMMANDS[cmd](*args[1:])
        except (KeyError, ValueError):
            print('Command `{}` not found!'.format(data))
        except (IndexError, KeyboardInterrupt):
            pass
        except TypeError:
            print('Sorry, I can\'t understand.')
        except Exception as err:
            print(err)

if __name__ == '__main__':
    main()

