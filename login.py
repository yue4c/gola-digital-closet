import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class LoginPage:
    def __init__(self, root):
        self.root = root

        # ==========================================
        # BACKGROUND + GOLA LOGO
        # ==========================================
        bg_image = Image.open("images/loginbg.png").convert("RGBA")
        bg_image = bg_image.resize((1000, 650))

        logo_image = Image.open("images/logo.png").convert("RGBA")
        logo_image.thumbnail((230, 230))

        logo_x = 65
        logo_y = 120

        bg_image.paste(
            logo_image,
            (logo_x, logo_y),
            logo_image
        )

        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.bg_label = tk.Label(
            root,
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
            root,
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
            root,
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
            root,
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
            root,
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
            root,
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
            root,
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
        # SHOW / HIDE PASSWORD BUTTON
        # ==========================================
        self.password_visible = False

        self.eye_button = tk.Button(
            root,
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
            root,
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
            root,
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
            root,
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
            root,
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
            root,
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

        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if username == "" or password == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter your username and password."
            )

        else:
            messagebox.showinfo(
                "Gola",
                "Login successful!"
            )

    # ==========================================
    # OPEN SIGN UP PAGE
    # ==========================================
    def open_signup(self, event=None):

        from signup import SignupPage

        for widget in self.root.winfo_children():
            widget.destroy()

        SignupPage(self.root)