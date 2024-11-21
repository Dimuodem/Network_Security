import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Database Connection Function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1520',
            database='CampusSecurity'
        )
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

# Styled button creation
def create_button(parent, text, command):
    return tk.Button(
        parent, text=text, command=command,
        font=("Arial", 12, "bold"),
        bg="#4CAF50", fg="white",
        activebackground="#45a049", activeforeground="white",
        padx=10, pady=5
    )

# Styled label creation
def create_label(parent, text):
    return tk.Label(
        parent, text=text,
        font=("Arial", 12),
        bg="#f4f4f4", fg="#333"
    )

# Styled entry creation
def create_entry(parent, show=None):
    return tk.Entry(
        parent, show=show,
        font=("Arial", 12),
        bg="white", fg="#333",
        relief="groove", width=30
    )

# Register User Function
def register_user():
    name = entry_name.get()
    password = entry_password.get()
    role = entry_role.get()

    if name and password and role:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (name, password))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Registration Success", f"User {name} registered successfully!")
            login_frame.pack_forget()
            show_role_buttons()
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")
    else:
        messagebox.showerror("Input Error", "All fields must be filled.")

# Login User Function
def login_user():
    name = entry_name.get()
    password = entry_password.get()

    if name and password:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user:
                messagebox.showinfo("Login Success", f"Welcome {name}!")
                login_frame.pack_forget()
                show_role_buttons()
            else:
                messagebox.showerror("Login Error", "Invalid credentials. Please try again.")
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")
    else:
        messagebox.showerror("Input Error", "Please enter both username and password.")

# Show Role-Based Buttons (Student or Admin)
def show_role_buttons():
    login_frame.pack_forget()
    role_frame.pack()
    role_frame.configure(bg="#e7e7e7")

    tk.Label(role_frame, text="Select an Action", font=("Arial", 14, "bold"), bg="#e7e7e7").pack(pady=10)

    create_button(role_frame, "Student Role 1: Report Issue", command=show_issue_form).pack(pady=10)
    create_button(role_frame, "Student Role 2: Submit Suggestion", command=show_suggestion_form).pack(pady=10)
    create_button(role_frame, "Back to Login", command=back_to_login).pack(pady=10)

# Show Issue Reporting Form (Student Role 1)
def show_issue_form():
    role_frame.pack_forget()
    issue_form.pack()
    issue_form.configure(bg="#e7e7e7")

# Submit Issue Function (Student Role 1)
def submit_issue():
    issue = entry_issue.get()
    if issue:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO issues (stuid, issue_description) VALUES (%s, %s)", (1, issue))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Issue Submitted", "Your issue has been successfully submitted to the Admin.")
            issue_form.pack_forget()
            show_role_buttons()
    else:
        messagebox.showerror("Input Error", "Please enter an issue description.")

# Show Suggestion Submission Form (Student Role 2)
def show_suggestion_form():
    role_frame.pack_forget()
    suggestion_form.pack()
    suggestion_form.configure(bg="#e7e7e7")

# Submit Suggestion Function (Student Role 2)
def submit_suggestion():
    suggestion = entry_suggestion.get()
    if suggestion:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO suggestions (stuid, suggestion_description) VALUES (%s, %s)", (1, suggestion))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Suggestion Submitted", "Your suggestion has been successfully submitted.")
            suggestion_form.pack_forget()
            show_role_buttons()
    else:
        messagebox.showerror("Input Error", "Please enter a suggestion.")

# Go back to the login page
def back_to_login():
    role_frame.pack_forget()
    login_frame.pack()

# Main Window Setup
root = tk.Tk()
root.title("Campus Security Management")
root.geometry("600x400")
root.configure(bg="#f4f4f4")

# First Page Login/Register
login_frame = tk.Frame(root, bg="#f4f4f4")

create_label(login_frame, "Name:").pack(pady=5)
entry_name = create_entry(login_frame)
entry_name.pack(pady=5)

create_label(login_frame, "Password:").pack(pady=5)
entry_password = create_entry(login_frame, show="*")
entry_password.pack(pady=5)

create_label(login_frame, "Role (Student or Admin):").pack(pady=5)
entry_role = create_entry(login_frame)
entry_role.pack(pady=5)

create_button(login_frame, "Register User", register_user).pack(pady=10)
create_button(login_frame, "Login", login_user).pack(pady=10)

login_frame.pack()

#second page
role_frame = tk.Frame(root)

# Role 1 for student
issue_form = tk.Frame(root)
create_label(issue_form, "Describe your issue:").pack(pady=5)
entry_issue = create_entry(issue_form)
entry_issue.pack(pady=5)
create_button(issue_form, "Submit Issue", submit_issue).pack(pady=10)
create_button(issue_form, "Back", back_to_login).pack(pady=10)

# Role for students
suggestion_form = tk.Frame(root)
create_label(suggestion_form, "Enter your suggestion:").pack(pady=5)
entry_suggestion = create_entry(suggestion_form)
entry_suggestion.pack(pady=5)
create_button(suggestion_form, "Submit Suggestion", submit_suggestion).pack(pady=10)
create_button(suggestion_form, "Back", back_to_login).pack(pady=10)

root.mainloop()
