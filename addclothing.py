import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
import os


class AddClothingPage:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.image_path = ""

        # Clear previous page
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF8F8")

        # ==========================================
        # TITLE
        # ==========================================
        title = tk.Label(
            self.root,
            text="Add Clothing",
            font=("Georgia", 26, "bold"),
            fg="#2F2A67",
            bg="#FFF8F8"
        )
        title.place(x=390, y=35)

        subtitle = tk.Label(
            self.root,
            text="Add a new item to your digital wardrobe",
            font=("Arial", 11),
            fg="#726C85",
            bg="#FFF8F8"
        )
        subtitle.place(x=350, y=80)

        # ==========================================
        # CLOTHING NAME
        # ==========================================
        name_label = tk.Label(
            self.root,
            text="Clothing Name",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF8F8"
        )
        name_label.place(x=270, y=135)

        self.name_entry = tk.Entry(
            self.root,
            font=("Arial", 11),
            fg="#555555",
            bg="white",
            relief="solid",
            borderwidth=1
        )
        self.name_entry.place(
            x=270,
            y=160,
            width=450,
            height=40
        )

        # ==========================================
        # CATEGORY
        # ==========================================
        category_label = tk.Label(
            self.root,
            text="Category",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF8F8"
        )
        category_label.place(x=270, y=215)

        self.category_var = tk.StringVar()
        self.category_var.set("Select Category")

        category_menu = tk.OptionMenu(
            self.root,
            self.category_var,
            "Top",
            "Bottom",
            "Dress",
            "Shoes",
            "Outerwear",
            "Accessory"
        )
        category_menu.config(
            font=("Arial", 10),
            fg="#554C52",
            bg="white",
            activebackground="#F5EAF8",
            relief="solid",
            borderwidth=1
        )
        category_menu.place(
            x=270,
            y=240,
            width=450,
            height=40
        )

        # ==========================================
        # COLOR
        # ==========================================
        color_label = tk.Label(
            self.root,
            text="Color",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF8F8"
        )
        color_label.place(x=270, y=295)

        self.color_entry = tk.Entry(
            self.root,
            font=("Arial", 11),
            fg="#555555",
            bg="white",
            relief="solid",
            borderwidth=1
        )
        self.color_entry.place(
            x=270,
            y=320,
            width=450,
            height=40
        )

        # ==========================================
        # CLOTHING IMAGE
        # ==========================================
        image_title = tk.Label(
            self.root,
            text="Clothing Image",
            font=("Arial", 10),
            fg="#554C52",
            bg="#FFF8F8"
        )
        image_title.place(x=270, y=375)

        self.image_label = tk.Label(
            self.root,
            text="No image selected",
            font=("Arial", 9),
            fg="#777777",
            bg="#FFF8F8"
        )
        self.image_label.place(
            x=270,
            y=410
        )

        choose_image_button = tk.Button(
            self.root,
            text="Choose Image",
            font=("Arial", 10, "bold"),
            fg="#554C52",
            bg="#E9DDF5",
            activebackground="#DDCDEE",
            borderwidth=0,
            cursor="hand2",
            command=self.choose_image
        )
        choose_image_button.place(
            x=590,
            y=400,
            width=130,
            height=38
        )

        # ==========================================
        # SAVE CLOTHING BUTTON
        # ==========================================
        save_button = tk.Button(
            self.root,
            text="Save Clothing",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#A467DF",
            activebackground="#9258CC",
            activeforeground="white",
            borderwidth=0,
            cursor="hand2",
            command=self.save_clothing
        )
        save_button.place(
            x=350,
            y=480,
            width=190,
            height=45
        )

        # ==========================================
        # BACK BUTTON
        # ==========================================
        back_button = tk.Button(
            self.root,
            text="Back",
            font=("Arial", 11, "bold"),
            fg="#554C52",
            bg="#F0E5F5",
            activebackground="#E5D6ED",
            borderwidth=0,
            cursor="hand2",
            command=self.go_back
        )
        back_button.place(
            x=560,
            y=480,
            width=130,
            height=45
        )

    # ==========================================
    # CHOOSE IMAGE
    # ==========================================
    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Clothing Image",
            filetypes=[
                (
                    "Image Files",
                    "*.png *.jpg *.jpeg"
                )
            ]
        )

        if file_path:
            self.image_path = file_path

            self.image_label.config(
                text=os.path.basename(file_path)
            )

    # ==========================================
    # SAVE CLOTHING
    # ==========================================
    def save_clothing(self):
        name = self.name_entry.get().strip()
        category = self.category_var.get()
        color = self.color_entry.get().strip()

        # Check clothing name
        if name == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter the clothing name."
            )
            return

        # Check category
        if category == "Select Category":
            messagebox.showwarning(
                "Missing Information",
                "Please select a category."
            )
            return

        # Check color
        if color == "":
            messagebox.showwarning(
                "Missing Information",
                "Please enter the clothing color."
            )
            return

        # Check image
        if self.image_path == "":
            messagebox.showwarning(
                "Missing Image",
                "Please choose a clothing image."
            )
            return

        try:
            # ======================================
            # CONNECT TO DATABASE
            # ======================================
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            # ======================================
            # FIND CURRENT USER
            # ======================================
            cursor.execute(
                """
                SELECT id
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
                    "The logged-in user could not be found."
                )
                return

            user_id = user[0]

            # ======================================
            # CREATE CLOTHING TABLE
            # ======================================
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS clothing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    color TEXT NOT NULL,
                    image_path TEXT,
                    FOREIGN KEY (user_id)
                    REFERENCES users(id)
                )
                """
            )

            # ======================================
            # INSERT CLOTHING
            # ======================================
            cursor.execute(
                """
                INSERT INTO clothing (
                    user_id,
                    name,
                    category,
                    color,
                    image_path
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    name,
                    category,
                    color,
                    self.image_path
                )
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Gola",
                "Clothing added successfully!"
            )

            # ======================================
            # CLEAR FORM
            # ======================================
            self.name_entry.delete(
                0,
                tk.END
            )

            self.category_var.set(
                "Select Category"
            )

            self.color_entry.delete(
                0,
                tk.END
            )

            self.image_path = ""

            self.image_label.config(
                text="No image selected"
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Something went wrong with the database.\n\n{error}"
            )

    # ==========================================
    # BACK TO DASHBOARD
    # ==========================================
    def go_back(self):
        from dashboard import DashboardPage

        for widget in self.root.winfo_children():
            widget.destroy()

        DashboardPage(
            self.root,
            self.username
        )