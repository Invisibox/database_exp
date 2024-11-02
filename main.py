import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import ctypes
import backend.backend as backend  # 导入后端函数
from ttkbootstrap import Style
from student import *
from book import *
from employee import *
from superadmin import *
from stu_function import *

class LoginWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.role_label = ttk.Label(self.frame, text="选择身份:")
        self.role_label.pack(pady=5)
        self.role_combobox = ttk.Combobox(self.frame, values=["管理员", "学生"])
        self.role_combobox.pack(pady=5)
        self.role_combobox.current(0)  # 默认选择管理员

        self.AdminID_label = ttk.Label(self.frame, text="用户ID:")
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
        role = self.role_combobox.get()
        AdminID = self.AdminID_entry.get()
        password = self.password_entry.get()

        if role == "管理员":
            if backend.validate_user(AdminID, password):
                self.app.user_role = "superadmin"
                self.app.show_main_menu()
            else:
                messagebox.showerror("错误", "用户名或密码错误")
        elif role == "学生":
            if backend.validate_student(AdminID, password):
                self.app.user_role = "student"
                self.app.show_stu_menu()
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

    # 管理员主菜单
    def show_main_menu(self):
        self.login_window.hide()
        self.main_menu = MainMenu(self.main_frame, self)
        self.main_menu.show()

    ## 学生管理界面
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

    ## 书籍管理界面
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
    
    def show_search_book(self):
        self.book_management.hide()
        self.search_book = SearchBooksWindow(self.main_frame, self)
        self.search_book.show()

    def show_update_view(self):
        self.book_management.hide()
        self.update_view = UpdateViewManageWindow(self.main_frame, self)
        self.update_view.show()

    def show_delete_book(self):
        self.book_management.hide()
        self.delete_book = DeleteBookWindow(self.main_frame, self)
        self.delete_book.show()

    def show_borrowing_info(self):
        self.book_management.hide()
        self.borrowing_info = BorrowingInfoWindow(self.main_frame, self)
        self.borrowing_info.show()

    ## 员工管理界面
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

    ## 超级管理员管理界面
    def show_superadmin_management(self):
        self.main_menu.hide()
        self.superadmin_management = SuperAdminManagementWindow(self.main_frame, self)
        self.superadmin_management.show()

    def show_add_superadmin(self):
        self.superadmin_management.hide()
        self.add_superadmin = AddSuperAdminWindow(self.main_frame, self)
        self.add_superadmin.show()

    def show_view_superadmins(self):
        self.superadmin_management.hide()
        self.view_superadmins = ViewSuperAdminsWindow(self.main_frame, self)
        self.view_superadmins.show()

    def show_update_superadmin(self):
        self.superadmin_management.hide()
        self.update_superadmin = UpdateSuperAdminWindow(self.main_frame, self)
        self.update_superadmin.show()

    def show_delete_superadmin(self):
        self.superadmin_management.hide()
        self.delete_superadmin = DeleteSuperAdminWindow(self.main_frame, self)
        self.delete_superadmin.show()

    def show_update_superadmin_account(self):
        self.superadmin_management.hide()
        self.update_superadmin_account = UpdateSuperAdminAccountWindow(self.main_frame, self)
        self.update_superadmin_account.show()

    # 显示学生主菜单
    def show_stu_menu(self):
        self.login_window.hide()
        self.stu_menu = StudentMenu(self.main_frame, self)
        self.stu_menu.show()

    def stu_search_book(self):
        self.stu_menu.hide()
        self.search_book = StuSearchBooksWindow(self.main_frame, self)
        self.search_book.show()

    def stu_borrow_book(self):
        self.stu_menu.hide()
        self.borrow_book = BorrowBookWindow(self.main_frame, self)
        self.borrow_book.show()

    def stu_return_book(self):
        self.stu_menu.hide()
        self.return_book = ReturnBookWindow(self.main_frame, self)
        self.return_book.show()

    def edit_student_info(self):
        self.stu_menu.hide()
        self.edit_student_info = UpdateStudentInfoWindow(self.main_frame, self)
        self.edit_student_info.show()

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

        self.superadmin_btn = ttk.Button(self.frame, text="超级管理员管理", command=self.app.show_superadmin_management, width=30)
        self.superadmin_btn.pack(pady=10, ipady=5)
        # 你可以在这里添加其他管理部分的按钮

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class StudentMenu:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.search_btn = ttk.Button(self.frame, text="查找书籍", command=self.app.stu_search_book, width=30)
        self.search_btn.pack(pady=10, ipady=5)

        self.borrow_btn = ttk.Button(self.frame, text="借阅书籍", command=self.app.stu_borrow_book, width=30)
        self.borrow_btn.pack(pady=10, ipady=5)

        self.return_btn = ttk.Button(self.frame, text="归还书籍", command=self.app.stu_return_book, width=30)
        self.return_btn.pack(pady=10, ipady=5)

        self.info_btn = ttk.Button(self.frame, text="修改个人信息", command=self.app.edit_student_info, width=30)
        self.info_btn.pack(pady=10, ipady=5)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

if __name__ == '__main__':
    root = tk.Tk()
    style = Style(theme='morph')

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