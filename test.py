import tkinter as tk
import pandas as pd
from tkinter import font as tkfont, ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import bcrypt
from tkcalendar import DateEntry
from datetime import datetime
import csv

class AlohaCorpApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aloha Corp")
        self.geometry("700x700")
        self.bg_color = "#f7f9fc"
        self.accent_color = "#007acc"
        self.configure(bg=self.bg_color)

        # Fonts
        self.header_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.sub_font = tkfont.Font(family="Segoe UI", size=12)

        # Mode flag: "login" or "create"
        self.current_mode = None

        # For store or role selection
        self.selected_store = None
        self.selected_role = None

        self.style = ttk.Style(self)
        self.style.theme_use("clam")  # Try 'alt' or 'default' too
        self.style.configure("TButton", font=("Segoe UI", 10), padding=6)
        self.style.configure("TLabel", background=self.bg_color)

        # ----------------------------------------------------------------
        # DATABASE CONNECTION & TABLE CREATION
        # ----------------------------------------------------------------
        try:
            self.connection = mysql.connector.connect(
                host="localhost",    # or your host address
                user="root",         # replace with your MySQL username
                password="root",     # replace with your MySQL password
                database="triall"    # replace with your database name
            )
            if self.connection.is_connected():
                print("Successfully connected to MySQL database")
                self.create_users_table()  # Create (or confirm) the users table if it doesn't exist
                self.create_invoices_table()
                self.create_merchandise_table()
                self.create_expenses_table()
                self.create_employee_bonus_table()
                self.create_employee_rates_table()
                self.create_withdrawals_table()
                self.create_payroll_table()
                self.create_day_closeout_table()
                self.create_in_out_bal_table()
            else:
                print("Connection failed")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

        # Create the top menu bar
        self.create_top_bar()

        #self.initiate_login()


        # Main content area
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.page_frame = tk.Frame(self)  # Frame for records (Treeview) to show up
        self.page_frame.pack(fill=tk.BOTH, expand=False)

        # Initially hide Treeview until data is fetched
        self.tree = ttk.Treeview(self.page_frame, show='headings')
        self.tree.pack_forget()  # Keep it hidden initially

        # Show the welcome screen
        self.show_welcome_screen()

    def create_users_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(255) NOT NULL
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
        except Error as err:
            print(f"Error creating users table: {err}")

    def create_invoices_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(50),
    date_received DATE,
    company VARCHAR(255),
    invoice_number VARCHAR(50),
    amount DECIMAL(10,2),
    location VARCHAR(255),
    date_due DATE
)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
        except Error as err:
            print(f"Error creating invoices table: {err}")

    def create_expenses_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_type VARCHAR(255),
    expense_value DECIMAL(10,2),
    location VARCHAR(255),
    date DATE
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating expenses table: {err}")

    def create_in_out_bal_table(self):
        create_table_query = """
                CREATE TABLE IF NOT EXISTS in_out_bal (
        id INT AUTO_INCREMENT PRIMARY KEY,
        emp_id INT,
        in_bal DECIMAL(10,2),
        out_bal DECIMAL(10,2),
        clock_in TIME,
        clock_out TIME,
        date DATE,
        location VARCHAR(255)
    )
                """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
        except Error as err:
            print(f"Error creating expenses table: {err}")

    def create_merchandise_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS merchandise (
    id INT AUTO_INCREMENT PRIMARY KEY,
    merchandise_type VARCHAR(255),
    merchandise_value DECIMAL(10,2),
    location VARCHAR(255),
    date DATE
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating merchandise table: {err}")

    def create_withdrawals_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS withdrawals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    user_id INT,
    location VARCHAR(255),
    amount DECIMAL(10,2)
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating withdrawals table: {err}")

    def create_employee_bonus_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employee_bonus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    location VARCHAR(255),
    start_date DATE,
    end_date DATE,
    bonus_amount DECIMAL(10,2)
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating bonus table: {err}")

    def create_employee_rates_table(self):
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employee_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    location VARCHAR(255),
    bonus_rate DECIMAL(5,2),
    rate_per_hour DECIMAL(10,2),
    date DATE
)
            """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
            except Error as err:
                print(f"Error creating rates table: {err}")

    def create_payroll_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS payroll (
            id INT AUTO_INCREMENT PRIMARY KEY,
            employee_id INT,
            store VARCHAR(255),
            start_date DATE,
            end_date DATE,
            total_hours DECIMAL(10,2),
            rate_per_hour DECIMAL(10,2),
            subtotal DECIMAL(10,2),
            bonus DECIMAL(10,2),
            total_payroll DECIMAL(10,2)    
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
        except Error as err:
            print(f"Error creating payroll table: {err}")

    def create_day_closeout_table(self):
            create_table_query = """
                CREATE TABLE IF NOT EXISTS day_closeout (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    cash DECIMAL(10,2),
    credit DECIMAL(10,2),
    total DECIMAL(10,2),
    difference DECIMAL(10,2),
    date DATE,
    location VARCHAR(255),
    notes TEXT
)
                """
            try:
                cursor = self.connection.cursor()
                cursor.execute(create_table_query)
                self.connection.commit()
                print("Users table is ready.")
            except Error as err:
                print(f"Error creating users table: {err}")

    def initiate_login(self):
        # function to create initial owner login
        pass1 = 'pass'
        hashed_pass1 = bcrypt.hashpw(pass1.encode('utf-8'), bcrypt.gensalt())
        insert_query = "INSERT INTO users (ID, name, password, role) VALUES (%s, %s, %s, %s)"
        cursor = self.connection.cursor()
        cursor.execute(insert_query, (123, 'andrew', hashed_pass1, 'Owner'))
        self.connection.commit()

    def create_top_bar(self):
        top_bar = tk.Frame(self, bg="white", height=40)
        top_bar.pack(side="top", fill="x")

        # Back button
        back_button = tk.Button(
            top_bar,
            text="← Back",
            bg="white",
            fg="black",
            bd=0,
            activebackground="white",
            command=self.go_back
        )
        back_button.pack(side="left", padx=10, pady=5)

        # 3-dot menu button
        menu_button = tk.Menubutton(
            top_bar,
            text="⋮",
            bg="white",
            fg="black",
            bd=0,
            activebackground="white"
        )
        menu_button.pack(side="right", padx=10, pady=5)

        dot_menu = tk.Menu(menu_button, tearoff=0)
        dot_menu.add_command(label="Sign Out", command=self.option1_action)
        dot_menu.add_command(label="Change Theme", command=self.toggle_dark_mode)

        # 1) Add our new 'Change Password' menu item
        dot_menu.add_command(label="Change Password", command=self.show_change_password_form)

        menu_button["menu"] = dot_menu

    def show_change_password_form(self):
        """
        Displays a form for changing the current user's password.
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Change Password",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Old Password
        old_pass_label = tk.Label(
            self.main_frame,
            text="Old Password:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        old_pass_label.pack(pady=(5, 2))
        self.old_password_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.old_password_entry.pack(pady=(0, 10))

        # New Password
        new_pass_label = tk.Label(
            self.main_frame,
            text="New Password:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        new_pass_label.pack(pady=(5, 2))
        self.new_password_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.new_password_entry.pack(pady=(0, 10))

        # Confirm New Password
        confirm_pass_label = tk.Label(
            self.main_frame,
            text="Confirm New Password:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        confirm_pass_label.pack(pady=(5, 2))
        self.confirm_password_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.confirm_password_entry.pack(pady=(0, 20))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_change_password
        )
        submit_button.pack(pady=10)

    def toggle_dark_mode(self):
        if hasattr(self, 'dark_mode') and self.dark_mode:
            self.dark_mode = False
            self.set_theme(light=True)
        else:
            self.dark_mode = True
            self.set_theme(light=False)

    def set_theme(self, light=True):
        bg = "white" if light else "#1e1e1e"
        fg = "black" if light else "#f5f5f5"
        entry_bg = "white" if light else "#333333"
        entry_fg = "black" if light else "#f5f5f5"
        btn_bg = "black" if light else "#444444"
        btn_fg = "white"
        highlight_color = "#666" if not light else "#ccc"

        self.configure(bg=bg)

        def apply_theme(widget):
            widget_type = widget.winfo_class()

            if widget_type in ("Frame", "LabelFrame", "TFrame"):
                widget.configure(bg=bg)
            elif widget_type in ("Label", "Menubutton"):
                widget.configure(bg=bg, fg=fg)
            elif widget_type == "Button":
                widget.configure(bg=btn_bg, fg=btn_fg)
            elif widget_type in ("Entry", "TEntry"):
                widget.configure(bg=entry_bg, fg=entry_fg, insertbackground=entry_fg)
            elif widget_type == "TCombobox":
                style = ttk.Style()
                theme_style = "dark.TCombobox" if not light else "light.TCombobox"
                style.theme_use("default")
                style.configure(theme_style,
                                fieldbackground=entry_bg,
                                background=entry_bg,
                                foreground=entry_fg)
                widget.configure(style=theme_style)
            elif widget_type == "Canvas":
                widget.configure(bg=bg)

            for child in widget.winfo_children():
                apply_theme(child)

        apply_theme(self)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ----------------------------------------------------------------
    # WELCOME SCREEN
    # ----------------------------------------------------------------
    def show_welcome_screen(self):
        self.current_mode = None
        self.clear_main_frame()


        heading_label = tk.Label(
            self.main_frame,
            text="Welcome",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(40, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="Sign in to continue.",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        welcome_label = ttk.Label(
            self.main_frame,
            text="👋 Welcome to Aloha Corp",
            font=self.header_font,
            foreground=self.accent_color
        )
        welcome_label.pack(pady=(60, 10))

        subtitle = ttk.Label(
            self.main_frame,
            text="Your all-in-one business dashboard",
            font=self.sub_font,
            foreground="#555"
        )
        subtitle.pack(pady=(0, 40))

        # Login button
        login_button = tk.Button(
            self.main_frame,
            text="Login",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.login_action
        )
        login_button.pack(pady=5)

        # Create New Account button
        create_account_button = tk.Button(
            self.main_frame,
            text="Create New Account",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.create_account_action
        )
        create_account_button.pack(pady=5)

    # ----------------------------------------------------------------
    # LOGIN FLOW
    # ----------------------------------------------------------------
    def login_action(self):
        self.current_mode = "login"
        self.show_store_selection()

    def show_store_selection(self):
        self.clear_main_frame()
        heading_label = tk.Label(
            self.main_frame,
            text="Login",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="Select Location",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 10))

        # Displaying store selection (not used in DB queries here)
        stores = ["Store 1", "Store 2", "Store 3"]
        self.store_var = tk.StringVar()
        self.store_var.set(stores[0])
        store_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.store_var,
            values=stores,
            state="readonly"
        )
        store_dropdown.pack(pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.handle_store_selection
        )
        submit_button.pack(pady=10)

    def handle_store_selection(self):
        self.selected_store = self.store_var.get()
        self.show_login_form()

    def show_login_form(self):
        self.clear_main_frame()

        label = tk.Label(
            self.main_frame,
            text=f"Login - {self.selected_store}",
            bg="white",
            fg="black",
            font=self.header_font
        )
        label.pack(pady=(20, 10))

        # Username field (stored in DB as 'name')
        username_label = tk.Label(
            self.main_frame,
            text="Username:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        username_label.pack(pady=(5, 2))
        self.username_entry = tk.Entry(self.main_frame, width=30)
        self.username_entry.pack(pady=(0, 20))  # extra space after username

        # Password field
        password_label = tk.Label(
            self.main_frame,
            text="Password:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        password_label.pack(pady=(0, 2))
        self.password_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.password_entry.pack(pady=(0, 10))

        login_btn = tk.Button(
            self.main_frame,
            text="Login",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_login
        )
        login_btn.pack(pady=10)

    def process_login(self):
        """
        Logs in a user (e.g., employees, managers, owners).
        If the user has a 'Manager' or 'Owner' role, we direct them
        to the manager/owner home screens after verifying the password.
        If 'Employee', show the employee home screen.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id, password, role FROM users WHERE name = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Login Error", "Invalid username.")
                return

            user_id, stored_password, role = result
            self.user_role = role

            # Verify the password using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                # 1) Store the current user's ID for future reference
                self.logged_in_user_id = user_id
                self.logged_in_username = username  # store the username

                messagebox.showinfo("Success", f"Welcome, {username}!")

                # 2) Navigate to the appropriate home screen
                if role == "Manager":
                    self.show_manager_home()
                elif role == "Owner":
                    self.show_owner_home()
                elif role == "Employee":
                    self.show_employee_home()
                else:
                    # For other roles, you could show a different screen
                    messagebox.showinfo("Info", f"No specific home screen for role: {role}")
            else:
                messagebox.showerror("Login Error", "Incorrect password.")
        except Error as err:
            messagebox.showerror("Database Error", f"Error during login: {err}")

    def process_change_password(self):
        # Step 1: Retrieve form data
        old_pass = self.old_password_entry.get()
        new_pass = self.new_password_entry.get()
        confirm_pass = self.confirm_password_entry.get()

        if not (old_pass and new_pass and confirm_pass):
            messagebox.showerror("Error", "All fields are required.")
            return

        if not hasattr(self, 'logged_in_user_id'):
            messagebox.showerror("Error", "No user is currently logged in. Cannot change password.")
            return

        user_id = self.logged_in_user_id

        # Step 2: Check old password
        try:
            cursor = self.connection.cursor()
            query = "SELECT password FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "User record not found.")
                return

            db_hashed_password = result[0]

            # verify old password
            if not bcrypt.checkpw(old_pass.encode('utf-8'), db_hashed_password.encode('utf-8')):
                messagebox.showerror("Error", "Old password is incorrect.")
                return

        except Error as err:
            messagebox.showerror("Database Error", f"Error fetching current password: {err}")
            return

        # Step 3: Validate new password match
        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New password and confirmation do not match.")
            return

        # Step 4: Update DB with new hashed password
        try:
            hashed_new_pass = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            update_query = "UPDATE users SET password = %s WHERE id = %s"
            cursor.execute(update_query, (hashed_new_pass, user_id))
            self.connection.commit()

            messagebox.showinfo("Success", "Password changed successfully!")
            self.go_back()  # Return to the appropriate screen

        except Error as err:
            messagebox.showerror("Database Error", f"Could not update password: {err}")

    # ----------------------------------------------------------------
    # CREATE ACCOUNT FLOW (Manager/Owner login only)
    # ----------------------------------------------------------------
    def create_account_action(self):
        self.current_mode = "create"
        self.show_role_selection()

    def show_role_selection(self):
        self.clear_main_frame()
        heading_label = tk.Label(
            self.main_frame,
            text="Create New Account",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="Select Role",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 10))

        roles = ["Manager", "Owner"]
        self.role_var = tk.StringVar()
        self.role_var.set(roles[0])

        role_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.role_var,
            values=roles,
            state="readonly"
        )
        role_dropdown.pack(pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.handle_role_selection
        )
        submit_button.pack(pady=10)

    def handle_role_selection(self):
        self.selected_role = self.role_var.get()
        # For demonstration, we'll default managers/owners to "Store 1"
        self.selected_store = "Store 1"
        self.show_manager_owner_login_form()

    def show_manager_owner_login_form(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Login",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You are logging in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Username field (stored in DB as 'name')
        username_label = tk.Label(
            self.main_frame,
            text="USERNAME",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        username_label.pack(pady=(0, 2))
        self.new_username_entry = tk.Entry(self.main_frame, width=30)
        self.new_username_entry.pack(pady=(0, 20))  # extra space after username

        # Password field
        password_label = tk.Label(
            self.main_frame,
            text="PASSWORD",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        password_label.pack(pady=(0, 2))
        self.new_password_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.new_password_entry.pack(pady=(0, 10))

        create_btn = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_manager_owner_login
        )
        create_btn.pack(pady=10)

    def process_manager_owner_login(self):
        """
        Attempts to log in an existing Manager/Owner (no new account insertion).
        """
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id, password FROM users WHERE name = %s AND role = %s"
            cursor.execute(query, (username, self.selected_role))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Login Error", "User not found or role mismatch.")
                return

            user_id, stored_password = result
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                messagebox.showinfo("Welcome", f"You are logged in as {username} ({self.selected_role}).")
                if self.selected_role == "Manager":
                    self.show_manager_home()
                else:
                    self.show_owner_home()
            else:
                messagebox.showerror("Login Error", "Incorrect password.")

        except Error as err:
            messagebox.showerror("Database Error", f"Error during login: {err}")

    # ----------------------------------------------------------------
    # EMPLOYEE HOME & FORMS
    # ----------------------------------------------------------------
    def show_employee_home(self):
        """
        Displays the Employee Home screen with the three buttons:
        1) Enter Day Closeout
        2) Enter In/Out Balance
        3) Enter Expense
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Employee Home",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="WHAT DID YOU WANT TO DO?",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack()

        employee_options = [
            "Enter Day Closeout",
            "Enter In/Out Balance",
            "Enter Expense"
        ]

        for option in employee_options:
            btn = tk.Button(
                button_frame,
                text=option,
                bg="white",
                fg="black",
                width=20,
                height=2,
                command=lambda opt=option: self.employee_option_action(opt)
            )
            btn.pack(pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.submit_employee_actions
        )
        submit_button.pack(pady=20)

    def employee_option_action(self, option):
        if option == "Enter Day Closeout":
            self.show_day_closeout_form()
        elif option == "Enter In/Out Balance":
            self.show_in_out_balance_form()
        elif option == "Enter Expense":
            self.show_expense_form()
        else:
            messagebox.showinfo("Employee Action", f"You clicked: {option}")

    def submit_employee_actions(self):
        messagebox.showinfo("Submit", "Employee actions submitted (placeholder).")

    def show_day_closeout_form(self):
        """
        Displays a form for entering day closeout data.
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Enter Day Closeout",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You’re logged in as {self.logged_in_username} in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )


        sub_label.pack(pady=(0, 20))

        # Employee Username
        emp_label = tk.Label(self.main_frame, text="EMPLOYEE ID", bg="white", fg="black", font=self.sub_font)
        emp_label.pack(pady=(0, 2))
        self.dayclose_emp_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_emp_entry.pack(pady=(0, 10))

        # Cash
        cash_label = tk.Label(self.main_frame, text="CASH", bg="white", fg="black", font=self.sub_font)
        cash_label.pack(pady=(0, 2))
        self.dayclose_cash_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_cash_entry.pack(pady=(0, 10))

        # Credit
        credit_label = tk.Label(self.main_frame, text="CREDIT", bg="white", fg="black", font=self.sub_font)
        credit_label.pack(pady=(0, 2))
        self.dayclose_credit_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_credit_entry.pack(pady=(0, 10))

        # Total
        total_label = tk.Label(self.main_frame, text="TOTAL", bg="white", fg="black", font=self.sub_font)
        total_label.pack(pady=(0, 2))
        self.dayclose_total_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_total_entry.pack(pady=(0, 10))

        # Difference
        diff_label = tk.Label(self.main_frame, text="DIFFERENCE", bg="white", fg="black", font=self.sub_font)
        diff_label.pack(pady=(0, 2))
        self.dayclose_diff_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_diff_entry.pack(pady=(0, 10))


        # Date (dropdown)
        date_label = tk.Label(self.main_frame, text="DATE", bg="white", fg="black", font=self.sub_font)
        date_label.pack(pady=(0, 2))
        self.dayclose_date_dropdown = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.dayclose_date_dropdown.pack(pady=(0, 10))

        # Notes
        notes_label = tk.Label(self.main_frame, text="NOTES", bg="white", fg="black", font=self.sub_font)
        notes_label.pack(pady=(0, 2))
        self.dayclose_notes_entry = tk.Entry(self.main_frame, width=30)
        self.dayclose_notes_entry.pack(pady=(0, 10))

        # sign up (submit) button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_day_closeout
        )
        submit_button.pack(pady=10)

    def process_day_closeout(self):
        """
        Processes the day closeout form.
        Retrieves the entered data, displays the values for confirmation,
        validates the input, and inserts the record into the day_closeout table.
        """
        emp_id = self.dayclose_emp_entry.get()
        cash = self.dayclose_cash_entry.get()
        credit = self.dayclose_credit_entry.get()
        total = self.dayclose_total_entry.get()
        diff = self.dayclose_diff_entry.get()
        # Retrieve the date from the DateEntry widget; ensure it's stored as an instance variable.
        date_val = self.dayclose_date_dropdown.get()
        location = self.selected_store
        notes = self.dayclose_notes_entry.get()

        # Display the entered values for confirmation.
        messagebox.showinfo(
            "Day Closeout Submitted",
            f"Employee: {emp_id}\n"
            f"Cash: {cash}\n"
            f"Credit: {credit}\n"
            f"Total: {total}\n"
            f"Difference: {diff}\n"
            f"Date: {date_val}\n"
            f"Notes: {notes}"
        )

        # Check for a valid database connection.
        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id FROM users WHERE id = %s"
            cursor.execute(query, (emp_id,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "Employee ID not found.")
                return

        except Error as err:
            messagebox.showerror("Database Error", "Error fetching employee ID")
            return  # Ensure function exits on database error

        # Validate that all required fields are provided.
        if not (emp_id and cash and credit and total and diff and date_val and location):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO day_closeout 
                (employee_id, cash, credit, total, difference, date, notes, location) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (emp_id, cash, credit, total, diff, date_val, notes, location))
            self.connection.commit()
            messagebox.showinfo("Success", "Day closeout data added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Day closeout data not added")

    def show_in_out_balance_form(self):
        """
        Displays a form for entering In/Out Balance data.
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Enter In/Out Balance",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You’re logged in as {self.logged_in_username} in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )


        sub_label.pack(pady=(0, 20))

        # Employee Username
        emp_label = tk.Label(self.main_frame, text="EMPLOYEE ID", bg="white", fg="black", font=self.sub_font)
        emp_label.pack(pady=(0, 2))
        self.inout_emp_entry = tk.Entry(self.main_frame, width=30)
        self.inout_emp_entry.pack(pady=(0, 10))

        # In Balance
        in_label = tk.Label(self.main_frame, text="IN BALANCE", bg="white", fg="black", font=self.sub_font)
        in_label.pack(pady=(0, 2))
        self.in_balance_entry = tk.Entry(self.main_frame, width=30)
        self.in_balance_entry.pack(pady=(0, 10))

        # Out Balance
        out_label = tk.Label(self.main_frame, text="OUT BALANCE", bg="white", fg="black", font=self.sub_font)
        out_label.pack(pady=(0, 2))
        self.out_balance_entry = tk.Entry(self.main_frame, width=30)
        self.out_balance_entry.pack(pady=(0, 10))


        # Clock-In Time
        cin_label = tk.Label(self.main_frame, text="CLOCK-IN TIME (HH:MM)", bg="white", fg="black", font=self.sub_font)
        cin_label.pack(pady=(0, 2))

        clockin_frame = tk.Frame(self.main_frame, bg="white")
        clockin_frame.pack(pady=(0, 10))

        # Spinbox for hours (00 to 23)
        self.clockin_hour_spin = tk.Spinbox(clockin_frame, from_=0, to=23, width=3, format="%02.0f")
        self.clockin_hour_spin.pack(side=tk.LEFT)

        # Colon separator
        tk.Label(clockin_frame, text=":", bg="white", fg="black", font=self.sub_font).pack(side=tk.LEFT)

        # Spinbox for minutes (00 to 59)
        self.clockin_min_spin = tk.Spinbox(clockin_frame, from_=0, to=59, width=3, format="%02.0f")
        self.clockin_min_spin.pack(side=tk.LEFT)

        # Clock-Out Time
        cout_label = tk.Label(self.main_frame, text="CLOCK-OUT TIME (HH:MM)", bg="white", fg="black",
                              font=self.sub_font)
        cout_label.pack(pady=(0, 2))

        clockout_frame = tk.Frame(self.main_frame, bg="white")
        clockout_frame.pack(pady=(0, 10))

        # Spinbox for hours (00 to 23)
        self.clockout_hour_spin = tk.Spinbox(clockout_frame, from_=0, to=23, width=3, format="%02.0f")
        self.clockout_hour_spin.pack(side=tk.LEFT)

        # Colon separator
        tk.Label(clockout_frame, text=":", bg="white", fg="black", font=self.sub_font).pack(side=tk.LEFT)

        # Spinbox for minutes (00 to 59)
        self.clockout_min_spin = tk.Spinbox(clockout_frame, from_=0, to=59, width=3, format="%02.0f")
        self.clockout_min_spin.pack(side=tk.LEFT)

        # Date (dropdown)
        date_label = tk.Label(self.main_frame, text="DATE", bg="white", fg="black", font=self.sub_font)
        date_label.pack(pady=(0, 2))
        self.inout_date_dropdown = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.inout_date_dropdown.pack(pady=(0, 10))

        # Location (dropdown)
        location_label = tk.Label(
            self.main_frame,
            text="LOCATION",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        location_label.pack(pady=(0, 2))
        self.location_var = tk.StringVar()
        # Example location list
        locations = ["Select", "Store 1", "Store 2", "Store 3"]
        self.location_var.set(locations[0])
        location_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.location_var,
            values=locations,
            state="readonly",
            width=28
        )
        location_dropdown.pack(pady=(0, 10))

        # sign up (submit) button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_in_out_balance
        )
        submit_button.pack(pady=10)

    def process_in_out_balance(self):
        """
        Just shows a message for now (no DB insert).
        """
        emp_id = self.inout_emp_entry.get()
        in_balance = self.in_balance_entry.get()
        out_balance = self.out_balance_entry.get()
        # clock_in = self.clockin_entry.get()
        # clock_out = self.clockout_entry.get()
        date_val = self.inout_date_dropdown.get()
        location = self.location_var.get()
        clock_in_hour = self.clockin_hour_spin.get()
        clock_in_min = self.clockin_min_spin.get()
        clock_in = f"{clock_in_hour}:{clock_in_min}"

        clock_out_hour = self.clockout_hour_spin.get()
        clock_out_min = self.clockout_min_spin.get()
        clock_out = f"{clock_out_hour}:{clock_out_min}"

        messagebox.showinfo(
            "In/Out Balance",
            f"Employee: {emp_id}\nIn Balance: {in_balance}\nOut Balance: {out_balance}\n"
            f"Clock-In: {clock_in}\nClock-Out: {clock_out}\nDate: {date_val}"
        )


        if not (emp_id and in_balance and out_balance and clock_in and clock_out):
            messagebox.showerror("Error", "All fields are required.")
            return

        # Convert numeric fields: emp_id should be an integer, balances should be floats.
        try:
            emp_id_val = int(emp_id)
            in_balance_val = float(in_balance)
            out_balance_val = float(out_balance)
        except ValueError:
            messagebox.showerror("Error",
                                 "Please enter valid numeric values for Employee ID, In Balance, and Out Balance.")
            return

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id FROM users WHERE id = %s"
            cursor.execute(query, (emp_id,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "Employee ID not found.")
                return

        except Error as err:
            messagebox.showerror("Database Error", "Error fetching employee ID")
            return  # Ensure function exits on database error

        # Validate that all required fields are provided.
        if not (emp_id and in_balance and out_balance and clock_in and clock_out and date_val and location):
            messagebox.showerror("Error", "All fields are required.")
            return

        # Insert the record into the database.
        try:
            cursor = self.connection.cursor()
            insert_query = """
                   INSERT INTO in_out_bal (emp_id, in_bal, out_bal, clock_in, clock_out)
                   VALUES (%s, %s, %s, %s, %s)
               """
            cursor.execute(insert_query, (emp_id_val, in_balance_val, out_balance_val, clock_in, clock_out))
            query = """
                        INSERT INTO in_out_bal 
                        (emp_id, in_bal, out_bal, clock_in, clock_out, date, location) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (emp_id, in_balance, out_balance, clock_in, clock_out, date_val, location))
            self.connection.commit()
            messagebox.showinfo("Success", "In/Out balance record inserted successfully.")
            self.go_back()  # Optionally, navigate back to the previous screen.
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to insert record: {e}")

    def show_expense_form(self):
        """
        Displays a form for entering an expense.
        """
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Enter Expense",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You’re logged in as {self.logged_in_username} in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Expense Type
        type_label = tk.Label(self.main_frame, text="EXPENSE TYPE", bg="white", fg="black", font=self.sub_font)
        type_label.pack(pady=(0, 2))
        self.expense_type_entry = tk.Entry(self.main_frame, width=30)
        self.expense_type_entry.pack(pady=(0, 10))

        # Expense Value
        val_label = tk.Label(self.main_frame, text="EXPENSE VALUE", bg="white", fg="black", font=self.sub_font)
        val_label.pack(pady=(0, 2))
        self.expense_value_entry = tk.Entry(self.main_frame, width=30)
        self.expense_value_entry.pack(pady=(0, 10))

        # Date (calendar)
        date_label = tk.Label(self.main_frame, text="DATE", bg="white", fg="black", font=self.sub_font)
        date_label.pack(pady=(0, 2))
        self.expense_date_var = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.expense_date_var.pack(pady=(0, 10))


        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_expense
        )
        submit_button.pack(pady=10)

    def process_expense(self):
        """
        Just shows a message for now (no DB insert).
        """
        expense_type = self.expense_type_entry.get()
        expense_value = self.expense_value_entry.get()
        date_val = self.expense_date_var.get()
        location = self.selected_store

        messagebox.showinfo(
            "Enter Expense",
            f"Expense Type: {expense_type}\nExpense Value: {expense_value}\nDate: {date_val}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (expense_type and expense_value and date_val and location):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO expenses (expense_type, expense_value, date, location) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (expense_type, expense_value, date_val, location))
            self.connection.commit()
            messagebox.showinfo("Success", "Expense added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Expense not added")

    # ----------------------------------------------------------------
    # MANAGER & OWNER HOME SCREENS
    # ----------------------------------------------------------------
    def show_manager_home(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Manager Home",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="WHAT DID YOU WANT TO DO?",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack()

        manager_options = [
            "Enter Invoice",
            "Enter Expense",
            "Enter Day Closeout",
            "Enter Withdraw",
            "Calculate Employee Bonus",
            "Add Employee",
            "Set Employee Rates",
            "View Records",
            "Payroll",
            "Enter Merchandise"
        ]

        for i, option in enumerate(manager_options):
            btn = tk.Button(
                button_frame,
                text=option,
                bg="white",
                fg="black",
                width=20,
                height=2,
                command=lambda opt=option: self.manager_option_action(opt)
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.submit_manager_actions
        )
        submit_button.pack(pady=20)

    def manager_option_action(self, option):
        if option == "Add Employee":
            self.show_add_employee_form()
        elif option == "Enter Expense":
            self.show_expense_form()
        elif option == "Enter Invoice":
            self.show_invoice_form()
        elif option == "Calculate Employee Bonus":
            self.show_calc_bonus_form()
        elif option == "Set Employee Rates":
            self.show_set_rates_form()
        elif option == "Enter Merchandise":
            self.show_merchandise_form()
        elif option == "Enter Withdraw":
            self.show_withdraw_form()
        elif option == "Payroll":
            self.show_payroll_form()
        else:
            messagebox.showinfo("Manager Action", f"You clicked: {option}")

    def submit_manager_actions(self):
        messagebox.showinfo("Submit", "Manager actions submitted (placeholder).")

    def show_owner_home(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Owner Home",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="WHAT DID YOU WANT TO DO?",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        button_frame = tk.Frame(self.main_frame, bg="white")
        button_frame.pack()

        owner_options = [
            "Enter Invoice",
            "Enter Expense",
            "Enter Day Closeout",
            "Enter Withdraw",
            "Calculate Employee Bonus",
            "Add Employee",
            "Set Employee Rates",
            "View Records",
            "Payroll",
            "Enter Merchandise"
        ]

        for i, option in enumerate(owner_options):
            btn = tk.Button(
                button_frame,
                text=option,
                bg="white",
                fg="black",
                width=20,
                height=2,
                command=lambda opt=option: self.owner_option_action(opt)
            )
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=5)

        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.submit_owner_actions
        )
        submit_button.pack(pady=20)

    def owner_option_action(self, option):
        if option == "Add Employee":
            self.show_add_employee_form()
        elif option == "Enter Expense":
            self.show_expense_form()
        elif option == "Enter Day Closeout":
            self.show_day_closeout_form()
        elif option == "Enter Invoice":
            self.show_invoice_form()
        elif option == "Calculate Employee Bonus":
            self.show_calc_bonus_form()
        elif option == "Set Employee Rates":
            self.show_set_rates_form()
        elif option == "Enter Merchandise":
            self.show_merchandise_form()
        elif option == "Enter Withdraw":
            self.show_withdraw_form()
        elif option == "Payroll":
            self.show_payroll_form()
        elif option == "View Records":
            self.show_records_form()
        else:
            messagebox.showinfo("Owner Action", f"You clicked: {option}")

    def submit_owner_actions(self):
        messagebox.showinfo("Submit", "Owner actions submitted (placeholder).")

    def show_records_form(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="View Records",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading
        sub_label = tk.Label(
            self.main_frame,
            text="Select Records to View",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Location (dropdown)
        location_label = tk.Label(
            self.main_frame,
            text="LOCATION",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        location_label.pack(pady=(0, 2))
        self.location_var = tk.StringVar()
        # Example location list
        locations = ["Select", "Store 1", "Store 2", "Store 3"]
        self.location_var.set(locations[0])
        location_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.location_var,
            values=locations,
            state="readonly",
            width=28
        )
        location_dropdown.pack(pady=(0, 10))

        # Record Type
        record_label = tk.Label(
            self.main_frame,
            text="RECORD TYPE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        record_label.pack(pady=(0, 2))
        self.record_var = tk.StringVar()
        # Example records list
        records = ["Select", "Invoices", "Expenses", "Merchandise", "Bonuses", "Day Closeouts", "In/Out Balances"]
        self.record_var.set(records[0])
        records_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.record_var,
            values=records,
            state="readonly",
            width=28
        )
        records_dropdown.pack(pady=(0, 10))

        # Start Date (DateEntry)
        start_label = tk.Label(
            self.main_frame,
            text="START DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        start_label.pack(pady=(0, 2))

        self.start_date = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.start_date.pack(pady=(0, 10))

        # End Date (DateEntry)
        end_label = tk.Label(
            self.main_frame,
            text="END DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        end_label.pack(pady=(0, 2))
        self.end_date = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.end_date.pack(pady=(0, 20))

        # Submit button – same style as in Add Employee form.
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_records
        )
        submit_button.pack(pady=10)

        export_button = tk.Button(
            self.main_frame,
            text="Export to CSV",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.export_to_csv
        )
        export_button.pack(pady=10)

        # Create the Treeview widget once
        self.tree = ttk.Treeview(self.page_frame, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.pack_forget()  # Hide it initially

        self.total_label = tk.Label(self.page_frame, text="", bg="white", fg="black", font=self.sub_font)
        self.total_label.pack(pady=(20, 20))
        self.total_label.pack_forget()  # Hide it initially

    def show_records_form(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="View Records",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading
        sub_label = tk.Label(
            self.main_frame,
            text="Select Records to View",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Location (dropdown)
        location_label = tk.Label(
            self.main_frame,
            text="LOCATION",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        location_label.pack(pady=(0, 2))
        self.location_var = tk.StringVar()
        # Example location list
        locations = ["Select", "Store 1", "Store 2", "Store 3"]
        self.location_var.set(locations[0])
        location_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.location_var,
            values=locations,
            state="readonly",
            width=28
        )
        location_dropdown.pack(pady=(0, 10))

        # Record Type
        record_label = tk.Label(
            self.main_frame,
            text="RECORD TYPE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        record_label.pack(pady=(0, 2))
        self.record_var = tk.StringVar()
        # Example records list
        records = ["Select", "Invoices", "Expenses", "Merchandise", "Bonuses", "Day Closeouts", "In/Out Balances"]
        self.record_var.set(records[0])
        records_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.record_var,
            values=records,
            state="readonly",
            width=28
        )
        records_dropdown.pack(pady=(0, 10))

        # Start Date (DateEntry)
        start_label = tk.Label(
            self.main_frame,
            text="START DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        start_label.pack(pady=(0, 2))

        self.start_date = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.start_date.pack(pady=(0, 10))

        # End Date (DateEntry)
        end_label = tk.Label(
            self.main_frame,
            text="END DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        end_label.pack(pady=(0, 2))
        self.end_date = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.end_date.pack(pady=(0, 20))

        # Submit button – same style as in Add Employee form.
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_records
        )
        submit_button.pack(pady=10)

        export_button = tk.Button(
            self.main_frame,
            text="Export to CSV",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.export_to_csv
        )
        export_button.pack(pady=10)

        # Create the Treeview widget once
        self.tree = ttk.Treeview(self.page_frame, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.pack_forget()  # Hide it initially

        self.total_label = tk.Label(self.page_frame, text="", bg="white", fg="black", font=self.sub_font)
        self.total_label.pack(pady=(20, 20))
        self.total_label.pack_forget()  # Hide it initially

    def process_records(self):
        self.tree.pack_forget()
        self.tree = ttk.Treeview(self.page_frame, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.total_label.pack_forget()  # Hide it initially
        self.total_label = tk.Label(self.page_frame, text="", bg="white", fg="black", font=self.sub_font)
        self.total_label.pack(pady=(20, 20))

        # 1) grab base filters
        location = self.location_var.get()
        record = self.record_var.get()
        start = self.start_date.get()
        end = self.end_date.get()

        # 2) validate
        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return
        if record == "Select" or not (location and start and end):
            messagebox.showerror("Error", "All fields are required.")
            return

        # 3) if invoices, store filters & show invoice-only form
        if record == "Invoices":
            self._invoice_base = {"location": location, "start": start, "end": end}
            return self.show_invoice_filters()

        # 4) generic lookup for other record types
        rec_map = {
            "Expenses": ("expenses", "date"),
            "Merchandise": ("merchandise", "date"),
            "Bonuses": ("employee_bonus", "start_date"),
            "Day Closeouts": ("day_closeout", "date"),
            "In/Out Balances": ("in_out_bal", "date"),
        }
        rec_type, date_name = rec_map.get(record, (None, None))
        if not rec_type:
            return

        try:
            cursor = self.connection.cursor()
            sql = f"SELECT * FROM {rec_type} WHERE location=%s AND {date_name}>=%s AND {date_name}<=%s"
            cursor.execute(sql, (location, start, end))
            rows = cursor.fetchall()
            if not rows:
                messagebox.showerror("Error", "No records found.")
                return

            cols = [d[0] for d in cursor.description]
            self.exported_data = rows
            self.exported_columns = cols

            self.tree["columns"] = cols
            self.tree.delete(*self.tree.get_children())

            for col in cols:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)

            for row in rows:
                self.tree.insert("", tk.END, values=row)

            self.tree.pack(fill=tk.BOTH, expand=True)

            # render table
            self.tree.pack_forget()
            self.tree = ttk.Treeview(self.page_frame, columns=cols, show='headings')
            for c in cols:
                self.tree.heading(c, text=c)
                self.tree.column(c, width=100)
            for r in rows:
                self.tree.insert("", tk.END, values=r)
            self.tree.pack(fill=tk.BOTH, expand=True)

            # (Insert your Day Closeouts / sum logic here)
            # Update Treeview
            self.tree["columns"] = cols
            self.tree.delete(*self.tree.get_children())

            for col in cols:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=100)

            for row in rows:
                self.tree.insert("", tk.END, values=row)

            self.tree.pack(fill=tk.BOTH, expand=True)

            if record == "Day Closeouts":
                total_sum = sum(float(row[4]) for row in rows if row[4] is not None)
                cash_sum = sum(float(row[2]) for row in rows if row[2] is not None)
                credit_sum = sum(float(row[3]) for row in rows if row[3] is not None)

                cursor = self.connection.cursor()
                query = f"SELECT * FROM expenses WHERE location = %s and date >= %s and date <= %s"
                cursor.execute(query, (location, start, end))
                expenses = cursor.fetchall()
                total_expenses = sum(float(row[2]) for row in expenses if row[2] is not None)

                query = f"SELECT * FROM merchandise WHERE location = %s and date >= %s and date <= %s"
                cursor.execute(query, (location, start, end))
                merchandise = cursor.fetchall()
                total_merchandise = sum(float(row[2]) for row in merchandise if row[2] is not None)

                profit = total_sum - total_expenses - total_merchandise

                self.total_label.config(
                    text=f"Cash Total: ${cash_sum:,.2f}      Credit Total: ${credit_sum:,.2f}      Gross Profit: ${total_sum:,.2f}      Net Profit: ${profit:,.2f}")
                self.total_label.pack()


            elif record == "Invoices":

                cursor = self.connection.cursor()
                query = f"SELECT * FROM invoices WHERE location = %s and status = %s and date_received >= %s and date_received <= %s"
                cursor.execute(query, (location, 'Not Paid', start, end))
                invoices = cursor.fetchall()
                total_invoices = sum(float(row[5]) for row in invoices if row[5] is not None)

                self.total_label.config(text=f"Total Unpaid Invoices: ${total_invoices:,.2f}")
                self.total_label.pack()

            else:

                # Try to find and sum a relevant amount column
                amount_column_candidates = ['expense_value', 'merchandise_value', 'amount', 'bonus_amount', 'total']
                amount_col_index = None
                for candidate in amount_column_candidates:
                    if candidate in cols:
                        amount_col_index = cols.index(candidate)
                        break

                if amount_col_index is not None:
                    total_sum = sum(float(row[amount_col_index]) for row in rows if row[amount_col_index] is not None)
                    if cols[amount_col_index] == "total":
                        self.total_label.config(text=f"Total: ${total_sum:,.2f}")
                        self.total_label.pack()
                    else:
                        self.total_label.config(text=f"Total {cols[amount_col_index].capitalize()}: ${total_sum:,.2f}")
                        self.total_label.pack()
                else:
                    self.total_label.config(text="")
                    self.total_label.pack_forget()

        except Error as err:
            messagebox.showerror("Database Error", "Records not found")

    def show_invoice_filters(self):
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Invoices – Filters",
                 bg="white", fg="black", font=self.header_font) \
            .pack(pady=(20, 10))

        # Status
        tk.Label(self.main_frame, text="STATUS", bg="white", fg="black", font=self.sub_font) \
            .pack(pady=(0, 2))
        self.status_var = tk.StringVar(value="All")
        ttk.Combobox(self.main_frame, textvariable=self.status_var,
                     values=["All", "Paid", "Not Paid"], state="readonly", width=28) \
            .pack(pady=(0, 10))

        # Order by due date
        tk.Label(self.main_frame, text="ORDER BY", bg="white", fg="black", font=self.sub_font) \
            .pack(pady=(0, 2))
        self.order_var = tk.StringVar(value="None")
        ttk.Combobox(self.main_frame, textvariable=self.order_var,
                     values=["None", "Due Date ↑", "Due Date ↓"], state="readonly", width=28) \
            .pack(pady=(0, 20))

        tk.Button(self.main_frame, text="Show Invoices", bg="black", fg="white",
                  width=20, height=2, command=self.process_invoices_filter) \
            .pack(pady=10)

    def process_invoices_filter(self):
        # pull base filters
        base = getattr(self, "_invoice_base", {})
        location = base.get("location", "")
        start = base.get("start", "")
        end = base.get("end", "")
        status = self.status_var.get()
        order = self.order_var.get()

        # build query
        sql = ("SELECT * FROM invoices "
               "WHERE location=%s AND date_received>=%s AND date_received<=%s")
        params = [location, start, end]
        if status in ("Paid", "Not Paid"):
            sql += " AND status=%s"
            params.append(status)
        if order != "None":
            direction = "ASC" if order.endswith("↑") else "DESC"
            sql += f" ORDER BY date_due {direction}"

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            if not rows:
                messagebox.showerror("Error", "No invoices found.")
                return

            cols = [d[0] for d in cursor.description]
            self.exported_data = rows
            self.exported_columns = cols

            # render table
            self.tree.pack_forget()
            self.tree = ttk.Treeview(self.page_frame, columns=cols, show='headings')
            for c in cols:
                self.tree.heading(c, text=c)
                self.tree.column(c, width=100)
            for r in rows:
                self.tree.insert("", tk.END, values=r)
            self.tree.pack(fill=tk.BOTH, expand=True)

            edit_button = tk.Button(
                self.page_frame,
                text="Edit Selected Invoice",
                bg="darkblue",
                fg="white",
                command=self.edit_selected_invoice
            )
            edit_button.pack(pady=10)

            # sum unpaid
            amt_idx = cols.index("amount")
            stat_idx = cols.index("status")
            total_unpaid = sum(float(r[amt_idx]) for r in rows if r[stat_idx] == "Not Paid")
            self.total_label.config(text=f"Total Unpaid Invoices: ${total_unpaid:,.2f}")
            self.total_label.pack(pady=10)

        except Error as err:
            messagebox.showerror("Database Error", str(err))

    def edit_selected_invoice(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select an invoice to edit.")
            return

        values = self.tree.item(selected, 'values')
        self.selected_invoice = dict(zip(self.exported_columns, values))
        self.show_invoice_edit_form()

    def show_invoice_edit_form(self):
        self.clear_main_frame()

        tk.Label(self.main_frame, text="Edit Invoice", font=self.header_font).pack(pady=10)
        self.invoice_fields = {}

        for col, val in self.selected_invoice.items():
            if col == "id":
                continue  # Don't edit the primary key

            tk.Label(self.main_frame, text=col, font=self.sub_font).pack()

            if col == "status":
                var = tk.StringVar(value=val)
                field = ttk.Combobox(self.main_frame, textvariable=var,
                                     values=["Paid", "Not Paid"], state="readonly", width=28)
            elif col in ["date_received", "date_due"]:
                # Use DateEntry for dates
                field = DateEntry(self.main_frame, width=28, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern="yyyy-mm-dd")
                field.set_date(val)
            else:
                field = tk.Entry(self.main_frame, width=30)
                field.insert(0, val)

            field.pack(pady=(0, 10))
            self.invoice_fields[col] = field

        # Submit button
        tk.Button(self.main_frame, text="Save Changes", bg="green", fg="white",
                  width=20, height=2, command=self.save_invoice_changes).pack(pady=20)

    def save_invoice_changes(self):
        try:
            updated = {col: field.get() for col, field in self.invoice_fields.items()}
            invoice_id = self.selected_invoice["id"]

            # Build SQL
            columns = ", ".join(f"{col} = %s" for col in updated.keys())
            values = list(updated.values()) + [invoice_id]
            query = f"UPDATE invoices SET {columns} WHERE id = %s"

            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()

            messagebox.showinfo("Success", "Invoice updated successfully.")
            # Hide the old table and totals
            self.tree.pack_forget()
            self.total_label.pack_forget()
            self.show_records_form()

        except Error as e:
            messagebox.showerror("Error", f"Failed to update invoice: {e}")


    def export_to_csv(self):
        """
        Exports the most recently fetched data (rows + column names)
        to a CSV file.
        """
        # Check if we have any data stored
        if not hasattr(self, 'exported_data') or not hasattr(self, 'exported_columns'):
            messagebox.showwarning("No Data", "No data to export. Please run a search first.")
            return

        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not file_path:
            return  # user canceled

        # Write to CSV
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                # Write column headers
                writer.writerow(self.exported_columns)
                # Write each row of data
                for row in self.exported_data:
                    writer.writerow(row)
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {e}")

    def show_invoice_form(self):
        self.clear_main_frame()

        # Heading: same style as "Create New Account" but with invoice-specific text.
        heading_label = tk.Label(
            self.main_frame,
            text="Add Invoice",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading
        sub_label = tk.Label(
            self.main_frame,
            text="Enter Invoice Details",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Invoice Number field
        invoice_num_label = tk.Label(
            self.main_frame,
            text="Invoice Number:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        invoice_num_label.pack(pady=(0, 2))
        self.invoice_num_entry = tk.Entry(self.main_frame, width=30)
        self.invoice_num_entry.pack(pady=(0, 10))

        # Company field
        company_label = tk.Label(
            self.main_frame,
            text="Company:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        company_label.pack(pady=(0, 2))
        self.invoice_company_entry = tk.Entry(self.main_frame, width=30)
        self.invoice_company_entry.pack(pady=(0, 10))

        # Amount field
        amount_label = tk.Label(
            self.main_frame,
            text="Amount:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        amount_label.pack(pady=(0, 2))
        self.invoice_amount_entry = tk.Entry(self.main_frame, width=30)
        self.invoice_amount_entry.pack(pady=(0, 10))

        # Date Received field
        date_received_label = tk.Label(
            self.main_frame,
            text="Date Received:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        date_received_label.pack(pady=(0, 2))
        self.invoice_date_received_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.invoice_date_received_entry.pack(pady=(0, 10))

        # Date Due field
        date_due_label = tk.Label(
            self.main_frame,
            text="Date Due:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        date_due_label.pack(pady=(0, 2))
        self.invoice_date_due_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.invoice_date_due_entry.pack(pady=(0, 10))

        # Store dropdown
        status_label = tk.Label(
            self.main_frame,
            text="Status:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        status_label.pack(pady=(0, 2))
        statuses = ["Paid", "Not Paid"]
        self.invoice_status_var = tk.StringVar()
        self.invoice_status_var.set(statuses[0])
        status_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.invoice_status_var,
            values=statuses,
            state="readonly"
        )
        status_dropdown.pack(pady=(0, 10))


        # Submit button – same style as in Add Employee form.
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_invoice
        )
        submit_button.pack(pady=10)


    def process_invoice(self):
        # For now, simply display the entered values.
        invoice_num = self.invoice_num_entry.get()
        company = self.invoice_company_entry.get()
        amount = self.invoice_amount_entry.get()
        date_received = self.invoice_date_received_entry.get()
        date_due = self.invoice_date_due_entry.get()
        location = self.selected_store
        status = self.invoice_status_var.get()

        messagebox.showinfo(
            "Invoice Submitted",
            f"Invoice Number: {invoice_num}\n"
            f"Company: {company}\n"
            f"Amount: {amount}\n"
            f"Date Received: {date_received}\n"
            f"Date Due: {date_due}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (invoice_num and company and amount and date_received and date_due and location):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO invoices (status, date_received, company, invoice_number, amount, date_due, location) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (status, date_received, company, invoice_num, amount, date_due, location))
            self.connection.commit()
            messagebox.showinfo("Success", "Invoice added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Invoice not added")


    def show_payroll_form(self):
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Payroll",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        # Subheading
        sub_label = tk.Label(
            self.main_frame,
            text="Enter Payroll Details",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Store dropdown
        store_label = tk.Label(
            self.main_frame,
            text="Select Store:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        store_label.pack(pady=(0, 2))
        stores = ["Store 1", "Store 2", "Store 3"]
        self.payroll_store_var = tk.StringVar()
        self.payroll_store_var.set(stores[0])
        store_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.payroll_store_var,
            values=stores,
            state="readonly"
        )
        store_dropdown.pack(pady=(0, 10))

        # Employee ID input
        emp_label = tk.Label(
            self.main_frame,
            text="Employee ID:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        emp_label.pack(pady=(0, 2))
        self.payroll_emp_id_entry = tk.Entry(self.main_frame, width=30)
        self.payroll_emp_id_entry.pack(pady=(0, 10))

        # Bonus input
        bonus_label = tk.Label(
            self.main_frame,
            text="Employee Bonus:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        bonus_label.pack(pady=(0, 2))
        self.payroll_bonus_entry = tk.Entry(self.main_frame, width=30)
        self.payroll_bonus_entry.pack(pady=(0, 10))

        # FROM Date field
        from_date_title = tk.Label(
            self.main_frame,
            text="From Date:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        from_date_title.pack(pady=(0, 2))

        self.from_date_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.from_date_entry.pack(pady=(0, 10))

        # FROM Date field with title
        to_date_title = tk.Label(
            self.main_frame,
            text="To Date:",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        to_date_title.pack(pady=(0, 2))

        self.to_date_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.to_date_entry.pack(pady=(0, 10))

        # Multiple Weeks View checkbox (if needed)
        # self.multiple_weeks_var = tk.BooleanVar(value=False)
        # multiple_weeks_check = tk.Checkbutton(
        #     self.main_frame,
        #     text="Multiple Weeks View",
        #     bg="white",
        #     fg="black",
        #     variable=self.multiple_weeks_var,
        #     onvalue=True,
        #     offvalue=False
        # )
        # multiple_weeks_check.pack(pady=(0, 20))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_payroll
        )
        submit_button.pack()

    def process_payroll(self):
        import datetime  # Ensure datetime is imported

        # Get inputs from the GUI form
        store = self.payroll_store_var.get()
        emp_id = self.payroll_emp_id_entry.get().strip()
        bonus_input = self.payroll_bonus_entry.get().strip()
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()
        #multiple_weeks = self.multiple_weeks_var.get()


        # Validate required fields
        if not (store and emp_id and from_date and to_date):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            bonus = float(bonus_input) if bonus_input else 0.0
        except ValueError:
            messagebox.showerror("Error", "Bonus must be a numeric value.")
            return

        # Query the in_out_bal table for time records within the date range
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT clock_in, clock_out 
                FROM in_out_bal 
                WHERE emp_id = %s AND location = %s 
                  AND date >= %s AND date <= %s
            """
            cursor.execute(query, (emp_id, store, from_date, to_date))
            rows = cursor.fetchall()
        except Error as err:
            messagebox.showerror("Database Error", f"Error retrieving time records: {err}")
            return

        if not rows:
            messagebox.showerror("Error", "No clock records found for this employee in the given date range.")
            return

        # Calculate the total hours worked
        total_hours = 0.0
        for row in rows:
            clock_in_str, clock_out_str = row
            try:
                t_in = datetime.datetime.strptime(str(clock_in_str), "%H:%M:%S")
                t_out = datetime.datetime.strptime(str(clock_out_str), "%H:%M:%S")
            except Exception as e:
                messagebox.showerror("Error", f"Time format error: {e}")
                return
            # Calculate the difference in seconds, then convert to hours
            diff = (t_out - t_in).seconds / 3600.0
            total_hours += diff

        # Query the employee_rates table for the latest rate
        try:
            rate_query = """
                SELECT rate_per_hour 
                FROM employee_rates 
                WHERE employee_id = %s AND location = %s 
                ORDER BY date DESC LIMIT 1
            """
            cursor.execute(rate_query, (emp_id, store))
            rate_result = cursor.fetchone()
            if not rate_result:
                messagebox.showerror("Error", "Employee rate not found for the selected store.")
                return
            rate_per_hour = float(rate_result[0])
        except Error as err:
            messagebox.showerror("Database Error", f"Error retrieving employee rate: {err}")
            return

        # Calculate subtotal (total hours * rate), then payroll total (subtotal + bonus)
        subtotal = total_hours * rate_per_hour
        payroll_total = subtotal + bonus

        # Create a details message
        details = (
            f"Total Hours Worked: {total_hours:.2f} hours\n"
            f"Rate per Hour: ${rate_per_hour:.2f}\n"
            f"Subtotal (Hours * Rate): ${subtotal:.2f}\n"
            f"Bonus: ${bonus:.2f}\n"
            f"Total Payroll: ${payroll_total:.2f}"
        )
        messagebox.showinfo("Payroll Calculation", details)

        # Insert the payroll record into the payroll table
        try:
            insert_query = """
                INSERT INTO payroll 
                (employee_id, store, start_date, end_date, total_hours, rate_per_hour, subtotal, bonus, total_payroll)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                emp_id, store, from_date, to_date, total_hours, rate_per_hour, subtotal, bonus, payroll_total

            ))
            self.connection.commit()
            messagebox.showinfo("Success", "Payroll record added successfully.")
        except Error as err:
            messagebox.showerror("Database Error", f"Error inserting payroll record: {err}")


    #from tkcalendar import DateEntry
    def show_withdraw_form(self):
        """
        Displays a form for entering a withdrawal.
        Fields:
          - Username
          - ID
          - Amount
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Enter Withdrawal",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You’re logged in as {self.logged_in_username} in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Username field
        username_label = tk.Label(
            self.main_frame,
            text="USERNAME",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        username_label.pack(pady=(0, 2))
        self.withdraw_username_entry = tk.Entry(self.main_frame, width=30)
        self.withdraw_username_entry.pack(pady=(0, 10))

        # ID field
        id_label = tk.Label(
            self.main_frame,
            text="ID",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        id_label.pack(pady=(0, 2))
        self.withdraw_id_entry = tk.Entry(self.main_frame, width=30)
        self.withdraw_id_entry.pack(pady=(0, 10))

        # Amount field
        amount_label = tk.Label(
            self.main_frame,
            text="AMOUNT",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        amount_label.pack(pady=(0, 2))
        self.withdraw_amount_entry = tk.Entry(self.main_frame, width=30)
        self.withdraw_amount_entry.pack(pady=(0, 10))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_withdraw
        )
        submit_button.pack(pady=10)

    def process_withdraw(self):
        """
        Collects the withdrawal data and displays it in a message.
        (No DB insert yet.)
        """
        username = self.withdraw_username_entry.get()
        user_id = self.withdraw_id_entry.get()
        amount = self.withdraw_amount_entry.get()
        location = self.selected_store

        # For demonstration, just show a message:
        messagebox.showinfo(
            "Withdrawal Submitted",
            f"Username: {username}\nID: {user_id}\nAmount: {amount}"
        )

        if not (username and user_id and amount and location):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT name, id FROM users WHERE name = %s AND id = %s"
            cursor.execute(query, (username, user_id))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "Employee ID and username not found.")
                return

        except Error as err:
            messagebox.showerror("Database Error", "Error fetching employee ID")
            return  # Ensure function exits on database error

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO withdrawals (username, user_id, amount, location) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, user_id, amount, location))
            self.connection.commit()
            messagebox.showinfo("Success", "Withdrawal added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Withdrawal not added")

    def show_merchandise_form(self):
        """
        Displays a form for entering merchandise data.
        Fields:
          - Merchandise Type
          - Merchandise Value
          - Date (dropdown or DateEntry)
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Enter Merchandise",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You’re logged in as {self.logged_in_username} in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # MERCHANDISE TYPE field
        merch_label = tk.Label(
            self.main_frame,
            text="MERCHANDISE TYPE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        merch_label.pack(pady=(0, 2))
        self.merch_type_entry = tk.Entry(self.main_frame, width=30)
        self.merch_type_entry.pack(pady=(0, 10))

        # MERCHANDISE VALUE field
        val_label = tk.Label(
            self.main_frame,
            text="MERCHANDISE VALUE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        val_label.pack(pady=(0, 2))
        self.merch_value_entry = tk.Entry(self.main_frame, width=30)
        self.merch_value_entry.insert(0, "0.0")  # Example placeholder
        self.merch_value_entry.pack(pady=(0, 10))

        # DATE field (DateEntry)
        date_label = tk.Label(
            self.main_frame,
            text="DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        date_label.pack(pady=(0, 2))

        self.merch_date_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.merch_date_entry.pack(pady=(0, 20))



        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_merchandise
        )
        submit_button.pack()

    def process_merchandise(self):
        """
        Collects the merchandise data and displays it in a message.
        (No DB insert yet.)
        """
        merch_type = self.merch_type_entry.get()
        merch_value = self.merch_value_entry.get()
        location = self.selected_store



        date_val = self.merch_date_entry.get_date()

        messagebox.showinfo(
            "Enter Merchandise",
            f"Merchandise Type: {merch_type}\n"
            f"Merchandise Value: {merch_value}\n"
            f"Date: {date_val}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (merch_type and merch_value and date_val and location):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO merchandise (merchandise_type, merchandise_value, date, location) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (merch_type, merch_value, date_val, location))
            self.connection.commit()
            messagebox.showinfo("Success", "Merchandise added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Merchandise not added")


    def show_calc_bonus_form(self):
        """
        Displays a form for calculating an employee's bonus.
        Fields:
          - Employee ID
          - Location (dropdown)
          - Start Date (DateEntry)
          - End Date (DateEntry)
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Calculate Employee Bonus",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You’re logged in as {self.logged_in_username} in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Employee ID
        emp_id_label = tk.Label(
            self.main_frame,
            text="EMPLOYEE ID",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        emp_id_label.pack(pady=(0, 2))
        self.bonus_emp_id_entry = tk.Entry(self.main_frame, width=30)
        self.bonus_emp_id_entry.pack(pady=(0, 10))

        # Location (dropdown)
        location_label = tk.Label(
            self.main_frame,
            text="LOCATION",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        location_label.pack(pady=(0, 2))
        self.location_var = tk.StringVar()
        # Example location list
        locations = ["Select", "Store 1", "Store 2", "Store 3"]
        self.location_var.set(locations[0])
        location_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.location_var,
            values=locations,
            state="readonly",
            width=28
        )
        location_dropdown.pack(pady=(0, 10))

        # Start Date (DateEntry)
        start_label = tk.Label(
            self.main_frame,
            text="START DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        start_label.pack(pady=(0, 2))

        self.start_date = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.start_date.pack(pady=(0, 10))

        # End Date (DateEntry)
        end_label = tk.Label(
            self.main_frame,
            text="END DATE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        end_label.pack(pady=(0, 2))
        self.end_date = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.end_date.pack(pady=(0, 20))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_calc_bonus
        )
        submit_button.pack()


    def show_set_rates_form(self):
        """
        Displays a form for setting employee rates.
        Fields:
          - Location (dropdown)
          - Employee ID
          - Bonus Rate
          - Rate Per Hour
          - Date (DateEntry)
          - Submit button
        """
        self.clear_main_frame()

        # Heading
        heading_label = tk.Label(
            self.main_frame,
            text="Set Employee Rates",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text=f"You’re logged in as {self.logged_in_username} in {self.selected_store}",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # Location (dropdown)
        loc_label = tk.Label(self.main_frame, text="LOCATION", bg="white", fg="black", font=self.sub_font)
        loc_label.pack(pady=(0, 2))
        self.rates_location_var = tk.StringVar()
        locations = ["Select", "Store 1", "Store 2", "Store 3"]
        self.rates_location_var.set(locations[0])
        loc_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.rates_location_var,
            values=locations,
            state="readonly",
            width=28
        )
        loc_dropdown.pack(pady=(0, 10))

        # Employee ID
        empid_label = tk.Label(self.main_frame, text="EMPLOYEE ID", bg="white", fg="black", font=self.sub_font)
        empid_label.pack(pady=(0, 2))
        self.rates_empid_entry = tk.Entry(self.main_frame, width=30)
        self.rates_empid_entry.pack(pady=(0, 10))

        # Bonus Rate
        bonus_label = tk.Label(self.main_frame, text="BONUS RATE", bg="white", fg="black", font=self.sub_font)
        bonus_label.pack(pady=(0, 2))
        self.rates_bonus_entry = tk.Entry(self.main_frame, width=30)
        self.rates_bonus_entry.insert(0, "0.02")  # Example default
        self.rates_bonus_entry.pack(pady=(0, 10))

        # Rate Per Hour
        rate_label = tk.Label(self.main_frame, text="RATE PER HOUR", bg="white", fg="black", font=self.sub_font)
        rate_label.pack(pady=(0, 2))
        self.rates_hour_entry = tk.Entry(self.main_frame, width=30)
        self.rates_hour_entry.insert(0, "16.00")  # Example default
        self.rates_hour_entry.pack(pady=(0, 10))

        # Date (DateEntry)
        date_label = tk.Label(self.main_frame, text="DATE", bg="white", fg="black", font=self.sub_font)
        date_label.pack(pady=(0, 2))
        self.rates_date_entry = DateEntry(
            self.main_frame,
            width=28,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern="yyyy-mm-dd",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day
        )
        self.rates_date_entry.pack(pady=(0, 20))

        # Submit button
        submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_set_rates
        )
        submit_button.pack()

    def process_set_rates(self):
        """
        Collects the data from the Set Employee Rates form
        and displays it in a message. (No DB insert yet.)
        """
        location = self.rates_location_var.get()
        emp_id = self.rates_empid_entry.get()
        bonus_rate = self.rates_bonus_entry.get()
        rate_per_hour = self.rates_hour_entry.get()
        date_val = self.rates_date_entry.get_date()  # .get_date() returns a Python date object

        # For now, just show the collected data in a messagebox
        messagebox.showinfo(
            "Set Employee Rates",
            f"Location: {location}\n"
            f"Employee ID: {emp_id}\n"
            f"Bonus Rate: {bonus_rate}\n"
            f"Rate Per Hour: {rate_per_hour}\n"
            f"Date: {date_val}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (location and emp_id and bonus_rate and rate_per_hour and date_val):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id FROM users WHERE id = %s"
            cursor.execute(query, (emp_id,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "Employee ID not found.")
                return

        except Error as err:
            messagebox.showerror("Database Error", "Error fetching employee ID")
            return  # Ensure function exits on database error

        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO employee_rates (employee_id, location, bonus_rate, rate_per_hour, date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (emp_id, location, bonus_rate, rate_per_hour, date_val))
            self.connection.commit()
            messagebox.showinfo("Success", "Rates added")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", "Rates not added")

    def process_calc_bonus(self):
        """
        Gathers the data from the bonus form fields
        and displays a message. (No DB insert yet.)
        """
        emp_id = self.bonus_emp_id_entry.get()
        location = self.location_var.get()
        start_date_val = self.start_date.get_date()  # .get_date() returns a Python date object
        end_date_val = self.end_date.get_date()

        # For demonstration, just show a message with the values:
        messagebox.showinfo(
            "Calculate Employee Bonus",
            f"Employee ID: {emp_id}\n"
            f"Location: {location}\n"
            f"Start Date: {start_date_val}\n"
            f"End Date: {end_date_val}"
        )

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (location and emp_id and start_date_val and end_date_val):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            cursor = self.connection.cursor()
            query = "SELECT id FROM users WHERE id = %s"
            cursor.execute(query, (emp_id,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "Employee ID not found.")
                return

        except Error as err:
            messagebox.showerror("Database Error", "Error fetching employee ID")
            return  # Ensure function exits on database error

        try:
            cursor = self.connection.cursor()
            query = "SELECT bonus_rate FROM employee_rates WHERE employee_id = %s AND location = %s"
            cursor.execute(query, (emp_id, location))
            rate_result = cursor.fetchone()

            if not rate_result or not rate_result[0]:
                messagebox.showerror("Error", "Bonus rate not found for this employee and location.")
                return

            # Extract the bonus rate (ensure it's a float)
            rate = float(rate_result[0])

            query = "SELECT in_bal, out_bal FROM in_out_bal WHERE emp_id = %s AND location = %s AND date > %s AND date < %s"
            emp_id = int(emp_id)
            cursor.execute(query, (emp_id, location, start_date_val, end_date_val))
            rows = cursor.fetchall()

            print("Fetched rows:", rows)

            if not rows:
                messagebox.showerror("Error",
                                     "No balance records found for this employee and location in the given date range.")
                return

            balances = pd.DataFrame(rows, columns=['in_bal', 'out_bal'])
            balances['balance_diff'] = balances['out_bal'] - balances['in_bal']
            total_diff = balances['balance_diff'].sum()

            print("Total balance difference:", total_diff)

            bonus_amt = float(total_diff) * float(rate)

            print("Calculated bonus amount:", bonus_amt)

            # Insert the bonus record into the employee_bonus table
            insert_query = """
                            INSERT INTO employee_bonus (employee_id, location, start_date, end_date, bonus_amount)
                            VALUES (%s, %s, %s, %s, %s)
                        """
            cursor.execute(insert_query, (emp_id, location, start_date_val, end_date_val, bonus_amt))
            self.connection.commit()

            messagebox.showinfo("Success", f"Bonus amount: ${bonus_amt:.2f}\nBonus data saved successfully.")
            self.go_back()

        except Error as err:
            messagebox.showerror("Database Error", "Bonus not calculated or not saved")

    # ----------------------------------------------------------------
    # ADD EMPLOYEE FORM
    # ----------------------------------------------------------------
    def show_add_employee_form(self):
        self.clear_main_frame()

        heading_label = tk.Label(
            self.main_frame,
            text="Create New Account",
            bg="white",
            fg="black",
            font=self.header_font
        )
        heading_label.pack(pady=(20, 5))

        sub_label = tk.Label(
            self.main_frame,
            text="Already Registered? Login",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        sub_label.pack(pady=(0, 20))

        # ROLE
        role_label = tk.Label(
            self.main_frame,
            text="ROLE",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        role_label.pack(pady=(0, 2))

        self.emp_role_var = tk.StringVar()
        roles = ["Employee", "Manager", "Owner"]
        self.emp_role_var.set(roles[0])
        role_dropdown = ttk.Combobox(
            self.main_frame,
            textvariable=self.emp_role_var,
            values=roles,
            state="readonly"
        )
        role_dropdown.pack(pady=(0, 10))

        # ID (not stored in the DB with this table structure)
        emp_id_label = tk.Label(
            self.main_frame,
            text="ID",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        emp_id_label.pack(pady=(0, 2))
        self.emp_id_entry = tk.Entry(self.main_frame, width=30)
        self.emp_id_entry.pack(pady=(0, 10))

        # NAME
        name_label = tk.Label(
            self.main_frame,
            text="NAME",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        name_label.pack(pady=(0, 2))
        self.emp_name_entry = tk.Entry(self.main_frame, width=30)
        self.emp_name_entry.pack(pady=(0, 10))

        # PASSWORD
        pass_label = tk.Label(
            self.main_frame,
            text="PASSWORD",
            bg="white",
            fg="black",
            font=self.sub_font
        )
        pass_label.pack(pady=(0, 2))
        self.emp_pass_entry = tk.Entry(self.main_frame, show="*", width=30)
        self.emp_pass_entry.pack(pady=(0, 10))

        # Sign Up button
        signup_button = tk.Button(
            self.main_frame,
            text="Sign up",
            bg="black",
            fg="white",
            width=20,
            height=2,
            command=self.process_add_employee
        )
        signup_button.pack(pady=10)

    def process_add_employee(self):
        role = self.emp_role_var.get()
        _ignored_id = self.emp_id_entry.get()
        name = self.emp_name_entry.get()
        password = self.emp_pass_entry.get()

        if not self.connection:
            messagebox.showwarning("Warning", "No database connection. This is a demo.")
            return

        if not (role and name and password):
            messagebox.showerror("Error", "Role, Name, and Password are required.")
            return

        try:
            cursor = self.connection.cursor()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            query = "INSERT INTO users (name, password, role) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, hashed_password, role))
            self.connection.commit()
            messagebox.showinfo("Success", f"New user '{name}' added with role '{role}'.")
            self.go_back()  # Return to the previous screen
        except Error as err:
            messagebox.showerror("Database Error", f"Error creating user: {err}")

    # ----------------------------------------------------------------
    # NAVIGATION & MISC
    # ----------------------------------------------------------------

    def go_back(self):
        self.tree.pack_forget()

        # Only try to hide total_label if it exists
        if hasattr(self, "total_label"):
            self.total_label.pack_forget()

        if hasattr(self, "user_role"):
            if self.user_role == "Manager":
                self.show_manager_home()
            elif self.user_role == "Owner":
                self.show_owner_home()
            elif self.user_role == "Employee":
                self.show_employee_home()
            else:
                messagebox.showerror("Error", "Unknown role. Returning to welcome screen.")
                self.show_welcome_screen()
        else:
            self.show_welcome_screen()

    # def option1_action(self):
    #     print("Option 1 selected.")

    def option1_action(self):
        # Clear any session-specific data if necessary here.
        self.user_role = None
        self.show_welcome_screen()
        messagebox.showinfo("Sign Out", "You have been signed out successfully.")

    def option2_action(self):
        print("Option 2 selected.")


if __name__ == "__main__":
    app = AlohaCorpApp()
    app.mainloop()
