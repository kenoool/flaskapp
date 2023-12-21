from flask import Blueprint

students = Blueprint('students', __name__)

from . import routes
# Define any specific configuration for the 'students' Blueprint here
