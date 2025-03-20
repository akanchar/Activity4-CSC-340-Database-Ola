import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import bcrypt

try:
    conn = mysql.connector.connect(
        host="localhost",  # or your host address
        user="root",  # replace with your MySQL username
        password="root",  # replace with your MySQL password
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
#insert_query = "INSERT INTO users (ID, name, password, role) VALUES (%s, %s, %s, %s)"
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

    if role == "Owner" or role == "Manager":
        menu_text = "Owner/Manager Select an Action"
    elif role == "Employee":
        menu_text = "Employee Select an Action"

    tk.Label(root, text=menu_text, font=("Arial", 16)).pack(pady=20)

    # Define actions based on role
    if role == "Owner" or role == "Manager":
        actions = [
            "Enter Invoice", "Enter Expense", "Enter Merchandise", "Enter Gross Profit",
            "Withdrawal", "Calculate Employee Bonus", "Add Employee", "Set Employee Rates",
            "View Records", "Payroll"
        ]
    elif role == "Employee":
        actions = [
            "Enter Expense", "Enter Day Closeout", "Enter In/Out Balance"
        ]

    action_var = tk.StringVar(root)
    action_var.set(actions[0])

    tk.Label(root, text="Select Action").pack()
    action_menu = tk.OptionMenu(root, action_var, *actions)
    action_menu.pack(pady=5)

    # Function to handle "Next" button press
    def next_action():
        selected_action = action_var.get()
        if selected_action == "Add Employee":
            load_add_employee_form()
        else:
            messagebox.showinfo("Action Selected", f"You have chosen: {selected_action}")

    # Next button to show the action in a popup
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

# Main window
root = tk.Tk()
root.title("Aloha Corp Login")
root.geometry("500x400")

# Load store selection page initially
load_store_page()

root.mainloop()

