import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def submit_employee():
    role = combo_role.get()
    name = entry_name.get()
    employee_id = entry_id.get()
    password = entry_password.get()

    try:
        cursor.execute("""
            INSERT INTO employees (role, name, employee_id, password)
            VALUES (%s, %s, %s, %s)
        """, (role, name, employee_id, password))
        conn.commit()
        messagebox.showinfo("Success", "Employee added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error saving data: {err}")


# Connect to MySQL
conn = mysql.connector.connect(host="your_host", user="your_user", password="your_password", database="your_database")
cursor = conn.cursor()

# Tkinter Window Setup
root = tk.Tk()
root.title("Add Employee")
root.geometry("500x400")
root.configure(bg="white")

# UI Elements
tk.Label(root, text="Add Employee", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
tk.Label(root, text="ROLE", bg="white").pack()
combo_role = ttk.Combobox(root, values=["Employee", "Manager", "Owner"], state="readonly")
combo_role.pack()

tk.Label(root, text="NAME", bg="white").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="ID", bg="white").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="PASSWORD", bg="white").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Submit", command=submit_employee).pack(pady=10)
tk.Button(root, text="Back", command=root.quit).pack(pady=5)

root.mainloop()