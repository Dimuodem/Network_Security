import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # MySQL username
        password="1520",  # MySQL password
        database="CampSec"
    )

# Function to submit issue
def submit_issue():
    issue_window = tk.Toplevel()
    issue_window.title("Report Issue")

    tk.Label(issue_window, text="Describe the Issue:").pack(pady=5)
    issue_description = tk.Entry(issue_window, width=50)
    issue_description.pack(pady=5)

    def submit():
        issue_text = issue_description.get()
        if not issue_text:
            messagebox.showwarning("Input Error", "Please describe the issue!")
            return

        # Save the issue to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO issues (issue_description) VALUES (%s)", (issue_text,))
        conn.commit()
        cursor.close()

        messagebox.showinfo("Issue Submitted", "Your issue has been successfully submitted to the admin.")
        issue_window.destroy()

    tk.Button(issue_window, text="Submit Issue", command=submit).pack(pady=10)
