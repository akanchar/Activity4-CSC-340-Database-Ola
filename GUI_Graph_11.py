import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def submit_bonus():
    employee_id = entry_employee_id.get()
    location = combo_location.get()
    start_date = combo_start_date.get()
    end_date = combo_end_date.get()

    try:
        cursor.execute("""
            INSERT INTO employee_bonus (employee_id, location, start_date, end_date)
            VALUES (%s, %s, %s, %s)
        """, (employee_id, location, start_date, end_date))
        conn.commit()
        messagebox.showinfo("Success", "Employee bonus calculated successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error saving data: {err}")


# Connect to MySQL
conn = mysql.connector.connect(host="your_host", user="your_user", password="your_password", database="your_database")
cursor = conn.cursor()

# Tkinter Window Setup
root = tk.Tk()
root.title("Calculate Employee Bonus")
root.geometry("500x400")
root.configure(bg="white")

# UI Elements
tk.Label(root, text="Calculate Employee Bonus", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
tk.Label(root, text="EMPLOYEE ID", bg="white").pack()
entry_employee_id = tk.Entry(root)
entry_employee_id.pack()

tk.Label(root, text="LOCATION", bg="white").pack()
combo_location = ttk.Combobox(root, state="readonly")
combo_location.pack()

tk.Label(root, text="START DATE", bg="white").pack()
combo_start_date = ttk.Combobox(root, state="readonly")
combo_start_date.pack()

tk.Label(root, text="END DATE", bg="white").pack()
combo_end_date = ttk.Combobox(root, state="readonly")
combo_end_date.pack()

tk.Button(root, text="Submit", command=submit_bonus).pack(pady=10)
tk.Button(root, text="Back", command=root.quit).pack(pady=5)

root.mainloop()