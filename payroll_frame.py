import tkinter as tk
from tkinter import ttk, messagebox

class PayrollFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="cyan4")
        self.controller = controller

        tk.Label(self, text="Payroll Calculator", font=("Arial", 20, "bold"), bg="white").pack(pady=20)

        # Input form
        form = tk.Frame(self, bg="white")
        form.pack(pady=10)

        tk.Label(form, text="Basic Salary:", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(form, text="Allowances:", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(form, text="Other Deductions:", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.basic = tk.Entry(form, width=20)
        self.allow = tk.Entry(form, width=20)
        self.other_deductions = tk.Entry(form, width=20)

        self.basic.grid(row=0, column=1, padx=10, pady=5)
        self.allow.grid(row=1, column=1, padx=10, pady=5)
        self.other_deductions.grid(row=2, column=1, padx=10, pady=5)
        self.other_deductions.insert(0, "0")

        # Buttons frame (side by side)
        buttons_frame = tk.Frame(self, bg="cyan4")
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="Calculate Net Salary", bg="lightgreen",
                  command=self.calculate_salary).pack(side="left", padx=10)
        tk.Button(buttons_frame, text="Back to Dashboard", bg="lightgray",
                  command=lambda: controller.show_frame("DashboardFrame")).pack(side="left", padx=10)

        # Results frame
        results_frame = tk.Frame(self, bg="white", relief="ridge", borderwidth=2)
        results_frame.pack(pady=10, padx=20, fill="both")

        tk.Label(results_frame, text="Salary Breakdown", font=("Arial", 14, "bold"), 
                bg="white").grid(row=0, column=0, columnspan=2, pady=10)

        # Gross Salary
        tk.Label(results_frame, text="Gross Salary:", font=("Arial", 11, "bold"),
                bg="white").grid(row=1, column=0, padx=20, pady=5, sticky="w")
        self.gross_label = tk.Label(results_frame, text="UGX 0.00", font=("Arial", 11),
                                   bg="white", fg="blue")
        self.gross_label.grid(row=1, column=1, padx=20, pady=5, sticky="e")

        # NSSF Deduction
        tk.Label(results_frame, text="NSSF (10%):", font=("Arial", 11, "bold"),
                bg="white").grid(row=2, column=0, padx=20, pady=5, sticky="w")
        self.nssf_label = tk.Label(results_frame, text="UGX 0.00", font=("Arial", 11),
                                  bg="white", fg="red")
        self.nssf_label.grid(row=2, column=1, padx=20, pady=5, sticky="e")

        # Chargeable Income
        tk.Label(results_frame, text="Chargeable Income:", font=("Arial", 11),
                bg="white").grid(row=3, column=0, padx=20, pady=5, sticky="w")
        self.chargeable_label = tk.Label(results_frame, text="UGX 0.00", font=("Arial", 11),
                                        bg="white")
        self.chargeable_label.grid(row=3, column=1, padx=20, pady=5, sticky="e")

        # PAYE Deduction
        tk.Label(results_frame, text="PAYE:", font=("Arial", 11, "bold"),
                bg="white").grid(row=4, column=0, padx=20, pady=5, sticky="w")
        self.paye_label = tk.Label(results_frame, text="UGX 0.00", font=("Arial", 11),
                                  bg="white", fg="red")
        self.paye_label.grid(row=4, column=1, padx=20, pady=5, sticky="e")

        # Other Deductions
        tk.Label(results_frame, text="Other Deductions:", font=("Arial", 11, "bold"),
                bg="white").grid(row=5, column=0, padx=20, pady=5, sticky="w")
        self.other_ded_label = tk.Label(results_frame, text="UGX 0.00", font=("Arial", 11),
                                       bg="white", fg="red")
        self.other_ded_label.grid(row=5, column=1, padx=20, pady=5, sticky="e")

        # Separator line
        ttk.Separator(results_frame, orient="horizontal").grid(row=6, column=0, columnspan=2, 
                                                               sticky="ew", padx=20, pady=10)

        # Total Deductions
        tk.Label(results_frame, text="Total Deductions:", font=("Arial", 11, "bold"),
                bg="white").grid(row=7, column=0, padx=20, pady=5, sticky="w")
        self.total_ded_label = tk.Label(results_frame, text="UGX 0.00", font=("Arial", 11, "bold"),
                                       bg="white", fg="darkred")
        self.total_ded_label.grid(row=7, column=1, padx=20, pady=5, sticky="e")

        # Net Salary (prominent display)
        self.result = tk.Label(self, text="Net Salary: UGX 0.00", 
                              font=("Arial", 16, "bold"), bg="yellow", 
                              relief="raised", padx=20, pady=10)
        self.result.pack(pady=15)

    def calculate_nssf(self, gross_salary):
        nssf_rate = 0.10
        nssf_ceiling = 2_000_000
        nssf_base = min(gross_salary, nssf_ceiling)
        nssf = nssf_base * nssf_rate
        return nssf

    def calculate_paye(self, chargeable_income):
        if chargeable_income <= 235_000:
            paye = 0
        elif chargeable_income <= 335_000:
            paye = (chargeable_income - 235_000) * 0.10
        elif chargeable_income <= 410_000:
            paye = (100_000 * 0.10) + (chargeable_income - 335_000) * 0.20
        elif chargeable_income <= 10_000_000:
            paye = (100_000 * 0.10) + (75_000 * 0.20) + (chargeable_income - 410_000) * 0.30
        else:
            paye = (100_000 * 0.10) + (75_000 * 0.20) + (9_590_000 * 0.30) + (chargeable_income - 10_000_000) * 0.40
        return paye

    def calculate_salary(self):
        try:
            basic = float(self.basic.get())
            allow = float(self.allow.get())
            other_ded = float(self.other_deductions.get())
            
            if basic < 0 or allow < 0 or other_ded < 0:
                messagebox.showwarning("Input Error", "Values cannot be negative")
                return
            
            gross_salary = basic + allow
            nssf = self.calculate_nssf(gross_salary)
            chargeable_income = gross_salary - nssf
            paye = self.calculate_paye(chargeable_income)
            total_deductions = nssf + paye + other_ded
            net_salary = gross_salary - total_deductions
            
            self.gross_label.config(text=f"UGX {gross_salary:,.2f}")
            self.nssf_label.config(text=f"UGX {nssf:,.2f}")
            self.chargeable_label.config(text=f"UGX {chargeable_income:,.2f}")
            self.paye_label.config(text=f"UGX {paye:,.2f}")
            self.other_ded_label.config(text=f"UGX {other_ded:,.2f}")
            self.total_ded_label.config(text=f"UGX {total_deductions:,.2f}")
            self.result.config(text=f"Net Salary: UGX {net_salary:,.2f}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers")
            self.gross_label.config(text="UGX 0.00")
            self.nssf_label.config(text="UGX 0.00")
            self.chargeable_label.config(text="UGX 0.00")
            self.paye_label.config(text="UGX 0.00")
            self.other_ded_label.config(text="UGX 0.00")
            self.total_ded_label.config(text="UGX 0.00")
            self.result.config(text="Net Salary: UGX 0.00")
