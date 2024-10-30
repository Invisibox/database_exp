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

def student_update_own_info(student_id, password, new_student_data, new_account_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 验证学生ID和密码
                verify_sql = "SELECT * FROM studentaccount WHERE StudentID = %s AND Password = %s"
                cursor.execute(verify_sql, (student_id, password))
                account = cursor.fetchone()
                
                if account:
                    # 更新学生信息
                    update_student_info_sql = "UPDATE StudentInfo SET "
                    update_student_info_params = []
                    if new_student_data[0] is not None:
                        update_student_info_sql += "Name=%s, "
                        update_student_info_params.append(new_student_data[0])
                    if new_student_data[1] is not None:
                        update_student_info_sql += "Gender=%s, "
                        update_student_info_params.append(new_student_data[1])
                    if new_student_data[2] is not None:
                        update_student_info_sql += "PhoneNumber=%s, "
                        update_student_info_params.append(new_student_data[2])
                    if new_student_data[3] is not None:
                        update_student_info_sql += "IDCardNumber=%s, "
                        update_student_info_params.append(new_student_data[3])
                    if new_student_data[4] is not None:
                        update_student_info_sql += "CampusCode=%s, "
                        update_student_info_params.append(new_student_data[4])
                    if new_student_data[5] is not None:
                        update_student_info_sql += "DateOfBirth=%s, "
                        update_student_info_params.append(new_student_data[5])
                    
                    # 移除最后一个逗号和空格
                    update_student_info_sql = update_student_info_sql.rstrip(', ')
                    update_student_info_sql += " WHERE StudentID=%s"
                    update_student_info_params.append(student_id)
                    
                    if update_student_info_params:
                        cursor.execute(update_student_info_sql, update_student_info_params)
                    
                    # 更新学生账户信息
                    update_student_account_sql = "UPDATE studentaccount SET "
                    update_student_account_params = []
                    if new_account_data[0] is not None:
                        update_student_account_sql += "Password=%s, "
                        update_student_account_params.append(new_account_data[0])
                    if new_account_data[1] is not None:
                        update_student_account_sql += "Email=%s, "
                        update_student_account_params.append(new_account_data[1])
                    
                    # 移除最后一个逗号和空格
                    update_student_account_sql = update_student_account_sql.rstrip(', ')
                    update_student_account_sql += " WHERE StudentID=%s"
                    update_student_account_params.append(student_id)
                    
                    if update_student_account_params:
                        cursor.execute(update_student_account_sql, update_student_account_params)
                    
                    connection.commit()
                    return True
                else:
                    messagebox.showerror("Error", "Invalid student ID or password")
                    return False
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()