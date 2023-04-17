from pymongo import MongoClient


def __get_database():
    mongodb_url = 'mongodb://flaskuser:fire23@mongodb:27017/flaskdb'
    client = MongoClient(mongodb_url)
    return client['flaskdb']


def add_match(match):
    matches = __get_database()['matches']
    matches.insert_one(match)


def add_driver_feedback(feedback):
    feedbacks = __get_database()['driver_feedback']
    feedbacks.insert_one(feedback)


def find_matches(team):
    all_matches = __get_database()['matches']
    matches = []
    for match in all_matches.find({'team_number': str(team)}):
        matches.append(match)
    return matches


def find_many_matches(teams):
    all_matches = __get_database()['matches']
    matches = {}
    for team in teams:
        matches[team] = []
        for match in all_matches.find({'team_number': str(team)}):
            matches[team].append(match)
    return matches


def find_all_matches():
    all_matches = __get_database()['matches']
    teams = {}
    for match in all_matches.find():
        team = match['team_number']
        if team not in teams:
            teams[team] = []
        teams[team].append(match)
    return teams


def find_feedback(team):
    all_feedback = __get_database()['driver_feedback']
    feedback = []
    for comment in all_feedback.find({'team_number': str(team)}):
        feedback.append(comment)
    return feedback


def calculate_summary(team):
    matches = find_matches(team)
    driver_feedback = find_feedback(team)
    if len(matches) == 0:
        return 0
    summary = {
        'team_number': team,

        'auto_cone_low': __calculate_average(matches, 'auto_cone_low'),
        'auto_cone_mid': __calculate_average(matches, 'auto_cone_mid'),
        'auto_cone_high': __calculate_average(matches, 'auto_cone_high'),
        'auto_cone_average': __calculate_average_multiple(matches,
                                                          ['auto_cone_low', 'auto_cone_mid', 'auto_cone_high']),
        'auto_cube_low': __calculate_average(matches, 'auto_cube_low'),
        'auto_cube_mid': __calculate_average(matches, 'auto_cube_mid'),
        'auto_cube_high': __calculate_average(matches, 'auto_cube_high'),
        'auto_cube_average': __calculate_average_multiple(matches,
                                                          ['auto_cube_low', 'auto_cube_mid', 'auto_cube_high']),
        'auto_mobility': __calculate_proportion(matches, 'auto_mobility'),
        'auto_docked': __calculate_proportion(matches, 'auto_docked'),
        'auto_balanced': __calculate_proportion(matches, 'auto_balanced'),
        'auto_comments': __all_comments(matches, 'auto_comments'),

        'teleop_cone_low': __calculate_average(matches, 'teleop_cone_low'),
        'teleop_cone_mid': __calculate_average(matches, 'teleop_cone_mid'),
        'teleop_cone_high': __calculate_average(matches, 'teleop_cone_high'),
        'teleop_cone_average': __calculate_average_multiple(matches,
                                                            ['teleop_cone_low', 'teleop_cone_mid', 'teleop_cone_high']),
        'teleop_cube_low': __calculate_average(matches, 'teleop_cube_low'),
        'teleop_cube_mid': __calculate_average(matches, 'teleop_cube_mid'),
        'teleop_cube_high': __calculate_average(matches, 'teleop_cube_high'),
        'teleop_cube_average': __calculate_average_multiple(matches,
                                                            ['teleop_cube_low', 'teleop_cube_mid', 'teleop_cube_high']),
        'floor_pickup': __calculate_proportion(matches, 'floor_pickup'),
        'hps_pickup': __calculate_proportion(matches, 'hps_pickup'),
        'summary': __all_comments(matches, 'summary'),
        'analysis': __all_comments(matches, 'analysis'),
        'feedback': __all_comments(driver_feedback, 'feedback')
    }
    return summary


def calculate_short_summaries(teams):
    robot = ['r1', 'r2', 'r3', 'b1', 'b2', 'b3']
    all_matches = find_many_matches(teams)
    summary = {}
    for i in range(6):
        team = teams[i]
        matches = all_matches[team]
        if len(matches) == 0:
            summary[robot[i]] = {
                'team_number': team,
                'auto_cone_average': 0,
                'auto_cube_average': 0,
                'auto_balanced': 0,
                'teleop_cone_average': 0,
                'teleop_cube_average': 0,
                'summary': ["No data yet."]
            }
            continue
        summary[robot[i]] = {
            'team_number': team,
            'auto_cone_average': __calculate_average_multiple(matches,
                                                              ['auto_cone_low', 'auto_cone_mid', 'auto_cone_high']),
            'auto_cube_average': __calculate_average_multiple(matches,
                                                              ['auto_cube_low', 'auto_cube_mid', 'auto_cube_high']),
            'auto_balanced': __calculate_proportion(matches, 'auto_balanced'),
            'teleop_cone_average': __calculate_average_multiple(matches,
                                                                ['teleop_cone_low', 'teleop_cone_mid',
                                                                 'teleop_cone_high']),
            'teleop_cube_average': __calculate_average_multiple(matches,
                                                                ['teleop_cube_low', 'teleop_cube_mid',
                                                                 'teleop_cube_high']),
            'summary': __all_comments(matches, 'summary')
        }
    return summary


def calculate_rankings():
    all_teams = find_all_matches()
    teams = []
    for team in all_teams.values():
        team_number = 0
        auto_points = 0
        teleop_points = 0
        recent_analysis = ""
        for match in team:
            team_number = match['team_number']
            auto_points += (int(match['auto_cone_low']) + int(match['auto_cube_low'])) * 3 + \
                           (int(match['auto_cone_mid']) + int(match['auto_cube_mid'])) * 4 + \
                           (int(match['auto_cone_high']) + int(match['auto_cube_high'])) * 6 + \
                           int(match['auto_mobility']) * 3 + int(match['auto_docked']) * 8 + \
                           int(match['auto_balanced']) * 12
            teleop_points += (int(match['teleop_cone_low']) + int(match['teleop_cube_low'])) * 2 + \
                             (int(match['teleop_cone_mid']) + int(match['teleop_cube_mid'])) * 3 + \
                             (int(match['teleop_cone_high']) + int(match['teleop_cube_high'])) * 5
            recent_analysis = match['analysis']
        teams.append({
            'team_number': team_number,
            'total_points': round((auto_points + teleop_points) / len(team), 1),
            'auto_points': round(auto_points / len(team), 1),
            'teleop_points': round(teleop_points / len(team), 1),
            'recent_analysis': recent_analysis
        })
    teams = sorted(teams, key=lambda d: d['total_points'], reverse=True)
    return teams


def __calculate_average(matches, key):
    total = 0
    for match in matches:
        total += int(match[key])
    return round(total / len(matches), 2)


def __calculate_average_multiple(matches, keys):
    total = 0
    for key in keys:
        for match in matches:
            total += int(match[key])
    return round(total / len(matches), 2)


def __calculate_proportion(matches, key):
    true = 0
    for match in matches:
        if match[key]:
            true += 1
    return "{:.1%}".format(round(true / len(matches), 2))


def __all_comments(matches, key):
    comments = []
    for match in matches:
        if match[key]:
            comments.append("Q" + match["quals_number"] + ": " + match[key])
    return comments
