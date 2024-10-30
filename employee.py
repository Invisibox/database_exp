import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import backend.backend as backend  # 导入后端函数

class EmployeeManagementWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.frame, text="员工管理")
        self.label.pack(pady=10)

        self.add_employee_btn = ttk.Button(self.frame, text="添加员工", command=self.app.show_add_employee, width=30)
        self.add_employee_btn.pack(pady=5, ipady=5)

        self.view_employees_btn = ttk.Button(self.frame, text="查看员工", command=self.app.show_view_employees, width=30)
        self.view_employees_btn.pack(pady=5, ipady=5)

        self.update_employee_btn = ttk.Button(self.frame, text="更新员工", command=self.app.show_update_employee, width=30)
        self.update_employee_btn.pack(pady=5, ipady=5)

        self.delete_employee_btn = ttk.Button(self.frame, text="删除员工", command=self.app.show_delete_employee, width=30)
        self.delete_employee_btn.pack(pady=5, ipady=5)

        self.update_employee_account_btn = ttk.Button(self.frame, text="更新员工账号", command=self.app.show_update_employee_account, width=30)
        self.update_employee_account_btn.pack(pady=5, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.main_menu), width=30)
        self.back_btn.pack(pady=5, ipady=5)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class AddEmployeeWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        labels = ['员工ID:', '姓名:', '性别:', '电话号码:', '身份证号:', '职位:']
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

        self.add_btn = ttk.Button(self.frame, text="添加员工", command=self.add_employee_to_db, width=15)
        self.add_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.employee_management), width=15)
        self.back_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, ipady=5)

    def add_employee_to_db(self):
        employee_data = (
            self.entries['员工ID:'].get(),
            self.entries['姓名:'].get(),
            self.gender_var.get(),
            self.entries['电话号码:'].get(),
            self.entries['身份证号:'].get(),
            self.entries['职位:'].get(),
        )

        success = backend.add_employee(employee_data)
        if success:
            messagebox.showinfo("成功", "员工添加成功，初始密码为password。")
            self.app.go_back(self, self.app.employee_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class ViewEmployeesWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        columns = ('员工ID', '姓名', '性别', '电话号码', '身份证号', '职位')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

        self.load_employees()

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.employee_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)

    def load_employees(self):
        employees = backend.get_all_employees()
        for row in employees:
            self.tree.insert('', 'end', values=(
                row['EmployeeID'], row['Name'], row['Gender'], row['PhoneNumber'],
                row['IDCardNumber'], row['Position']
            ))

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class UpdateEmployeeWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.employee_id_label = ttk.Label(self.frame, text="输入要更新的员工ID:")
        self.employee_id_label.pack(pady=5)
        self.employee_id_entry = ttk.Entry(self.frame)
        self.employee_id_entry.pack(pady=5)

        self.fetch_btn = ttk.Button(self.frame, text="获取数据", command=self.fetch_employee_data)
        self.fetch_btn.pack(pady=5, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.employee_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)

    def fetch_employee_data(self):
        employee_id = self.employee_id_entry.get()
        employee_data = backend.get_employee_by_id(employee_id)
        if employee_data:
            self.show_update_form(employee_data)
        else:
            messagebox.showerror("错误", "未找到员工。")

    def show_update_form(self, employee_data):
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title("更新员工数据")

        labels = ['姓名:', '性别:', '电话号码:', '身份证号:', '职位:']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.update_window, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')

            if text == '性别:':
                self.gender_var = tk.StringVar(value=employee_data['Gender'])
                gender_male = ttk.Radiobutton(self.update_window, text="男", variable=self.gender_var, value="Male")
                gender_female = ttk.Radiobutton(self.update_window, text="女", variable=self.gender_var, value="Female")
                gender_male.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                gender_female.grid(row=idx, column=1, padx=80, pady=10)
            else:
                entry = ttk.Entry(self.update_window)
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[text] = entry

                if text == '姓名:':
                    entry.insert(0, employee_data['Name'])
                elif text == '电话号码:':
                    entry.insert(0, employee_data['PhoneNumber'])
                elif text == '身份证号:':
                    entry.insert(0, employee_data['IDCardNumber'])
                elif text == '职位:':
                    entry.insert(0, employee_data['Position'])

        self.update_btn = ttk.Button(self.update_window, text="更新员工",
                                    command=lambda: self.update_employee_in_db(employee_data['EmployeeID']), width=15)
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)

    def update_employee_in_db(self, employee_id):
        employee_data = (
            self.entries['姓名:'].get(),
            self.gender_var.get(),
            self.entries['电话号码:'].get(),
            self.entries['身份证号:'].get(),
            self.entries['职位:'].get(),
        )

        success = backend.update_employee(employee_id, employee_data)
        if success:
            messagebox.showinfo("成功", "员工更新成功。")
            self.update_window.destroy()
            self.app.go_back(self, self.app.employee_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class DeleteEmployeeWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.employee_id_label = ttk.Label(self.frame, text="输入要删除的员工ID:")
        self.employee_id_label.pack(pady=5)
        self.employee_id_entry = ttk.Entry(self.frame)
        self.employee_id_entry.pack(pady=5)

        self.delete_btn = ttk.Button(self.frame, text="删除员工", command=self.delete_employee_from_db)
        self.delete_btn.pack(pady=5, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.employee_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)

    def delete_employee_from_db(self):
        employee_id = self.employee_id_entry.get()
        success = backend.delete_employee(employee_id)
        if success:
            messagebox.showinfo("成功", "员工删除成功。")
            self.app.go_back(self, self.app.employee_management)
        else:
            messagebox.showerror("错误", "未找到员工或无法删除。")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class UpdateEmployeeAccountWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.employee_id_label = ttk.Label(self.frame, text="输入要更新的员工ID:")
        self.employee_id_label.pack(pady=5)
        self.employee_id_entry = ttk.Entry(self.frame)
        self.employee_id_entry.pack(pady=5)

        self.fetch_btn = ttk.Button(self.frame, text="获取数据", command=self.fetch_account_data)
        self.fetch_btn.pack(pady=5, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.employee_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)

    def fetch_account_data(self):
        employee_id = self.employee_id_entry.get()
        account_data = backend.get_employee_account_by_id(employee_id)
        if account_data:
            self.show_update_form(account_data)
        else:
            messagebox.showerror("错误", "未找到员工账号信息。")

    def show_update_form(self, account_data):
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title("更新员工账号信息")

        labels = ['密码:', '安全问题:', '安全答案:']
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

        self.update_btn = ttk.Button(self.update_window, text="更新账号信息",
                                    command=lambda: self.update_account_in_db(account_data['EmployeeID']), width=15)
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)

    def update_account_in_db(self, employee_id):
        account_data = (
            self.entries['密码:'].get(),
            self.entries['安全问题:'].get(),
            self.entries['安全答案:'].get(),
        )

        success = backend.update_employee_account(employee_id, account_data)
        if success:
            messagebox.showinfo("成功", "员工账号信息更新成功。")
            self.update_window.destroy()
            self.app.go_back(self, self.app.employee_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()