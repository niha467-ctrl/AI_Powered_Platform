# USER INTERFACE DEVELOPMENT SYSTEM (SINGLE FILE - TKINTER)

import tkinter as tk
from tkinter import messagebox, ttk
import time


# -----------------------------
# APP STATE
# -----------------------------

class AppState:
    def __init__(self):
        self.user = None
        self.data = []


state = AppState()


# -----------------------------
# MAIN APP
# -----------------------------

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("UI Development System")
        self.geometry("800x500")
        self.resizable(False, False)

        self.frames = {}

        for F in (LoginPage, DashboardPage, FormPage):
            frame = F(self)
            self.frames[F] = frame
            frame.place(x=0, y=0, width=800, height=500)

        self.show_frame(LoginPage)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


# -----------------------------
# LOGIN PAGE
# -----------------------------

class LoginPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="LOGIN", font=("Arial", 24, "bold")).pack(pady=40)

        tk.Label(self, text="Username").pack()
        self.username = tk.Entry(self)
        self.username.pack()

        tk.Label(self, text="Password").pack()
        self.password = tk.Entry(self, show="*")
        self.password.pack()

        tk.Button(
            self,
            text="Login",
            command=self.login
        ).pack(pady=20)

    def login(self):
        user = self.username.get()
        pwd = self.password.get()

        if user == "admin" and pwd == "1234":
            state.user = user
            messagebox.showinfo("Success", "Login Successful")
            self.master.show_frame(DashboardPage)
        else:
            messagebox.showerror("Error", "Invalid credentials")


# -----------------------------
# DASHBOARD PAGE
# -----------------------------

class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="DASHBOARD", font=("Arial", 22, "bold")).pack(pady=20)

        self.label = tk.Label(self, text="")
        self.label.pack()

        tk.Button(
            self,
            text="Add Data",
            command=lambda: parent.show_frame(FormPage)
        ).pack(pady=10)

        tk.Button(
            self,
            text="Refresh Table",
            command=self.load_table
        ).pack(pady=10)

        tk.Button(
            self,
            text="Logout",
            command=self.logout
        ).pack(pady=10)

        # Table
        self.tree = ttk.Treeview(self, columns=("Name", "Time"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Time", text="Timestamp")
        self.tree.pack(fill="both", expand=True, pady=20)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.load_table()

    def load_table(self):
        self.tree.delete(*self.tree.get_children())

        for item in state.data:
            self.tree.insert("", "end", values=(item["name"], item["time"]))

    def logout(self):
        state.user = None
        self.master.show_frame(LoginPage)


# -----------------------------
# FORM PAGE
# -----------------------------

class FormPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        tk.Label(self, text="ADD DATA", font=("Arial", 22, "bold")).pack(pady=20)

        tk.Label(self, text="Enter Name").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        tk.Button(
            self,
            text="Save",
            command=self.save_data
        ).pack(pady=10)

        tk.Button(
            self,
            text="Back to Dashboard",
            command=lambda: parent.show_frame(DashboardPage)
        ).pack(pady=10)

    def save_data(self):
        name = self.name_entry.get()

        if not name:
            messagebox.showerror("Error", "Name required")
            return

        state.data.append({
            "name": name,
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        })

        messagebox.showinfo("Saved", "Data added successfully")
        self.name_entry.delete(0, tk.END)


# -----------------------------
# RUN APP
# -----------------------------

if __name__ == "__main__":
    app = Application()
    app.mainloop()