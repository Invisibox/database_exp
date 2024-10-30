import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import backend.backend as backend  # 导入后端函数

class BookManagementWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.frame, text="书籍管理")
        self.label.pack(pady=10)

        self.add_book_btn = ttk.Button(self.frame, text="添加书籍", command=self.app.show_add_book, width=30)
        self.add_book_btn.pack(pady=5, ipady=5)

        self.view_books_btn = ttk.Button(self.frame, text="查看书籍", command=self.app.show_view_books, width=30)
        self.view_books_btn.pack(pady=5, ipady=5)

        self.update_book_btn = ttk.Button(self.frame, text="更新书籍", command=self.app.show_update_book, width=30)
        self.update_book_btn.pack(pady=5, ipady=5)

        self.delete_book_btn = ttk.Button(self.frame, text="删除书籍", command=self.app.show_delete_book, width=30)
        self.delete_book_btn.pack(pady=5, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.main_menu), width=30)
        self.back_btn.pack(pady=5, ipady=5)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class AddBookWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        labels = ['书籍ID:', '标题:', '作者:', '出版社:', '译者:', '类别:', '到达时间 (YYYY-MM-DD):', '库存:']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.frame, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.frame)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[text] = entry

        self.add_btn = ttk.Button(self.frame, text="添加书籍", command=self.add_book_to_db, width=15)
        self.add_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=15)
        self.back_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=10, ipady=5)

    def add_book_to_db(self):
        book_data = (
            self.entries['书籍ID:'].get(),
            self.entries['标题:'].get(),
            self.entries['作者:'].get(),
            self.entries['出版社:'].get(),
            self.entries['译者:'].get(),
            self.entries['类别:'].get(),
            self.entries['到达时间 (YYYY-MM-DD):'].get(),
            self.entries['库存:'].get(),
        )

        success = backend.add_book(book_data)
        if success:
            messagebox.showinfo("成功", "书籍添加成功。")
            self.app.go_back(self, self.app.book_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class ViewBooksWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        columns = ('书籍ID', '标题', '作者', '出版社', '译者', '类别', '到达时间', '库存')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

        self.load_books()

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)

    def load_books(self):
        books = backend.get_all_books()
        for row in books:
            self.tree.insert('', 'end', values=(
                row['BookID'], row['Title'], row['Author'], row['Publisher'],
                row['Translator'], row['Category'], row['ArrivalTime'], row['Stock']
            ))

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class UpdateBookWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.book_id_label = ttk.Label(self.frame, text="输入要更新的书籍ID:")
        self.book_id_label.pack(pady=5)
        self.book_id_entry = ttk.Entry(self.frame)
        self.book_id_entry.pack(pady=5)

        self.fetch_btn = ttk.Button(self.frame, text="获取数据", command=self.fetch_book_data)
        self.fetch_btn.pack(pady=5, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)

    def fetch_book_data(self):
        book_id = self.book_id_entry.get()
        book_data = backend.get_book_by_id(book_id)
        if book_data:
            self.show_update_form(book_data)
        else:
            messagebox.showerror("错误", "未找到书籍。")

    def show_update_form(self, book_data):
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title("更新书籍数据")

        labels = ['标题:', '作者:', '出版社:', '译者:', '类别:', '到达时间 (YYYY-MM-DD):', '库存:']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = ttk.Label(self.update_window, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(self.update_window)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            self.entries[text] = entry

            if text == '标题:':
                entry.insert(0, book_data['Title'])
            elif text == '作者:':
                entry.insert(0, book_data['Author'])
            elif text == '出版社:':
                entry.insert(0, book_data['Publisher'])
            elif text == '译者:':
                entry.insert(0, book_data['Translator'])
            elif text == '类别:':
                entry.insert(0, book_data['Category'])
            elif text == '到达时间 (YYYY-MM-DD):':
                entry.insert(0, book_data['ArrivalTime'])
            elif text == '库存:':
                entry.insert(0, book_data['Stock'])

        self.update_btn = ttk.Button(self.update_window, text="更新书籍",
                                    command=lambda: self.update_book_in_db(book_data['BookID']), width=15)
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10, ipady=5)

    def update_book_in_db(self, book_id):
        book_data = (
            self.entries['标题:'].get(),
            self.entries['作者:'].get(),
            self.entries['出版社:'].get(),
            self.entries['译者:'].get(),
            self.entries['类别:'].get(),
            self.entries['到达时间 (YYYY-MM-DD):'].get(),
            self.entries['库存:'].get(),
        )

        success = backend.update_book(book_id, book_data)
        if success:
            messagebox.showinfo("成功", "书籍更新成功。")
            self.update_window.destroy()
            self.app.go_back(self, self.app.book_management)

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class DeleteBookWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.book_id_label = ttk.Label(self.frame, text="输入要删除的书籍ID:")
        self.book_id_label.pack(pady=5)
        self.book_id_entry = ttk.Entry(self.frame)
        self.book_id_entry.pack(pady=5)

        self.delete_btn = ttk.Button(self.frame, text="删除书籍", command=self.delete_book_from_db)
        self.delete_btn.pack(pady=5, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)

    def delete_book_from_db(self):
        book_id = self.book_id_entry.get()
        success = backend.delete_book(book_id)
        if success:
            messagebox.showinfo("成功", "书籍删除成功。")
            self.app.go_back(self, self.app.book_management)
        else:
            messagebox.showerror("错误", "未找到书籍或无法删除。")

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()