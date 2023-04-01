from pymongo import MongoClient


def __get_database():
    mongodb_url = "mongodb+srv://kastuparu:S5qbLeQ1dby8DxpJ@cluster0.juawsdp.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(mongodb_url)
    return client["23_wpi_district"]


def add_match(match):
    matches = __get_database()['matches']
    matches.insert_one(match)


def find_matches(team):
    all_matches = __get_database()['matches']
    matches = []
    for match in all_matches.find({'team_number': str(team)}):
        matches.append(match)
    return matches


def calculate_summary(team):
    matches = find_matches(team)
    if len(matches) is 0:
        return 0
    summary = {
        'team_number': team,
        'auto_cone_low': __calculate_average(matches, 'auto_cone_low'),
        'auto_cone_mid': __calculate_average(matches, 'auto_cone_mid'),
        'auto_cone_high': __calculate_average(matches, 'auto_cone_high'),
        'auto_cube_low': __calculate_average(matches, 'auto_cube_low'),
        'auto_cube_mid': __calculate_average(matches, 'auto_cube_mid'),
        'auto_cube_high': __calculate_average(matches, 'auto_cube_high'),
        'auto_mobility': __calculate_proportion(matches, 'auto_mobility'),
        'auto_docked': __calculate_proportion(matches, 'auto_docked'),
        'auto_balanced': __calculate_proportion(matches, 'auto_balanced'),
        'auto_comments': __all_comments(matches, 'auto_comments'),
        'teleop_cone_low': __calculate_average(matches, 'teleop_cone_low'),
        'teleop_cone_mid': __calculate_average(matches, 'teleop_cone_mid'),
        'teleop_cone_high': __calculate_average(matches, 'teleop_cone_high'),
        'teleop_cube_low': __calculate_average(matches, 'teleop_cube_low'),
        'teleop_cube_mid': __calculate_average(matches, 'teleop_cube_mid'),
        'teleop_cube_high': __calculate_average(matches, 'teleop_cube_high'),
        'floor_pickup': __calculate_proportion(matches, 'floor_pickup'),
        'hps_pickup': __calculate_proportion(matches, 'hps_pickup'),
        'analysis': __all_comments(matches, 'analysis')
    }
    return summary


def __calculate_average(matches, key):
    total = 0
    for match in matches:
        total += int(match[key])
    return round(total / len(matches), 2)


def __calculate_proportion(matches, key):
    true = 0
    for match in matches:
        if match[key]:
            true += 1
    return round(true / len(matches), 2)


def __all_comments(matches, key):
    comments = []
    for match in matches:
        if match[key]:
            comments.append(match[key])
    return comments
