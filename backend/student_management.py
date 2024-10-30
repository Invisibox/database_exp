import pymysql
from tkinter import messagebox
from .db_connection import connect_db

# 学生操作
def add_student(student_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO StudentInfo (StudentID, Name, Gender, PhoneNumber, IDCardNumber, CampusCode, DateOfBirth)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, student_data)
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def get_all_students():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM StudentInfo"
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()

def get_student_by_id(student_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM StudentInfo WHERE StudentID = %s"
                cursor.execute(sql, (student_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
        finally:
            connection.close()

def update_student(student_id, student_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE StudentInfo
                    SET Name=%s, Gender=%s, PhoneNumber=%s, IDCardNumber=%s, CampusCode=%s, DateOfBirth=%s
                    WHERE StudentID=%s
                """
                cursor.execute(sql, (*student_data, student_id))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def delete_student(student_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM StudentInfo WHERE StudentID = %s"
                cursor.execute(sql, (student_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()