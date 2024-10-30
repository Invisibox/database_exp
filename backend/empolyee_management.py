import pymysql
from tkinter import messagebox
from .db_connection import connect_db

# 员工操作
def add_employee(employee_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO employeeinfo (EmployeeID, Name, Gender, PhoneNumber, IDCardNumber, Position)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, employee_data)
                
                # 在 employeeaccount 表中添加对应记录
                employee_id = employee_data[0]
                account_sql = """
                    INSERT INTO employeeaccount (EmployeeID, Password, SecurityQuestion, SecurityAnswer)
                    VALUES (%s, %s, %s, %s)
                """
                account_data = (employee_id, '', '', '')  # 默认密码随机，安全问题和答案为空
                cursor.execute(account_sql, account_data)
                
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def get_all_employees():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM employeeinfo"
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()

def get_employee_by_id(employee_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM employeeinfo WHERE EmployeeID = %s"
                cursor.execute(sql, (employee_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
        finally:
            connection.close()

def get_employee_account_by_id(employee_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM employeeaccount WHERE EmployeeID = %s"
                cursor.execute(sql, (employee_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
        finally:
            connection.close()

def update_employee(employee_id, employee_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE employeeinfo
                    SET Name=%s, Gender=%s, PhoneNumber=%s, IDCardNumber=%s, Position=%s
                    WHERE EmployeeID=%s
                """
                cursor.execute(sql, (*employee_data, employee_id))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def delete_employee(employee_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 先删除 employeeaccount 表中的记录
                account_sql = "DELETE FROM employeeaccount WHERE EmployeeID = %s"
                cursor.execute(account_sql, (employee_id,))
                
                # 再删除 employeeinfo 表中的记录
                sql = "DELETE FROM employeeinfo WHERE EmployeeID = %s"
                cursor.execute(sql, (employee_id,))
                
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def update_employee_account(employee_id, account_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE employeeaccount
                    SET Password=%s, SecurityQuestion=%s, SecurityAnswer=%s
                    WHERE EmployeeID=%s
                """
                cursor.execute(sql, (*account_data, employee_id))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()