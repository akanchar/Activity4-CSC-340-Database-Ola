import tkinter as tk
from tkinter import messagebox

def show_payroll():
    messagebox.showinfo("Payroll", "Displaying payroll details...")

# Tkinter Window Setup
root = tk.Tk()
root.title("Payroll View")
root.geometry("500x300")
root.configure(bg="white")

# UI Elements
tk.Label(root, text="Payroll", font=("Arial", 20, "bold"), bg="white").pack(pady=10)

tk.Button(root, text="View Payroll", command=show_payroll).pack(pady=10)
tk.Button(root, text="Back", command=root.quit).pack(pady=5)

root.mainloop()
