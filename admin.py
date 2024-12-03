import customtkinter as ctk
import tkinter.messagebox
import sqlite3

# Set the appearance mode to "Light"
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class FeedbackApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Admin Feedback System")
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

        self.register_email_label = ctk.CTkLabel(self.register_frame, text="Email")
        self.register_email_label.grid(row=0, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_email_entry = ctk.CTkEntry(self.register_frame)
        self.register_email_entry.grid(row=0, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_password_label = ctk.CTkLabel(self.register_frame, text="Password")
        self.register_password_label.grid(row=1, column=0, padx=(50, 10), pady=(20, 0), sticky="w")
        self.register_password_entry = ctk.CTkEntry(self.register_frame, show="*")
        self.register_password_entry.grid(row=1, column=1, padx=(100, 100), pady=(20, 0), sticky="ew")

        self.register_button = ctk.CTkButton(self.register_frame, text="Register", width=100, command=self.register)
        self.register_button.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=10)

        self.back_to_login_button = ctk.CTkButton(self.register_frame, text="Back to Login", width=100, command=self.setup_login_frame)
        self.back_to_login_button.grid(row=3, column=0, columnspan=1, padx=(50, 10), pady=10)

        self.register_frame.grid_columnconfigure(1, weight=1)

    def register(self):
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()

        try:
            self.cursor.execute('INSERT INTO Users (email, password) VALUES (?, ?)', (email, password))
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

        self.welcome_label = ctk.CTkLabel(self.dashboard_frame, text="Welcome to the Admin Dashboard!")
        self.welcome_label.pack(pady=10)

        self.all_feedback_button = ctk.CTkButton(self.dashboard_frame, text="View All Feedback", command=self.show_all_feedback)
        self.all_feedback_button.pack(pady=10)

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

        self.back_button = ctk.CTkButton(self.all_feedback_frame, text="Back to Dashboard", command=self.setup_dashboard)
        self.back_button.pack(pady=10)

if __name__ == "__main__":
    app = FeedbackApp()
    app.mainloop()
