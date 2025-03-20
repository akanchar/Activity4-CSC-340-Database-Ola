import tkinter as tk
from tkinter import messagebox
import mysql.connector


def submit_withdrawal():
    username = entry_username.get()
    withdrawal_id = entry_id.get()
    amount = entry_amount.get()

    try:
        cursor.execute("""
            INSERT INTO withdrawals (username, withdrawal_id, amount)
            VALUES (%s, %s, %s)
        """, (username, withdrawal_id, amount))
        conn.commit()
        messagebox.showinfo("Success", "Withdrawal recorded successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error saving data: {err}")


# Connect to MySQL
conn = mysql.connector.connect(host="your_host", user="your_user", password="your_password", database="your_database")
cursor = conn.cursor()

# Tkinter Window Setup
root = tk.Tk()
root.title("Enter Withdrawal")
root.geometry("500x300")
root.configure(bg="white")

# UI Elements
tk.Label(root, text="Enter Withdrawal", font=("Arial", 20, "bold"), bg="white").pack(pady=10)
tk.Label(root, text="USERNAME", bg="white").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="ID", bg="white").pack()
entry_id = tk.Entry(root)
entry_id.pack()

tk.Label(root, text="AMOUNT", bg="white").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Button(root, text="Submit", command=submit_withdrawal).pack(pady=10)
tk.Button(root, text="Back", command=root.quit).pack(pady=5)

root.mainloop()