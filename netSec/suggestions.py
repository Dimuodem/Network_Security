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

# Function to submit suggestion
def submit_suggestion():
    suggestion_window = tk.Toplevel()
    suggestion_window.title("Add Suggestion")

    tk.Label(suggestion_window, text="Enter your suggestion:").pack(pady=5)
    suggestion_description = tk.Entry(suggestion_window, width=50)
    suggestion_description.pack(pady=5)

    def submit():
        suggestion_text = suggestion_description.get()
        if not suggestion_text:
            messagebox.showwarning("Input Error", "Please enter a suggestion!")
            return

        # Save the suggestion to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO suggestions (suggestion_description) VALUES (%s)", (suggestion_text,))
        conn.commit()
        cursor.close()

        messagebox.showinfo("Suggestion Submitted", "Your suggestion has been successfully submitted to the admin.")
        suggestion_window.destroy()
