import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from styles import apply_styles

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

# Register Admin Function
def register_admin():
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
            messagebox.showinfo("Registration Success", f"Admin {name} registered successfully!")
            login_frame.pack_forget()
            show_admin_buttons()
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")
    else:
        messagebox.showerror("Input Error", "All fields must be filled.")

# Login Admin Function
def login_admin():
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
                messagebox.showinfo("Login Success", f"Welcome Admin {name}!")
                login_frame.pack_forget()
                show_admin_buttons()
            else:
                messagebox.showerror("Login Error", "Invalid credentials. Please try again.")
        else:
            messagebox.showerror("Database Error", "Failed to connect to the database.")
    else:
        messagebox.showerror("Input Error", "Please enter both username and password.")

# Show Admin Functions Buttons 
def show_admin_buttons():
    # Hide the login/register page
    login_frame.pack_forget()

    # Create a new frame for admin options
    admin_frame.pack()

    tk.Button(admin_frame, text="View Student Issues", command=view_student_issues).pack(pady=10)
    tk.Button(admin_frame, text="Delete User", command=delete_user).pack(pady=10)
    tk.Button(admin_frame, text="Close Network", command=close_network).pack(pady=10)
    tk.Button(admin_frame, text="Respond to Suggestions", command=respond_to_suggestions).pack(pady=10)
    tk.Button(admin_frame, text="Open Network", command=open_network).pack(pady=10)
    tk.Button(admin_frame, text="Back to Login", command=back_to_login).pack(pady=10)

# View and Address Student Issues
def view_student_issues():
    admin_frame.pack_forget()
    issues_frame.pack()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM issues")
    issues = cursor.fetchall()
    cursor.close()
    conn.close()

    for issue in issues:
        issue_id = issue[0]
        stuid = issue[1]
        description = issue[3]
        tk.Button(issues_frame, text=f"Issue ID: {issue_id} - {description}", command=lambda issue_id=issue_id: address_issue(issue_id)).pack(pady=10)

def address_issue(issue_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM issues WHERE issue_id = %s", (issue_id,))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Issue Addressed", "The issue has been addressed and removed from the database.")
    issues_frame.pack_forget()
    show_admin_buttons()

# Delete User Function
def delete_user():
    admin_frame.pack_forget()
    delete_user_frame.pack()

    tk.Label(delete_user_frame, text="Enter user ID to delete:").pack(pady=5)
    entry_user_id = tk.Entry(delete_user_frame)
    entry_user_id.pack(pady=5)
    tk.Button(delete_user_frame, text="Delete User", command=lambda: delete_user_from_db(entry_user_id.get())).pack(pady=10)

def delete_user_from_db(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("User Deleted", f"User with ID {user_id} has been deleted.")
    delete_user_frame.pack_forget()
    show_admin_buttons()

# Close Network Function
def close_network():
    messagebox.showinfo("Network Status", "Campus network has been closed by Admin.")
    show_admin_buttons()

# Respond to Suggestions Function
def respond_to_suggestions():
    admin_frame.pack_forget()
    respond_suggestion_frame.pack()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM suggestions")
    suggestions = cursor.fetchall()
    cursor.close()
    conn.close()

    for suggestion in suggestions:
        suggestion_id = suggestion[0]
        suggestion_description = suggestion[3]
        tk.Button(respond_suggestion_frame, text=f"Suggestion ID: {suggestion_id} - {suggestion_description}", command=lambda suggestion_id=suggestion_id: respond_to_single_suggestion(suggestion_id)).pack(pady=10)

def respond_to_single_suggestion(suggestion_id):
    respond_suggestion_frame.pack_forget()
    response_form.pack()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT suggestion_description FROM suggestions WHERE suggestion_id = %s", (suggestion_id,))
    suggestion = cursor.fetchone()
    cursor.close()
    conn.close()

    tk.Label(response_form, text=f"Responding to suggestion: {suggestion[0]}").pack(pady=5)
    response_entry = tk.Entry(response_form, width=50)
    response_entry.pack(pady=5)
    tk.Button(response_form, text="Submit Response", command=lambda: submit_suggestion_response(suggestion_id, response_entry.get())).pack(pady=10)

def submit_suggestion_response(suggestion_id, response):
    if response:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO responses (suggestion_id, response_description) VALUES (%s, %s)", (suggestion_id, response))
        cursor.execute("DELETE FROM suggestions WHERE suggestion_id = %s", (suggestion_id,))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Response Submitted", "The suggestion has been responded to and removed from the database.")
        response_form.pack_forget()
        show_admin_buttons()
    else:
        messagebox.showerror("Input Error", "Please enter a response.")

# Open Network Function
def open_network():
    messagebox.showinfo("Network Status", "Campus network has been reopened successfully by Admin.")
    show_admin_buttons()

# Back to Login page
def back_to_login():
    admin_frame.pack_forget()
    login_frame.pack()

# Main Tkinter Window Setup
root = tk.Tk()
root.title("Campus Security Management")

# First Page (Login/Register)
login_frame = tk.Frame(root)

# Create input fields and labels for Register/Login
tk.Label(login_frame, text="Name:").pack(pady=5)
entry_name = tk.Entry(login_frame)
entry_name.pack(pady=5)

tk.Label(login_frame, text="Password:").pack(pady=5)
entry_password = tk.Entry(login_frame, show="*")
entry_password.pack(pady=5)

tk.Label(login_frame, text="Role (Admin):").pack(pady=5)
entry_role = tk.Entry(login_frame)
entry_role.pack(pady=5)

# Buttons for Register and Login
tk.Button(login_frame, text="Register Admin", command=register_admin).pack(pady=10)
tk.Button(login_frame, text="Login", command=login_admin).pack(pady=10)

login_frame.pack()

# Admin Buttons Page
admin_frame = tk.Frame(root)

# Frame for Viewing Issues
issues_frame = tk.Frame(root)

# Frame for Deleting Users
delete_user_frame = tk.Frame(root)

# Frame for Responding to Suggestions
respond_suggestion_frame = tk.Frame(root)

# Frame for Submitting Responses
response_form = tk.Frame(root)

# Run the Tkinter main loop
root.mainloop()
