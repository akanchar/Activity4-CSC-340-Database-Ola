import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import bcrypt

try:
    conn = mysql.connector.connect(
        host="localhost",  # or your host address
        user="root",  # replace with your MySQL username
        password="34691",  # replace with your MySQL password
        database="triall"  # replace with your database name
    )

    if conn.is_connected():
        print("Successfully connected to MySQL database")
    else:
        print("Connection failed")

except Error as e:
    print(f"Error connecting to MySQL: {e}")

'''
finally:
    if conn.is_connected():
        conn.close()
'''

'''        
# Connect to the MySQL database
try:
    conn = mysql.connector.connect(
        host="@localhost",
        username="root",       # Replace with your MySQL username
        password="root",
        database="triall"
    )'''
cursor = conn.cursor()
'''except mysql.connector.Error as err:
    messagebox.showerror("Connection Error", f"Error connecting to MySQL: {err}")
    exit(1)'''


# Create the table if it doesn't exist
create_table_query ="""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL
)
"""


try:
    cursor.execute(create_table_query)
    conn.commit()
except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error creating table: {err}")

#function to create initial owner login
#pass1 = 'pass'
#hashed_pass1 = bcrypt.hashpw(pass1.encode('utf-8'), bcrypt.gensalt())
#insert_query = "INSERT INTO  users (ID, name, password, role) VALUES (%s, %s, %s, %s)"
#cursor.execute(insert_query, (123, 'owner1', hashed_pass1, 'Owner'))
#conn.commit()

# Function to add a new user (employee) to the database
def add_user_to_db(emp_id, name, password, role):
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        # Insert the new employee into the users table with their ID, name, password, and role
        insert_query = "INSERT INTO users (id, name, password, role) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (emp_id, name, hashed_password, role))
        conn.commit()
        messagebox.showinfo("Success", f"{role} added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error inserting data: {err}")

# Function to load the role and login page
def load_role_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Select Your Role", font=("Arial", 16)).pack(pady=20)

    roles = ["Employee", "Manager", "Owner"]
    role_var = tk.StringVar(root)
    role_var.set(roles[0])

    tk.Label(root, text="Select Role").pack()
    role_menu = tk.OptionMenu(root, role_var, *roles)
    role_menu.pack(pady=5)

    tk.Label(root, text="User ID").pack()
    user_id_entry = tk.Entry(root, width=30)
    user_id_entry.pack(pady=5)

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, width=30, show="*")
    password_entry.pack(pady=5)

    def login():
        user_id = user_id_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if check_credentials(user_id, password, role):
            messagebox.showinfo("Login Success", "Login successful!")
            load_select_action_page(role)  # Pass the role to the action page
        else:
            messagebox.showerror("Login Failed", "Invalid credentials. Please try again.")

    login_button = tk.Button(root, text="Login", command=login, width=20, bg="black", fg="white")
    login_button.pack(pady=20)


# Function to load the select an action page
def load_select_action_page(role):
    for widget in root.winfo_children():
        widget.destroy()

    menu_text = "Owner/Manager Select an Action" if role in ["Owner", "Manager"] else "Employee Select an Action"
    tk.Label(root, text=menu_text, font=("Arial", 16)).pack(pady=20)

    actions = [
        "Enter Invoice", "Enter Expense", "Enter Merchandise", "Enter Gross Profit",
        "Withdrawal", "Calculate Employee Bonus", "Add Employee", "Set Employee Rates",
        "View Records", "Payroll"
    ] if role in ["Owner", "Manager"] else [
        "Enter Expense", "Enter Day Closeout", "Enter In/Out Balance"
    ]

    action_var = tk.StringVar(root)
    action_var.set(actions[0])

    tk.Label(root, text="Select Action").pack()
    action_menu = tk.OptionMenu(root, action_var, *actions)
    action_menu.pack(pady=5)

    def next_action():
        selected_action = action_var.get()
        if selected_action == "Enter Expense":
            load_enter_expense_page()
        elif selected_action == "Enter Invoice":
            load_enter_invoice_page()
        elif selected_action == "Add Employee":
            load_add_employee_form()
        else:
            messagebox.showinfo("Action Selected", f"You have chosen: {selected_action}")

    next_button = tk.Button(root, text="Next", command=next_action, width=20, bg="black", fg="white")
    next_button.pack(pady=10)


    # Function to load the add employee form with role validation
    def load_add_employee_form():
        # Clear all existing widgets first
        for widget in root.winfo_children():
            widget.destroy()

        # Add label for Add Employee page
        tk.Label(root, text="Add New Employee", font=("Arial", 16)).pack(pady=20)

        # Entry fields for employee ID, name, password, and role
        tk.Label(root, text="Employee ID").pack()
        id_entry = tk.Entry(root, width=30)
        id_entry.pack(pady=5)

        tk.Label(root, text="Employee Name").pack()
        name_entry = tk.Entry(root, width=30)
        name_entry.pack(pady=5)

        tk.Label(root, text="Employee Password").pack()
        password_entry = tk.Entry(root, width=30, show="*")
        password_entry.pack(pady=5)

        tk.Label(root, text="Employee Role (e.g., Employee)").pack()
        role_entry = tk.Entry(root, width=30)
        role_entry.pack(pady=5)

        # Submit function for adding the employee to the database
        def submit_employee():
            emp_id = id_entry.get()
            name = name_entry.get()
            password = password_entry.get()
            role = role_entry.get()

            # Validate that role is one of the allowed options
            if role not in ["Employee", "Manager", "Owner"]:
                messagebox.showerror("Role Error", "Please enter a valid role: 'Employee', 'Manager', or 'Owner'.")
                return

            if emp_id and name and password and role:
                try:
                    # Convert ID to integer (ensure it's a valid ID)
                    emp_id = int(emp_id)
                    add_user_to_db(emp_id, name, password, role)  # Add the user to the database
                    # Clear entry fields after submission
                    id_entry.delete(0, tk.END)
                    name_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
                    role_entry.delete(0, tk.END)
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter a valid numeric ID.")
            else:
                messagebox.showerror("Input Error", "Please fill in all fields.")

        # Submit button to add the employee
        submit_button = tk.Button(root, text="Add Employee", command=submit_employee, width=20, bg="black", fg="white")
        submit_button.pack(pady=10)

        # Back to Select Action page button
        back_button = tk.Button(root, text="Back to Actions", command=lambda: load_select_action_page("Manager"),
                                width=20, bg="black", fg="white")
        back_button.pack(pady=10)

        # Ensure that the window refreshes after these widgets are added
        root.update_idletasks()

    # Log out button
    def logout():
        load_store_page()  # Go back to store selection page

    logout_button = tk.Button(root, text="Log Out", command=logout, width=20, bg="black", fg="white")
    logout_button.pack(pady=20)


# Function to load the store selection page
def load_store_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Select Your Store", font=("Arial", 16)).pack(pady=20)

    stores = ["Store 1", "Store 2", "Store 3", "Store 4"]
    store_var = tk.StringVar(root)
    store_var.set(stores[0])

    tk.Label(root, text="Select Store").pack()
    store_menu = tk.OptionMenu(root, store_var, *stores)
    store_menu.pack(pady=5)

    next_button = tk.Button(root, text="Next", command=load_role_page, width=20, bg="black", fg="white")
    next_button.pack(pady=20)


def check_credentials(user_id, password, role):
    # Query to select the necessary columns (password) for MySQL
    cursor.execute("SELECT password FROM users WHERE id=%s AND role=%s", (user_id, role))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]  # The hashed password from the database

        # Compare the entered plaintext password with the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return True  # Credentials are correct
    return False  # Credentials are incorrect


# Create invoices table if not exists
create_invoice_table_query = """
CREATE TABLE IF NOT EXISTS invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(50),
    date_received DATE,
    company VARCHAR(255),
    invoice_number VARCHAR(50),
    amount DECIMAL(10,2),
    date_due DATE
)
"""

# Create expenses table if not exists
create_expense_table_query = """
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    expense_type VARCHAR(255),
    expense_value DECIMAL(10,2),
    date DATE
)
"""

# Create merchandise table if not exists
create_merchandise_table_query = """
CREATE TABLE IF NOT EXISTS merchandise (
    id INT AUTO_INCREMENT PRIMARY KEY,
    merchandise_type VARCHAR(255),
    merchandise_value DECIMAL(10,2),
    date DATE
)
"""
# Create withdrawals table if not exists
create_withdrawals_table_query = """
CREATE TABLE IF NOT EXISTS withdrawals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    user_id INT,
    amount DECIMAL(10,2)
)
"""
# Create tables if not exist
create_employee_bonus_table_query = """
CREATE TABLE IF NOT EXISTS employee_bonus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    location VARCHAR(255),
    start_date DATE,
    end_date DATE,
    bonus_amount DECIMAL(10,2)
)
"""

# Create tables if not exist
create_employee_rates_table_query = """
CREATE TABLE IF NOT EXISTS employee_rates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    location VARCHAR(255),
    bonus_rate DECIMAL(5,2),
    rate_per_hour DECIMAL(10,2),
    date DATE
)
"""
# Create tables if not exist
create_payroll_table_query = """
CREATE TABLE IF NOT EXISTS payroll (
    id INT AUTO_INCREMENT PRIMARY KEY,
    start_date DATE,
    end_date DATE,
    multiple_weeks_view BOOLEAN
)
"""

try:
    cursor.execute(create_invoice_table_query)
    cursor.execute(create_expense_table_query)
    cursor.execute(create_merchandise_table_query)
    cursor.execute(create_withdrawals_table_query)
    cursor.execute(create_employee_bonus_table_query)
    cursor.execute(create_employee_rates_table_query)
    cursor.execute(create_payroll_table_query)
    conn.commit()
except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error creating tables: {err}")

# Function to load Enter Invoice Page
def load_enter_invoice_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Enter Invoice", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="You're logged in as Manager 1").pack(pady=5)

    tk.Label(root, text="PAID/NOT PAID").pack()
    status_var = tk.StringVar(root)
    status_menu = tk.OptionMenu(root, status_var, "Paid", "Not Paid")
    status_menu.pack(pady=5)

    tk.Label(root, text="DATE RECEIVED").pack()
    date_received_entry = tk.Entry(root, width=30)
    date_received_entry.pack(pady=5)

    tk.Label(root, text="COMPANY").pack()
    company_entry = tk.Entry(root, width=30)
    company_entry.pack(pady=5)

    tk.Label(root, text="INVOICE #").pack()
    invoice_number_entry = tk.Entry(root, width=30)
    invoice_number_entry.pack(pady=5)

    tk.Label(root, text="AMOUNT").pack()
    amount_entry = tk.Entry(root, width=30)
    amount_entry.pack(pady=5)

    tk.Label(root, text="DATE DUE").pack()
    date_due_entry = tk.Entry(root, width=30)
    date_due_entry.pack(pady=5)

    def submit_invoice():
        status = status_var.get()
        date_received = date_received_entry.get()
        company = company_entry.get()
        invoice_number = invoice_number_entry.get()
        amount = amount_entry.get()
        date_due = date_due_entry.get()

        if not all([status, date_received, company, invoice_number, amount, date_due]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            cursor.execute(
                "INSERT INTO invoices (status, date_received, company, invoice_number, amount, date_due) VALUES (%s, %s, %s, %s, %s, %s)",
                (status, date_received, company, invoice_number, amount, date_due)
            )
            conn.commit()
            messagebox.showinfo("Success", "Invoice added successfully!")
            load_enter_invoice_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting invoice: {err}")

    submit_button = tk.Button(root, text="Submit", command=submit_invoice, width=20, bg="black", fg="white")
    submit_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: load_select_action_page("Manager"), width=20, bg="black", fg="white")
    back_button.pack(pady=5)

# Function to load Enter Expense Page
def load_enter_expense_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Enter Expense", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="You're logged in as Manager 1 in Store 1").pack(pady=5)

    tk.Label(root, text="EXPENSE TYPE").pack()
    expense_type_entry = tk.Entry(root, width=30)
    expense_type_entry.pack(pady=5)

    tk.Label(root, text="EXPENSE VALUE").pack()
    expense_value_entry = tk.Entry(root, width=30)
    expense_value_entry.pack(pady=5)

    tk.Label(root, text="DATE").pack()
    date_entry = tk.Entry(root, width=30)
    date_entry.pack(pady=5)

    def submit_expense():
        expense_type = expense_type_entry.get()
        expense_value = expense_value_entry.get()
        date = date_entry.get()

        if not all([expense_type, expense_value, date]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            cursor.execute(
                "INSERT INTO expenses (expense_type, expense_value, date) VALUES (%s, %s, %s)",
                (expense_type, expense_value, date)
            )
            conn.commit()
            messagebox.showinfo("Success", "Expense added successfully!")
            load_enter_expense_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting expense: {err}")

    submit_button = tk.Button(root, text="Submit", command=submit_expense, width=20, bg="black", fg="white")
    submit_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: load_select_action_page("Manager"), width=20, bg="black", fg="white")
    back_button.pack(pady=5)

# Function to load Enter Merchandise Page
def load_enter_merchandise_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Enter Merchandise", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="You're logged in as Manager 1 in Store 1").pack(pady=5)

    tk.Label(root, text="MERCHANDISE TYPE").pack()
    merchandise_type_entry = tk.Entry(root, width=30)
    merchandise_type_entry.pack(pady=5)

    tk.Label(root, text="MERCHANDISE VALUE").pack()
    merchandise_value_entry = tk.Entry(root, width=30)
    merchandise_value_entry.pack(pady=5)

    tk.Label(root, text="DATE").pack()
    date_entry = tk.Entry(root, width=30)
    date_entry.pack(pady=5)

    def submit_merchandise():
        merchandise_type = merchandise_type_entry.get()
        merchandise_value = merchandise_value_entry.get()
        date = date_entry.get()

        if not all([merchandise_type, merchandise_value, date]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            cursor.execute(
                "INSERT INTO merchandise (merchandise_type, merchandise_value, date) VALUES (%s, %s, %s)",
                (merchandise_type, merchandise_value, date)
            )
            conn.commit()
            messagebox.showinfo("Success", "Merchandise added successfully!")
            load_enter_merchandise_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting merchandise: {err}")

    submit_button = tk.Button(root, text="Submit", command=submit_merchandise, width=20, bg="black", fg="white")
    submit_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: load_select_action_page("Manager"), width=20, bg="black", fg="white")
    back_button.pack(pady=5)






# Function to load Enter Withdrawal Page
def load_enter_withdrawal_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Enter Withdrawal", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="You're logged in as Manager 1 in Store 1").pack(pady=5)

    tk.Label(root, text="USERNAME").pack()
    username_entry = tk.Entry(root, width=30)
    username_entry.pack(pady=5)

    tk.Label(root, text="ID").pack()
    user_id_entry = tk.Entry(root, width=30)
    user_id_entry.pack(pady=5)

    tk.Label(root, text="AMOUNT").pack()
    amount_entry = tk.Entry(root, width=30)
    amount_entry.pack(pady=5)

    def submit_withdrawal():
        username = username_entry.get()
        user_id = user_id_entry.get()
        amount = amount_entry.get()

        if not all([username, user_id, amount]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            cursor.execute(
                "INSERT INTO withdrawals (username, user_id, amount) VALUES (%s, %s, %s)",
                (username, user_id, amount)
            )
            conn.commit()
            messagebox.showinfo("Success", "Withdrawal added successfully!")
            load_enter_withdrawal_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting withdrawal: {err}")

    submit_button = tk.Button(root, text="Submit", command=submit_withdrawal, width=20, bg="black", fg="white")
    submit_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: load_select_action_page("Manager"), width=20, bg="black", fg="white")
    back_button.pack(pady=5)






# Function to load Calculate Employee Bonus Page
def load_calculate_employee_bonus_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Calculate Employee Bonus", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="You're logged in as Manager 1").pack(pady=5)

    tk.Label(root, text="EMPLOYEE ID").pack()
    employee_id_entry = tk.Entry(root, width=30)
    employee_id_entry.pack(pady=5)

    tk.Label(root, text="LOCATION").pack()
    location_var = tk.StringVar(root)
    location_menu = tk.OptionMenu(root, location_var, "Store 1", "Store 2", "Store 3")
    location_menu.pack(pady=5)

    tk.Label(root, text="START DATE").pack()
    start_date_entry = tk.Entry(root, width=30)
    start_date_entry.pack(pady=5)

    tk.Label(root, text="END DATE").pack()
    end_date_entry = tk.Entry(root, width=30)
    end_date_entry.pack(pady=5)

    def submit_employee_bonus():
        employee_id = employee_id_entry.get()
        location = location_var.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()

        if not all([employee_id, location, start_date, end_date]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Placeholder for bonus calculation logic
        bonus_amount = 500.00  # Example static value

        try:
            cursor.execute(
                "INSERT INTO employee_bonus (employee_id, location, start_date, end_date, bonus_amount) VALUES (%s, %s, %s, %s, %s)",
                (employee_id, location, start_date, end_date, bonus_amount)
            )
            conn.commit()
            messagebox.showinfo("Success", "Employee bonus calculated successfully!")
            load_calculate_employee_bonus_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting bonus: {err}")

    submit_button = tk.Button(root, text="Submit", command=submit_employee_bonus, width=20, bg="black", fg="white")
    submit_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: load_select_action_page("Manager"), width=20, bg="black",
                            fg="white")
    back_button.pack(pady=5)







# Function to load Set Employee Rates Page
def load_set_employee_rates_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Set Employee Rates", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="You're logged in as Manager 1").pack(pady=5)

    tk.Label(root, text="LOCATION").pack()
    location_var = tk.StringVar(root)
    location_menu = tk.OptionMenu(root, location_var, "Store 1", "Store 2", "Store 3")
    location_menu.pack(pady=5)

    tk.Label(root, text="EMPLOYEE ID").pack()
    employee_id_entry = tk.Entry(root, width=30)
    employee_id_entry.pack(pady=5)

    tk.Label(root, text="BONUS RATE").pack()
    bonus_rate_entry = tk.Entry(root, width=30)
    bonus_rate_entry.pack(pady=5)

    tk.Label(root, text="RATE PER HOUR").pack()
    rate_per_hour_entry = tk.Entry(root, width=30)
    rate_per_hour_entry.pack(pady=5)

    tk.Label(root, text="DATE").pack()
    date_entry = tk.Entry(root, width=30)
    date_entry.pack(pady=5)

    def submit_employee_rate():
        employee_id = employee_id_entry.get()
        location = location_var.get()
        bonus_rate = bonus_rate_entry.get()
        rate_per_hour = rate_per_hour_entry.get()
        date = date_entry.get()

        if not all([employee_id, location, bonus_rate, rate_per_hour, date]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            cursor.execute(
                "INSERT INTO employee_rates (employee_id, location, bonus_rate, rate_per_hour, date) VALUES (%s, %s, %s, %s, %s)",
                (employee_id, location, bonus_rate, rate_per_hour, date)
            )
            conn.commit()
            messagebox.showinfo("Success", "Employee rates set successfully!")
            load_set_employee_rates_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting employee rate: {err}")

    submit_button = tk.Button(root, text="Submit", command=submit_employee_rate, width=20, bg="black", fg="white")
    submit_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: load_select_action_page("Manager"), width=20, bg="black",
                            fg="white")
    back_button.pack(pady=5)


# Modify function to navigate to Set Employee Rates page
def load_select_action_page(role):
    for widget in root.winfo_children():
        widget.destroy()

    menu_text = "Owner/Manager Select an Action" if role in ["Owner", "Manager"] else "Employee Select an Action"
    tk.Label(root, text=menu_text, font=("Arial", 16)).pack(pady=20)

    actions = [
        "Enter Invoice", "Enter Expense", "Enter Merchandise", "Enter Withdrawal",
        "Calculate Employee Bonus", "Set Employee Rates", "Add Employee",
        "View Records", "Payroll"
    ] if role in ["Owner", "Manager"] else [
        "Enter Expense", "Enter Day Closeout", "Enter In/Out Balance"
    ]

    action_var = tk.StringVar(root)
    action_var.set(actions[0])

    tk.Label(root, text="Select Action").pack()
    action_menu = tk.OptionMenu(root, action_var, *actions)
    action_menu.pack(pady=5)



# Function to load Payroll Page
def load_payroll_page():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Payroll", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="You're logged in as Manager").pack(pady=5)

    tk.Label(root, text="FROM").pack()
    from_var = tk.StringVar(root)
    from_menu = tk.OptionMenu(root, from_var, "2/24 - 3/2", "3/3 - 3/9", "3/10 - 3/16")
    from_menu.pack(pady=5)

    tk.Label(root, text="TO").pack()
    to_var = tk.StringVar(root)
    to_menu = tk.OptionMenu(root, to_var, "2/24 - 3/2", "3/3 - 3/9", "3/10 - 3/16")
    to_menu.pack(pady=5)

    multiple_weeks_var = tk.BooleanVar()
    multiple_weeks_check = tk.Checkbutton(root, text="MULTIPLE WEEKS VIEW", variable=multiple_weeks_var)
    multiple_weeks_check.pack(pady=5)

    def submit_payroll():
        start_date = from_var.get()
        end_date = to_var.get()
        multiple_weeks_view = multiple_weeks_var.get()

        if not all([start_date, end_date]):
            messagebox.showerror("Error", "Please select both dates.")
            return

        try:
            cursor.execute(
                "INSERT INTO payroll (start_date, end_date, multiple_weeks_view) VALUES (%s, %s, %s)",
                (start_date, end_date, multiple_weeks_view)
            )
            conn.commit()
            messagebox.showinfo("Success", "Payroll data submitted successfully!")
            load_payroll_page()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting payroll data: {err}")

    submit_button = tk.Button(root, text="Submit", command=submit_payroll, width=20, bg="black", fg="white")
    submit_button.pack(pady=10)

    back_button = tk.Button(root, text="Back", command=lambda: load_select_action_page("Manager"), width=20, bg="black",
                            fg="white")
    back_button.pack(pady=5)


# Modify function to navigate to Payroll page
def load_select_action_page(role):
    for widget in root.winfo_children():
        widget.destroy()

    menu_text = "Owner/Manager Select an Action" if role in ["Owner", "Manager"] else "Employee Select an Action"
    tk.Label(root, text=menu_text, font=("Arial", 16)).pack(pady=20)

    actions = [
        "Enter Invoice", "Enter Expense", "Enter Merchandise", "Enter Withdrawal",
        "Calculate Employee Bonus", "Set Employee Rates", "Payroll", "Add Employee",
        "View Records"
    ] if role in ["Owner", "Manager"] else [
        "Enter Expense", "Enter Day Closeout", "Enter In/Out Balance"
    ]

    action_var = tk.StringVar(root)
    action_var.set(actions[0])

    tk.Label(root, text="Select Action").pack()
    action_menu = tk.OptionMenu(root, action_var, *actions)
    action_menu.pack(pady=5)

    def next_action():
        selected_action = action_var.get()
        if selected_action == "Payroll":
            load_payroll_page()
        elif selected_action == "Set Employee Rates":
            load_set_employee_rates_page()
        elif selected_action == "Calculate Employee Bonus":
            load_calculate_employee_bonus_page()
        elif selected_action == "Enter Withdrawal":
            load_enter_withdrawal_page()
        elif selected_action == "Enter Merchandise":
            load_enter_merchandise_page()
        elif selected_action == "Enter Expense":
            load_enter_expense_page()
        elif selected_action == "Enter Invoice":
            load_enter_invoice_page()
        elif selected_action == "Add Employee":
            load_add_employee_form()
        else:
            messagebox.showinfo("Action Selected", f"You have chosen: {selected_action}")

    next_button = tk.Button(root, text="Next", command=next_action, width=20, bg="black", fg="white")
    next_button.pack(pady=10)




#Main window
root = tk.Tk()
root.title("Aloha Corp Login")
root.geometry("500x500")

# Load store selection page initially
load_store_page()

root.mainloop()

