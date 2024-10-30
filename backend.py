import pymysql
from tkinter import messagebox

# Database connection parameters
db_host = 'localhost'
db_user = 'root'
db_password = '123456'  # Replace with your MySQL root password
db_name = 'lib'

def connect_db():
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

def validate_user(AdminID, password):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 检查 superadmin 账号
                sql = "SELECT * FROM superadminaccount WHERE AdminID = %s AND password = %s"
                cursor.execute(sql, (AdminID, password))
                result = cursor.fetchone()
                if result:
                    return "superadmin"
                
                # 检查 admin 账号
                sql = "SELECT * FROM adminaccount WHERE AdminID = %s AND password = %s"
                cursor.execute(sql, (AdminID, password))
                result = cursor.fetchone()
                if result:
                    return "admin"
                
                return None
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
        finally:
            connection.close()
    else:
        return None

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

# Similarly, you can add backend functions for Books, Borrowing, Employees, and Admins.
