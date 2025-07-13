import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

def validate_email(email):
	if "@" in email and "." in email:
		return True
	else:
		return False

def validate_phone_number(phone_number):
	if phone_number.isdigit() and len(phone_number) == 10:
		return True
	else:
		return False

def validate_name(name):
	if not name.strip():
		return False
	if any(char.isdigit() or not char.isalnum() for char in name):
		return False
	return True

def submit_feedback():
	name = name_entry.get()
	email = email_entry.get()
	phone_number = phone_entry.get()
	feedback = feedback_entry.get("1.0", tk.END)
	choice = choice_var.get()

	if not name or not email or not phone_number or not feedback.strip() or choice == "":
		messagebox.showerror("Error", "Please fill in all fields.")
		return
	if not validate_email(email):
		messagebox.showerror("Error", "Invalid email format.")
		return
	if not validate_phone_number(phone_number):
		messagebox.showerror("Error", "Invalid phone number format. Phone number must be 10 digits long and contain only digits.")
		return
	if not validate_name(name):
		messagebox.showerror("Error", "Invalid name format. Name cannot contain digits, special characters, or spaces.")
		return

	conn = sqlite3.connect('feedbackkkk.db')
	c = conn.cursor()
	c.execute("INSERT INTO feedbacks (name, email, phone_number, feedback, choice) VALUES (?, ?, ?, ?, ?)", (name, email, phone_number, feedback, choice))
	conn.close()

	messagebox.showinfo("Success", "Feedback submitted successfully.")

def view_feedbacks():
	conn = sqlite3.connect('feedbackkkk.db')
	c = conn.cursor()
	c.execute("SELECT * FROM feedbacks")
	feedback_list = c.fetchall()
	conn.commit()
	conn.close()

	if feedback_list:
		feedback_window = tk.Toplevel(root)
		feedback_window.title("Feedbacks")
		feedback_text = tk.Text(feedback_window)
		feedback_text.pack()
		for feedback in feedback_list:
			feedback_text.insert(tk.END, f"Name: {feedback[0]}\nEmail: {feedback[1]}\nPhone Number: {feedback[2]}\nFeedback: {feedback[3]}\nChoice: {feedback[4]}\n\n")
		feedback_text.configure(state='disabled')
	else:	
		messagebox.showinfo("Info", "No feedbacks available.")

def admin_login():
	username = simpledialog.askstring("Admin Login", "Enter admin username:")
	password = simpledialog.askstring("Admin Login", "Enter admin password:", show='*')

	conn = sqlite3.connect("feedbackkkk.db")
	c = conn.cursor()
	c.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
	admin_data = c.fetchone()
	conn.close()

	if admin_data:
		global admin
		admin = True
		delete_button.config(state="normal")
		view_button.config(state="normal")
		messagebox.showinfo("Success", "Admin login successful.")
	else:
		messagebox.showerror("Error", "Invalid admin credentials.")


def delete_feedbacks():
	confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete all feedbacks?")
	if confirm:
		conn = sqlite3.connect('feedbackkkk.db')
		c = conn.cursor()
		c.execute("DELETE FROM feedbacks")
		conn.commit()
		conn.close()
		messagebox.showinfo("Success", "All feedbacks deleted successfully.")

def quit_app():
	confirm = messagebox.askyesno("Confirmation", "Are you sure you want to quit the application?")
	if confirm:
		root.destroy()

root = tk.Tk()
root.title("Feedback Management System")
f=("Century")
root.configure(bg="#008080")

label_title = tk.Label(root, text="Feedback Management System", font=(f, 20, "bold"))
label_title.grid(row=0, column=1, padx=10, pady=10)

label_name = tk.Label(root, text="Name:", font=(f, 16, "bold"))
label_name.grid(row=1, column=1, padx=10, pady=10)

name_entry = tk.Entry(root)
name_entry.grid(row=1, column=2, padx=20, pady=10)

label_email = tk.Label(root, text="Email:", font=(f, 16, "bold"))
label_email.grid(row=2, column=1, padx=10, pady=10)

email_entry = tk.Entry(root)
email_entry.grid(row=2, column=2, padx=10, pady=10)

label_phone = tk.Label(root, text="Phone Number:", font=(f, 16, "bold"))
label_phone.grid(row=3, column=1, padx=10, pady=10)

phone_entry = tk.Entry(root)
phone_entry.grid(row=3, column=2, padx=10, pady=10)

label_feedback = tk.Label(root, text="Feedback:", font=(f, 16, "bold"))
label_feedback.grid(row=4, column=1, padx=10, pady=10)

feedback_entry = tk.Text(root, height=5, width=30)
feedback_entry.grid(row=4, column=2, padx=10, pady=10)

label_choice = tk.Label(root, text="Rating:", font=(f, 16, "bold"))
label_choice.grid(row=5, column=1, padx=10, pady=10)

choice_var = tk.StringVar()
choices = ["1", "2", "3", "4", "5"]
choice_dropdown = tk.OptionMenu(root, choice_var, *choices)
choice_dropdown.grid(row=5, column=2, padx=10, pady=10)

submit_button = tk.Button(root, text="Submit", command=submit_feedback, font=(f, 14, "bold"))
submit_button.grid(row=6, column=1, padx=10, pady=10)

admin_login_button = tk.Button(root, text="Admin Login", command=admin_login, font=(f, 14, "bold"))
admin_login_button.grid(row=6, column=2, padx=10, pady=10)

delete_button = tk.Button(root, text="Delete Feedbacks", command=delete_feedbacks, state="disabled", font=(f, 14, "bold"))
delete_button.grid(row=7, column=1, padx=10, pady=10)

view_button = tk.Button(root, text="View Feedbacks", command=view_feedbacks, state="disabled", font=(f, 14, "bold"))
view_button.grid(row=7, column=2, padx=10, pady=10)

quit_button = tk.Button(root, text="Quit", command=quit_app, font=(f, 14, "bold"))
quit_button.grid(row=8, column=1, padx=10, pady=10)

root.mainloop()
