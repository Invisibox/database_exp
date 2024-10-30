import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
import ctypes
import sv_ttk
import backend  # 导入后端函数

class LoginWindow:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.master.title("登录")
        self.create_widgets()

    def create_widgets(self):
        self.AdminID_label = ttk.Label(self.master, text="管理员ID:")
        self.AdminID_label.pack(pady=5)
        self.AdminID_entry = ttk.Entry(self.master)
        self.AdminID_entry.pack(pady=5)

        self.password_label = ttk.Label(self.master, text="密码:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.master, show="*")
        self.password_entry.pack(pady=5)

        self.login_btn = ttk.Button(self.master, text="登录", command=self.login)
        self.login_btn.pack(pady=10)

    def login(self):
        AdminID = self.AdminID_entry.get()
        password = self.password_entry.get()
        user_role = backend.validate_user(AdminID, password)
        if user_role in ["superadmin", "admin"]:
            self.master.destroy()
            self.on_login_success(user_role)
        else:
            messagebox.showerror("错误", "用户名或密码错误")

class LibraryManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("图书管理系统")
        self.user_role = None
        self.show_login_window()

    def show_login_window(self):
        login_window = tk.Toplevel(self.master)
        LoginWindow(login_window, self.on_login_success)

    def on_login_success(self, user_role):
        self.user_role = user_role
        self.create_widgets()

    def create_widgets(self):
        if self.user_role in ["superadmin", "admin"]:
            self.student_btn = ttk.Button(self.master, text="学生管理", command=self.open_student_management, width=80)
            self.student_btn.pack(pady=10)
            # 你可以在这里添加其他管理部分的按钮
        else:
            messagebox.showerror("错误", "无权限访问")

    def open_student_management(self):
        StudentManagementWindow(self.master)

class StudentManagementWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("学生管理")
        self.create_widgets()

    def create_widgets(self):
        # 创建学生管理的控件
        self.label = ttk.Label(self.master, text="学生管理")
        self.label.pack(pady=10)

        self.add_student_btn = ttk.Button(self.master, text="添加学生", command=self.add_student, width=50)
        self.add_student_btn.pack(pady=5)

        self.view_students_btn = ttk.Button(self.master, text="查看学生", command=self.view_students, width=50)
        self.view_students_btn.pack(pady=5)

        self.update_student_btn = ttk.Button(self.master, text="更新学生", command=self.update_student, width=50)
        self.update_student_btn.pack(pady=5)

        self.delete_student_btn = ttk.Button(self.master, text="删除学生", command=self.delete_student, width=50)
        self.delete_student_btn.pack(pady=5)

    def add_student(self):
        AddStudentWindow(self.master)

    def view_students(self):
        ViewStudentsWindow(self.master)

    def update_student(self):
        UpdateStudentWindow(self.master)

    def delete_student(self):
        DeleteStudentWindow(self.master)

class AddStudentWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("添加学生")
        self.create_widgets()

    def create_widgets(self):
        # 创建学生信息的输入字段
        labels = ['学号:', '姓名:', '性别:', '电话号码:', '身份证号:', '校区代码:', '出生日期 (YYYY-MM-DD):']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.master, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')

            if text == '性别:':
                self.gender_var = tk.StringVar(value="男")
                gender_male = ttk.Radiobutton(self.master, text="男", variable=self.gender_var, value="Male")
                gender_female = ttk.Radiobutton(self.master, text="女", variable=self.gender_var, value="Female")
                gender_male.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                gender_female.grid(row=idx, column=1, padx=70, pady=5)
            else:
                entry = ttk.Entry(self.master)
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[text] = entry

        self.add_btn = ttk.Button(self.master, text="添加学生", command=self.add_student_to_db, width=15)
        self.add_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

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
            messagebox.showinfo("成功", "学生添加成功。")
            self.master.destroy()

class ViewStudentsWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("查看学生")
        self.create_widgets()

    def create_widgets(self):
        # 创建一个 Treeview 来显示学生信息
        columns = ('学号', '姓名', '性别', '电话号码', '身份证号', '校区代码', '出生日期')
        self.tree = ttk.Treeview(self.master, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

        self.load_students()

    def load_students(self):
        students = backend.get_all_students()
        for row in students:
            self.tree.insert('', 'end', values=(
                row['StudentID'], row['Name'], row['Gender'], row['PhoneNumber'],
                row['IDCardNumber'], row['CampusCode'], row['DateOfBirth']
            ))

class UpdateStudentWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("更新学生")
        self.create_widgets()

    def create_widgets(self):
        self.student_id_label = ttk.Label(self.master, text="输入要更新的学生学号:")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ttk.Entry(self.master)
        self.student_id_entry.pack(pady=5)

        self.fetch_btn = ttk.Button(self.master, text="获取数据", command=self.fetch_student_data)
        self.fetch_btn.pack(pady=5)

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

        # 创建更新表单
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

                # 插入现有数据
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
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

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
            self.master.destroy()

class DeleteStudentWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("删除学生")
        self.create_widgets()

    def create_widgets(self):
        self.student_id_label = ttk.Label(self.master, text="输入要删除的学生学号:")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ttk.Entry(self.master)
        self.student_id_entry.pack(pady=5)

        self.delete_btn = ttk.Button(self.master, text="删除学生", command=self.delete_student_from_db)
        self.delete_btn.pack(pady=5)

    def delete_student_from_db(self):
        student_id = self.student_id_entry.get()
        success = backend.delete_student(student_id)
        if success:
            messagebox.showinfo("成功", "学生删除成功。")
            self.master.destroy()
        else:
            messagebox.showerror("错误", "未找到学生或无法删除。")

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