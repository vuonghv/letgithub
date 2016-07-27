import json

from github import Github
from utils import perr

config = {}

def load_config(filename: str):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        perr(e)

