import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class EmployeeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="cyan4")
        self.controller = controller
        
        # Initialize database
        self.init_database()

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

        button_frame = tk.Frame(self, bg="cyan4")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Employee", bg="lightgreen",
                  command=self.add_employee).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Delete Selected", bg="lightcoral",
                  command=self.delete_employee).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Refresh", bg="lightblue",
                  command=self.load_employees).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Dept", "Salary"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Dept", text="Department")
        self.tree.heading("Salary", text="Salary")
        
        # Set column widths
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=150)
        self.tree.column("Dept", width=150)
        self.tree.column("Salary", width=100)
        
        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        tk.Button(self, text="Back to Dashboard", bg="lightgray",
                  command=lambda: controller.show_frame("DashboardFrame")).pack(pady=10)
        
        # Load existing employees when frame is created
        self.load_employees()

    def init_database(self):
        """Initialize SQLite database and create employees table if it doesn't exist"""
        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL,
                    salary REAL NOT NULL
                )
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

    def add_employee(self):
        """Add employee to database and treeview"""
        name = self.name_entry.get().strip()
        dept = self.dept_entry.get().strip()
        salary = self.salary_entry.get().strip()
        
        if not name or not dept or not salary:
            messagebox.showwarning("Input Error", "Please fill in all fields")
            return
        
        try:
            salary_value = float(salary)
            if salary_value < 0:
                messagebox.showwarning("Input Error", "Salary must be positive")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Salary must be a valid number")
            return
        
        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (name, department, salary)
                VALUES (?, ?, ?)
            ''', (name, dept, salary_value))
            conn.commit()
            conn.close()
            
            # Clear entries
            self.name_entry.delete(0, "end")
            self.dept_entry.delete(0, "end")
            self.salary_entry.delete(0, "end")
            
            # Reload the treeview
            self.load_employees()
            messagebox.showinfo("Success", "Employee added successfully")
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add employee: {e}")

    def load_employees(self):
        """Load all employees from database into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, department, salary FROM employees ORDER BY id')
            rows = cursor.fetchall()
            conn.close()
            
            for row in rows:
                self.tree.insert("", "end", values=row)
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load employees: {e}")

    def delete_employee(self):
        """Delete selected employee from database and treeview"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select an employee to delete")
            return
        
        # Get the employee ID from the selected row
        employee_id = self.tree.item(selected_item[0])['values'][0]
        employee_name = self.tree.item(selected_item[0])['values'][1]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {employee_name}?"):
            try:
                conn = sqlite3.connect('payroll.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
                conn.commit()
                conn.close()
                
                # Reload the treeview
                self.load_employees()
                messagebox.showinfo("Success", "Employee deleted successfully")
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete employee: {e}")