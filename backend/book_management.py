import pymysql
from tkinter import messagebox
from .db_connection import connect_db
from .valid import validate_student

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
                sql = "SELECT * FROM view_all_books"
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()

def get_books_by_category():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM view_books_by_category"
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()

def get_books_by_author():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM view_books_by_author"
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

def borrow_book(student_id, password, book_id):
    if not validate_student(student_id, password):
        messagebox.showerror("Error", "学生身份验证失败")
        return False

    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 检查书籍库存
                cursor.execute("SELECT Stock FROM bookinfo WHERE BookID = %s", (book_id,))
                book = cursor.fetchone()
                if not book or book['Stock'] <= 0:
                    messagebox.showerror("Error", "书籍库存不足")
                    return False

                # 插入借书记录
                sql = """
                    INSERT INTO borrowinginfo (StudentID, BookID, BorrowDate)
                    VALUES (%s, %s, CURDATE())
                """
                cursor.execute(sql, (student_id, book_id))

                # 更新书籍库存
                cursor.execute("UPDATE bookinfo SET Stock = Stock - 1 WHERE BookID = %s", (book_id,))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()
    else:
        return False

def return_book(student_id, password, book_id):
    if not validate_student(student_id, password):
        messagebox.showerror("Error", "学生身份验证失败")
        return False

    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                # 更新还书记录
                sql = """
                    UPDATE borrowinginfo
                    SET ReturnDate = CURDATE()
                    WHERE StudentID = %s AND BookID = %s AND ReturnDate IS NULL
                """
                cursor.execute(sql, (student_id, book_id))

                # 检查是否有更新
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "没有找到未归还的借书记录")
                    return False

                # 更新书籍库存
                cursor.execute("UPDATE bookinfo SET Stock = Stock + 1 WHERE BookID = %s", (book_id,))
            connection.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False
        finally:
            connection.close()
    else:
        return False
    
def get_borrowing_info():
    connection = connect_db()
    if connection:
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT si.Name AS StudentName, si.StudentID, bi.BookID, bi.Title AS BookTitle, bo.BorrowDate, bo.ReturnDate
                    FROM borrowinginfo bo
                    JOIN studentinfo si ON bo.StudentID = si.StudentID
                    JOIN bookinfo bi ON bo.BookID = bi.BookID
                """
                cursor.execute(sql)
                results = cursor.fetchall()
                return results
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
        finally:
            connection.close()