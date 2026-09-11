import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os


class WardrobePage:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.image_refs = []

        # Current selected category
        self.selected_category = "All"

        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF8F8")

        # ==========================================
        # TITLE
        # ==========================================
        title = tk.Label(
            self.root,
            text="My Wardrobe",
            font=("Georgia", 26, "bold"),
            fg="#2F2A67",
            bg="#FFF8F8"
        )
        title.place(x=390, y=25)

        subtitle = tk.Label(
            self.root,
            text="Browse and organize your digital closet",
            font=("Arial", 11),
            fg="#726C85",
            bg="#FFF8F8"
        )
        subtitle.place(x=365, y=70)

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
            y=30,
            width=100,
            height=35
        )

        # ==========================================
        # ADD CLOTHING BUTTON
        # ==========================================
        add_button = tk.Button(
            self.root,
            text="+ Add Clothing",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#A467DF",
            activebackground="#9258CC",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.open_add_clothing
        )
        add_button.place(
            x=815,
            y=30,
            width=140,
            height=35
        )

        # ==========================================
        # CATEGORY FILTER AREA
        # ==========================================
        category_frame = tk.Frame(
            self.root,
            bg="#FFF8F8",
            width=920,
            height=60
        )
        category_frame.place(
            x=40,
            y=100
        )

        categories = [
            "All",
            "Top",
            "Bottom",
            "Dress",
            "Shoes",
            "Outerwear",
            "Accessory"
        ]

        x_position = 0

        for category in categories:
            button = tk.Button(
                category_frame,
                text=category,
                font=("Arial", 9, "bold"),
                fg="#554C52",
                bg="#EDE3F5",
                activebackground="#DCC9EC",
                relief="flat",
                borderwidth=0,
                cursor="hand2",
                command=lambda c=category: self.filter_category(c)
            )

            button.place(
                x=x_position,
                y=10,
                width=115,
                height=35
            )

            x_position += 125

        # ==========================================
        # WARDROBE CONTAINER
        # ==========================================
        container = tk.Frame(
            self.root,
            bg="#FFF8F8"
        )
        container.place(
            x=40,
            y=160,
            width=920,
            height=450
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

        self.prepare_database()
        self.load_clothing()

    # ==========================================
    # PREPARE DATABASE
    # ==========================================
    def prepare_database(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS clothing (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    color TEXT NOT NULL,
                    image_path TEXT,
                    favorite INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id)
                    REFERENCES users(id)
                )
                """
            )

            cursor.execute("PRAGMA table_info(clothing)")
            columns = cursor.fetchall()

            column_names = [
                column[1]
                for column in columns
            ]

            if "favorite" not in column_names:
                cursor.execute(
                    """
                    ALTER TABLE clothing
                    ADD COLUMN favorite INTEGER DEFAULT 0
                    """
                )

            connection.commit()
            connection.close()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not prepare wardrobe.\n\n{error}"
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
    # FILTER CATEGORY
    # ==========================================
    def filter_category(self, category):
        self.selected_category = category
        self.load_clothing()

    # ==========================================
    # LOAD CLOTHING
    # ==========================================
    def load_clothing(self):

        # Clear old cards
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        self.image_refs = []

        user_id = self.get_user_id()

        if user_id is None:
            messagebox.showerror(
                "User Error",
                "The logged-in user could not be found."
            )
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            # ALL CLOTHES
            if self.selected_category == "All":

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        category,
                        color,
                        image_path,
                        favorite
                    FROM clothing
                    WHERE user_id = ?
                    ORDER BY id DESC
                    """,
                    (user_id,)
                )

            # SELECTED CATEGORY
            else:

                cursor.execute(
                    """
                    SELECT
                        id,
                        name,
                        category,
                        color,
                        image_path,
                        favorite
                    FROM clothing
                    WHERE user_id = ?
                    AND category = ?
                    ORDER BY id DESC
                    """,
                    (
                        user_id,
                        self.selected_category
                    )
                )

            clothes = cursor.fetchall()

            connection.close()

            # ======================================
            # EMPTY CATEGORY
            # ======================================
            if len(clothes) == 0:

                if self.selected_category == "All":
                    empty_text = (
                        "Your wardrobe is empty.\n\n"
                        "Add your first clothing item ♡"
                    )
                else:
                    empty_text = (
                        f"No {self.selected_category} items yet.\n\n"
                        f"Add a {self.selected_category} "
                        "to your wardrobe ♡"
                    )

                empty_label = tk.Label(
                    self.cards_frame,
                    text=empty_text,
                    font=("Arial", 14),
                    fg="#817A96",
                    bg="#FFF8F8",
                    justify="center"
                )

                empty_label.grid(
                    row=0,
                    column=0,
                    padx=300,
                    pady=120
                )

                return

            # ======================================
            # CREATE CARDS
            # ======================================
            row = 0
            column = 0

            for item in clothes:

                clothing_id = item[0]
                name = item[1]
                category = item[2]
                color = item[3]
                image_path = item[4]
                favorite = item[5]

                self.create_card(
                    clothing_id,
                    name,
                    category,
                    color,
                    image_path,
                    favorite,
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
                f"Could not load your wardrobe.\n\n{error}"
            )

    # ==========================================
    # CREATE CLOTHING CARD
    # ==========================================
    def create_card(
        self,
        clothing_id,
        name,
        category,
        color,
        image_path,
        favorite,
        row,
        column
    ):

        card = tk.Frame(
            self.cards_frame,
            bg="white",
            width=260,
            height=350,
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

        # ==========================================
        # IMAGE
        # ==========================================
        if image_path and os.path.exists(image_path):

            try:
                image = Image.open(image_path)

                image.thumbnail(
                    (210, 190)
                )

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

        # ==========================================
        # NAME
        # ==========================================
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

        # CATEGORY
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

        # COLOR
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

        # ==========================================
        # FAVORITE BUTTON
        # ==========================================
        if favorite == 1:
            favorite_text = "♥ Favorite"
            favorite_color = "#E656A2"

        else:
            favorite_text = "♡ Favorite"
            favorite_color = "#A467DF"

        favorite_button = tk.Button(
            card,
            text=favorite_text,
            font=("Arial", 9, "bold"),
            fg="white",
            bg=favorite_color,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda:
            self.toggle_favorite(
                clothing_id,
                favorite
            )
        )

        favorite_button.place(
            x=20,
            y=305,
            width=105,
            height=28
        )

        # ==========================================
        # DELETE BUTTON
        # ==========================================
        delete_button = tk.Button(
            card,
            text="Delete",
            font=("Arial", 9, "bold"),
            fg="white",
            bg="#E56B86",
            activebackground="#CF5874",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda:
            self.delete_clothing(
                clothing_id,
                name
            )
        )

        delete_button.place(
            x=170,
            y=305,
            width=65,
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
    # FAVORITE / UNFAVORITE
    # ==========================================
    def toggle_favorite(
        self,
        clothing_id,
        current_favorite
    ):

        if current_favorite == 1:
            new_favorite = 0

        else:
            new_favorite = 1

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE clothing
                SET favorite = ?
                WHERE id = ?
                """,
                (
                    new_favorite,
                    clothing_id
                )
            )

            connection.commit()
            connection.close()

            # Reload same selected category
            self.load_clothing()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not update favorite.\n\n{error}"
            )

    # ==========================================
    # DELETE CLOTHING
    # ==========================================
    def delete_clothing(
        self,
        clothing_id,
        name
    ):

        answer = messagebox.askyesno(
            "Delete Clothing",
            f"Do you want to delete '{name}'?"
        )

        if not answer:
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM clothing
                WHERE id = ?
                """,
                (clothing_id,)
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Gola",
                "Clothing deleted successfully."
            )

            # Reload current category
            self.load_clothing()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not delete clothing.\n\n{error}"
            )

    # ==========================================
    # ADD CLOTHING
    # ==========================================
    def open_add_clothing(self):

        from addclothing import AddClothingPage

        AddClothingPage(
            self.root,
            self.username
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