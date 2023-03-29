import json
from pymongo_get_database import get_database


def add_match(match):
    matches = get_database()["matches"]
    matches.insert_one(match)


# TODO: method for getting all matches given a team
# TODO: add indexing for team numbers

if __name__ == "__main__":
    add_match(json.load(open('match_template.json')))
