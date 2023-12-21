from flask import Blueprint

courses = Blueprint('courses', __name__)

from . import routes

# Define any specific configuration for the 'courses' Blueprint here
