import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


def submit_day_closeout():
    username = entry_username.get()
    cash = entry_cash.get()
    credit = entry_credit.get()
    total = entry_total.get()
    difference = entry_difference.get()
    closeout_date = combo_date.get()
    notes = entry_notes.get("1.0", tk.END)

    try:
        cursor.execute("""
            INSERT INTO day_closeout (employee_name, cash, credit, total, difference, closeout_date, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (username, cash, credit, total, difference, closeout_date, notes))
        conn.commit()
        messagebox.showinfo("Success", "Day Closeout recorded successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error saving data: {err}")


# Connect to MySQL
conn = mysql.connector.connect(host="your_host", user="your_user", password="your_password", database="your_database")
cursor = conn.cursor()

# Tkinter Window Setup
root = tk.Tk()
root.title("Enter Day Closeout")
root.geometry("500x500")
root.configure(bg="white")

# UI Elements
tk.Label(root, text="Enter Day Closeout", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
tk.Label(root, text="EMPLOYEE USERNAME", bg="white").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="CASH", bg="white").pack()
entry_cash = tk.Entry(root)
entry_cash.pack()

tk.Label(root, text="CREDIT", bg="white").pack()
entry_credit = tk.Entry(root)
entry_credit.pack()

tk.Label(root, text="TOTAL", bg="white").pack()
entry_total = tk.Entry(root)
entry_total.pack()

tk.Label(root, text="DIFFERENCE", bg="white").pack()
entry_difference = tk.Entry(root)
entry_difference.pack()

tk.Label(root, text="DATE", bg="white").pack()
combo_date = ttk.Combobox(root, state="readonly")
combo_date.pack()

tk.Label(root, text="NOTES", bg="white").pack()
entry_notes = tk.Text(root, height=5, width=40)
entry_notes.pack()

tk.Button(root, text="Submit", command=submit_day_closeout).pack(pady=10)
tk.Button(root, text="Back", command=root.quit).pack(pady=5)

root.mainloop()