import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import random
import os


class OutfitGeneratorPage:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        self.image_refs = []
        self.current_outfit = []

        # Clear previous page
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF8F8")

        # ==========================================
        # TITLE
        # ==========================================
        title = tk.Label(
            self.root,
            text="Outfit Generator",
            font=("Georgia", 26, "bold"),
            fg="#2F2A67",
            bg="#FFF8F8"
        )
        title.place(x=365, y=30)

        subtitle = tk.Label(
            self.root,
            text="Let Gola create an outfit from your wardrobe ✨",
            font=("Arial", 11),
            fg="#726C85",
            bg="#FFF8F8"
        )
        subtitle.place(x=340, y=75)

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
        # OUTFIT DISPLAY FRAME
        # ==========================================
        self.outfit_frame = tk.Frame(
            self.root,
            bg="#FFF8F8",
            width=900,
            height=390
        )
        self.outfit_frame.place(
            x=50,
            y=120
        )

        # ==========================================
        # GENERATE BUTTON
        # ==========================================
        generate_button = tk.Button(
            self.root,
            text="✨ Generate Again",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#A467DF",
            activebackground="#9258CC",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.generate_outfit
        )
        generate_button.place(
            x=290,
            y=535,
            width=190,
            height=45
        )

        # ==========================================
        # SAVE BUTTON
        # ==========================================
        save_button = tk.Button(
            self.root,
            text="♡ Save Outfit",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#E656A2",
            activebackground="#D84A94",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.save_outfit
        )
        save_button.place(
            x=520,
            y=535,
            width=190,
            height=45
        )

        # Prepare outfits table
        self.prepare_database()

        # Generate first outfit automatically
        self.generate_outfit()

    # ==========================================
    # PREPARE DATABASE
    # ==========================================
    def prepare_database(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS outfits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    top_id INTEGER,
                    bottom_id INTEGER,
                    shoes_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

            connection.commit()
            connection.close()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not prepare outfit table.\n\n{error}"
            )

    # ==========================================
    # GET USER ID
    # ==========================================
    def get_user_id(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT id
                FROM users
                WHERE username = ?
                """,
                (self.username,)
            )

            user = cursor.fetchone()

            connection.close()

            if user:
                return user[0]

            return None

        except sqlite3.Error:
            return None

    # ==========================================
    # GET CLOTHING BY CATEGORY
    # ==========================================
    def get_clothes(self, category):
        user_id = self.get_user_id()

        if user_id is None:
            return []

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    name,
                    category,
                    color,
                    image_path
                FROM clothing
                WHERE user_id = ?
                AND category = ?
                """,
                (user_id, category)
            )

            clothes = cursor.fetchall()

            connection.close()

            return clothes

        except sqlite3.Error:
            return []

    # ==========================================
    # GENERATE OUTFIT
    # ==========================================
    def generate_outfit(self):

        # Clear previous outfit
        for widget in self.outfit_frame.winfo_children():
            widget.destroy()

        self.image_refs = []
        self.current_outfit = []

        # Get clothing
        tops = self.get_clothes("Top")
        bottoms = self.get_clothes("Bottom")
        shoes = self.get_clothes("Shoes")

        # Check if user has enough clothing
        if len(tops) == 0 or len(bottoms) == 0 or len(shoes) == 0:

            missing = []

            if len(tops) == 0:
                missing.append("Top")

            if len(bottoms) == 0:
                missing.append("Bottom")

            if len(shoes) == 0:
                missing.append("Shoes")

            missing_text = ", ".join(missing)

            messagebox.showwarning(
                "Not Enough Clothes",
                f"Please add at least one item for:\n\n{missing_text}"
            )

            empty_label = tk.Label(
                self.outfit_frame,
                text=(
                    "Your wardrobe needs a few more pieces 👗\n\n"
                    "Add at least one Top, one Bottom and one Shoes item."
                ),
                font=("Arial", 15),
                fg="#817A96",
                bg="#FFF8F8",
                justify="center"
            )

            empty_label.place(
                x=240,
                y=120
            )

            return

        # Randomly choose clothes
        selected_top = random.choice(tops)
        selected_bottom = random.choice(bottoms)
        selected_shoes = random.choice(shoes)

        self.current_outfit = [
            selected_top,
            selected_bottom,
            selected_shoes
        ]

        # Create cards
        self.create_item_card(
            selected_top,
            "TOP",
            20
        )

        self.create_item_card(
            selected_bottom,
            "BOTTOM",
            320
        )

        self.create_item_card(
            selected_shoes,
            "SHOES",
            620
        )

    # ==========================================
    # CREATE CLOTHING CARD
    # ==========================================
    def create_item_card(
        self,
        item,
        category_title,
        x_position
    ):
        clothing_id = item[0]
        name = item[1]
        category = item[2]
        color = item[3]
        image_path = item[4]

        card = tk.Frame(
            self.outfit_frame,
            bg="white",
            width=250,
            height=340,
            highlightbackground="#E8DDEA",
            highlightthickness=1
        )

        card.place(
            x=x_position,
            y=20
        )

        # Category heading
        category_label = tk.Label(
            card,
            text=category_title,
            font=("Arial", 11, "bold"),
            fg="#A467DF",
            bg="white"
        )

        category_label.place(
            x=20,
            y=15
        )

        # ======================================
        # IMAGE
        # ======================================
        if image_path and os.path.exists(image_path):

            try:
                image = Image.open(image_path)

                image.thumbnail(
                    (190, 190)
                )

                photo = ImageTk.PhotoImage(image)

                self.image_refs.append(photo)

                image_label = tk.Label(
                    card,
                    image=photo,
                    bg="#F7F1F8"
                )

                image_label.place(
                    x=30,
                    y=50,
                    width=190,
                    height=190
                )

            except Exception:
                self.create_placeholder(card)

        else:
            self.create_placeholder(card)

        # ======================================
        # CLOTHING NAME
        # ======================================
        name_label = tk.Label(
            card,
            text=name,
            font=("Arial", 12, "bold"),
            fg="#39356F",
            bg="white"
        )

        name_label.place(
            x=20,
            y=255
        )

        # ======================================
        # COLOR
        # ======================================
        color_label = tk.Label(
            card,
            text=f"Color: {color}",
            font=("Arial", 9),
            fg="#756D84",
            bg="white"
        )

        color_label.place(
            x=20,
            y=285
        )

    # ==========================================
    # IMAGE PLACEHOLDER
    # ==========================================
    def create_placeholder(self, card):

        placeholder = tk.Label(
            card,
            text="👗\nNo Image",
            font=("Arial", 18),
            fg="#A895B1",
            bg="#F5EDF6",
            justify="center"
        )

        placeholder.place(
            x=30,
            y=50,
            width=190,
            height=190
        )

    # ==========================================
    # SAVE OUTFIT
    # ==========================================
    def save_outfit(self):

        if len(self.current_outfit) != 3:

            messagebox.showwarning(
                "No Outfit",
                "Please generate an outfit first."
            )

            return

        user_id = self.get_user_id()

        if user_id is None:

            messagebox.showerror(
                "User Error",
                "Could not find the logged-in user."
            )

            return

        top_id = self.current_outfit[0][0]
        bottom_id = self.current_outfit[1][0]
        shoes_id = self.current_outfit[2][0]

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO outfits (
                    user_id,
                    top_id,
                    bottom_id,
                    shoes_id
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    top_id,
                    bottom_id,
                    shoes_id
                )
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Gola",
                "Outfit saved successfully! ♡"
            )

        except sqlite3.Error as error:

            messagebox.showerror(
                "Database Error",
                f"Could not save outfit.\n\n{error}"
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