import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ReportsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(
            self, 
            text="Employee Reports", 
            font=("Arial", 20, "bold"), 
            bg="white"
        ).pack(pady=15)

        # Control buttons frame
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="🔄 Refresh",
            bg="#43a047",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.load_employee_reports,
            width=12
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Return to Dashboard",
            bg="#757575",
            fg="white",
            font=("Arial", 11, "bold"),
            command=lambda: controller.show_frame("DashboardFrame"),
            width=18
        ).pack(side="left", padx=5)

        # Search frame
        search_frame = tk.Frame(self, bg="white")
        search_frame.pack(pady=5)
        
        tk.Label(search_frame, text="Search by Name:", bg="white").pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=25)
        self.search_entry.pack(side="left", padx=5)
        
        tk.Button(
            search_frame,
            text="Search",
            bg="#1e88e5",
            fg="white",
            command=self.search_employee
        ).pack(side="left", padx=5)
        
        tk.Button(
            search_frame,
            text="Show All",
            bg="#1e88e5",
            fg="white",
            command=self.load_employee_reports
        ).pack(side="left", padx=5)

        # Table frame with scrollbar
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        self.tree = ttk.Treeview(
            table_frame,
            columns=("ID", "Name", "Department", "Salary"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.tree.yview)

        # Column headings
        self.tree.heading("ID", text="Employee ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Salary", text="Salary")
        
        # Column widths
        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Department", width=150, anchor="center")
        self.tree.column("Salary", width=150, anchor="e")

        self.tree.pack(fill="both", expand=True)
        
        # Summary frame
        summary_frame = tk.Frame(self, bg="#f5f5f5", relief="ridge", bd=2)
        summary_frame.pack(fill="x", padx=20, pady=10)
        
        self.summary_label = tk.Label(
            summary_frame, 
            text="Total Employees: 0 | Total Salary Budget: UGX 0",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#1e88e5",
            pady=10
        )
        self.summary_label.pack()
        
        # Department breakdown
        self.dept_label = tk.Label(
            summary_frame,
            text="",
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#424242"
        )
        self.dept_label.pack()
        
        # Load data on startup
        self.load_employee_reports()

    def load_employee_reports(self):
        """Load all employees from the database"""
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, name, department, salary FROM employees ORDER BY name')
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo(
                    "No Data", 
                    "No employees found in the database.\n\nGo to Employee Management to add employees."
                )
                self.update_summary([], {})
                return

            total_salary = 0
            dept_stats = {}
            
            for emp_id, name, department, salary in rows:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        emp_id,
                        name,
                        department,
                        f"UGX {salary:,.0f}"
                    )
                )
                total_salary += salary
                
                # Track department statistics
                if department not in dept_stats:
                    dept_stats[department] = {'count': 0, 'total': 0}
                dept_stats[department]['count'] += 1
                dept_stats[department]['total'] += salary
            
            self.update_summary(rows, dept_stats)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load employees: {e}")
            self.update_summary([], {})
    
    def search_employee(self):
        """Search for employees by name"""
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            messagebox.showwarning("Search Error", "Please enter a name to search")
            return
        
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            conn = sqlite3.connect('payroll.db')
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, name, department, salary FROM employees WHERE LOWER(name) LIKE ? ORDER BY name',
                (f'%{search_term}%',)
            )
            rows = cursor.fetchall()
            conn.close()
            
            if not rows:
                messagebox.showinfo("No Results", f"No employees found matching '{search_term}'")
                self.update_summary([], {})
                return
            
            total_salary = 0
            dept_stats = {}
            
            for emp_id, name, department, salary in rows:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        emp_id,
                        name,
                        department,
                        f"UGX {salary:,.0f}"
                    )
                )
                total_salary += salary
                
                if department not in dept_stats:
                    dept_stats[department] = {'count': 0, 'total': 0}
                dept_stats[department]['count'] += 1
                dept_stats[department]['total'] += salary
            
            self.update_summary(rows, dept_stats)
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to search employees: {e}")
    
    def update_summary(self, rows, dept_stats):
        """Update summary labels"""
        total_employees = len(rows)
        total_salary = sum(row[3] for row in rows) if rows else 0
        
        self.summary_label.config(
            text=f"Total Employees: {total_employees} | Total Salary Budget: UGX {total_salary:,.0f}"
        )
        
        # Update department breakdown
        if dept_stats:
            dept_text = "Department Breakdown: "
            dept_info = []
            for dept, stats in dept_stats.items():
                dept_info.append(f"{dept}: {stats['count']} employees (UGX {stats['total']:,.0f})")
            dept_text += " | ".join(dept_info)
            self.dept_label.config(text=dept_text)
        else:
            self.dept_label.config(text="")