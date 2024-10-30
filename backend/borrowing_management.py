from tkinter import messagebox
from .db_connection import connect_db

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