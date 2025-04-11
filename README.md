Aloha Corp Application

Aloha Corp is a role-based desktop application built with Python and Tkinter that streamlines essential business operations for employees, managers, and owners. Users can log in according to their assigned role to 
manage invoices, expenses, payroll, daily closeouts, and more. The application integrates with a MySQL database and enforces authentication through bcrypt for secure password handling.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Table of Contents

1. Project Overview

2. Installation Instructions

3. Usage Guide

4. Database Details

5. Code Structure

6. Future Enhancements

7. Contributor Information

8. Additional Context

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Project Overview

The Aloha Corp application provides a unified interface for day-to-day operations:

  - Role-based Login for Employee, Manager, and Owner.

  - Daily Closeouts (cash, credit totals, differences).

  - Invoice and Expense data entry.

  - Payroll Reporting and bonus calculations.

  - Employee Management (adding new employees, setting rates).

  - Database Connectivity to store and retrieve data in MySQL.

  - Managers and owners have elevated access to tasks like setting employee rates, viewing records, and entering withdrawals, while employees focus on daily tasks such as closeouts and in/out balances.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Installation Instructions

Clone the repository:
cd aloha-corp-app

Setup MySQL Database with your own Username and Password:
host="localhost"
user="root"        #Chnage to your unique user
password="root"    #Change to your unique password
database="triall"  #create this database in your DataGrip

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Usage Guide

1. Welcome Screen
On launching the application, you'll see a welcome screen with:

- Login: Directs you to the login flow.
- Create New Account: For managers/owners to create new managerial/ownership accounts.

2. Account Creation
- Roles supported: Employee, Manager, Owner.
- Employees can only be created by existing managers or owners.
- Passwords are hashed with bcrypt for security.

3. Login Workflow
- Select a store location (e.g., “Store 1”).
- Enter your username and password.
- If authentication is successful, you’ll be directed to either the Employee, Manager, or Owner home screen based on your assigned role.

4. Role-Specific Dashboards
Employee Home
- Enter Day Closeout (cash, credit, totals).
- Record In/Out Balance (start/end shifts).
- Log Expenses.

Manager Home
- Access Invoices, Expenses, Day Closeout, Withdrawals, Employee Rates, etc.
- Perform tasks like adding employees, calculating bonuses, and entering merchandise info.

Owner Home
- Similar to Manager, but with additional privileges if needed (such as advanced or company-wide settings).

Payroll & Bonus
- A dedicated form to set date ranges for payroll or to calculate bonuses based on established rates.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Database Details

1. Table Creation
The application will auto-create the following tables on startup if they don’t exist:
- Users: Stores username, hashed password, and role.
- Invoices: Tracks company invoices, amounts, and due dates.
- Expenses: Logs business expenses with date and type.
- Day Closeout: Records employee daily totals, differences, and notes.
- In/Out Bal: Tracks beginning and ending balances, clock-in/out times, and location.
- Merchandise, Withdrawals, Employee Rates, Payroll, Employee Bonus.

2. Integration
- Insert and retrieval queries are performed within the Tkinter event handlers (e.g., pressing “Submit”).
- bcrypt is used in the login logic to verify hashed passwords.

3. Potential for Stored Procedures / Triggers
- You could define SQL triggers to enforce business logic (e.g., automatically mark invoices ‘Past Due’).
- Stored procedures can handle complex tasks (like batch payroll calculations).

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Code Structure

AlohaCorpApp.py
The main file containing:
Class AlohaCorpApp: Inherits from tk.Tk, sets up the main window, top bar, and frames.
Database Setup: Creates tables if they do not exist.
GUI Screens: Functions like show_welcome_screen(), show_manager_home(), etc.
Flow: go_back() method to navigate, role-based logic for employees vs. managers vs. owners.

Key Functions:
login_action() / process_login(): Handle user authentication.
create_account_action() / process_manager_owner_login(): Manager/Owner account creation.
show_employee_home(), show_manager_home(), show_owner_home(): Role-based dashboards.
toggle_dark_mode(), set_theme(): Provides a dark mode theme for the GUI.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Future Enhancements:

TTK Styles
Switch from tk.* to ttk.* widgets for a more modern look. Add a style manager for consistent fonts, backgrounds, etc.

Reporting & Export
Provide an option to export daily closeout, invoice, or expense data to CSV/PDF for record-keeping.

Triggers and Procedures
Incorporate SQL triggers for actions like automatically updating invoice status. Use stored procedures for complex tasks like payroll or advanced bonus calculations.

Audit Logs
Implement an audit_log table to track major changes (e.g., user creation, day closeout submissions) with timestamps.

More Granular Role Permissions
Introduce sub-roles or additional constraints so some managers can only view certain stores, etc.

Enhanced UI
Add a tabbed interface (ttk.Notebook) for manager/owner tasks to keep the interface cleaner and simpler.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Contributor Information

Ola Abdelnaby ola.abdelnaby@spartans.ut.edu

Philip Corrado philip.corrado@spartans.ut.edu

Andrew Hunt andrew.hunt@spartans.ut.edu

Salvatore Romano salvatore.romano@spartans.ut.edu

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Additional Context










