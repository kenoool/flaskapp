from app import mysql

class StudentModel:
    @staticmethod
    def get_all_students():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM students")
        students_data = cur.fetchall()
        cur.close()
        return students_data

class CourseModel:
    @staticmethod
    def get_all_courses():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM courses")
        courses_data = cur.fetchall()
        cur.close()
        return courses_data


class CollegeModel:
    @staticmethod
    def get_all_colleges():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM colleges")
        colleges_data = cur.fetchall()
        cur.close()
        return colleges_data

