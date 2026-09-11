import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os


class FavoritesPage:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.image_refs = []

        # Clear previous screen
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF8F8")

        # ==========================================
        # TITLE
        # ==========================================
        title = tk.Label(
            self.root,
            text="My Favorites",
            font=("Georgia", 26, "bold"),
            fg="#2F2A67",
            bg="#FFF8F8"
        )
        title.place(
            x=395,
            y=30
        )

        subtitle = tk.Label(
            self.root,
            text="Your favorite clothing items",
            font=("Arial", 11),
            fg="#726C85",
            bg="#FFF8F8"
        )
        subtitle.place(
            x=400,
            y=75
        )

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
        # SCROLLABLE AREA
        # ==========================================
        container = tk.Frame(
            self.root,
            bg="#FFF8F8"
        )
        container.place(
            x=40,
            y=120,
            width=920,
            height=490
        )

        self.canvas = tk.Canvas(
            container,
            bg="#FFF8F8",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.cards_frame = tk.Frame(
            self.canvas,
            bg="#FFF8F8"
        )

        self.cards_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.cards_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.load_favorites()

    # ==========================================
    # LOAD FAVORITES
    # ==========================================
    def load_favorites(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            # Get current user
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
                return

            user_id = user[0]

            # Get only favorite clothes
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
                AND favorite = 1
                ORDER BY id DESC
                """,
                (user_id,)
            )

            favorites = cursor.fetchall()

            connection.close()

            # ======================================
            # NO FAVORITES
            # ======================================
            if len(favorites) == 0:
                empty_label = tk.Label(
                    self.cards_frame,
                    text="No favorite clothes yet ♡\n\nGo to My Wardrobe and mark your favorite items.",
                    font=("Arial", 14),
                    fg="#817A96",
                    bg="#FFF8F8",
                    justify="center"
                )
                empty_label.grid(
                    row=0,
                    column=0,
                    padx=260,
                    pady=140
                )

                return

            # ======================================
            # DISPLAY CARDS
            # ======================================
            row = 0
            column = 0

            for item in favorites:
                clothing_id = item[0]
                name = item[1]
                category = item[2]
                color = item[3]
                image_path = item[4]

                self.create_card(
                    clothing_id,
                    name,
                    category,
                    color,
                    image_path,
                    row,
                    column
                )

                column += 1

                if column == 3:
                    column = 0
                    row += 1

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load favorites.\n\n{error}"
            )

    # ==========================================
    # CREATE FAVORITE CARD
    # ==========================================
    def create_card(
        self,
        clothing_id,
        name,
        category,
        color,
        image_path,
        row,
        column
    ):
        card = tk.Frame(
            self.cards_frame,
            bg="white",
            width=260,
            height=340,
            highlightbackground="#E8DDEA",
            highlightthickness=1
        )

        card.grid(
            row=row,
            column=column,
            padx=18,
            pady=15
        )

        card.grid_propagate(False)

        # ======================================
        # IMAGE
        # ======================================
        if image_path and os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                image.thumbnail((210, 190))

                photo = ImageTk.PhotoImage(image)

                self.image_refs.append(photo)

                image_label = tk.Label(
                    card,
                    image=photo,
                    bg="#F8F3F8"
                )
                image_label.place(
                    x=25,
                    y=15,
                    width=210,
                    height=190
                )

            except Exception:
                self.create_placeholder(card)

        else:
            self.create_placeholder(card)

        # ======================================
        # NAME
        # ======================================
        name_label = tk.Label(
            card,
            text=name,
            font=("Arial", 13, "bold"),
            fg="#39356F",
            bg="white"
        )
        name_label.place(
            x=20,
            y=215
        )

        # ======================================
        # CATEGORY
        # ======================================
        category_label = tk.Label(
            card,
            text=f"Category: {category}",
            font=("Arial", 9),
            fg="#756D84",
            bg="white"
        )
        category_label.place(
            x=20,
            y=245
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
            y=268
        )

        # ======================================
        # REMOVE FAVORITE BUTTON
        # ======================================
        remove_button = tk.Button(
            card,
            text="♥ Remove",
            font=("Arial", 9, "bold"),
            fg="white",
            bg="#E656A2",
            activebackground="#D84A94",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda: self.remove_favorite(
                clothing_id
            )
        )

        remove_button.place(
            x=70,
            y=300,
            width=120,
            height=28
        )

    # ==========================================
    # PLACEHOLDER IMAGE
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
            x=25,
            y=15,
            width=210,
            height=190
        )

    # ==========================================
    # REMOVE FROM FAVORITES
    # ==========================================
    def remove_favorite(self, clothing_id):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE clothing
                SET favorite = 0
                WHERE id = ?
                """,
                (clothing_id,)
            )

            connection.commit()
            connection.close()

            FavoritesPage(
                self.root,
                self.username
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not remove favorite.\n\n{error}"
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