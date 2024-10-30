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

def search_books(book_id=None, title=None, author=None, category=None):
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM bookinfo WHERE 1=1"
                params = []

                if book_id:
                    sql += " AND BookID = %s"
                    params.append(book_id)
                if title:
                    sql += " AND Title LIKE %s"
                    params.append(f"%{title}%")
                if author:
                    sql += " AND Author LIKE %s"
                    params.append(f"%{author}%")
                if category:
                    sql += " AND Category LIKE %s"
                    params.append(f"%{category}%")

                cursor.execute(sql, params)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()

def list_books_by_category():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 获取所有分类
                cursor.execute("SELECT DISTINCT Category FROM bookinfo")
                categories = cursor.fetchall()

                books_by_category = {}
                for category in categories:
                    category_name = category['Category']
                    cursor.execute("SELECT * FROM bookinfo WHERE Category = %s", (category_name,))
                    books = cursor.fetchall()
                    books_by_category[category_name] = books

                return books_by_category
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return {}
        finally:
            connection.close()
