import tkinter as tk
from login_frame import LoginFrame
from dashboard_frame import DashboardFrame
from employee_frame import EmployeeFrame
from payroll_frame import PayrollFrame
from reports_frame import ReportsFrame

class PayrollApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Payroll Management System")
        self.geometry("900x600")
        self.resizable(False, False)

        # ---- Container holds all frames ----
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Allow the container to expand in all directions
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # ---- Register all frames ----
        for F in (LoginFrame, DashboardFrame, EmployeeFrame, PayrollFrame, ReportsFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame

            # Make each frame fill the container fully
            frame.grid(row=0, column=0, sticky="nsew")

        # Start with login page
        self.show_frame("LoginFrame")

    def show_frame(self, frame_name):
        """Raise the requested frame"""
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == "__main__":
    app = PayrollApp()
    app.mainloop()
