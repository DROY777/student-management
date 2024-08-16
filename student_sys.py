import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from mysql.connector import Error

# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Droy",
        database="student_management"
    )

# User authentication functions
def register_user(username, password):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        connection.close()
        return True
    except Error as e:
        print(f"The error '{e}' occurred")
        return False

def login_user(username, password):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        connection.close()
        return user is not None
    except Error as e:
        print(f"The error '{e}' occurred")
        return False

# Student management functions with validation for null values
def add_student(name, age, grade):
    if not name or not age or not grade:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, age, grade) VALUES (%s, %s, %s)", (name, age, grade))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Student added successfully!")
    except Error as e:
        print(f"The error '{e}' occurred")

def update_student(student_id, name=None, age=None, grade=None):
    if not student_id:
        messagebox.showerror("Error", "Student ID is required to update a record!")
        return

    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Fetch current values if fields are empty
        cursor.execute("SELECT name, age, grade FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()

        if student is None:
            messagebox.showerror("Error", "Student not found!")
            connection.close()
            return

        current_name, current_age, current_grade = student

        # Use the current values if no new value is provided
        name = name if name else current_name
        age = age if age else current_age
        grade = grade if grade else current_grade

        cursor.execute(
            "UPDATE students SET name = %s, age = %s, grade = %s WHERE id = %s",
            (name, age, grade, student_id)
        )
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Student updated successfully!")
    except Error as e:
        print(f"The error '{e}' occurred")

def delete_student(student_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", "Student deleted successfully!")
    except Error as e:
        print(f"The error '{e}' occurred")

def search_student(student_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        connection.close()
        return student
    except Error as e:
        print(f"The error '{e}' occurred")
        return None

def get_all_students():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        connection.close()
        return students
    except Error as e:
        print(f"The error '{e}' occurred")
        return []

# GUI functions
def register():
    username = entry_username.get()
    password = entry_password.get()
    if register_user(username, password):
        messagebox.showinfo("Success", "Registration successful!")
    else:
        messagebox.showerror("Error", "Registration failed!")

def login():
    username = entry_username.get()
    password = entry_password.get()
    if login_user(username, password):
        open_management_window()
    else:
        messagebox.showerror("Error", "Login failed!")

def open_management_window():
    management_window = tk.Toplevel(root)
    management_window.title("Student Management")
    management_window.geometry("1000x500")

    # Load background image for management window
    bg_image = Image.open("E:\IITM\Python\manage.png")  # Provide the path to your image here
    bg_image = bg_image.resize((1000, 500), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create canvas and set background image
    canvas_mgmt = tk.Canvas(management_window, width=1000, height=500)
    canvas_mgmt.pack(fill="both", expand=True)
    canvas_mgmt.create_image(0, 0, image=bg_photo, anchor="nw")
     
    # Add student
    canvas_mgmt.create_text(160, 15, text="Student Console", fill="black", font=("Arial", 25))
    canvas_mgmt.create_text(70, 60, text="Name", fill="black", font=("Arial", 15))
    entry_name = tk.Entry(management_window, font=("Arial", 15))
    canvas_mgmt.create_window(220, 60, window=entry_name)

    canvas_mgmt.create_text(80, 90, text="Age", fill="black", font=("Arial", 15))
    entry_age = tk.Entry(management_window, font=("Arial", 15))
    canvas_mgmt.create_window(220, 90, window=entry_age)

    canvas_mgmt.create_text(90, 130, text="Grade", fill="black", font=("Arial", 15))
    entry_grade = tk.Entry(management_window, font=("Arial", 15))
    canvas_mgmt.create_window(250, 130, window=entry_grade)

    def add():
        name = entry_name.get()
        age = entry_age.get()
        grade = entry_grade.get()
        add_student(name, age, grade)

    button_add = tk.Button(management_window, text="Add Student", font=("Arial", 12), command=add)
    canvas_mgmt.create_window(190, 210, window=button_add)

    # Update student
    canvas_mgmt.create_text(70, 170, text="Student ID", fill="black", font=("Arial", 15))
    entry_id = tk.Entry(management_window, font=("Arial", 15))
    canvas_mgmt.create_window(250, 170, window=entry_id)

    def update():
        student_id = entry_id.get()
        name = entry_name.get()
        age = entry_age.get()
        grade = entry_grade.get()
        update_student(student_id, name, age, grade)

    button_update = tk.Button(management_window, text="Update Student", font=("Arial", 12), command=update)
    canvas_mgmt.create_window(440, 210, window=button_update)

    # Delete student
    def delete():
        student_id = entry_id.get()
        delete_student(student_id)

    button_delete = tk.Button(management_window, text="Delete Student", font=("Arial", 12), command=delete)
    canvas_mgmt.create_window(310, 210, window=button_delete)

    # Search student
    def search():
        student_id = entry_id.get()
        student = search_student(student_id)
        if student:
            entry_name.delete(0, tk.END)
            entry_name.insert(0, student[1])
            entry_age.delete(0, tk.END)
            entry_age.insert(0, student[2])
            entry_grade.delete(0, tk.END)
            entry_grade.insert(0, student[3])
        else:
            messagebox.showerror("Error", "Student not found!")

    button_search = tk.Button(management_window, text="Search Student", font=("Arial", 12), command=search)
    canvas_mgmt.create_window(200, 250, window=button_search)

    # List students
    text_students = tk.Text(management_window, height=10, width=60, font=("Arial", 10))
    canvas_mgmt.create_window(350, 370, window=text_students)

    def list_students():
        text_students.delete(1.0, tk.END)
        students = get_all_students()
        for student in students:
            text_students.insert(tk.END, f"ID: {student[0]}, Name: {student[1]}, Age: {student[2]}, Grade: {student[3]}\n")

    button_list = tk.Button(management_window, text="List Students", font=("Arial", 12), command=list_students)
    canvas_mgmt.create_window(330, 250, window=button_list)

    management_window.mainloop()

# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("600x400")

# Load background image for main window
background_image = Image.open("E:\IITM\Python\stu.jpg")  # Provide the path to your image here
background_image = background_image.resize((600, 400), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

# Create canvas and set background image
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

text_id = canvas.create_text(300, 50, text="Student Management System", fill="black", font=("Arial", 25))
# Measure the text to draw the underline
text_bbox = canvas.bbox(text_id)  # Get the bounding box of the text
underline_y = text_bbox[3] + 5  # Position for the underline, slightly below the text
# Draw the underline
canvas.create_line(text_bbox[0], underline_y, text_bbox[2], underline_y, fill="black", width=2) 

# Add labels and entries
canvas.create_text(140, 120, text="Username", fill="black", font=("Arial", 15))
entry_username = tk.Entry(root, font=("Arial", 12))
canvas.create_window(300, 120, window=entry_username)

canvas.create_text(140, 170, text="Password", fill="black", font=("Arial", 15))
entry_password = tk.Entry(root, show="*", font=("Arial", 12))
canvas.create_window(300, 170, window=entry_password)

# Register button
button_register = tk.Button(root, text="Register", font=("Arial", 12), command=register)
canvas.create_window(140, 222, window=button_register)

button_login = tk.Button(root, text="Login", font=("Arial", 12), command=login)
canvas.create_window(270, 222, window=button_login)
root.mainloop()
