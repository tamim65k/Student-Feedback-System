import customtkinter as ctk
import tkinter.messagebox
import sqlite3

# Set the appearance mode to "Light"
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class FeedbackApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Student Feedback System")
        self.geometry("600x400")

        # Initialize a frame reference to keep track of the current frame
        self.current_frame = None

        # Initialize the SQLite database
        self.init_db()

        # Setup the initial login frame
        self.setup_login_frame()

    def init_db(self):
    # Connect to SQLite database
        self.conn = sqlite3.connect('feedback_app.db')
        self.cursor = self.conn.cursor()

        # Create Users table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                name TEXT,
                number TEXT,
                department TEXT,
                batch TEXT,
                roll TEXT,
                reg_no TEXT,
                blood_group TEXT
            )
        ''')

        # Create Feedback table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                course TEXT,
                instructor TEXT,
                feedback TEXT,
                rating INTEGER,
                anonymous INTEGER DEFAULT 0,
                upvotes INTEGER DEFAULT 0,
                downvotes INTEGER DEFAULT 0,
                FOREIGN KEY(user_id) REFERENCES Users(id)
            )
        ''')

        # Check if the 'anonymous' column exists, if not, add it
        self.cursor.execute("PRAGMA table_info(Feedback)")
        columns = [column[1] for column in self.cursor.fetchall()]
        if 'anonymous' not in columns:
            self.cursor.execute('ALTER TABLE Feedback ADD COLUMN anonymous INTEGER DEFAULT 0')

        # Check if the 'upvotes' column exists, if not, add it
        if 'upvotes' not in columns:
            self.cursor.execute('ALTER TABLE Feedback ADD COLUMN upvotes INTEGER DEFAULT 0')

        # Check if the 'downvotes' column exists, if not, add it
        if 'downvotes' not in columns:
            self.cursor.execute('ALTER TABLE Feedback ADD COLUMN downvotes INTEGER DEFAULT 0')

        # Drop the existing Votes table if it exists
        self.cursor.execute('DROP TABLE IF EXISTS Votes')

        # Create Votes table
        self.cursor.execute('''
            CREATE TABLE Votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                feedback_id INTEGER,
                vote_type TEXT,
                FOREIGN KEY(user_id) REFERENCES Users(id),
                FOREIGN KEY(feedback_id) REFERENCES Feedback(id)
            )
        ''')

        self.conn.commit()


    def setup_login_frame(self):
        # Clear the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        # Login Frame
        self.login_frame = ctk.CTkFrame(self)
        self.login_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = self.login_frame

        self.email_label = ctk.CTkLabel(self.login_frame, text="Email")
        self.email_label.grid(row=0, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.email_entry = ctk.CTkEntry(self.login_frame)
        self.email_entry.grid(row=0, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.password_label = ctk.CTkLabel(self.login_frame, text="Password")
        self.password_label.grid(row=1, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", width=100, command=self.login)
        self.login_button.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=10)

        self.register_button = ctk.CTkButton(self.login_frame, text="Register", width=100, command=self.show_register_frame)
        self.register_button.grid(row=3, column=0, columnspan=1, padx=(50, 10), pady=10)

        self.login_frame.grid_columnconfigure(1, weight=1)

    def show_register_frame(self):
        # Clear the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        # Register Frame
        self.register_frame = ctk.CTkFrame(self)
        self.register_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = self.register_frame

        self.register_name_label = ctk.CTkLabel(self.register_frame, text="Name")
        self.register_name_label.grid(row=0, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_name_entry = ctk.CTkEntry(self.register_frame)
        self.register_name_entry.grid(row=0, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_email_label = ctk.CTkLabel(self.register_frame, text="Email")
        self.register_email_label.grid(row=1, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_email_entry = ctk.CTkEntry(self.register_frame)
        self.register_email_entry.grid(row=1, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_password_label = ctk.CTkLabel(self.register_frame, text="Password")
        self.register_password_label.grid(row=2, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_password_entry = ctk.CTkEntry(self.register_frame, show="*")
        self.register_password_entry.grid(row=2, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_number_label = ctk.CTkLabel(self.register_frame, text="Phone Number")
        self.register_number_label.grid(row=3, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_number_entry = ctk.CTkEntry(self.register_frame)
        self.register_number_entry.grid(row=3, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_department_label = ctk.CTkLabel(self.register_frame, text="Department")
        self.register_department_label.grid(row=4, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_department_entry = ctk.CTkEntry(self.register_frame)
        self.register_department_entry.grid(row=4, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_batch_label = ctk.CTkLabel(self.register_frame, text="Batch")
        self.register_batch_label.grid(row=5, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_batch_entry = ctk.CTkEntry(self.register_frame)
        self.register_batch_entry.grid(row=5, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_roll_label = ctk.CTkLabel(self.register_frame, text="Roll Number")
        self.register_roll_label.grid(row=6, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_roll_entry = ctk.CTkEntry(self.register_frame)
        self.register_roll_entry.grid(row=6, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_reg_no_label = ctk.CTkLabel(self.register_frame, text="Registration Number")
        self.register_reg_no_label.grid(row=7, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_reg_no_entry = ctk.CTkEntry(self.register_frame)
        self.register_reg_no_entry.grid(row=7, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_blood_group_label = ctk.CTkLabel(self.register_frame, text="Blood Group")
        self.register_blood_group_label.grid(row=8, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_blood_group_entry = ctk.CTkEntry(self.register_frame)
        self.register_blood_group_label.grid(row=8, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_blood_group_entry = ctk.CTkEntry(self.register_frame)
        self.register_blood_group_entry.grid(row=8, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_button = ctk.CTkButton(self.register_frame, text="Register", width=100, command=self.register)
        self.register_button.grid(row=9, column=1, columnspan=1, padx=(20, 0), pady=10)

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", width=100, command=self.setup_login_frame)
        self.back_to_login_button.grid(row=9, column=0, columnspan=1, padx=(50, 10), pady=10)

        self.register_frame.grid_columnconfigure(1, weight=1)

    def register(self):
        name = self.register_name_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        number = self.register_number_entry.get()
        department = self.register_department_entry.get()
        batch = self.register_batch_entry.get()
        roll = self.register_roll_entry.get()
        reg_no = self.register_reg_no_entry.get()
        blood_group = self.register_blood_group_entry.get()

        try:
            self.cursor.execute('''
                INSERT INTO Users (name, email, password, number, department, batch, roll, reg_no, blood_group)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, password, number, department, batch, roll, reg_no, blood_group))
            self.conn.commit()
            tkinter.messagebox.showinfo("Register", "Registration Successful!")
            self.setup_login_frame()
        except sqlite3.IntegrityError:
            tkinter.messagebox.showerror("Register", "Email already registered!")

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        self.cursor.execute('SELECT id FROM Users WHERE email = ? AND password = ?', (email, password))
        user = self.cursor.fetchone()

        if user:
            self.user_id = user[0]
            tkinter.messagebox.showinfo("Login", "Login Successful!")
            self.setup_dashboard()
        else:
            tkinter.messagebox.showerror("Login", "Invalid credentials")

    def setup_dashboard(self):
        # Clear the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        self.dashboard_frame = ctk.CTkFrame(self)
        self.dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = self.dashboard_frame

        self.welcome_label = ctk.CTkLabel(self.dashboard_frame, text="Welcome to the Dashboard!")
        self.welcome_label.pack(pady=10)

        self.profile_button = ctk.CTkButton(self.dashboard_frame, text="User Profile", command=self.show_profile)
        self.profile_button.pack(pady=10)

        self.feedback_button = ctk.CTkButton(self.dashboard_frame, text="Give Feedback", command=self.show_feedback_form)
        self.feedback_button.pack(pady=10)

        self.history_button = ctk.CTkButton(self.dashboard_frame, text="Feedback History", command=self.show_feedback_history)
        self.history_button.pack(pady=10)

        self.all_feedback_button = ctk.CTkButton(self.dashboard_frame, text="Show All Feedback", command=self.show_all_feedback)
        self.all_feedback_button.pack(pady=10)

    def show_profile(self):
        # Clear the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        self.profile_frame = ctk.CTkFrame(self)
        self.profile_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = self.profile_frame

        self.profile_label = ctk.CTkLabel(self.profile_frame, text="User Profile")
        self.profile_label.pack(pady=10)

        self.cursor.execute('SELECT name, email, number, department, batch, roll, reg_no, blood_group FROM Users WHERE id = ?', (self.user_id,))
        user_data = self.cursor.fetchone()

        self.name_label = ctk.CTkLabel(self.profile_frame, text=f"Name: {user_data[0]}")
        self.name_label.pack(pady=5)
        self.email_label = ctk.CTkLabel(self.profile_frame, text=f"Email: {user_data[1]}")
        self.email_label.pack(pady=5)
        self.number_label = ctk.CTkLabel(self.profile_frame, text=f"Phone Number: {user_data[2]}")
        self.number_label.pack(pady=5)
        self.department_label = ctk.CTkLabel(self.profile_frame, text=f"Department: {user_data[3]}")
        self.department_label.pack(pady=5)
        self.batch_label = ctk.CTkLabel(self.profile_frame, text=f"Batch: {user_data[4]}")
        self.batch_label.pack(pady=5)
        self.roll_label = ctk.CTkLabel(self.profile_frame, text=f"Roll Number: {user_data[5]}")
        self.roll_label.pack(pady=5)
        self.reg_no_label = ctk.CTkLabel(self.profile_frame, text=f"Registration Number: {user_data[6]}")
        self.reg_no_label.pack(pady=5)
        self.blood_group_label = ctk.CTkLabel(self.profile_frame, text=f"Blood Group: {user_data[7]}")
        self.blood_group_label.pack(pady=5)

        self.back_button = ctk.CTkButton(self.profile_frame, text="Back to Dashboard", command=self.setup_dashboard)
        self.back_button.pack(pady=20)

    def show_feedback_form(self):
        # Clear the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        self.feedback_frame = ctk.CTkFrame(self)
        self.feedback_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = self.feedback_frame

        self.feedback_label = ctk.CTkLabel(self.feedback_frame, text="Feedback Form")
        self.feedback_label.pack(pady=10)

        self.course_label = ctk.CTkLabel(self.feedback_frame, text="Course")
        self.course_label.pack(pady=5)
        self.course_entry = ctk.CTkEntry(self.feedback_frame)
        self.course_entry.pack(pady=5)

        self.instructor_label = ctk.CTkLabel(self.feedback_frame, text="Instructor")
        self.instructor_label.pack(pady=5)
        self.instructor_entry = ctk.CTkEntry(self.feedback_frame)
        self.instructor_entry.pack(pady=5)

        self.feedback_text_label = ctk.CTkLabel(self.feedback_frame, text="Feedback")
        self.feedback_text_label.pack(pady=5)
        self.feedback_entry = ctk.CTkEntry(self.feedback_frame)
        self.feedback_entry.pack(pady=5)

        self.rating_label = ctk.CTkLabel(self.feedback_frame, text="Rating (out of 5)")
        self.rating_label.pack(pady=5)
        self.rating_entry = ctk.CTkEntry(self.feedback_frame)
        self.rating_entry.pack(pady=5)

        self.anonymous_var = ctk.IntVar()
        self.anonymous_check = ctk.CTkCheckBox(self.feedback_frame, text="Submit Anonymously", variable=self.anonymous_var)
        self.anonymous_check.pack(pady=5)

        self.submit_button = ctk.CTkButton(self.feedback_frame, text="Submit", command=self.submit_feedback)
        self.submit_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.feedback_frame, text="Back to Dashboard", command=self.setup_dashboard)
        self.back_button.pack(pady=10)

    def submit_feedback(self):
        course = self.course_entry.get()
        instructor = self.instructor_entry.get()
        feedback = self.feedback_entry.get()
        rating = self.rating_entry.get()
        anonymous = self.anonymous_var.get()

        user_id = None if anonymous else self.user_id

        # Save feedback to the database
        self.cursor.execute('''
            INSERT INTO Feedback (user_id, course, instructor, feedback, rating, anonymous)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, course, instructor, feedback, rating, anonymous))
        self.conn.commit()

        tkinter.messagebox.showinfo("Feedback", "Feedback Submitted!")
        self.setup_dashboard()

    def show_feedback_history(self):
        # Clear the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = self.history_frame

        self.history_label = ctk.CTkLabel(self.history_frame, text="Feedback History")
        self.history_label.pack(pady=10)

        # Load feedback history from the database
        self.cursor.execute('SELECT id, course, instructor, feedback, rating, anonymous FROM Feedback WHERE user_id = ? OR anonymous = 1', (self.user_id,))
        feedbacks = self.cursor.fetchall()

        for feedback in feedbacks:
            feedback_id, course, instructor, feedback_text, rating, anonymous = feedback
            anonymity_status = "Anonymous" if anonymous else "User"
            feedback_text = f"Course: {course}, Instructor: {instructor}, Feedback: {feedback_text}, Rating: {rating}/5, Status: {anonymity_status}"
            feedback_label = ctk.CTkLabel(self.history_frame, text=feedback_text)
            feedback_label.pack(pady=5)

            edit_button = ctk.CTkButton(self.history_frame, text="Edit", command=lambda fid=feedback_id: self.edit_feedback(fid))
            edit_button.pack(pady=2)

            delete_button = ctk.CTkButton(self.history_frame, text="Delete", command=lambda fid=feedback_id: self.delete_feedback(fid))
            delete_button.pack(pady=2)

        self.back_button = ctk.CTkButton(self.history_frame, text="Back to Dashboard", command=self.setup_dashboard)
        self.back_button.pack(pady=10)

    def edit_feedback(self, feedback_id):
        # Clear the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        self.edit_feedback_frame = ctk.CTkFrame(self)
        self.edit_feedback_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = self.edit_feedback_frame

        self.cursor.execute('SELECT course, instructor, feedback, rating FROM Feedback WHERE id = ?', (feedback_id,))
        feedback = self.cursor.fetchone()

        self.course_label = ctk.CTkLabel(self.edit_feedback_frame, text="Course")
        self.course_label.pack(pady=5)
        self.course_entry = ctk.CTkEntry(self.edit_feedback_frame)
        self.course_entry.insert(0, feedback[0])
        self.course_entry.pack(pady=5)

        self.instructor_label = ctk.CTkLabel(self.edit_feedback_frame, text="Instructor")
        self.instructor_label.pack(pady=5)
        self.instructor_entry = ctk.CTkEntry(self.edit_feedback_frame)
        self.instructor_entry.insert(0, feedback[1])
        self.instructor_entry.pack(pady=5)

        self.feedback_text_label = ctk.CTkLabel(self.edit_feedback_frame, text="Feedback")
        self.feedback_text_label.pack(pady=5)
        self.feedback_entry = ctk.CTkEntry(self.edit_feedback_frame)
        self.feedback_entry.insert(0, feedback[2])
        self.feedback_entry.pack(pady=5)

        self.rating_label = ctk.CTkLabel(self.edit_feedback_frame, text="Rating (out of 5)")
        self.rating_label.pack(pady=5)
        self.rating_entry = ctk.CTkEntry(self.edit_feedback_frame)
        self.rating_entry.insert(0, feedback[3])
        self.rating_entry.pack(pady=5)

        self.update_button = ctk.CTkButton(self.edit_feedback_frame, text="Update", command=lambda: self.update_feedback(feedback_id))
        self.update_button.pack(pady=10)

        self.back_button = ctk.CTkButton(self.edit_feedback_frame, text="Back to History", command=self.show_feedback_history)
        self.back_button.pack(pady=10)

    def update_feedback(self, feedback_id):
        course = self.course_entry.get()
        instructor = self.instructor_entry.get()
        feedback_text = self.feedback_entry.get()
        rating = self.rating_entry.get()

        # Update feedback in the database
        self.cursor.execute('''
            UPDATE Feedback
            SET course = ?, instructor = ?, feedback = ?, rating = ?
            WHERE id = ?
        ''', (course, instructor, feedback_text, rating, feedback_id))
        self.conn.commit()

        tkinter.messagebox.showinfo("Feedback", "Feedback Updated!")
        self.show_feedback_history()

    def delete_feedback(self, feedback_id):
        # Delete feedback from the database
        self.cursor.execute('DELETE FROM Feedback WHERE id = ?', (feedback_id,))
        self.conn.commit()

        tkinter.messagebox.showinfo("Feedback", "Feedback Deleted!")
        self.show_feedback_history()

    def show_all_feedback(self):
    # Clear the current frame if it exists
        if self.current_frame is not None:
            self.current_frame.pack_forget()

        self.all_feedback_frame = ctk.CTkFrame(self)
        self.all_feedback_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.current_frame = self.all_feedback_frame

        self.all_feedback_label = ctk.CTkLabel(self.all_feedback_frame, text="All Feedback")
        self.all_feedback_label.pack(pady=10)

        # Load all feedback from the database
        self.cursor.execute('''
            SELECT Feedback.id, Users.email, Feedback.course, Feedback.instructor, Feedback.feedback, Feedback.rating, Feedback.anonymous, Feedback.upvotes, Feedback.downvotes
            FROM Feedback 
            LEFT JOIN Users ON Feedback.user_id = Users.id
        ''')
        feedbacks = self.cursor.fetchall()

        for feedback in feedbacks:
            feedback_id, email, course, instructor, feedback_text, rating, anonymous, upvotes, downvotes = feedback
            user_display = "Anonymous" if anonymous else email

            feedback_frame = ctk.CTkFrame(self.all_feedback_frame, corner_radius=10)
            feedback_frame.pack(fill="x", expand=True, padx=10, pady=10)

            feedback_text_label = ctk.CTkLabel(feedback_frame, text=f"User: {user_display}\nCourse: {course}\nInstructor: {instructor}\nFeedback: {feedback_text}\nRating: {rating}/5\nUpvotes: {upvotes}\nDownvotes: {downvotes}", anchor="w", justify="left")
            feedback_text_label.pack(pady=5)

            icon_frame = ctk.CTkFrame(feedback_frame)
            icon_frame.pack(fill="x", expand=True)

            upvote_icon = ctk.CTkLabel(icon_frame, text="👍", cursor="hand2")
            upvote_icon.bind("<Button-1>", lambda event, fid=feedback_id: self.vote_feedback(fid, "upvote"))
            upvote_icon.pack(side="left", padx=10, pady=2)

            downvote_icon = ctk.CTkLabel(icon_frame, text="👎", cursor="hand2")
            downvote_icon.bind("<Button-1>", lambda event, fid=feedback_id: self.vote_feedback(fid, "downvote"))
            downvote_icon.pack(side="left", padx=10, pady=2)

        self.back_button = ctk.CTkButton(self.all_feedback_frame, text="Back to Dashboard", command=self.setup_dashboard)
        self.back_button.pack(pady=10)

    def vote_feedback(self, feedback_id, vote_type):
        # Check if the user has already voted on this feedback
        self.cursor.execute('SELECT * FROM Votes WHERE user_id = ? AND feedback_id = ?', (self.user_id, feedback_id))
        vote = self.cursor.fetchone()

        if vote:
            tkinter.messagebox.showerror("Vote", "You have already voted on this feedback!")
            return

        # Add vote to the Votes table
        self.cursor.execute('INSERT INTO Votes (user_id, feedback_id, vote_type) VALUES (?, ?, ?)', (self.user_id, feedback_id, vote_type))

        # Update the upvotes or downvotes count in the Feedback table
        if vote_type == "upvote":
            self.cursor.execute('UPDATE Feedback SET upvotes = upvotes + 1 WHERE id = ?', (feedback_id,))
        elif vote_type == "downvote":
            self.cursor.execute('UPDATE Feedback SET downvotes = downvotes + 1 WHERE id = ?', (feedback_id,))

        self.conn.commit()

        tkinter.messagebox.showinfo("Vote", "Your vote has been recorded!")
        self.show_all_feedback()


if __name__ == "__main__":
    app = FeedbackApp()
    app.mainloop()
