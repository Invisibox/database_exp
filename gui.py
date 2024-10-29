import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import backend  # Import backend functions

class LibraryManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.create_widgets()

    def create_widgets(self):
        # Create buttons for different management sections
        self.student_btn = tk.Button(self.master, text="Student Management", command=self.open_student_management, width=30)
        self.student_btn.pack(pady=10)

        # You can add buttons for other management sections here

    def open_student_management(self):
        StudentManagementWindow(self.master)

class StudentManagementWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Student Management")
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for student management
        self.label = tk.Label(self.master, text="Student Management", font=('Arial', 16))
        self.label.pack(pady=10)

        self.add_student_btn = tk.Button(self.master, text="Add Student", command=self.add_student, width=20)
        self.add_student_btn.pack(pady=5)

        self.view_students_btn = tk.Button(self.master, text="View Students", command=self.view_students, width=20)
        self.view_students_btn.pack(pady=5)

        self.update_student_btn = tk.Button(self.master, text="Update Student", command=self.update_student, width=20)
        self.update_student_btn.pack(pady=5)

        self.delete_student_btn = tk.Button(self.master, text="Delete Student", command=self.delete_student, width=20)
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
        self.master.title("Add Student")
        self.create_widgets()

    def create_widgets(self):
        # Create entry fields for student information
        labels = ['Student ID:', 'Name:', 'Gender:', 'Phone Number:', 'ID Card Number:', 'Campus Code:', 'Date of Birth (YYYY-MM-DD):']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = tk.Label(self.master, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')

            if text == 'Gender:':
                self.gender_var = tk.StringVar(value="Male")
                gender_male = tk.Radiobutton(self.master, text="Male", variable=self.gender_var, value="Male")
                gender_female = tk.Radiobutton(self.master, text="Female", variable=self.gender_var, value="Female")
                gender_male.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                gender_female.grid(row=idx, column=1, padx=70, pady=5)
            else:
                entry = tk.Entry(self.master)
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[text] = entry

        self.add_btn = tk.Button(self.master, text="Add Student", command=self.add_student_to_db, width=15)
        self.add_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def add_student_to_db(self):
        student_data = (
            self.entries['Student ID:'].get(),
            self.entries['Name:'].get(),
            self.gender_var.get(),
            self.entries['Phone Number:'].get(),
            self.entries['ID Card Number:'].get(),
            self.entries['Campus Code:'].get(),
            self.entries['Date of Birth (YYYY-MM-DD):'].get(),
        )

        success = backend.add_student(student_data)
        if success:
            messagebox.showinfo("Success", "Student added successfully.")
            self.master.destroy()

class ViewStudentsWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("View Students")
        self.create_widgets()

    def create_widgets(self):
        # Create a Treeview to display students
        columns = ('StudentID', 'Name', 'Gender', 'PhoneNumber', 'IDCardNumber', 'CampusCode', 'DateOfBirth')
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
        self.master.title("Update Student")
        self.create_widgets()

    def create_widgets(self):
        self.student_id_label = tk.Label(self.master, text="Enter Student ID to Update:")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = tk.Entry(self.master)
        self.student_id_entry.pack(pady=5)

        self.fetch_btn = tk.Button(self.master, text="Fetch Data", command=self.fetch_student_data)
        self.fetch_btn.pack(pady=5)

    def fetch_student_data(self):
        student_id = self.student_id_entry.get()
        student_data = backend.get_student_by_id(student_id)
        if student_data:
            self.show_update_form(student_data)
        else:
            messagebox.showerror("Error", "Student not found.")

    def show_update_form(self, student_data):
        self.update_window = tk.Toplevel(self.master)
        self.update_window.title("Update Student Data")

        labels = ['Name:', 'Gender:', 'Phone Number:', 'ID Card Number:', 'Campus Code:', 'Date of Birth (YYYY-MM-DD):']
        self.entries = {}

        for idx, text in enumerate(labels):
            label = tk.Label(self.update_window, text=text)
            label.grid(row=idx, column=0, padx=5, pady=5, sticky='e')

            if text == 'Gender:':
                self.gender_var = tk.StringVar(value=student_data['Gender'])
                gender_male = tk.Radiobutton(self.update_window, text="Male", variable=self.gender_var, value="Male")
                gender_female = tk.Radiobutton(self.update_window, text="Female", variable=self.gender_var, value="Female")
                gender_male.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                gender_female.grid(row=idx, column=1, padx=70, pady=5)
            else:
                entry = tk.Entry(self.update_window)
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[text] = entry

                # Insert existing data
                if text == 'Name:':
                    entry.insert(0, student_data['Name'])
                elif text == 'Phone Number:':
                    entry.insert(0, student_data['PhoneNumber'])
                elif text == 'ID Card Number:':
                    entry.insert(0, student_data['IDCardNumber'])
                elif text == 'Campus Code:':
                    entry.insert(0, student_data['CampusCode'])
                elif text == 'Date of Birth (YYYY-MM-DD):':
                    entry.insert(0, student_data['DateOfBirth'])

        self.update_btn = tk.Button(self.update_window, text="Update Student",
                                    command=lambda: self.update_student_in_db(student_data['StudentID']), width=15)
        self.update_btn.grid(row=len(labels), column=0, columnspan=2, pady=10)

    def update_student_in_db(self, student_id):
        student_data = (
            self.entries['Name:'].get(),
            self.gender_var.get(),
            self.entries['Phone Number:'].get(),
            self.entries['ID Card Number:'].get(),
            self.entries['Campus Code:'].get(),
            self.entries['Date of Birth (YYYY-MM-DD):'].get(),
        )

        success = backend.update_student(student_id, student_data)
        if success:
            messagebox.showinfo("Success", "Student updated successfully.")
            self.update_window.destroy()
            self.master.destroy()

class DeleteStudentWindow:
    def __init__(self, master):
        self.master = tk.Toplevel(master)
        self.master.title("Delete Student")
        self.create_widgets()

    def create_widgets(self):
        self.student_id_label = tk.Label(self.master, text="Enter Student ID to Delete:")
        self.student_id_label.pack(pady=5)
        self.student_id_entry = tk.Entry(self.master)
        self.student_id_entry.pack(pady=5)

        self.delete_btn = tk.Button(self.master, text="Delete Student", command=self.delete_student_from_db)
        self.delete_btn.pack(pady=5)

    def delete_student_from_db(self):
        student_id = self.student_id_entry.get()
        success = backend.delete_student(student_id)
        if success:
            messagebox.showinfo("Success", "Student deleted successfully.")
            self.master.destroy()
        else:
            messagebox.showerror("Error", "Student not found or could not be deleted.")

if __name__ == '__main__':
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()
