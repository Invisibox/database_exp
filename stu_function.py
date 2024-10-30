from tkinter import ttk, messagebox
import backend.backend as backend  # 导入后端函数

class StuSearchBooksWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.frame, text="搜索书籍")
        self.label.pack(pady=10)

        self.id_label = ttk.Label(self.frame, text="书籍ID:")
        self.id_label.pack(pady=5)
        self.id_entry = ttk.Entry(self.frame)
        self.id_entry.pack(pady=5)

        self.title_label = ttk.Label(self.frame, text="书名:")
        self.title_label.pack(pady=5)
        self.title_entry = ttk.Entry(self.frame)
        self.title_entry.pack(pady=5)

        self.author_label = ttk.Label(self.frame, text="作者:")
        self.author_label.pack(pady=5)
        self.author_entry = ttk.Entry(self.frame)
        self.author_entry.pack(pady=5)

        self.category_label = ttk.Label(self.frame, text="类别:")
        self.category_label.pack(pady=5)
        self.category_entry = ttk.Entry(self.frame)
        self.category_entry.pack(pady=5)

        self.search_btn = ttk.Button(self.frame, text="搜索", command=self.search_books)
        self.search_btn.pack(pady=10, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.stu_menu), width=30)
        self.back_btn.pack(pady=5, ipady=5)

        self.tree = ttk.Treeview(self.frame, columns=('书籍ID', '标题', '作者', '出版社', '译者', '类别', '到达时间', '库存'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

    def search_books(self):
        book_id = self.id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        category = self.category_entry.get()

        # 将空字符串转换为 None
        book_id = book_id if book_id else None
        title = title if title else None
        author = author if author else None
        category = category if category else None

        books = backend.search_books(book_id=book_id, title=title, author=author, category=category)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for book in books:
            self.tree.insert('', 'end', values=(book['BookID'], book['Title'], book['Author'], book['Publisher'], book['Translator'], book['Category'], book['ArrivalTime'], book['Stock']))

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class BorrowBookWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        labels = ['学生ID:', '密码:', '书籍ID:']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.frame, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.frame, show="*" if text == '密码:' else None)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[text] = entry

        self.borrow_btn = ttk.Button(self.frame, text="借书", command=self.borrow_book, width=15)
        self.borrow_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.stu_menu), width=15)
        self.back_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, ipady=5)

    def borrow_book(self):
        student_id = self.entries['学生ID:'].get()
        password = self.entries['密码:'].get()
        book_id = self.entries['书籍ID:'].get()

        success = backend.borrow_book(student_id, password, book_id)
        if success:
            messagebox.showinfo("成功", "借书成功。")
        else:
            messagebox.showerror("错误", "借书失败。")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class ReturnBookWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        labels = ['学生ID:', '密码:', '书籍ID:']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.frame, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.frame, show="*" if text == '密码:' else None)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[text] = entry

        self.return_btn = ttk.Button(self.frame, text="还书", command=self.return_book, width=15)
        self.return_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.stu_menu), width=15)
        self.back_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, ipady=5)

    def return_book(self):
        student_id = self.entries['学生ID:'].get()
        password = self.entries['密码:'].get()
        book_id = self.entries['书籍ID:'].get()

        success = backend.return_book(student_id, password, book_id)
        if success:
            messagebox.showinfo("成功", "还书成功。")
            self.app.go_back(self, self.app.book_management)
        else:
            messagebox.showerror("错误", "还书失败。")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class UpdateStudentInfoWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.labels = ['学生ID:', '密码:', '新名字:', '新性别:', '新电话号码:', '新身份证号:', '新校区代码:', '新出生日期:', '新密码:', '新邮箱:']
        self.entries = {}

        for idx, text in enumerate(self.labels[:2]):  # 只显示学生ID和密码输入字段
            label = ttk.Label(self.frame, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.frame, show="*" if text == '密码:' else None)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[text] = entry

        self.verify_btn = ttk.Button(self.frame, text="验证", command=self.verify_info, width=15)
        self.verify_btn.grid(row=2, column=0, columnspan=2, pady=10, ipady=5)

        self.update_btn = ttk.Button(self.frame, text="更新信息", command=self.update_info, width=15)
        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.stu_menu), width=15)

    def verify_info(self):
        student_id = self.entries['学生ID:'].get()
        password = self.entries['密码:'].get()

        if backend.validate_student(student_id, password):  # 假设有一个函数 verify_student 用于验证学生ID和密码
            self.show_update_fields()
        else:
            messagebox.showerror("错误", "学生ID或密码错误。")

    def show_update_fields(self):
        for idx, text in enumerate(self.labels[2:], start=3):  # 显示更新信息的输入字段
            label = ttk.Label(self.frame, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.frame, show="*" if text == '新密码:' else None)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[text] = entry

        self.verify_btn.grid_forget()  # 隐藏验证按钮
        self.update_btn.grid(row=len(self.labels), column=0, columnspan=2, pady=10, ipady=5)
        self.back_btn.grid(row=len(self.labels)+1, column=0, columnspan=2, pady=10, ipady=5)

    def update_info(self):
        student_id = self.entries['学生ID:'].get()
        password = self.entries['密码:'].get()
        new_student_data = (
            self.entries['新名字:'].get() or None,
            self.entries['新性别:'].get() or None,
            self.entries['新电话号码:'].get() or None,
            self.entries['新身份证号:'].get() or None,
            self.entries['新校区代码:'].get() or None,
            self.entries['新出生日期:'].get() or None
        )
        new_account_data = (
            self.entries['新密码:'].get() or None,
            self.entries['新邮箱:'].get() or None
        )

        success = backend.student_update_own_info(student_id, password, new_student_data, new_account_data)
        if success:
            messagebox.showinfo("成功", "信息更新成功。")
        else:
            messagebox.showerror("错误", "信息更新失败。")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()