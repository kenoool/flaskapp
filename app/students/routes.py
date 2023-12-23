from flask import render_template, redirect, request, flash, url_for, current_app
from . import students
from app.students.models import Students
from app.students.forms import StudentForm
from app.courses.models import Courses
from app import mysql
from pymysql import IntegrityError
import cloudinary, cloudinary.uploader
from cloudinary.uploader import upload


# rest of the code...


@students.route('/')
def index():
    return redirect(url_for('students.student'))

# ... (previous imports)

@students.route('/students', methods=['GET', 'POST'])
def student():
    form = StudentForm()

    if request.method == 'POST':
        search_term = request.form.get('search')
        students_data = Students.all(search_term)
    else:
        students_data = Students.all()

    return render_template('students/students.html', students=students_data, form=form)

def handle_error(error, duplicate_message='Student with this id already exists.', generic_message='Failed to perform the operation.'):
    if "Duplicate entry" in str(error.args):
        flash(f'Error: {duplicate_message}', 'danger')
    else:
        flash(f'Error: {generic_message}', 'danger')

@students.route("/add_student", methods=['POST', 'GET'])
def add_student():
    form = StudentForm()

    # Set the course choices for the dropdown
    form.set_course_choices()

    if request.method == 'POST':

        if form.image_url.data and not is_image_file(form.image_url.data.filename):
            flash('Error: Only image files (jpg, jpeg, png, svg) are allowed for the photo.', 'danger')
            return render_template('students/add_student.html', form=form)
        # Check file-related conditions before calling validate_on_submit
        if not is_file_size_valid(form.image_url.data):
            flash('Error: File size must be no more than 1 MB.', 'danger')
            return render_template('students/add_student.html', form=form)

        if form.validate_on_submit():
            try:
                image_url = None

                if form.image_url.data:
                    try:
                        # Use cloudinary.uploader.upload directly
                        response = cloudinary.uploader.upload(form.image_url.data, folder="Students")
                        image_url = response['url']
                    except Exception as e:
                        flash(f'Error: Cloudinary upload failed. {e}', 'danger')
                        return render_template('students/add_student.html', form=form)

                student = Students(
                    id=form.id.data,
                    firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    course_code=form.course_code.data,
                    year=form.year.data,
                    gender=form.gender.data,
                    image_url=image_url
                )

                # Call the add_student method without passing the file
                student.add_student()

                flash('Student added successfully', 'success')
                return redirect(url_for('.student'))

            except IntegrityError as e:
                if "Duplicate entry" in str(e.args):
                    flash('Error: Student with this ID already exists. Please choose a different ID.', 'danger')
                else:
                    flash('Error: Failed to add student.', 'danger')

        else:
            flash('Error: Please correct the form errors and try again.', 'danger')
            print(form.errors)

    # Pass an empty student instance to the template
    return render_template('students/add_student.html', form=form)



def is_image_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'svg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def is_file_size_valid(file_field):
    try:
        file_size = len(file_field.read())
        file_field.seek(0)  # Reset file cursor position
        max_size = 1024 * 1024  # 1 MB

        if file_size > max_size:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error checking file size: {e}")
        return False


@students.route("/update_student/<id>", methods=['GET', 'POST'])
def update_student(id):
    student = Students.get_by_id(id)
    form = StudentForm(obj=student)

    # Set the course choices for the dropdown
    form.set_course_choices()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                # Update the student object with the new data
                student.new_id = form.id.data
                student.firstname = form.firstname.data
                student.lastname = form.lastname.data
                student.year = form.year.data
                student.gender = form.gender.data
                student.course_code = form.course_code.data
                student.new_image_url = form.image_url.data  # Use form.image_url.data

                # Check if a new image is provided
                if student.new_image_url:
                    if not is_image_file(student.new_image_url.filename):
                        flash('Error: Only image files (jpg, jpeg, png, svg) are allowed for the photo.', 'danger')
                        return render_template('students/update_student.html', form=form, student=student, id=id)

                    if not is_file_size_valid(student.new_image_url):
                        flash('Error: File size must be no more than 1 MB.', 'danger')
                        return render_template('students/update_student.html', form=form, student=student, id=id)

                    try:
                        # Use cloudinary.uploader.upload directly
                        response = cloudinary.uploader.upload(student.new_image_url, folder="Students")
                        student.new_image_url = response['url']
                    except Exception as e:
                        flash(f'Error: Cloudinary upload failed. {e}', 'danger')
                        return render_template('students/update_student.html', form=form, student=student, id=id)

                # Update student data
                student.update_student()

                flash('Student updated successfully', 'success')
                return redirect(url_for('.student'))

            except IntegrityError as e:
                if "Duplicate entry" in str(e.args):
                    flash('Error: Student with this id already exists.', 'danger')
                else:
                    flash('Error: Failed to update student.', 'danger')
                # Rollback any changes if an integrity error occurs
                mysql.connection.rollback()

        else:
            flash('Error: Please correct the form errors and try again.', 'danger')
            print(form.errors)

    return render_template('students/update_student.html', form=form, student=student, id=id)


@students.route("/delete_student/<string:id>", methods=['POST'])
def delete_student(id):
    student = Students.get_by_id(id)
    try:
        student.delete_student()
        flash('Student deleted successfully', 'success')
    except Exception as e:
        flash('Error: Failed to delete student.', 'danger')
    return redirect(url_for('.student'))