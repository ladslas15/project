import tkinter as tk
from tkinter import messagebox
import hashlib
from database.db import get_connection  # make sure this returns a valid DB connection


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="cyan4")
        self.controller = controller

        # Title
        tk.Label(self, text="Payroll Login", font=("Arial", 20, "bold"), bg="lightblue").pack(pady=40)

        # Username
        tk.Label(self, text="Username:", bg="lightblue").pack(pady=5)
        self.username = tk.Entry(self, width=30)
        self.username.pack()

        # Password
        tk.Label(self, text="Password:", bg="lightblue").pack(pady=5)
        self.password = tk.Entry(self, width=30, show="*")
        self.password.pack()

        # Login Button
        tk.Button(self, text="Login", bg="dodgerblue", fg="white",
                  command=self.login).pack(pady=20)

        # Optional: Bind Enter key to login
        self.bind_all("<Return>", lambda event: self.login())

    # Hash password using SHA-256
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Login function
    def login(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (self.username.get(),)
        )

        result = cursor.fetchone()
        conn.close()

        if result and result[0] == self.hash_password(self.password.get()):
            self.controller.show_frame("DashboardFrame")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.password.delete(0, tk.END)  # clear password field
