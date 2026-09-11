import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import re


class SignupPage:
    def __init__(self, root):
        self.root = root

        # Clear previous screen
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

        bg_label = tk.Label(
            self.root,
            image=self.bg_photo,
            borderwidth=0
        )

        bg_label.place(
            x=0,
            y=0,
            width=1000,
            height=650
        )

        # ==========================================
        # TITLE
        # ==========================================
        title = tk.Label(
            self.root,
            text="Create Account",
            font=("Arial", 22, "bold italic"),
            fg="#CB62E5",
            bg="#FFF4F5"
        )

        title.place(
            x=560,
            y=25
        )

        subtitle = tk.Label(
            self.root,
            text="Fill in the details to get started",
            font=("Arial", 11),
            fg="#554C52",
            bg="#FFF4F5"
        )

        subtitle.place(
            x=535,
            y=65
        )

        # ==========================================
        # USERNAME
        # ==========================================
        username_label = tk.Label(
            self.root,
            text="Username",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF4F5"
        )

        username_label.place(
            x=450,
            y=105
        )

        self.username_entry = tk.Entry(
            self.root,
            font=("Arial", 11),
            bg="white",
            fg="#555555",
            relief="solid",
            borderwidth=1
        )

        self.username_entry.place(
            x=450,
            y=130,
            width=400,
            height=40
        )

        # ==========================================
        # EMAIL
        # ==========================================
        email_label = tk.Label(
            self.root,
            text="Email",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF4F5"
        )

        email_label.place(
            x=450,
            y=180
        )

        self.email_entry = tk.Entry(
            self.root,
            font=("Arial", 11),
            bg="white",
            fg="#555555",
            relief="solid",
            borderwidth=1
        )

        self.email_entry.place(
            x=450,
            y=205,
            width=400,
            height=40
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
            x=450,
            y=255
        )

        self.password_entry = tk.Entry(
            self.root,
            font=("Arial", 11),
            bg="white",
            fg="#555555",
            relief="solid",
            borderwidth=1,
            show="*"
        )

        self.password_entry.place(
            x=450,
            y=280,
            width=350,
            height=40
        )

        # Password eye button
        self.password_visible = False

        self.password_eye = tk.Button(
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

        self.password_eye.place(
            x=800,
            y=280,
            width=50,
            height=40
        )

        # Password rule
        password_rule = tk.Label(
            self.root,
            text="8+ characters, uppercase, lowercase, number & special character",
            font=("Arial", 8),
            fg="#8A7A83",
            bg="#FFF4F5"
        )

        password_rule.place(
            x=450,
            y=323
        )

        # ==========================================
        # CONFIRM PASSWORD
        # ==========================================
        confirm_label = tk.Label(
            self.root,
            text="Confirm Password",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF4F5"
        )

        confirm_label.place(
            x=450,
            y=350
        )

        self.confirm_entry = tk.Entry(
            self.root,
            font=("Arial", 11),
            bg="white",
            fg="#555555",
            relief="solid",
            borderwidth=1,
            show="*"
        )

        self.confirm_entry.place(
            x=450,
            y=375,
            width=350,
            height=40
        )

        # Confirm password eye button
        self.confirm_visible = False

        self.confirm_eye = tk.Button(
            self.root,
            text="👁",
            font=("Arial", 12),
            bg="white",
            activebackground="white",
            relief="solid",
            borderwidth=1,
            cursor="hand2",
            command=self.toggle_confirm_password
        )

        self.confirm_eye.place(
            x=800,
            y=375,
            width=50,
            height=40
        )

        # ==========================================
        # TERMS AND CONDITIONS
        # ==========================================
        self.terms_var = tk.BooleanVar()

        terms_checkbox = tk.Checkbutton(
            self.root,
            text="I agree to the Terms of Service and Privacy Policy",
            variable=self.terms_var,
            font=("Arial", 9),
            fg="#554C52",
            bg="#FFF4F5",
            activebackground="#FFF4F5",
            selectcolor="white",
            cursor="hand2"
        )

        terms_checkbox.place(
            x=450,
            y=430
        )

        # ==========================================
        # CREATE ACCOUNT BUTTON
        # ==========================================
        create_button = tk.Button(
            self.root,
            text="Create Account",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#A467DF",
            activebackground="#9258CC",
            activeforeground="white",
            borderwidth=0,
            cursor="hand2",
            command=self.create_account
        )

        create_button.place(
            x=480,
            y=475,
            width=340,
            height=45
        )

        # ==========================================
        # BACK TO LOGIN
        # ==========================================
        login_text = tk.Label(
            self.root,
            text="Already have an account?",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF4F5"
        )

        login_text.place(
            x=535,
            y=545
        )

        login_label = tk.Label(
            self.root,
            text="Login",
            font=("Arial", 10, "bold"),
            fg="#FF62C4",
            bg="#FFF4F5",
            cursor="hand2"
        )

        login_label.place(
            x=710,
            y=545
        )

        login_label.bind(
            "<Button-1>",
            self.open_login
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
    # SHOW / HIDE CONFIRM PASSWORD
    # ==========================================
    def toggle_confirm_password(self):
        if self.confirm_visible:
            self.confirm_entry.config(show="*")
            self.confirm_visible = False
        else:
            self.confirm_entry.config(show="")
            self.confirm_visible = True

    # ==========================================
    # EMAIL VALIDATION
    # ==========================================
    def valid_email(self, email):
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return re.match(pattern, email) is not None

    # ==========================================
    # PASSWORD VALIDATION
    # ==========================================
    def valid_password(self, password):

        if len(password) < 8:
            return False

        if not re.search(r"[A-Z]", password):
            return False

        if not re.search(r"[a-z]", password):
            return False

        if not re.search(r"[0-9]", password):
            return False

        if not re.search(r"[!@#$%^&*()_+\-=]", password):
            return False

        return True

    # ==========================================
    # CREATE ACCOUNT
    # ==========================================
    def create_account(self):

        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_entry.get()

        # Check empty fields
        if (
            username == ""
            or email == ""
            or password == ""
            or confirm_password == ""
        ):
            messagebox.showwarning(
                "Missing Information",
                "Please fill in all fields."
            )
            return

        # Username rule
        if len(username) < 3:
            messagebox.showwarning(
                "Invalid Username",
                "Username must contain at least 3 characters."
            )
            return

        # Email rule
        if not self.valid_email(email):
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address.\n\n"
                "Example: name@example.com"
            )
            return

        # Password rule
        if not self.valid_password(password):
            messagebox.showwarning(
                "Weak Password",
                "Password must contain:\n\n"
                "• At least 8 characters\n"
                "• One uppercase letter\n"
                "• One lowercase letter\n"
                "• One number\n"
                "• One special character"
            )
            return

        # Confirm password
        if password != confirm_password:
            messagebox.showwarning(
                "Password Error",
                "Passwords do not match."
            )
            return

        # Terms checkbox
        if not self.terms_var.get():
            messagebox.showwarning(
                "Terms",
                "Please agree to the Terms of Service and Privacy Policy."
            )
            return

        # Success
        messagebox.showinfo(
            "Gola",
            "Account created successfully!"
        )

        self.open_login()

    # ==========================================
    # OPEN LOGIN PAGE
    # ==========================================
    def open_login(self, event=None):

        from login import LoginPage

        for widget in self.root.winfo_children():
            widget.destroy()

        LoginPage(self.root)