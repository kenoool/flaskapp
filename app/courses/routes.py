from flask import render_template, redirect, request, flash, url_for
from . import courses
from app.courses.models import Courses
from app.courses.forms import CourseForm
from app.colleges.models import Colleges
from app import mysql
from pymysql import IntegrityError

@courses.route('/courses', methods=['GET', 'POST'])
def course():
    form = CourseForm()

    if request.method == 'POST':
        search_term = request.form.get('search')
        courses_data = Courses.all(search_term)
    else:
        courses_data = Courses.all()

    return render_template('courses/courses.html', courses=courses_data, form=form)


@courses.route("/add_course", methods=['POST', 'GET'])
def add_course():
    form = CourseForm()

    # Set the college choices for the dropdown
    form.set_college_choices()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Use form.college_code.data to get the selected college code
            course = Courses(code=form.code.data, name=form.name.data, college_code=form.college_code.data)
            try:
                course.add_course()
                flash('Course added successfully', 'success')
                return redirect(url_for('.course'))
            except IntegrityError as e:
                if "Duplicate entry" in str(e.args):
                    flash('Error: Course with this code already exists.', 'danger')
                else:
                    flash('Error: Failed to add course.', 'danger')
        else:
            flash('Error: All fields are required.', 'danger')
            print(form.errors)
    return render_template('courses/add_course.html', form=form)

@courses.route("/update_course/<code>", methods=['GET', 'POST'])
def update_course(code):
    course = Courses.get_by_code(code)
    form = CourseForm(obj=course)

    # Set the college choices for the dropdown
    form.set_college_choices()

    if request.method == 'POST':
        if form.validate_on_submit():
            course.name = form.name.data
            course.new_code = form.code.data  # Set new_code attribute
            course.college_code = form.college_code.data  # Set college_code attribute
            try:
                course.update_course()
                flash('Course updated successfully', 'success')
                return redirect(url_for('.course'))
            except IntegrityError as e:
                if "Duplicate entry" in str(e.args):
                    flash('Error: Course with this code already exists.', 'danger')
                else:
                    flash('Error: Failed to update course.', 'danger')
        else:
            flash('Error: All fields are required.', 'danger')
            print(form.errors)
    return render_template('courses/update_course.html', form=form, code=code)

@courses.route("/delete_course/<string:code>", methods=['POST'])
def delete_course(code):
    course = Courses.get_by_code(code)
    try:
        course.delete_course()
        flash('College deleted successfully', 'success')
    except Exception as e:
        flash('Error: Failed to delete course.', 'danger')
    return redirect(url_for('.course'))
