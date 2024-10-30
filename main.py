import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import ctypes
import sv_ttk
import backend.backend as backend  # 导入后端函数
from student import *
from book import *
from employee import *

class LoginWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.AdminID_label = ttk.Label(self.frame, text="管理员ID:")
        self.AdminID_label.pack(pady=5)
        self.AdminID_entry = ttk.Entry(self.frame)
        self.AdminID_entry.pack(pady=5)

        self.password_label = ttk.Label(self.frame, text="密码:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_btn = ttk.Button(self.frame, text="登录", command=self.login)
        self.login_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def login(self):
        AdminID = self.AdminID_entry.get()
        password = self.password_entry.get()
        user_role = backend.validate_user(AdminID, password)
        if user_role in ["superadmin", "admin"]:
            self.app.user_role = user_role
            self.app.show_main_menu()
        else:
            messagebox.showerror("错误", "用户名或密码错误")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class LibraryManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("图书管理系统")
        self.master.minsize(800, 600)  # 设置最小尺寸
        self.master.maxsize(1200, 800)  # 设置最大尺寸
        self.user_role = None
        self.book_management = None
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill='both', expand=True)
        self.login_window = LoginWindow(self.main_frame, self)
        self.login_window.show()

    def show_main_menu(self):
        self.login_window.hide()
        self.main_menu = MainMenu(self.main_frame, self)
        self.main_menu.show()

    def show_student_management(self):
        self.main_menu.hide()
        self.student_management = StudentManagementWindow(self.main_frame, self)
        self.student_management.show()

    def show_add_student(self):
        self.student_management.hide()
        self.add_student = AddStudentWindow(self.main_frame, self)
        self.add_student.show()

    def show_view_students(self):
        self.student_management.hide()
        self.view_students = ViewStudentsWindow(self.main_frame, self)
        self.view_students.show()

    def show_update_student(self):
        self.student_management.hide()
        self.update_student = UpdateStudentWindow(self.main_frame, self)
        self.update_student.show()

    def show_delete_student(self):
        self.student_management.hide()
        self.delete_student = DeleteStudentWindow(self.main_frame, self)
        self.delete_student.show()

    def show_update_student_account(self):
        self.student_management.hide()
        self.update_student_account = UpdateStudentAccountWindow(self.main_frame, self)
        self.update_student_account.show()

    def show_book_management(self):
        self.main_menu.hide()
        self.book_management = BookManagementWindow(self.main_frame, self)
        self.book_management.show()

    def show_add_book(self):
        self.book_management.hide()
        self.add_book = AddBookWindow(self.main_frame, self)
        self.add_book.show()

    def show_view_books(self):
        self.book_management.hide()
        self.view_books = ViewBooksWindow(self.main_frame, self)
        self.view_books.show()

    def show_update_book(self):
        self.book_management.hide()
        self.update_book = UpdateBookWindow(self.main_frame, self)
        self.update_book.show()

    def show_delete_book(self):
        self.book_management.hide()
        self.delete_book = DeleteBookWindow(self.main_frame, self)
        self.delete_book.show()

    def show_employee_management(self):
        self.main_menu.hide()
        self.employee_management = EmployeeManagementWindow(self.main_frame, self)
        self.employee_management.show()

    def show_add_employee(self):
        self.employee_management.hide()
        self.add_employee = AddEmployeeWindow(self.main_frame, self)
        self.add_employee.show()

    def show_view_employees(self):
        self.employee_management.hide()
        self.view_employees = ViewEmployeesWindow(self.main_frame, self)
        self.view_employees.show()

    def show_update_employee(self):
        self.employee_management.hide()
        self.update_employee = UpdateEmployeeWindow(self.main_frame, self)
        self.update_employee.show()

    def show_delete_employee(self):
        self.employee_management.hide()
        self.delete_employee = DeleteEmployeeWindow(self.main_frame, self)
        self.delete_employee.show()

    def show_update_employee_account(self):
        self.employee_management.hide()
        self.update_employee_account = UpdateEmployeeAccountWindow(self.main_frame, self)
        self.update_employee_account.show()

    def go_back(self, current_window, previous_window):
        current_window.hide()
        previous_window.show()

class MainMenu:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.student_btn = ttk.Button(self.frame, text="学生管理", command=self.app.show_student_management, width=30)
        self.student_btn.pack(pady=10, ipady=5)  # 增加按钮高度

        self.book_btn = ttk.Button(self.frame, text="书籍管理", command=self.app.show_book_management, width=30)
        self.book_btn.pack(pady=10, ipady=5)

        self.employee_btn = ttk.Button(self.frame, text="员工管理", command=self.app.show_employee_management, width=30)
        self.employee_btn.pack(pady=10, ipady=5)
        # 你可以在这里添加其他管理部分的按钮

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

if __name__ == '__main__':
    root = tk.Tk()
    sv_ttk.set_theme("light")
    style = ttk.Style()

    # 设置 DPI 感知
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    root.tk.call('tk', 'scaling', ScaleFactor / 75)

    # 设置所有常见小部件的默认字体
    default_font = tkfont.nametofont("TkDefaultFont")
    default_font.configure(family="Microsoft YaHei", size=9)
    root.option_add("*Font", default_font)

    # 设置特定小部件的字体
    style.configure('TButton', font=('Microsoft YaHei', 10))
    style.configure('TRadiobutton', font=('Microsoft YaHei', 9))
    style.configure('TLabel', font=('Microsoft YaHei', 9))
    style.configure('TEntry', font=('Microsoft YaHei', 9))
    style.configure('TFrame', font=('Microsoft YaHei', 9))
    style.configure('Treeview', font=('Microsoft YaHei', 9))
    style.configure("Treeview.Heading", font=('Microsoft YaHei', 8))
    
    app = LibraryManagementApp(root)
    root.mainloop()