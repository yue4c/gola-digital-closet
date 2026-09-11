import tkinter as tk
import sqlite3


class DashboardPage:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        # Clear previous page
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#F4DADB")

        # Prepare database tables
        self.prepare_clothing_table()
        self.prepare_outfit_table()
        self.prepare_calendar_table()

        # Get dashboard counts
        total_clothes = self.get_total_clothes()
        total_favorites = self.get_total_favorites()
        total_outfits = self.get_total_outfits()
        total_events = self.get_total_events()

        # ==========================================
        # SIDEBAR
        # ==========================================
        sidebar = tk.Frame(
            self.root,
            bg="white",
            width=205,
            height=630
        )
        sidebar.place(x=5, y=10)

        # LOGO
        logo_label = tk.Label(
            sidebar,
            text="GOLA",
            font=("Georgia", 24, "bold"),
            fg="#8B63D9",
            bg="white"
        )
        logo_label.place(x=55, y=20)

        # USER
        welcome_label = tk.Label(
            sidebar,
            text=f"Hi, {self.username}",
            font=("Arial", 10),
            fg="#756D84",
            bg="white"
        )
        welcome_label.place(x=60, y=58)

        # HOME
        home_button = tk.Button(
            sidebar,
            text="⌂   Home",
            font=("Arial", 11, "bold"),
            anchor="w",
            padx=18,
            fg="#312D65",
            bg="#F0EDFF",
            activebackground="#E8E2FF",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.refresh_dashboard
        )
        home_button.place(x=18, y=100, width=170, height=42)

        # WARDROBE
        wardrobe_button = tk.Button(
            sidebar,
            text="👗   My Wardrobe",
            font=("Arial", 10),
            anchor="w",
            padx=15,
            fg="#312D65",
            bg="white",
            activebackground="#F5F1FF",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.open_wardrobe
        )
        wardrobe_button.place(x=18, y=150, width=170, height=42)

        # ADD CLOTHING
        add_button = tk.Button(
            sidebar,
            text="+   Add Clothing",
            font=("Arial", 10),
            anchor="w",
            padx=18,
            fg="#312D65",
            bg="white",
            activebackground="#F5F1FF",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.open_add_clothing
        )
        add_button.place(x=18, y=200, width=170, height=42)

        # FAVORITES
        favorite_button = tk.Button(
            sidebar,
            text="♡   Favorites",
            font=("Arial", 10),
            anchor="w",
            padx=18,
            fg="#312D65",
            bg="white",
            activebackground="#F5F1FF",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.open_favorites
        )
        favorite_button.place(x=18, y=250, width=170, height=42)

        # OUTFIT GENERATOR
        generator_button = tk.Button(
            sidebar,
            text="✦   Outfit Generator",
            font=("Arial", 10),
            anchor="w",
            padx=18,
            fg="#312D65",
            bg="white",
            activebackground="#F5F1FF",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.open_generator
        )
        generator_button.place(x=18, y=300, width=170, height=42)

        # CALENDAR
        calendar_button = tk.Button(
            sidebar,
            text="▣   Calendar",
            font=("Arial", 10),
            anchor="w",
            padx=18,
            fg="#312D65",
            bg="white",
            activebackground="#F5F1FF",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.open_calendar
        )
        calendar_button.place(x=18, y=350, width=170, height=42)

        # SETTINGS
        settings_button = tk.Button(
            sidebar,
            text="⚙   Settings",
            font=("Arial", 10),
            anchor="w",
            padx=18,
            fg="#312D65",
            bg="white",
            activebackground="#F5F1FF",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.open_settings
        )
        settings_button.place(x=18, y=400, width=170, height=42)

        # LOGOUT
        logout_button = tk.Button(
            sidebar,
            text="Logout",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#A96FD5",
            activebackground="#935FC0",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.logout
        )
        logout_button.place(x=45, y=550, width=115, height=38)

        # ==========================================
        # MAIN AREA
        # ==========================================
        main_area = tk.Frame(
            self.root,
            bg="#FFF8F8",
            width=775,
            height=610
        )
        main_area.place(x=215, y=20)

        heading = tk.Label(
            main_area,
            text="Wardrobe Overview",
            font=("Georgia", 25, "bold"),
            fg="#2F2A67",
            bg="#FFF8F8"
        )
        heading.place(x=50, y=50)

        subtitle = tk.Label(
            main_area,
            text="Here is a quick look at your digital closet.",
            font=("Arial", 11),
            fg="#726C85",
            bg="#FFF8F8"
        )
        subtitle.place(x=52, y=95)

        # ==========================================
        # TOTAL CLOTHES
        # ==========================================
        clothes_card = tk.Frame(
            main_area,
            bg="white",
            width=285,
            height=135,
            highlightbackground="#EFE8F3",
            highlightthickness=1
        )
        clothes_card.place(x=45, y=155)

        clothes_icon = tk.Label(
            clothes_card,
            text="👗",
            font=("Arial", 32),
            bg="#EEE9FF"
        )
        clothes_icon.place(x=20, y=35, width=70, height=70)

        total_clothes_label = tk.Label(
            clothes_card,
            text=str(total_clothes),
            font=("Arial", 30, "bold"),
            fg="#6E63F4",
            bg="white"
        )
        total_clothes_label.place(x=125, y=22)

        clothes_text = tk.Label(
            clothes_card,
            text="Total Clothes",
            font=("Arial", 13),
            fg="#39356F",
            bg="white"
        )
        clothes_text.place(x=125, y=78)

        # ==========================================
        # FAVORITES
        # ==========================================
        favorites_card = tk.Frame(
            main_area,
            bg="white",
            width=285,
            height=135,
            highlightbackground="#EFE8F3",
            highlightthickness=1
        )
        favorites_card.place(x=365, y=155)

        favorite_icon = tk.Label(
            favorites_card,
            text="♡",
            font=("Arial", 38),
            fg="#ED5CA9",
            bg="#FFEAF4"
        )
        favorite_icon.place(x=20, y=35, width=70, height=70)

        favorites_label = tk.Label(
            favorites_card,
            text=str(total_favorites),
            font=("Arial", 30, "bold"),
            fg="#E656A2",
            bg="white"
        )
        favorites_label.place(x=125, y=22)

        favorite_text = tk.Label(
            favorites_card,
            text="Favorites",
            font=("Arial", 13),
            fg="#39356F",
            bg="white"
        )
        favorite_text.place(x=125, y=78)

        # ==========================================
        # OUTFITS CREATED
        # ==========================================
        outfits_card = tk.Frame(
            main_area,
            bg="white",
            width=285,
            height=135,
            highlightbackground="#EFE8F3",
            highlightthickness=1
        )
        outfits_card.place(x=45, y=325)

        outfit_icon = tk.Label(
            outfits_card,
            text="✨",
            font=("Arial", 28),
            bg="#FFF0DF"
        )
        outfit_icon.place(x=20, y=35, width=70, height=70)

        outfits_label = tk.Label(
            outfits_card,
            text=str(total_outfits),
            font=("Arial", 30, "bold"),
            fg="#FF8A49",
            bg="white"
        )
        outfits_label.place(x=125, y=22)

        outfit_text = tk.Label(
            outfits_card,
            text="Outfits Created",
            font=("Arial", 13),
            fg="#39356F",
            bg="white"
        )
        outfit_text.place(x=125, y=78)

        # ==========================================
        # CALENDAR EVENTS
        # ==========================================
        calendar_card = tk.Frame(
            main_area,
            bg="white",
            width=285,
            height=135,
            highlightbackground="#EFE8F3",
            highlightthickness=1
        )
        calendar_card.place(x=365, y=325)

        calendar_icon = tk.Label(
            calendar_card,
            text="📅",
            font=("Arial", 28),
            bg="#E8FAF3"
        )
        calendar_icon.place(x=20, y=35, width=70, height=70)

        calendar_label = tk.Label(
            calendar_card,
            text=str(total_events),
            font=("Arial", 30, "bold"),
            fg="#38B89B",
            bg="white"
        )
        calendar_label.place(x=125, y=22)

        calendar_text = tk.Label(
            calendar_card,
            text="Calendar Events",
            font=("Arial", 13),
            fg="#39356F",
            bg="white"
        )
        calendar_text.place(x=125, y=78)

        bottom_message = tk.Label(
            main_area,
            text="Build your closet, create outfits, and plan what to wear ♡",
            font=("Arial", 11),
            fg="#817A96",
            bg="#FFF8F8"
        )
        bottom_message.place(x=160, y=510)

    # ==========================================
    # DATABASE TABLES
    # ==========================================
    def prepare_clothing_table(self):
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
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

            cursor.execute("PRAGMA table_info(clothing)")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]

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
            print("Clothing table error:", error)

    def prepare_outfit_table(self):
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
            print("Outfit table error:", error)

    def prepare_calendar_table(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS calendar_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    event_date TEXT NOT NULL,
                    outfit_id INTEGER NOT NULL,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (outfit_id) REFERENCES outfits(id)
                )
                """
            )

            connection.commit()
            connection.close()

        except sqlite3.Error as error:
            print("Calendar table error:", error)

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
    # DASHBOARD COUNTS
    # ==========================================
    def get_total_clothes(self):
        user_id = self.get_user_id()

        if user_id is None:
            return 0

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM clothing
                WHERE user_id = ?
                """,
                (user_id,)
            )

            total = cursor.fetchone()[0]
            connection.close()

            return total

        except sqlite3.Error:
            return 0

    def get_total_favorites(self):
        user_id = self.get_user_id()

        if user_id is None:
            return 0

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM clothing
                WHERE user_id = ?
                AND favorite = 1
                """,
                (user_id,)
            )

            total = cursor.fetchone()[0]
            connection.close()

            return total

        except sqlite3.Error:
            return 0

    def get_total_outfits(self):
        user_id = self.get_user_id()

        if user_id is None:
            return 0

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM outfits
                WHERE user_id = ?
                """,
                (user_id,)
            )

            total = cursor.fetchone()[0]
            connection.close()

            return total

        except sqlite3.Error:
            return 0

    def get_total_events(self):
        user_id = self.get_user_id()

        if user_id is None:
            return 0

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM calendar_events
                WHERE user_id = ?
                """,
                (user_id,)
            )

            total = cursor.fetchone()[0]
            connection.close()

            return total

        except sqlite3.Error:
            return 0

    # ==========================================
    # NAVIGATION
    # ==========================================
    def refresh_dashboard(self):
        DashboardPage(
            self.root,
            self.username
        )

    def open_wardrobe(self):
        from wardrobe import WardrobePage

        WardrobePage(
            self.root,
            self.username
        )

    def open_add_clothing(self):
        from addclothing import AddClothingPage

        AddClothingPage(
            self.root,
            self.username
        )

    def open_favorites(self):
        from favorites import FavoritesPage

        FavoritesPage(
            self.root,
            self.username
        )

    def open_generator(self):
        from outfitgenerator import OutfitGeneratorPage

        OutfitGeneratorPage(
            self.root,
            self.username
        )

    def open_calendar(self):
        from calenderpage import CalendarPage

        CalendarPage(
            self.root,
            self.username
        )

    def open_settings(self):
        from settingspage import SettingsPage

        SettingsPage(
            self.root,
            self.username
        )

    def logout(self):
        from login import LoginPage

        LoginPage(self.root)