from flask import render_template, redirect, request, flash, url_for
from . import colleges
from app.colleges.models import Colleges
from app.colleges.forms import CollegeForm
from app import mysql
from pymysql import IntegrityError

@colleges.route('/colleges', methods=['GET', 'POST'])
def college():
    form = CollegeForm()

    if request.method == 'POST':
        search_term = request.form.get('search')
        colleges_data = Colleges.all(search_term)
    else:
        colleges_data = Colleges.all()

    return render_template('colleges/colleges.html', colleges=colleges_data, form=form)



@colleges.route("/add_college", methods=['POST', 'GET'])
def add_college():
    form = CollegeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            college = Colleges(code=form.code.data, name=form.name.data)
            try:
                college.add_college()
                flash('College added successfully', 'success')
                return redirect(url_for('.college'))
            except IntegrityError as e:
                if "Duplicate entry" in str(e.args):
                    flash('Error: College with this code already exists.', 'danger')
                else:
                    flash('Error: Failed to add college.', 'danger')
        else:
            flash('Error: All fields are required.', 'danger')
            print(form.errors)
    return render_template('colleges/add_college.html', form=form)

@colleges.route("/update_college/<code>", methods=['GET', 'POST'])
def update_college(code):
    college = Colleges.get_by_code(code)
    form = CollegeForm(obj=college)
    if request.method == 'POST':
        if form.validate_on_submit():
            college.name = form.name.data
            college.new_code = form.code.data  # Set new_code attribute
            try:
                college.update_college()
                flash('College updated successfully', 'success')
                return redirect(url_for('.college'))
            except IntegrityError as e:
                if "Duplicate entry" in str(e.args):
                    flash('Error: College with this code already exists.', 'danger')
                else:
                    flash('Error: Failed to update college.', 'danger')
        else:
            flash('Error: All fields are required.', 'danger')
            print(form.errors)
    return render_template('colleges/update_college.html', form=form, code=code)



@colleges.route("/delete_college/<string:code>", methods=['POST'])
def delete_college(code):
    college = Colleges.get_by_code(code)
    try:
        college.delete_college()
        flash('College deleted successfully', 'success')
    except Exception as e:
        flash('Error: Failed to delete college.', 'danger')
    return redirect(url_for('.college'))
