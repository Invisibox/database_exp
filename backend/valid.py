from tkinter import messagebox
from .db_connection import connect_db

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
                    return True
                
                return False
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()
    else:
        return False

def validate_student(StudentID, password):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 检查学生账号
                sql = "SELECT * FROM studentaccount WHERE StudentID = %s AND password = %s"
                cursor.execute(sql, (StudentID, password))
                result = cursor.fetchone()
                if result:
                    return True
                
                return False
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()
    else:
        return False