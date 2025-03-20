import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def submit_payroll():
    start_date = combo_start_date.get()
    end_date = combo_end_date.get()
    multiple_weeks = var_multiple_weeks.get()

    try:
        cursor.execute("""
            INSERT INTO payroll (start_date, end_date, multiple_weeks)
            VALUES (%s, %s, %s)
        """, (start_date, end_date, multiple_weeks))
        conn.commit()
        messagebox.showinfo("Success", "Payroll recorded successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error saving data: {err}")


# Connect to MySQL
conn = mysql.connector.connect(host="your_host", user="your_user", password="your_password", database="your_database")
cursor = conn.cursor()

# Tkinter Window Setup
root = tk.Tk()
root.title("Payroll")
root.geometry("500x300")
root.configure(bg="white")

# UI Elements
tk.Label(root, text="Payroll", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
tk.Label(root, text="FROM", bg="white").pack()
combo_start_date = ttk.Combobox(root, state="readonly")
combo_start_date.pack()

tk.Label(root, text="TO", bg="white").pack()
combo_end_date = ttk.Combobox(root, state="readonly")
combo_end_date.pack()

tk.Label(root, text="MULTIPLE WEEKS VIEW", bg="white").pack()
var_multiple_weeks = tk.BooleanVar()
chk_multiple_weeks = tk.Checkbutton(root, variable=var_multiple_weeks, bg="white")
chk_multiple_weeks.pack()

tk.Button(root, text="Submit", command=submit_payroll).pack(pady=10)
tk.Button(root, text="Back", command=root.quit).pack(pady=5)

root.mainloop()
