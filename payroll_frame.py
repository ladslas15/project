import tkinter as tk

class PayrollFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="cyan4")
        self.controller = controller

        tk.Label(self, text="Payroll Calculator", font=("Arial", 20, "bold"), bg="white").pack(pady=20)

        form = tk.Frame(self, bg="white")
        form.pack()

        tk.Label(form, text="Basic Salary:", bg="white").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(form, text="Allowances:", bg="white").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(form, text="Tax Deduction:", bg="white").grid(row=2, column=0, padx=10, pady=5)

        self.basic = tk.Entry(form)
        self.allow = tk.Entry(form)
        self.tax = tk.Entry(form)

        self.basic.grid(row=0, column=1)
        self.allow.grid(row=1, column=1)
        self.tax.grid(row=2, column=1)

        tk.Button(self, text="Calculate Net Salary", bg="lightgreen",
                  command=self.calculate_salary).pack(pady=10)

        self.result = tk.Label(self, text="Net Salary: UGX 0", font=("Arial", 14), bg="white")
        self.result.pack(pady=10)

        tk.Button(self, text="Back to Dashboard", bg="lightgray",
                  command=lambda: controller.show_frame("DashboardFrame")).pack(pady=10)

    def calculate_salary(self):
        try:
            basic = float(self.basic.get())
            allow = float(self.allow.get())
            tax = float(self.tax.get())
            net = basic + allow - tax
            self.result.config(text=f"Net Salary: UGX {net:,.2f}")
        except ValueError:
            self.result.config(text="Please enter valid numbers")
