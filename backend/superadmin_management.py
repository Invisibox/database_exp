from tkinter import messagebox
from .db_connection import connect_db

# 超级管理员操作
def add_superadmin(admin_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO superadmininfo (AdminID, Name, Gender, PhoneNumber, IDCardNumber, Email)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, admin_data)
                
                # 在 superadminaccount 表中添加对应记录
                admin_id = admin_data[0]
                account_sql = """
                    INSERT INTO superadminaccount (AdminID, Password, SecurityQuestion, SecurityAnswer)
                    VALUES (%s, %s, %s, %s)
                """
                account_data = (admin_id, '', '', '')  # 默认密码随机，安全问题和答案为空
                cursor.execute(account_sql, account_data)
                
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def get_all_superadmins():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM superadmininfo"
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()

def get_superadmin_by_id(admin_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM superadmininfo WHERE AdminID = %s"
                cursor.execute(sql, (admin_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
        finally:
            connection.close()

def get_superadmin_account_by_id(admin_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM superadminaccount WHERE AdminID = %s"
                cursor.execute(sql, (admin_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
        finally:
            connection.close()

def update_superadmin(admin_id, admin_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE superadmininfo
                    SET Name=%s, Gender=%s, PhoneNumber=%s, IDCardNumber=%s, Email=%s
                    WHERE AdminID=%s
                """
                cursor.execute(sql, (*admin_data, admin_id))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def delete_superadmin(admin_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 先删除 superadminaccount 表中的记录
                account_sql = "DELETE FROM superadminaccount WHERE AdminID = %s"
                cursor.execute(account_sql, (admin_id,))
                
                # 再删除 superadmininfo 表中的记录
                sql = "DELETE FROM superadmininfo WHERE AdminID = %s"
                cursor.execute(sql, (admin_id,))
                
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def update_superadmin_account(admin_id, account_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE superadminaccount
                    SET Password=%s, SecurityQuestion=%s, SecurityAnswer=%s
                    WHERE AdminID=%s
                """
                cursor.execute(sql, (*account_data, admin_id))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()