import pymysql
from tkinter import messagebox
from .db_connection import connect_db

# 书籍操作
def add_book(book_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO bookinfo (BookID, Title, Author, Publisher, Translator, Category, ArrivalTime, Stock)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, book_data)
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def get_all_books():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM bookinfo"
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()

def get_book_by_id(book_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM bookinfo WHERE BookID = %s"
                cursor.execute(sql, (book_id,))
                result = cursor.fetchone()
                return result
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None
        finally:
            connection.close()

def update_book(book_id, book_data):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE bookinfo
                    SET Title=%s, Author=%s, Publisher=%s, Translator=%s, Category=%s, ArrivalTime=%s, Stock=%s
                    WHERE BookID=%s
                """
                cursor.execute(sql, (*book_data, book_id))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

def delete_book(book_id):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM bookinfo WHERE BookID = %s"
                cursor.execute(sql, (book_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()