import sys
import os
import textwrap


def quit(msg: str, status: int):
    print(msg)
    sys.exit(status)

def clear_screen(*args, **kwagrs):
    os.system('cls' if os.name == 'nt' else 'clear')

def perr(msg: str):
    print(msg, file=sys.stderr)

def align_text(text: str, left_margin: int=4, max_width: int=80):
    lines = []
    for line in text.split('\n'):
        tmp_lines = textwrap.wrap(line.strip(), max_width - left_margin)
        tmp_lines = ['{}{}'.format(' ' * left_margin, l) for l in tmp_lines]
        lines.append('\n'.join(tmp_lines))
    ret = '\n'.join(lines)
    return ret

