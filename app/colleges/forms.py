# app/colleges/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CollegeForm(FlaskForm):
    code = StringField('Code', validators=[validators.InputRequired()])
    name = StringField('Name', validators=[validators.InputRequired()])
    search = StringField('Search')
