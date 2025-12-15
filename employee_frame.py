import tkinter as tk
from tkinter import ttk

class EmployeeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="cyan4")
        self.controller = controller

        tk.Label(self, text="Employee Management", font=("Arial", 20, "bold"), bg="white").pack(pady=20)

        form_frame = tk.Frame(self, bg="white")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:", bg="white").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Department:", bg="white").grid(row=1, column=0, padx=10, pady=5)
        self.dept_entry = tk.Entry(form_frame)
        self.dept_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Salary:", bg="white").grid(row=2, column=0, padx=10, pady=5)
        self.salary_entry = tk.Entry(form_frame)
        self.salary_entry.grid(row=2, column=1, padx=10)

        tk.Button(self, text="Add Employee", bg="lightgreen",
                  command=self.add_employee).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("Name", "Dept", "Salary"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Dept", text="Department")
        self.tree.heading("Salary", text="Salary")
        self.tree.pack(pady=10, fill="x")

        tk.Button(self, text="Back to Dashboard", bg="lightgray",
                  command=lambda: controller.show_frame("DashboardFrame")).pack(pady=10)

    def add_employee(self):
        name = self.name_entry.get()
        dept = self.dept_entry.get()
        salary = self.salary_entry.get()
        if name and dept and salary:
            self.tree.insert("", "end", values=(name, dept, salary))
            self.name_entry.delete(0, "end")
            self.dept_entry.delete(0, "end")
            self.salary_entry.delete(0, "end")
