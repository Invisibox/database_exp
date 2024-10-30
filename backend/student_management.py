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
                
                # 在 studentaccount 表中添加对应记录
                student_id = student_data[0]
                account_sql = """
                    INSERT INTO studentaccount (StudentID, Password, SecurityQuestion, SecurityAnswer, RemainingAttempts)
                    VALUES (%s, %s, %s, %s, %s)
                """
                account_data = (student_id, '', '', '', 3)  # 默认密码随机，安全问题和答案为空，剩余尝试次数为3
                cursor.execute(account_sql, account_data)
                
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

def get_student_account_by_id(student_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM studentaccount WHERE StudentID = %s"
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
                # 先删除 studentaccount 表中的记录
                account_sql = "DELETE FROM studentaccount WHERE StudentID = %s"
                cursor.execute(account_sql, (student_id,))
                
                # 再删除 StudentInfo 表中的记录
                sql = "DELETE FROM StudentInfo WHERE StudentID = %s"
                cursor.execute(sql, (student_id,))
                
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def update_student_account(student_id, account_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE studentaccount
                    SET Password=%s, SecurityQuestion=%s, SecurityAnswer=%s, RemainingAttempts=%s
                    WHERE StudentID=%s
                """
                cursor.execute(sql, (*account_data, student_id))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def update_student_account(student_id, account_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE studentaccount
                    SET Password=%s, SecurityQuestion=%s, SecurityAnswer=%s, RemainingAttempts=%s
                    WHERE StudentID=%s
                """
                cursor.execute(sql, (*account_data, student_id))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()