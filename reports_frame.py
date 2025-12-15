import tkinter as tk
from tkinter import ttk

class ReportsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text="Payroll Reports", font=("Arial", 20, "bold"), bg="white").pack(pady=20)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Net Salary", "Date"), show="headings")
        self.tree.heading("ID", text="Emp ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Net Salary", text="Net Salary")
        self.tree.heading("Date", text="Date Paid")
        self.tree.pack(pady=10, fill="x")

        # sample data
        self.tree.insert("", "end", values=("E001", "Batimbo Ladslas", "UGX 1,200,000", "2025-11-01"))
        self.tree.insert("", "end", values=("E002", "Kayanja Samuel", "UGX 950,000", "2025-11-05"))

        tk.Button(self, text="Back to Dashboard", bg="lightgray",
                  command=lambda: controller.show_frame("DashboardFrame")).pack(pady=10)
