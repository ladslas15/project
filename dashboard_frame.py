import tkinter as tk

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="cyan4")
        self.controller = controller

        tk.Label(self, text="Dashboard", font=("Arial", 24, "bold"), bg="white").pack(pady=30)

        tk.Button(self, text="Manage Employees", width=20, height=2, bg="lightgreen",
                  command=lambda: controller.show_frame("EmployeeFrame")).pack(pady=10)

        tk.Button(self, text="Payroll Calculator", width=20, height=2, bg="lightyellow",
                  command=lambda: controller.show_frame("PayrollFrame")).pack(pady=10)

        tk.Button(self, text="Reports", width=20, height=2, bg="lightblue",
                  command=lambda: controller.show_frame("ReportsFrame")).pack(pady=10)

        tk.Button(self, text="Logout", width=20, height=2, bg="lightcoral",
                  command=lambda: controller.show_frame("LoginFrame")).pack(pady=10)
