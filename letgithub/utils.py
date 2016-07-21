import sys
import os


def quit(msg: str, status: int):
    print(msg)
    sys.exit(status)

def clear_screen(*args, **kwagrs):
    os.system('cls' if os.name == 'nt' else 'clear')
