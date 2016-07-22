from github import Github
import json

config = {}

def load_config(filename: str=None):
    try:
        with open(filename, 'r') as f:
            config.update(json.load(f))
    except FileNotFoundError as err:
        print(err)

