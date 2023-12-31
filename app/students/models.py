import cloudinary.uploader
from flask import current_app, request
from app import mysql
from werkzeug.utils import secure_filename
import os
import logging
# Configure logging in your Flask app
logging.basicConfig(level=logging.DEBUG)


class Students(object):
    def __init__(self, id=None, firstname=None, lastname=None, course_code=None, year=None, gender=None, new_id=None, image_url=None, new_image_url=None, college_name=None):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.course_code = course_code
        self.year = year
        self.gender = gender
        self.new_id = new_id
        self.image_url = image_url
        self.new_image_url = new_image_url
        self.college_name = college_name


    @classmethod
    def all(cls, search_term=None):
        try:
            with mysql.connection.cursor() as curs:
                sql = """
                    SELECT 
                        s.id, 
                        s.firstname, 
                        s.lastname, 
                        s.course_code, 
                        s.year, 
                        s.gender, 
                        s.image_url, 
                        c.college_code,
                        co.name AS college_name  -- Alias for college name
                    FROM students s
                    LEFT JOIN courses c ON s.course_code = c.code
                    LEFT JOIN colleges co ON c.college_code = co.code  -- Join with colleges table to get college name
                """

                if search_term:
                    conditions = [
                        f"s.id LIKE %s",
                        f"s.firstname LIKE %s",
                        f"s.lastname LIKE %s",
                        f"s.course_code LIKE %s",
                        f"s.year LIKE %s",
                        f"s.gender LIKE %s",
                        f"c.college_code LIKE %s",  # Add condition for college code
                        f"co.name LIKE %s",  # Add condition for college name
                    ]

                    where_clause = " OR ".join(conditions)
                    sql += f" WHERE {where_clause}"

                    search_pattern = f"%{search_term}%"
                    # Add wildcards to search for partial matches in string columns
                    curs.execute(sql, (search_pattern,) * 8)
                else:
                    curs.execute(sql)

                result = curs.fetchall()

            students_data = []
            for row in result:
                student = cls(
                    id=row[0],
                    firstname=row[1],
                    lastname=row[2],
                    course_code=row[3],
                    year=row[4],
                    gender=row[5],
                    image_url=row[6]
                )
                student.college_code = row[7]  # Assign college code from the result
                student.college_name = row[8]  # Assign college name from the result
                students_data.append(student)

            return students_data

        except Exception as e:
            print(f"Error fetching all students: {e}")
            return []


            
    @classmethod
    def get_by_id(cls, student_id):
        try:
            with mysql.connection.cursor() as curs:
                sql = "SELECT id, firstname, lastname, course_code, year, gender, image_url FROM students WHERE id = %s"
                curs.execute(sql, (student_id,))
                result = curs.fetchone()

            if result:
                return cls(id=result[0], firstname=result[1], lastname=result[2], course_code=result[3], year=result[4], gender=result[5], image_url=result[6])
            else:
                return None

        except Exception as e:
            print(f"Error fetching student by ID: {e}")
            return None
        
    def add_student(self):
        conn = mysql.connection
        curs = conn.cursor()
        sql = "INSERT INTO students (image_url, id, firstname, lastname, course_code, year, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.image_url, self.id, self.firstname, self.lastname, self.course_code, self.year, self.gender)

        try:
            curs.execute(sql, values)
            conn.commit()
        except Exception as e:
            print(f"Error adding student: {e}")
            conn.rollback()

    def update_student(self):
        conn = mysql.connection
        curs = conn.cursor()

        # Check if a new image file is provided
        if self.new_image_url is not None:
            try:
                # Use cloudinary.uploader.upload directly
                response = cloudinary.uploader.upload(self.new_image_url, folder="Students")
                self.image_url = response['url']
            except Exception as e:
                print(f"Error: Cloudinary upload failed. {e}")

        # Update the student data in the database
        sql = "UPDATE students SET image_url=%s, id=%s, firstname=%s, lastname=%s, course_code=%s, year=%s, gender=%s WHERE id=%s"
        values = (self.image_url, self.new_id, self.firstname, self.lastname, self.course_code, self.year, self.gender, self.id)

        curs.execute(sql, values)
        conn.commit()



    def delete_student(self):
        conn = mysql.connection
        curs = conn.cursor()
        sql = "DELETE FROM students WHERE id=%s"
        curs.execute(sql, (self.id,))
        conn.commit()

    @classmethod
    def get_college_code_by_course_code(cls, course_code):
        try:
            with mysql.connection.cursor() as curs:
                # Assuming there is a column named 'college_code' in the 'courses' table
                sql = "SELECT college_code FROM courses WHERE code = %s"
                curs.execute(sql, (course_code,))
                result = curs.fetchone()

            if result:
                return result[0]
            else:
                return None

        except Exception as e:
            print(f"Error fetching college code by course code: {e}")
            return None

