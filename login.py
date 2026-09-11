import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3


class LoginPage:
    def __init__(self, root):
        self.root = root

        # ==========================================
        # CLEAR PREVIOUS SCREEN
        # ==========================================
        for widget in self.root.winfo_children():
            widget.destroy()

        # ==========================================
        # BACKGROUND + GOLA LOGO
        # ==========================================
        bg_image = Image.open("images/loginbg.png").convert("RGBA")
        bg_image = bg_image.resize((1000, 650))

        logo_image = Image.open("images/logo.png").convert("RGBA")
        logo_image.thumbnail((230, 230))

        bg_image.paste(
            logo_image,
            (65, 120),
            logo_image
        )

        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(
            self.root,
            image=self.bg_photo,
            borderwidth=0
        )
        self.bg_label.place(
            x=0,
            y=0,
            width=1000,
            height=650
        )

        # ==========================================
        # WELCOME BACK
        # ==========================================
        welcome_label = tk.Label(
            self.root,
            text="Welcome Back!",
            font=("Georgia", 30),
            fg="#CB62E5",
            bg="#FFF4F5"
        )
        welcome_label.place(
            x=500,
            y=65
        )

        subtitle_label = tk.Label(
            self.root,
            text="Login to continue to your wardrobe",
            font=("Arial", 12),
            fg="#554C52",
            bg="#FFF4F5"
        )
        subtitle_label.place(
            x=500,
            y=115
        )

        # ==========================================
        # USERNAME OR EMAIL
        # ==========================================
        username_label = tk.Label(
            self.root,
            text="Username or Email",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF4F5"
        )
        username_label.place(
            x=440,
            y=165
        )

        self.username_entry = tk.Entry(
            self.root,
            font=("Arial", 12),
            fg="#555555",
            bg="white",
            relief="solid",
            borderwidth=1
        )
        self.username_entry.place(
            x=440,
            y=190,
            width=470,
            height=48
        )

        # ==========================================
        # PASSWORD
        # ==========================================
        password_label = tk.Label(
            self.root,
            text="Password",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF4F5"
        )
        password_label.place(
            x=440,
            y=250
        )

        self.password_entry = tk.Entry(
            self.root,
            font=("Arial", 12),
            fg="#555555",
            bg="white",
            relief="solid",
            borderwidth=1,
            show="*"
        )
        self.password_entry.place(
            x=440,
            y=275,
            width=420,
            height=48
        )

        # ==========================================
        # PASSWORD EYE BUTTON
        # ==========================================
        self.password_visible = False

        self.eye_button = tk.Button(
            self.root,
            text="👁",
            font=("Arial", 12),
            bg="white",
            activebackground="white",
            relief="solid",
            borderwidth=1,
            cursor="hand2",
            command=self.toggle_password
        )
        self.eye_button.place(
            x=860,
            y=275,
            width=50,
            height=48
        )

        # ==========================================
        # REMEMBER ME
        # ==========================================
        self.remember_var = tk.BooleanVar()

        remember_checkbox = tk.Checkbutton(
            self.root,
            text="Remember Me",
            variable=self.remember_var,
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF4F5",
            activebackground="#FFF4F5",
            selectcolor="white",
            cursor="hand2"
        )
        remember_checkbox.place(
            x=440,
            y=335
        )

        # ==========================================
        # FORGOT PASSWORD
        # ==========================================
        forgot_password = tk.Label(
            self.root,
            text="Forgot Password?",
            font=("Arial", 10),
            fg="#D35FE5",
            bg="#FFF4F5",
            cursor="hand2"
        )
        forgot_password.place(
            x=795,
            y=340
        )

        # ==========================================
        # LOGIN BUTTON
        # ==========================================
        login_button = tk.Button(
            self.root,
            text="Login",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#9869C4",
            activebackground="#875AB5",
            activeforeground="white",
            borderwidth=0,
            cursor="hand2",
            command=self.login
        )
        login_button.place(
            x=480,
            y=390,
            width=390,
            height=45
        )

        # ==========================================
        # SIGN UP
        # ==========================================
        account_label = tk.Label(
            self.root,
            text="Don't have an account?",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF4F5"
        )
        account_label.place(
            x=535,
            y=465
        )

        signup_label = tk.Label(
            self.root,
            text="Sign Up",
            font=("Arial", 10, "bold"),
            fg="#FF62C4",
            bg="#FFF4F5",
            cursor="hand2"
        )
        signup_label.place(
            x=700,
            y=465
        )

        signup_label.bind(
            "<Button-1>",
            self.open_signup
        )

        # Press Enter to login
        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

    # ==========================================
    # SHOW / HIDE PASSWORD
    # ==========================================
    def toggle_password(self):
        if self.password_visible:
            self.password_entry.config(show="*")
            self.password_visible = False
        else:
            self.password_entry.config(show="")
            self.password_visible = True

    # ==========================================
    # LOGIN FUNCTION
    # ==========================================
    def login(self):
        username_or_email = self.username_entry.get().strip()
        password = self.password_entry.get()

        # Check empty fields
        if username_or_email == "" or password == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter your username/email and password."
            )
            return

        try:
            # Connect to SQLite database
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            # Search for matching username/email + password
            cursor.execute(
                """
                SELECT * FROM users
                WHERE (username = ? OR email = ?)
                AND password = ?
                """,
                (
                    username_or_email,
                    username_or_email,
                    password
                )
            )

            user = cursor.fetchone()

            connection.close()

            # ======================================
            # LOGIN SUCCESSFUL
            # ======================================
            if user:
                username = user[1]

                messagebox.showinfo(
                    "Gola",
                    f"Welcome, {username}!"
                )

                # Open Dashboard
                from dashboard import DashboardPage

                for widget in self.root.winfo_children():
                    widget.destroy()

                DashboardPage(
                    self.root,
                    username
                )

            # ======================================
            # LOGIN FAILED
            # ======================================
            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid username/email or password."
                )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Something went wrong with the database.\n\n{error}"
            )

    # ==========================================
    # OPEN SIGN UP PAGE
    # ==========================================
    def open_signup(self, event=None):
        from signup import SignupPage

        for widget in self.root.winfo_children():
            widget.destroy()

        SignupPage(self.root)