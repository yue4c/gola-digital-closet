import tkinter as tk
from tkinter import messagebox
import sqlite3


class SettingsPage:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF8F8")

        self.prepare_database()
        self.user_data = self.get_user_data()

        # ==========================================
        # TITLE
        # ==========================================
        title = tk.Label(
            self.root,
            text="Settings",
            font=("Georgia", 26, "bold"),
            fg="#2F2A67",
            bg="#FFF8F8"
        )
        title.place(x=420, y=30)

        subtitle = tk.Label(
            self.root,
            text="Manage your profile, password and notifications",
            font=("Arial", 11),
            fg="#726C85",
            bg="#FFF8F8"
        )
        subtitle.place(x=330, y=75)

        # ==========================================
        # BACK BUTTON
        # ==========================================
        back_button = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10, "bold"),
            fg="#554C52",
            bg="#E9DDF5",
            activebackground="#DDCDEE",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.go_back
        )
        back_button.place(
            x=40,
            y=35,
            width=100,
            height=35
        )

        # ==========================================
        # PROFILE CARD
        # ==========================================
        profile_frame = tk.Frame(
            self.root,
            bg="white",
            width=420,
            height=440,
            highlightbackground="#E8DDEA",
            highlightthickness=1
        )
        profile_frame.place(x=55, y=125)

        profile_title = tk.Label(
            profile_frame,
            text="Edit Profile",
            font=("Arial", 17, "bold"),
            fg="#39356F",
            bg="white"
        )
        profile_title.place(x=30, y=25)

        # USERNAME
        username_label = tk.Label(
            profile_frame,
            text="Username",
            font=("Arial", 10),
            fg="#554C52",
            bg="white"
        )
        username_label.place(x=30, y=80)

        self.username_entry = tk.Entry(
            profile_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.username_entry.place(
            x=30,
            y=105,
            width=355,
            height=40
        )

        # EMAIL
        email_label = tk.Label(
            profile_frame,
            text="Email",
            font=("Arial", 10),
            fg="#554C52",
            bg="white"
        )
        email_label.place(x=30, y=170)

        self.email_entry = tk.Entry(
            profile_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.email_entry.place(
            x=30,
            y=195,
            width=355,
            height=40
        )

        if self.user_data:
            self.username_entry.insert(
                0,
                self.user_data[1]
            )

            self.email_entry.insert(
                0,
                self.user_data[2]
            )

        save_profile_button = tk.Button(
            profile_frame,
            text="Save Profile Changes",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#A467DF",
            activebackground="#9258CC",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.save_profile
        )
        save_profile_button.place(
            x=105,
            y=280,
            width=210,
            height=45
        )

        profile_info = tk.Label(
            profile_frame,
            text="Your new username or email will be used next time you log in.",
            font=("Arial", 9),
            fg="#8B8495",
            bg="white",
            wraplength=340,
            justify="center"
        )
        profile_info.place(
            x=40,
            y=350,
            width=340
        )

        # ==========================================
        # ACCOUNT SETTINGS CARD
        # ==========================================
        account_frame = tk.Frame(
            self.root,
            bg="white",
            width=420,
            height=440,
            highlightbackground="#E8DDEA",
            highlightthickness=1
        )
        account_frame.place(x=525, y=125)

        account_title = tk.Label(
            account_frame,
            text="Account Settings",
            font=("Arial", 17, "bold"),
            fg="#39356F",
            bg="white"
        )
        account_title.place(x=30, y=25)

        # ==========================================
        # CHANGE PASSWORD
        # ==========================================
        current_password_label = tk.Label(
            account_frame,
            text="Current Password",
            font=("Arial", 10),
            fg="#554C52",
            bg="white"
        )
        current_password_label.place(x=30, y=75)

        self.current_password_entry = tk.Entry(
            account_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1,
            show="*"
        )
        self.current_password_entry.place(
            x=30,
            y=100,
            width=355,
            height=38
        )

        new_password_label = tk.Label(
            account_frame,
            text="New Password",
            font=("Arial", 10),
            fg="#554C52",
            bg="white"
        )
        new_password_label.place(x=30, y=155)

        self.new_password_entry = tk.Entry(
            account_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1,
            show="*"
        )
        self.new_password_entry.place(
            x=30,
            y=180,
            width=355,
            height=38
        )

        confirm_password_label = tk.Label(
            account_frame,
            text="Confirm New Password",
            font=("Arial", 10),
            fg="#554C52",
            bg="white"
        )
        confirm_password_label.place(x=30, y=235)

        self.confirm_password_entry = tk.Entry(
            account_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1,
            show="*"
        )
        self.confirm_password_entry.place(
            x=30,
            y=260,
            width=355,
            height=38
        )

        change_password_button = tk.Button(
            account_frame,
            text="Change Password",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#E656A2",
            activebackground="#D84A94",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.change_password
        )
        change_password_button.place(
            x=30,
            y=320,
            width=170,
            height=40
        )

        # ==========================================
        # NOTIFICATIONS
        # ==========================================
        self.notification_var = tk.BooleanVar()

        if self.user_data and len(self.user_data) > 3:
            self.notification_var.set(
                bool(self.user_data[3])
            )

        notification_checkbox = tk.Checkbutton(
            account_frame,
            text="Enable Notifications",
            variable=self.notification_var,
            font=("Arial", 10, "bold"),
            fg="#39356F",
            bg="white",
            activebackground="white",
            selectcolor="#F5EDF8",
            cursor="hand2",
            command=self.save_notification_setting
        )
        notification_checkbox.place(
            x=225,
            y=325
        )

        notification_info = tk.Label(
            account_frame,
            text="Turn app notifications on or off.",
            font=("Arial", 9),
            fg="#8B8495",
            bg="white"
        )
        notification_info.place(
            x=220,
            y=365
        )

    # ==========================================
    # PREPARE DATABASE
    # ==========================================
    def prepare_database(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute("PRAGMA table_info(users)")
            columns = cursor.fetchall()

            column_names = [
                column[1]
                for column in columns
            ]

            if "notifications" not in column_names:
                cursor.execute(
                    """
                    ALTER TABLE users
                    ADD COLUMN notifications INTEGER DEFAULT 1
                    """
                )

            connection.commit()
            connection.close()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not prepare settings.\n\n{error}"
            )

    # ==========================================
    # GET USER DATA
    # ==========================================
    def get_user_data(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    username,
                    email,
                    notifications
                FROM users
                WHERE username = ?
                """,
                (self.username,)
            )

            user = cursor.fetchone()

            connection.close()

            return user

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load your profile.\n\n{error}"
            )

            return None

    # ==========================================
    # SAVE PROFILE
    # ==========================================
    def save_profile(self):
        new_username = self.username_entry.get().strip()
        new_email = self.email_entry.get().strip()

        if new_username == "":
            messagebox.showwarning(
                "Missing Username",
                "Please enter a username."
            )
            return

        if len(new_username) < 3:
            messagebox.showwarning(
                "Invalid Username",
                "Username must contain at least 3 characters."
            )
            return

        if new_email == "":
            messagebox.showwarning(
                "Missing Email",
                "Please enter your email."
            )
            return

        if "@" not in new_email or "." not in new_email:
            messagebox.showwarning(
                "Invalid Email",
                "Please enter a valid email address."
            )
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            # Check whether another user has this username
            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                AND username != ?
                """,
                (
                    new_username,
                    self.username
                )
            )

            if cursor.fetchone():
                connection.close()

                messagebox.showwarning(
                    "Username Exists",
                    "That username is already being used."
                )
                return

            # Check whether another user has this email
            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE email = ?
                AND username != ?
                """,
                (
                    new_email,
                    self.username
                )
            )

            if cursor.fetchone():
                connection.close()

                messagebox.showwarning(
                    "Email Exists",
                    "That email is already registered."
                )
                return

            cursor.execute(
                """
                UPDATE users
                SET username = ?, email = ?
                WHERE username = ?
                """,
                (
                    new_username,
                    new_email,
                    self.username
                )
            )

            connection.commit()
            connection.close()

            self.username = new_username
            self.user_data = self.get_user_data()

            messagebox.showinfo(
                "Gola",
                "Profile updated successfully! ♡"
            )

        except sqlite3.IntegrityError:
            messagebox.showwarning(
                "Account Exists",
                "That username or email is already registered."
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not update profile.\n\n{error}"
            )

    # ==========================================
    # CHANGE PASSWORD
    # ==========================================
    def change_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if (
            current_password == ""
            or new_password == ""
            or confirm_password == ""
        ):
            messagebox.showwarning(
                "Missing Information",
                "Please complete all password fields."
            )
            return

        if len(new_password) < 8:
            messagebox.showwarning(
                "Weak Password",
                "New password must contain at least 8 characters."
            )
            return

        if new_password != confirm_password:
            messagebox.showwarning(
                "Password Mismatch",
                "New password and confirm password do not match."
            )
            return

        if current_password == new_password:
            messagebox.showwarning(
                "Same Password",
                "Your new password must be different from your current password."
            )
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT password
                FROM users
                WHERE username = ?
                """,
                (self.username,)
            )

            user = cursor.fetchone()

            if user is None:
                connection.close()

                messagebox.showerror(
                    "User Error",
                    "Could not find your account."
                )
                return

            saved_password = user[0]

            if current_password != saved_password:
                connection.close()

                messagebox.showerror(
                    "Incorrect Password",
                    "Your current password is incorrect."
                )
                return

            cursor.execute(
                """
                UPDATE users
                SET password = ?
                WHERE username = ?
                """,
                (
                    new_password,
                    self.username
                )
            )

            connection.commit()
            connection.close()

            self.current_password_entry.delete(
                0,
                tk.END
            )

            self.new_password_entry.delete(
                0,
                tk.END
            )

            self.confirm_password_entry.delete(
                0,
                tk.END
            )

            messagebox.showinfo(
                "Gola",
                "Password changed successfully!"
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not change password.\n\n{error}"
            )

    # ==========================================
    # SAVE NOTIFICATION SETTING
    # ==========================================
    def save_notification_setting(self):
        if self.notification_var.get():
            notification_value = 1
        else:
            notification_value = 0

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE users
                SET notifications = ?
                WHERE username = ?
                """,
                (
                    notification_value,
                    self.username
                )
            )

            connection.commit()
            connection.close()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not update notification setting.\n\n{error}"
            )

    # ==========================================
    # BACK TO DASHBOARD
    # ==========================================
    def go_back(self):
        from dashboard import DashboardPage

        DashboardPage(
            self.root,
            self.username
        )