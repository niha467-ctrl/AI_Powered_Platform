"""
UI Enhancements (Single File)
Modern Tkinter Dashboard with:
✔ Sidebar Navigation
✔ Top Header
✔ Light/Dark Theme Toggle
✔ Search Box
✔ Statistics Cards
✔ Progress Bars
✔ Data Table
✔ Status Bar
✔ Responsive Layout
✔ Refresh Functionality
"""

import tkinter as tk
from tkinter import ttk
import random
import time

# ----------------------------------
# MAIN APPLICATION
# ----------------------------------

class ModernDashboard(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Financial Settlement Dashboard")
        self.geometry("1200x700")
        self.minsize(1000,600)

        self.dark_mode = False

        self.configure_theme()

        self.create_sidebar()
        self.create_header()
        self.create_dashboard()
        self.create_statusbar()

        self.load_data()

    # ----------------------------------
    # THEMES
    # ----------------------------------

    def configure_theme(self):

        if self.dark_mode:
            self.bg = "#202124"
            self.card = "#303134"
            self.text = "white"
        else:
            self.bg = "#F5F7FA"
            self.card = "white"
            self.text = "black"

        self.configure(bg=self.bg)

    def toggle_theme(self):

        self.dark_mode = not self.dark_mode
        self.destroy()

        app = ModernDashboard()
        app.dark_mode = self.dark_mode
        app.configure_theme()
        app.mainloop()

    # ----------------------------------
    # SIDEBAR
    # ----------------------------------

    def create_sidebar(self):

        self.sidebar = tk.Frame(
            self,
            width=220,
            bg="#2C3E50"
        )

        self.sidebar.pack(side="left", fill="y")

        title = tk.Label(
            self.sidebar,
            text="AI Dashboard",
            fg="white",
            bg="#2C3E50",
            font=("Arial",18,"bold")
        )

        title.pack(pady=20)

        menus = [
            "Dashboard",
            "Loans",
            "Settlements",
            "Customers",
            "Analytics",
            "Reports",
            "Settings"
        ]

        for menu in menus:

            b = tk.Button(
                self.sidebar,
                text=menu,
                relief="flat",
                fg="white",
                bg="#2C3E50",
                activebackground="#34495E",
                activeforeground="white",
                font=("Arial",11),
                padx=20,
                pady=10
            )

            b.pack(fill="x", padx=10, pady=3)

    # ----------------------------------
    # HEADER
    # ----------------------------------

    def create_header(self):

        self.header = tk.Frame(
            self,
            bg=self.card,
            height=60
        )

        self.header.pack(fill="x")

        tk.Label(
            self.header,
            text="Financial Health & Settlement System",
            bg=self.card,
            fg=self.text,
            font=("Arial",18,"bold")
        ).pack(side="left", padx=20)

        self.search = tk.Entry(
            self.header,
            width=30
        )

        self.search.pack(side="left", padx=20)

        tk.Button(
            self.header,
            text="Search",
            command=self.search_data
        ).pack(side="left")

        tk.Button(
            self.header,
            text="Refresh",
            command=self.load_data
        ).pack(side="right", padx=10)

        tk.Button(
            self.header,
            text="Theme",
            command=self.toggle_theme
        ).pack(side="right")

    # ----------------------------------
    # DASHBOARD
    # ----------------------------------

    def create_dashboard(self):

        self.main = tk.Frame(
            self,
            bg=self.bg
        )

        self.main.pack(fill="both", expand=True)

        self.cards = tk.Frame(
            self.main,
            bg=self.bg
        )

        self.cards.pack(fill="x", pady=10)

        self.card_labels=[]

        metrics=[
            "Customers",
            "Loans",
            "Settlements",
            "Recovered"
        ]

        for metric in metrics:

            card=tk.Frame(
                self.cards,
                bg=self.card,
                width=220,
                height=90,
                relief="ridge",
                bd=1
            )

            card.pack(side="left", padx=10)

            tk.Label(
                card,
                text=metric,
                bg=self.card,
                fg=self.text,
                font=("Arial",12)
            ).pack()

            value=tk.Label(
                card,
                text="0",
                bg=self.card,
                fg="blue",
                font=("Arial",24,"bold")
            )

            value.pack()

            self.card_labels.append(value)

        # Progress

        self.progress=ttk.Progressbar(
            self.main,
            orient="horizontal",
            length=500,
            mode="determinate"
        )

        self.progress.pack(pady=10)

        # Table

        cols=(
            "Customer",
            "Loan",
            "Settlement",
            "Health Score"
        )

        self.tree=ttk.Treeview(
            self.main,
            columns=cols,
            show="headings",
            height=15
        )

        for c in cols:
            self.tree.heading(c,text=c)
            self.tree.column(c,width=180)

        self.tree.pack(fill="both",expand=True,padx=10)

    # ----------------------------------
    # STATUS BAR
    # ----------------------------------

    def create_statusbar(self):

        self.status=tk.Label(
            self,
            text="Ready",
            bd=1,
            relief="sunken",
            anchor="w"
        )

        self.status.pack(fill="x",side="bottom")

    # ----------------------------------
    # LOAD DATA
    # ----------------------------------

    def load_data(self):

        self.tree.delete(*self.tree.get_children())

        customers=random.randint(100,500)
        loans=random.randint(50,300)
        settlements=random.randint(20,150)
        recovered=random.randint(100000,900000)

        values=[
            customers,
            loans,
            settlements,
            f"₹{recovered:,}"
        ]

        for i,v in enumerate(values):
            self.card_labels[i].config(text=str(v))

        for i in range(1,21):

            loan=random.randint(50000,400000)
            settle=random.randint(30000,loan)
            health=random.randint(40,100)

            self.tree.insert(
                "",
                "end",
                values=(
                    f"Customer {i}",
                    f"₹{loan:,}",
                    f"₹{settle:,}",
                    health
                )
            )

        self.progress["value"]=random.randint(40,100)

        self.status.config(
            text="Last Updated : "+time.strftime("%H:%M:%S")
        )

    # ----------------------------------
    # SEARCH
    # ----------------------------------

    def search_data(self):

        keyword=self.search.get().lower()

        for item in self.tree.get_children():

            values=self.tree.item(item)["values"]

            if keyword in str(values).lower():

                self.tree.selection_set(item)
                self.tree.focus(item)
                self.tree.see(item)
                break

        self.status.config(text="Search Completed")


# ----------------------------------
# RUN APPLICATION
# ----------------------------------

if __name__=="__main__":
    app=ModernDashboard()
    app.mainloop()