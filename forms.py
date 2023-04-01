from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import InputRequired, NumberRange


class MatchForm(FlaskForm):
    quals_number = IntegerField("Qualification Match #", validators=[InputRequired(), NumberRange(min=1, max=100)])
    scouter_name = StringField("Scouter Name", validators=[InputRequired()])
    team_number = IntegerField("Team #", validators=[InputRequired(), NumberRange(min=1, max=1000)])

    auto_cone_low = IntegerField("Cone Low", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cone_mid = IntegerField("Cone Mid", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cone_high = IntegerField("Cone High", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cube_low = IntegerField("Cube Low", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cube_mid = IntegerField("Cube Mid", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_cube_high = IntegerField("Cube High", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    auto_mobility = BooleanField("Mobility?", default=False)
    auto_docked = BooleanField("Docked?", default=False)
    auto_balanced = BooleanField("Docked and Engaged?", default=False)
    auto_comments = TextAreaField("Comments")

    teleop_cone_low = IntegerField("Cone Low", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cone_mid = IntegerField("Cone Mid", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cone_high = IntegerField("Cone High", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cube_low = IntegerField("Cube Low", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cube_mid = IntegerField("Cube Mid", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    teleop_cube_high = IntegerField("Cube High", default=0, validators=[InputRequired(), NumberRange(min=0, max=9)])
    floor_pickup = BooleanField("Floor Pickup?", default=False)
    hps_pickup = BooleanField("Human Player Station Pickup?", default=False)

    analysis = TextAreaField("Focus on the following questions when providing your analysis.")
