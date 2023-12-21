# app/courses/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from app.colleges.models import Colleges

class CourseForm(FlaskForm):
    code = StringField('Code', validators=[validators.InputRequired()])
    name = StringField('Name', validators=[validators.InputRequired()])
    college_code = SelectField('College Code', coerce=str, validators=[validators.InputRequired()])
    new_code = StringField('New Code', validators=[validators.Optional()])

    def set_college_choices(self):
        # Assuming you have a method 'all' in the Colleges class to fetch all colleges
        college_choices = [(college.code, college.code) for college in Colleges.all()]
        self.college_code.choices = [('', '--Select a College--')] + college_choices
