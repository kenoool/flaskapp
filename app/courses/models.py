from app import mysql

class Courses(object):
    def __init__(self, code=None, name=None, new_code=None, college_code=None):
        self.code = code
        self.name = name
        self.new_code = new_code
        self.college_code = college_code

    @classmethod
    def all(cls, search_term=None):
        try:
            with mysql.connection.cursor() as curs:
                sql = "SELECT code, name, college_code FROM courses"

                if search_term:
                    conditions = [
                        f"code LIKE %s",
                        f"name LIKE %s",
                        f"college_code LIKE %s",
                    ]

                    where_clause = " OR ".join(conditions)
                    sql += f" WHERE {where_clause}"

                    search_pattern = f"%{search_term}%"
                    curs.execute(sql, (search_pattern,) * 3)
                else:
                    curs.execute(sql)

                result = curs.fetchall()

            return [cls(code=row[0], name=row[1], college_code=row[2]) for row in result]

        except Exception as e:
            print(f"Error fetching all courses: {e}")
            return []

    # ... rest of the class


    @classmethod
    def get_by_code(cls, course_code):
        try:
            with mysql.connection.cursor() as curs:
                sql = "SELECT * FROM courses WHERE code = %s"
                curs.execute(sql, (course_code,))
                result = curs.fetchone()
            return cls(*result) if result else None
        except Exception as e:
            # Handle the exception (e.g., log the error)
            print(f"Error fetching course by code: {e}")
            return None

    def add_course(self):
        conn = mysql.connection
        curs = conn.cursor()
        sql = "INSERT INTO courses (code, name, college_code) VALUES (%s, %s, %s)"
        values = (self.code, self.name, self.college_code)
        curs.execute(sql, values)
        conn.commit()

    def update_course(self):
        conn = mysql.connection
        curs = conn.cursor()
        sql = "UPDATE courses SET code=%s, name=%s, college_code=%s WHERE code=%s"
        values = (self.new_code, self.name, self.college_code, self.code)
        curs.execute(sql, values)
        conn.commit()

    def delete_course(self):
        conn = mysql.connection
        curs = conn.cursor()
        sql = "DELETE FROM courses WHERE code=%s"
        curs.execute(sql, (self.code,))
        conn.commit()
