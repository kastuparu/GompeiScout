import os
from flask import Flask, render_template, request, url_for, redirect
from flask_navigation import Navigation
from forms import MatchForm, DriverForm, SearchForm, AllianceForm
import backend

app_version = '1.1.0'
app = Flask(__name__)
app.config['SECRET_KEY'] = '1779a432af577b347e5bafd92119971506f90ae7746b93db'
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Match Input', 'match_input'),
    nav.Item('Driver Input', 'driver_input'),
    nav.Item('Data Search', 'team_summary_search'),
    nav.Item('Alliance Search', 'alliance_summary_search'),
    nav.Item('Rankings', 'rankings')
])


@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title="Home")


@app.route('/match_input', methods=['GET', 'POST'])
def match_input():
    if request.method == 'GET':
        return render_template('match_input.html', form=MatchForm(), title="Match Input")
    if request.method == 'POST':
        match_data = set_booleans(request.form.to_dict())
        backend.add_match(match_data)
        return redirect(url_for('match_input'))


@app.route('/driver_input', methods=['GET', 'POST'])
def driver_input():
    if request.method == 'GET':
        return render_template('driver_input.html', form=DriverForm(), title="Driver Input")
    if request.method == 'POST':
        backend.add_driver_feedback(request.form.to_dict())
        return redirect(url_for('driver_input'))


@app.route('/team_summary_search', methods=['GET', 'POST'])
def team_summary_search():
    if request.method == 'POST':
        team_number = request.form['team_number']
        return redirect(url_for('team_summary', team_number=team_number))
    return render_template('team_summary_search.html', form=SearchForm(), title="Data Search")


@app.route('/team_summary/<team_number>', methods=['GET'])
def team_summary(team_number):
    data = backend.calculate_summary(team_number)
    if data == 0:
        return redirect(url_for('index'))
    return render_template('team_summary.html', summary=data, title="Data: FRC " + str(team_number))


@app.route('/alliance_summary_search', methods=['GET', 'POST'])
def alliance_summary_search():
    if request.method == 'POST':
        team_numbers = request.form.to_dict()
        return redirect(url_for('alliance_summary', r1=team_numbers['red_1'], r2=team_numbers['red_2'],
                                r3=team_numbers['red_3'], b1=team_numbers['blue_1'], b2=team_numbers['blue_2'],
                                b3=team_numbers['blue_3']))
    return render_template('alliance_summary_search.html', form=AllianceForm(), title="Alliance Search")


@app.route('/alliance_summary/<r1>_<r2>_<r3>_<b1>_<b2>_<b3>', methods=['GET'])
def alliance_summary(r1, r2, r3, b1, b2, b3):
    data = backend.calculate_short_summaries([r1, r2, r3, b1, b2, b3])
    return render_template('alliance_summary.html', summary=data, title="Upcoming Match Data")


@app.route('/rankings', methods=['GET'])
def rankings():
    team_rankings = backend.calculate_rankings()
    return render_template('rankings.html', rankings=team_rankings, title="Rankings")


def set_booleans(match_data):
    if 'auto_mobility' in match_data:
        match_data.update({'auto_mobility': True})
    else:
        match_data.update({'auto_mobility': False})
    if 'auto_docked' in match_data:
        match_data.update({'auto_docked': True})
    else:
        match_data.update({'auto_docked': False})
    if 'auto_balanced' in match_data:
        match_data.update({'auto_balanced': True})
    else:
        match_data.update({'auto_balanced': False})
    if 'floor_pickup' in match_data:
        match_data.update({'floor_pickup': True})
    else:
        match_data.update({'floor_pickup': False})
    if 'hps_pickup' in match_data:
        match_data.update({'hps_pickup': True})
    else:
        match_data.update({'hps_pickup': False})
    return match_data


if __name__ == '__main__':
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("APP_PORT", 5000)
    app.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)
