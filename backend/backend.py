import pymysql
from tkinter import messagebox
from .student_management import *
from .book_management import *
from .empolyee_management import *
from .superadmin_management import *
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





# TODO： add backend functions for Books, Borrowing, Employees, and Admins.
