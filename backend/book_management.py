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

def count_books_by_category():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT Category, COUNT(*) as count
                    FROM bookinfo
                    GROUP BY Category
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()

# 创建视图
def create_views():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 视图1：显示所有书籍的详细信息
                sql1 = """
                    CREATE OR REPLACE VIEW view_all_books AS
                    SELECT * FROM bookinfo
                """
                cursor.execute(sql1)

                # 视图2：显示每个类别的书籍数量
                sql2 = """
                    CREATE OR REPLACE VIEW view_books_count_by_category AS
                    SELECT Category, COUNT(*) as count
                    FROM bookinfo
                    GROUP BY Category
                """
                cursor.execute(sql2)

            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()

# 为常用属性建立索引
def create_indexes():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 在 Title 字段上建立索引
                sql1 = "CREATE INDEX idx_title ON bookinfo (Title)"
                cursor.execute(sql1)

                # 在 Author 字段上建立索引
                sql2 = "CREATE INDEX idx_author ON bookinfo (Author)"
                cursor.execute(sql2)

                # 在 Category 字段上建立索引
                sql3 = "CREATE INDEX idx_category ON bookinfo (Category)"
                cursor.execute(sql3)

            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()