import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def submit_employee_rates():
    location = combo_location.get()
    employee_id = entry_employee_id.get()
    bonus_rate = entry_bonus_rate.get()
    rate_per_hour = entry_rate_per_hour.get()
    date = combo_date.get()

    try:
        cursor.execute("""
            INSERT INTO employee_rates (location, employee_id, bonus_rate, rate_per_hour, date)
            VALUES (%s, %s, %s, %s, %s)
        """, (location, employee_id, bonus_rate, rate_per_hour, date))
        conn.commit()
        messagebox.showinfo("Success", "Employee rates updated successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error saving data: {err}")


# Connect to MySQL
conn = mysql.connector.connect(host="your_host", user="your_user", password="your_password", database="your_database")
cursor = conn.cursor()

# Tkinter Window Setup
root = tk.Tk()
root.title("Set Employee Rates")
root.geometry("500x400")
root.configure(bg="white")

# UI Elements
tk.Label(root, text="Set Employee Rates", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
tk.Label(root, text="LOCATION", bg="white").pack()
combo_location = ttk.Combobox(root, state="readonly")
combo_location.pack()

tk.Label(root, text="EMPLOYEE ID", bg="white").pack()
entry_employee_id = tk.Entry(root)
entry_employee_id.pack()

tk.Label(root, text="BONUS RATE", bg="white").pack()
entry_bonus_rate = tk.Entry(root)
entry_bonus_rate.pack()

tk.Label(root, text="RATE PER HOUR", bg="white").pack()
entry_rate_per_hour = tk.Entry(root)
entry_rate_per_hour.pack()

tk.Label(root, text="DATE", bg="white").pack()
combo_date = ttk.Combobox(root, state="readonly")
combo_date.pack()

tk.Button(root, text="Submit", command=submit_employee_rates).pack(pady=10)
tk.Button(root, text="Back", command=root.quit).pack(pady=5)

root.mainloop()
