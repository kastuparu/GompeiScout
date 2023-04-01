from flask import Flask, render_template, request, url_for, redirect
from flask_navigation import Navigation
from forms import MatchForm, SearchForm
import backend
import uuid

app_version = '1.1.0'
app = Flask(__name__)
app.config['SECRET_KEY'] = '1779a432af577b347e5bafd92119971506f90ae7746b93db'
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home', 'home'),
    nav.Item('Match Input', 'match_input'),
    nav.Item('Team Summary Search', 'team_summary_search')
])


@app.route('/')
def root():
    return render_template('home.html', title="Home")


@app.route('/home')
def home():
    return render_template('home.html', title="home")


@app.route('/match_input', methods=['GET', 'POST'])
def match_input():
    if request.method == 'GET':
        return render_template('match_input.html', form=MatchForm(), title="Match Input")
    if request.method == 'POST':
        match_data = set_booleans(request.form.to_dict())
        match_data.update({'_id': str(uuid.uuid4())})
        backend.add_match(match_data)
        return redirect(url_for('match_input'))


@app.route('/team_summary_search', methods=['GET', 'POST'])
def team_summary_search():
    if request.method == 'POST':
        team_number = request.form['team_number']
        return redirect(url_for('team_summary', team_number=team_number))
    return render_template('team_summary_search.html', form=SearchForm(), title="Team Summary Search")


@app.route('/team_summary/<team_number>', methods=['GET'])
def team_summary(team_number):
    data = backend.calculate_summary(team_number)
    if data == 0:
        return redirect(url_for('home'))
    return render_template('team_summary.html', summary=data, title="Summary: " + str(team_number))


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
    app.run(debug=True)
