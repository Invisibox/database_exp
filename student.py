import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import backend.backend as backend  # 导入后端函数

class StudentManagementWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.frame, text="学生管理")
        self.label.pack(pady=10)

        self.add_student_btn = ttk.Button(self.frame, text="添加学生", command=self.app.show_add_student, width=30)
        self.add_student_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.view_students_btn = ttk.Button(self.frame, text="查看学生", command=self.app.show_view_students, width=30)
        self.view_students_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.update_student_btn = ttk.Button(self.frame, text="更新学生", command=self.app.show_update_student, width=30)
        self.update_student_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.delete_student_btn = ttk.Button(self.frame, text="删除学生", command=self.app.show_delete_student, width=30)
        self.delete_student_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.update_student_account_btn = ttk.Button(self.frame, text="更新学生账号", command=self.app.show_update_student_account, width=30)
        self.update_student_account_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.main_menu), width=30)
        self.back_btn.pack(pady=5, ipady=5)  # 增加按钮高度

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class AddStudentWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        labels = ['学号:', '姓名:', '性别:', '电话号码:', '身份证号:', '校区代码:', '出生日期 (YYYY-MM-DD):']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.frame, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')

            if text == '性别:':
                self.gender_var = tk.StringVar(value="男")
                gender_male = ttk.Radiobutton(self.frame, text="男", variable=self.gender_var, value="Male")
                gender_female = ttk.Radiobutton(self.frame, text="女", variable=self.gender_var, value="Female")
                gender_male.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                gender_female.grid(row=idx, column=1, padx=70, pady=5)
            else:
                entry = ttk.Entry(self.frame)
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[text] = entry

        self.add_btn = ttk.Button(self.frame, text="添加学生", command=self.add_student_to_db, width=15)
        self.add_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.student_management), width=15)
        self.back_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, ipady=5)  # 增加按钮高度

    def add_student_to_db(self):
        student_data = (
            self.entries['学号:'].get(),
            self.entries['姓名:'].get(),
            self.gender_var.get(),
            self.entries['电话号码:'].get(),
            self.entries['身份证号:'].get(),
            self.entries['校区代码:'].get(),
            self.entries['出生日期 (YYYY-MM-DD):'].get(),
        )

        success = backend.add_student(student_data)
        if success:
            messagebox.showinfo("成功", "学生添加成功，初始密码为password。")
            self.app.go_back(self, self.app.student_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class ViewStudentsWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        columns = ('学号', '姓名', '性别', '电话号码', '身份证号', '校区代码', '出生日期')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

        self.load_students()

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.student_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def load_students(self):
        students = backend.get_all_students()
        for row in students:
            self.tree.insert('', 'end', values=(
                row['StudentID'], row['Name'], row['Gender'], row['PhoneNumber'],
                row['IDCardNumber'], row['CampusCode'], row['DateOfBirth']
            ))

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class UpdateStudentWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.student_id_label = ttk.Label(self.frame, text="输入要更新的学生学号:")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ttk.Entry(self.frame)
        self.student_id_entry.pack(pady=5)

        self.fetch_btn = ttk.Button(self.frame, text="获取数据", command=self.fetch_student_data)
        self.fetch_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.student_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def fetch_student_data(self):
        student_id = self.student_id_entry.get()
        student_data = backend.get_student_by_id(student_id)
        if student_data:
            self.show_update_form(student_data)
        else:
            messagebox.showerror("错误", "未找到学生。")

    def show_update_form(self, student_data):
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title("更新学生数据")

        labels = ['姓名:', '性别:', '电话号码:', '身份证号:', '校区代码:', '出生日期 (YYYY-MM-DD):']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.update_window, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')

            if text == '性别:':
                self.gender_var = tk.StringVar(value=student_data['Gender'])
                gender_male = ttk.Radiobutton(self.update_window, text="男", variable=self.gender_var, value="Male")
                gender_female = ttk.Radiobutton(self.update_window, text="女", variable=self.gender_var, value="Female")
                gender_male.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                gender_female.grid(row=idx, column=1, padx=80, pady=10)
            else:
                entry = ttk.Entry(self.update_window)
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[text] = entry

                if text == '姓名:':
                    entry.insert(0, student_data['Name'])
                elif text == '电话号码:':
                    entry.insert(0, student_data['PhoneNumber'])
                elif text == '身份证号:':
                    entry.insert(0, student_data['IDCardNumber'])
                elif text == '校区代码:':
                    entry.insert(0, student_data['CampusCode'])
                elif text == '出生日期 (YYYY-MM-DD):':
                    entry.insert(0, student_data['DateOfBirth'])

        self.update_btn = ttk.Button(self.update_window, text="更新学生",
                                    command=lambda: self.update_student_in_db(student_data['StudentID']), width=15)
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)  # 增加按钮高度

    def update_student_in_db(self, student_id):
        student_data = (
            self.entries['姓名:'].get(),
            self.gender_var.get(),
            self.entries['电话号码:'].get(),
            self.entries['身份证号:'].get(),
            self.entries['校区代码:'].get(),
            self.entries['出生日期 (YYYY-MM-DD):'].get(),
        )

        success = backend.update_student(student_id, student_data)
        if success:
            messagebox.showinfo("成功", "学生更新成功。")
            self.update_window.destroy()
            self.app.go_back(self, self.app.student_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class DeleteStudentWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.student_id_label = ttk.Label(self.frame, text="输入要删除的学生学号:")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ttk.Entry(self.frame)
        self.student_id_entry.pack(pady=5)

        self.delete_btn = ttk.Button(self.frame, text="删除学生", command=self.delete_student_from_db)
        self.delete_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.student_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def delete_student_from_db(self):
        student_id = self.student_id_entry.get()
        success = backend.delete_student(student_id)
        if success:
            messagebox.showinfo("成功", "学生删除成功。")
            self.app.go_back(self, self.app.student_management)
        else:
            messagebox.showerror("错误", "未找到学生或无法删除。")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class UpdateStudentAccountWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.student_id_label = ttk.Label(self.frame, text="输入要更新的学生学号:")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ttk.Entry(self.frame)
        self.student_id_entry.pack(pady=5)

        self.fetch_btn = ttk.Button(self.frame, text="获取数据", command=self.fetch_account_data)
        self.fetch_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.student_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def fetch_account_data(self):
        student_id = self.student_id_entry.get()
        account_data = backend.get_student_account_by_id(student_id)
        if account_data:
            self.show_update_form(account_data)
        else:
            messagebox.showerror("错误", "未找到学生账号信息。")

    def show_update_form(self, account_data):
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title("更新学生账号信息")

        labels = ['密码:', '安全问题:', '安全答案:', '剩余尝试次数:']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.update_window, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')

            entry = ttk.Entry(self.update_window)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[text] = entry

            if text == '密码:':
                entry.insert(0, account_data['Password'])
            elif text == '安全问题:':
                entry.insert(0, account_data['SecurityQuestion'])
            elif text == '安全答案:':
                entry.insert(0, account_data['SecurityAnswer'])
            elif text == '剩余尝试次数:':
                entry.insert(0, account_data['RemainingAttempts'])

        self.update_btn = ttk.Button(self.update_window, text="更新账号信息",
                                    command=lambda: self.update_account_in_db(account_data['StudentID']), width=15)
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)  # 增加按钮高度

    def update_account_in_db(self, student_id):
        account_data = (
            self.entries['密码:'].get(),
            self.entries['安全问题:'].get(),
            self.entries['安全答案:'].get(),
            self.entries['剩余尝试次数:'].get(),
        )

        success = backend.update_student_account(student_id, account_data)
        if success:
            messagebox.showinfo("成功", "学生账号信息更新成功。")
            self.update_window.destroy()
            self.app.go_back(self, self.app.student_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()