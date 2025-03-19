import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

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
    email VARCHAR(255) NOT NULL UNIQUE
)
"""

try:
    cursor.execute(create_table_query)
    conn.commit()
except mysql.connector.Error as err:
    messagebox.showerror("Error", f"Error creating table: {err}")

# Function to add a new user to the database
def add_user():
    name = entry_name.get()
    email = entry_email.get()
    if name and email:
        try:
            insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
            cursor.execute(insert_query, (name, email))
            conn.commit()
            messagebox.showinfo("Success", "User added successfully!")
            entry_name.delete(0, tk.END)
            entry_email.delete(0, tk.END)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error inserting data: {err}")
    else:
        messagebox.showerror("Input Error", "Please fill in all fields.")

# Create the main Tkinter window
root = tk.Tk()
root.title("User Registration")

# Create and place labels and entry fields
tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Email:").grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=10, pady=10)

# Create and place the button that will add a new user
btn_add = tk.Button(root, text="Add User", command=add_user)
btn_add.grid(row=2, column=0, columnspan=2, pady=10)

# Start the GUI event loop
root.mainloop()

# Clean up: close the cursor and connection
cursor.close()
conn.close()