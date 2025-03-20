import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def submit_access():
    login_type = combo_login_type.get()
    employee = entry_employee.get()
    manager = entry_manager.get()
    owner = entry_owner.get()

    try:
        cursor.execute("""
            INSERT INTO access_management (login_type, employee, manager, owner)
            VALUES (%s, %s, %s, %s)
        """, (login_type, employee, manager, owner))
        conn.commit()
        messagebox.showinfo("Success", "Access details saved successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error saving data: {err}")


# Connect to MySQL
conn = mysql.connector.connect(host="your_host", user="your_user", password="your_password", database="your_database")
cursor = conn.cursor()

# Tkinter Window Setup
root = tk.Tk()
root.title("Full Access")
root.geometry("500x400")
root.configure(bg="white")

# UI Elements
tk.Label(root, text="Full Access", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
tk.Label(root, text="LOGIN TYPE", bg="white").pack()
combo_login_type = ttk.Combobox(root, values=["Employee", "Manager", "Owner"], state="readonly")
combo_login_type.pack()

tk.Label(root, text="Employee", bg="white").pack()
entry_employee = tk.Entry(root)
entry_employee.pack()

tk.Label(root, text="Manager", bg="white").pack()
entry_manager = tk.Entry(root)
entry_manager.pack()

tk.Label(root, text="Owner", bg="white").pack()
entry_owner = tk.Entry(root)
entry_owner.pack()

tk.Button(root, text="Submit", command=submit_access).pack(pady=10)
tk.Button(root, text="Back", command=root.quit).pack(pady=5)

root.mainloop()
