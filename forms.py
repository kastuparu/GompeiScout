from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import InputRequired, NumberRange, Length


class MatchForm(FlaskForm):
    quals_number = IntegerField("Match #", validators=[InputRequired(), NumberRange(min=1, max=100)])
    scouter_name = StringField("Scouter Name", validators=[InputRequired()])
    team_number = IntegerField("Team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])

    auto_cone_low = IntegerField("Cone Low", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cone_mid = IntegerField("Cone Mid", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cone_high = IntegerField("Cone High", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cube_low = IntegerField("Cube Low", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cube_mid = IntegerField("Cube Mid", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cube_high = IntegerField("Cube High", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_mobility = BooleanField("Mobility?", default=False)
    auto_docked = BooleanField("Docked?", default=False)
    auto_balanced = BooleanField("Docked and Engaged?", default=False)
    auto_comments = TextAreaField("Auto Comments")

    teleop_cone_low = IntegerField("Cone Low", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cone_mid = IntegerField("Cone Mid", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cone_high = IntegerField("Cone High", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cube_low = IntegerField("Cube Low", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cube_mid = IntegerField("Cube Mid", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cube_high = IntegerField("Cube High", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    floor_pickup = BooleanField("Floor Pickup?", default=False)
    hps_pickup = BooleanField("Human Player Station Pickup?", default=False)

    summary = TextAreaField("Summarize the team/robot in a few words.", validators=[Length(max=150)])
    analysis = TextAreaField("Focus on the following questions when providing your analysis.")


class DriverForm(FlaskForm):
    quals_number = IntegerField("Match #", validators=[InputRequired(), NumberRange(min=1, max=100)])
    team_number = IntegerField("Team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])
    feedback = TextAreaField("How successful was communication with this team?")


class SearchForm(FlaskForm):
    team_number = IntegerField("Enter team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])


class AllianceForm(FlaskForm):
    red_1 = IntegerField("Red 1 team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])
    red_2 = IntegerField("Red 2 team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])
    red_3 = IntegerField("Red 3 team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])
    blue_1 = IntegerField("Blue 1 team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])
    blue_2 = IntegerField("Blue 2 team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])
    blue_3 = IntegerField("Blue 3 team #", validators=[InputRequired(), NumberRange(min=1, max=10000)])
