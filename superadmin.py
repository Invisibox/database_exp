import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import backend.backend as backend  # 导入后端函数

class SuperAdminManagementWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.frame, text="超级管理员管理")
        self.label.pack(pady=10)

        self.add_superadmin_btn = ttk.Button(self.frame, text="添加超级管理员", command=self.app.show_add_superadmin, width=30)
        self.add_superadmin_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.view_superadmins_btn = ttk.Button(self.frame, text="查看超级管理员", command=self.app.show_view_superadmins, width=30)
        self.view_superadmins_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.update_superadmin_btn = ttk.Button(self.frame, text="更新超级管理员", command=self.app.show_update_superadmin, width=30)
        self.update_superadmin_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.delete_superadmin_btn = ttk.Button(self.frame, text="删除超级管理员", command=self.app.show_delete_superadmin, width=30)
        self.delete_superadmin_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.update_superadmin_account_btn = ttk.Button(self.frame, text="更新超级管理员账号", command=self.app.show_update_superadmin_account, width=30)
        self.update_superadmin_account_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.main_menu), width=30)
        self.back_btn.pack(pady=5, ipady=5)  # 增加按钮高度

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class AddSuperAdminWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        labels = ['管理员ID:', '姓名:', '性别:', '电话号码:', '身份证号:', '邮箱:']
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

        self.add_btn = ttk.Button(self.frame, text="添加超级管理员", command=self.add_superadmin_to_db, width=15)
        self.add_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.superadmin_management), width=15)
        self.back_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, ipady=5)  # 增加按钮高度

    def add_superadmin_to_db(self):
        superadmin_data = (
            self.entries['管理员ID:'].get(),
            self.entries['姓名:'].get(),
            self.gender_var.get(),
            self.entries['电话号码:'].get(),
            self.entries['身份证号:'].get(),
            self.entries['邮箱:'].get(),
        )

        success = backend.add_superadmin(superadmin_data)
        if success:
            messagebox.showinfo("成功", "超级管理员添加成功，初始密码为password。")
            self.app.go_back(self, self.app.superadmin_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class ViewSuperAdminsWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        columns = ('管理员ID', '姓名', '性别', '电话号码', '身份证号', '邮箱')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

        self.load_superadmins()

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.superadmin_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def load_superadmins(self):
        superadmins = backend.get_all_superadmins()
        for row in superadmins:
            self.tree.insert('', 'end', values=(
                row['AdminID'], row['Name'], row['Gender'], row['PhoneNumber'],
                row['IDCardNumber'], row['Email']
            ))

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class UpdateSuperAdminWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.admin_id_label = ttk.Label(self.frame, text="输入要更新的管理员ID:")
        self.admin_id_label.pack(pady=5)
        self.admin_id_entry = ttk.Entry(self.frame)
        self.admin_id_entry.pack(pady=5)

        self.fetch_btn = ttk.Button(self.frame, text="获取数据", command=self.fetch_superadmin_data)
        self.fetch_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.superadmin_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def fetch_superadmin_data(self):
        admin_id = self.admin_id_entry.get()
        superadmin_data = backend.get_superadmin_by_id(admin_id)
        if superadmin_data:
            self.show_update_form(superadmin_data)
        else:
            messagebox.showerror("错误", "未找到超级管理员。")

    def show_update_form(self, superadmin_data):
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title("更新超级管理员数据")

        labels = ['姓名:', '性别:', '电话号码:', '身份证号:', '邮箱:']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.update_window, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')

            if text == '性别:':
                self.gender_var = tk.StringVar(value=superadmin_data['Gender'])
                gender_male = ttk.Radiobutton(self.update_window, text="男", variable=self.gender_var, value="Male")
                gender_female = ttk.Radiobutton(self.update_window, text="女", variable=self.gender_var, value="Female")
                gender_male.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                gender_female.grid(row=idx, column=1, padx=80, pady=10)
            else:
                entry = ttk.Entry(self.update_window)
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[text] = entry

                if text == '姓名:':
                    entry.insert(0, superadmin_data['Name'])
                elif text == '电话号码:':
                    entry.insert(0, superadmin_data['PhoneNumber'])
                elif text == '身份证号:':
                    entry.insert(0, superadmin_data['IDCardNumber'])
                elif text == '邮箱:':
                    entry.insert(0, superadmin_data['Email'])

        self.update_btn = ttk.Button(self.update_window, text="更新超级管理员",
                                    command=lambda: self.update_superadmin_in_db(superadmin_data['AdminID']), width=15)
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)  # 增加按钮高度

    def update_superadmin_in_db(self, admin_id):
        superadmin_data = (
            self.entries['姓名:'].get(),
            self.gender_var.get(),
            self.entries['电话号码:'].get(),
            self.entries['身份证号:'].get(),
            self.entries['邮箱:'].get(),
        )

        success = backend.update_superadmin(admin_id, superadmin_data)
        if success:
            messagebox.showinfo("成功", "超级管理员更新成功。")
            self.update_window.destroy()
            self.app.go_back(self, self.app.superadmin_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class DeleteSuperAdminWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.admin_id_label = ttk.Label(self.frame, text="输入要删除的管理员ID:")
        self.admin_id_label.pack(pady=5)
        self.admin_id_entry = ttk.Entry(self.frame)
        self.admin_id_entry.pack(pady=5)

        self.delete_btn = ttk.Button(self.frame, text="删除超级管理员", command=self.delete_superadmin_from_db)
        self.delete_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.superadmin_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def delete_superadmin_from_db(self):
        admin_id = self.admin_id_entry.get()
        success = backend.delete_superadmin(admin_id)
        if success:
            messagebox.showinfo("成功", "超级管理员删除成功。")
            self.app.go_back(self, self.app.superadmin_management)
        else:
            messagebox.showerror("错误", "未找到超级管理员或无法删除。")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class UpdateSuperAdminAccountWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.admin_id_label = ttk.Label(self.frame, text="输入要更新的管理员ID:")
        self.admin_id_label.pack(pady=5)
        self.admin_id_entry = ttk.Entry(self.frame)
        self.admin_id_entry.pack(pady=5)

        self.fetch_btn = ttk.Button(self.frame, text="获取数据", command=self.fetch_account_data)
        self.fetch_btn.pack(pady=5, ipady=5)  # 增加按钮高度

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.superadmin_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)  # 增加按钮高度

    def fetch_account_data(self):
        admin_id = self.admin_id_entry.get()
        account_data = backend.get_superadmin_account_by_id(admin_id)
        if account_data:
            self.show_update_form(account_data)
        else:
            messagebox.showerror("错误", "未找到超级管理员账号信息。")

    def show_update_form(self, account_data):
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title("更新超级管理员账号信息")

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
                                    command=lambda: self.update_account_in_db(account_data['AdminID']), width=15)
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)  # 增加按钮高度

    def update_account_in_db(self, admin_id):
        account_data = (
            self.entries['密码:'].get(),
            self.entries['安全问题:'].get(),
            self.entries['安全答案:'].get(),
        )

        success = backend.update_superadmin_account(admin_id, account_data)
        if success:
            messagebox.showinfo("成功", "超级管理员账号信息更新成功。")
            self.update_window.destroy()
            self.app.go_back(self, self.app.superadmin_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()