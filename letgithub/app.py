import sys
import utils
import repos
import users
from core import config


COMMANDS = {
    'whois': users.get_user,
    'whoami': users.get_user,
    'login': users.login,
    'repos': repos.display_repos,
    'issue': None,
    'c': utils.clear_screen,
    'q': utils.quit
}

EXIT_SUCCESS = 0
EXIT_FAILED = -1

if __name__ == '__main__':
    while True:
        try:
            data = input(config.get('promt_msg')).strip()
        except EOFError:
            print()
            continue
        except KeyboardInterrupt:
            sys.exit('\nGoodby, see you!')
        except Exception:
            continue

        if data == 'q':
            utils.quit('Bye, see you!', EXIT_SUCCESS)

        try:
            args = data.split()
            cmd = args[0]
            COMMANDS[cmd](*args[1:])
        except (KeyError, ValueError):
            print('Command `{}` not found!'.format(data))
        except IndexError:
            pass
        except KeyboardInterrupt:
            pass
        except TypeError:
            print('Sorry, I can\'t understand.')
        except Exception as err:
            print(err)

