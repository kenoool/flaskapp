from app import mysql

class Colleges(object):
    def __init__(self, code=None, name=None, new_code=None):
        self.code = code
        self.name = name
        self.new_code = new_code


    @classmethod
    def all(cls, search_term=None):
        try:
            with mysql.connection.cursor() as curs:
                sql = "SELECT code, name FROM colleges"

                if search_term:
                    conditions = [
                        f"code LIKE %s",
                        f"name LIKE %s",
                    ]

                    where_clause = " OR ".join(conditions)
                    sql += f" WHERE {where_clause}"

                    search_pattern = f"%{search_term}%"
                    curs.execute(sql, (search_pattern, search_pattern))
                else:
                    curs.execute(sql)

                result = curs.fetchall()

            return [cls(code=row[0], name=row[1]) for row in result]

        except Exception as e:
            print(f"Error fetching all colleges: {e}")
            return []


    @classmethod
    def get_by_code(cls, college_code):
        try:
            with mysql.connection.cursor() as curs:
                sql = "SELECT * FROM colleges WHERE code = %s"
                curs.execute(sql, (college_code,))
                result = curs.fetchone()
            return cls(*result) if result else None
        except Exception as e:
            # Handle the exception (e.g., log the error)
            print(f"Error fetching college by code: {e}")
            return None

    def add_college(self):
        conn = mysql.connection
        curs = conn.cursor()
        sql = "INSERT INTO colleges (code, name) VALUES (%s, %s)"
        values = (self.code, self.name)
        curs.execute(sql, values)
        conn.commit()

    def update_college(self):
        conn = mysql.connection
        curs = conn.cursor()
        sql = "UPDATE colleges SET name=%s, code=%s WHERE code=%s"
        values = (self.name, self.new_code, self.code)
        curs.execute(sql, values)
        conn.commit()


    def delete_college(self):
        conn = mysql.connection
        curs = conn.cursor()
        sql = "DELETE FROM colleges WHERE code=%s"
        curs.execute(sql, (self.code,))
        conn.commit()

