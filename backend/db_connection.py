import pymysql
from tkinter import messagebox

# Database connection parameters
db_host = 'localhost'
db_user = 'root'
db_password = '123456'  # Replace with your MySQL root password
db_name = 'lib'

def connect_db():
    try:
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None
