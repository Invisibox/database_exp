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

        self.search_books_btn = ttk.Button(self.frame, text="搜索书籍", command=self.app.show_search_book, width=30)
        self.search_books_btn.pack(pady=5, ipady=5)

        self.view_management_btn = ttk.Button(self.frame, text="更新视图和索引", command=self.app.show_update_view, width=30)
        self.view_management_btn.pack(pady=5, ipady=5)

        self.borrowing_info_btn = ttk.Button(self.frame, text="借书信息", command=self.app.show_borrowing_info, width=30)
        self.borrowing_info_btn.pack(pady=5, ipady=5)

        self.borrowing_search_btn = ttk.Button(self.frame, text="借书查询", command=self.app.show_borrowing_search, width=30)
        self.borrowing_search_btn.pack(pady=5, ipady=5)

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
        self.selected_view = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        columns = ('书籍ID', '标题', '作者', '出版社', '译者', '类别', '到达时间', '库存')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

        # 添加下拉菜单选择视图
        self.view_selector = ttk.Combobox(self.frame, textvariable=self.selected_view)
        self.view_selector['values'] = ('view_all_books', 'view_books_by_category', 'view_books_by_author')
        self.view_selector.current(0)
        self.view_selector.bind('<<ComboboxSelected>>', self.load_books)
        self.view_selector.pack(pady=10)

        self.load_books()

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=15)
        self.back_btn.pack(pady=10, ipady=5)

    def load_books(self, event=None):
        view = self.selected_view.get()
        if view == 'view_all_books':
            books = backend.get_all_books()
        elif view == 'view_books_by_category':
            books = backend.get_books_by_category()
        elif view == 'view_books_by_author':
            books = backend.get_books_by_author()
        else:
            books = []

        # 清空当前树视图内容
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 插入新数据
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

class SearchBooksWindow:
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

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=30)
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

class UpdateViewManageWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.frame, text="更新视图和索引")
        self.label.pack(pady=10)

        self.update_views_btn = ttk.Button(self.frame, text="更新视图", command=self.update_views, width=30)
        self.update_views_btn.pack(pady=5, ipady=5)

        self.update_index_btn = ttk.Button(self.frame, text="更新索引", command=self.update_index, width=30)
        self.update_index_btn.pack(pady=5, ipady=5)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=30)
        self.back_btn.pack(pady=5, ipady=5)

    def update_views(self):
        success = backend.update_views()
        if success:
            messagebox.showinfo("成功", "视图更新成功。")
        else:
            messagebox.showerror("错误", "视图更新失败。")

    def update_index(self):
        success = backend.update_index()
        if success:
            messagebox.showinfo("成功", "索引更新成功。")
        else:
            messagebox.showerror("错误", "索引更新失败。")

    def show(self):
        print("Showing UpdateViewManageWindow")
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class BorrowingInfoWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.frame, text="借书信息")
        self.label.pack(pady=10)

        columns = ('学生姓名', '学生ID', '书籍ID', '书籍名称', '借书时间', '还书时间')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

        self.load_borrowing_info()

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=30)
        self.back_btn.pack(pady=10, ipady=5)

    def load_borrowing_info(self):
        borrowing_info = backend.get_borrowing_info()
        for row in self.tree.get_children():
            self.tree.delete(row)
        for info in borrowing_info:
            self.tree.insert('', 'end', values=(info['StudentName'], info['StudentID'], info['BookID'], info['BookTitle'], info['BorrowDate'], info['ReturnDate']))

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()

class BorrowingSearchWindow:
    def __init__(self, master, app):
        self.master = master
        self.app = app
        self.frame = ttk.Frame(self.master)
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.frame, text="借书信息")
        self.label.pack(pady=10)

        self.student_id_label = ttk.Label(self.frame, text="学生ID:")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = ttk.Entry(self.frame)
        self.student_id_entry.pack(pady=5)

        self.search_btn = ttk.Button(self.frame, text="查询", command=self.search_borrowing_info)
        self.search_btn.pack(pady=10, ipady=5)

        columns = ('学生姓名', '学生ID', '书籍ID', '书籍名称', '借书时间', '还书时间')
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill='both', expand=True)

        self.back_btn = ttk.Button(self.frame, text="返回", command=lambda: self.app.go_back(self, self.app.book_management), width=30)
        self.back_btn.pack(pady=10, ipady=5)

    def search_borrowing_info(self):
        student_id = self.student_id_entry.get()
        borrowing_info = backend.get_borrowing_info_by_student(student_id)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for info in borrowing_info:
            self.tree.insert('', 'end', values=(info['StudentName'], info['StudentID'], info['BookID'], info['BookTitle'], info['BorrowDate'], info['ReturnDate']))

    def show(self):
        self.frame.pack(fill='both', expand=True)

    def hide(self):
        self.frame.pack_forget()