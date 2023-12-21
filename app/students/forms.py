# app/students/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, validators  # Modify this import
from flask_wtf.file import FileAllowed
from app.courses.models import Courses

class StudentForm(FlaskForm):
    id = StringField('ID', validators=[validators.InputRequired()])
    firstname = StringField('First Name', validators=[validators.InputRequired()])
    lastname = StringField('Last Name', validators=[validators.InputRequired()])
    course_code = SelectField('Course Code', coerce=str, validators=[validators.InputRequired()])
    year = StringField('Year', validators=[validators.InputRequired()])
    gender = StringField('Gender', validators=[validators.InputRequired()])
    image_url = FileField('Choose an Image', validators=[validators.Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'svg'], 'Images only!'),])  # Modify this field name
    new_id = StringField('New ID', validators=[validators.Optional()])

    def set_course_choices(self):
        # Assuming you have a method 'all' in the Courses class to fetch all courses
        course_choices = [(course.code, course.code) for course in Courses.all()]
        self.course_code.choices = [('', '--Select a Course--')] + course_choices
