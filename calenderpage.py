import tkinter as tk
from tkinter import messagebox
import sqlite3


class CalendarPage:
    def __init__(self, root, username):
        self.root = root
        self.username = username

        self.outfit_map = {}

        # Clear previous page
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#FFF8F8")

        self.prepare_database()
        self.build_ui()
        self.load_outfits()
        self.load_events()

    # =========================================================
    # DATABASE PREPARATION
    # =========================================================
    def prepare_database(self):
        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            # -------------------------------------------------
            # Make sure outfits table exists
            # -------------------------------------------------
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS outfits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    top_id INTEGER,
                    bottom_id INTEGER,
                    shoes_id INTEGER,
                    dress_id INTEGER,
                    outerwear_id INTEGER,
                    accessory_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """
            )

            # -------------------------------------------------
            # Add missing new outfit columns
            # -------------------------------------------------
            cursor.execute("PRAGMA table_info(outfits)")
            columns = cursor.fetchall()

            column_names = [
                column[1]
                for column in columns
            ]

            if "dress_id" not in column_names:
                cursor.execute(
                    """
                    ALTER TABLE outfits
                    ADD COLUMN dress_id INTEGER
                    """
                )

            if "outerwear_id" not in column_names:
                cursor.execute(
                    """
                    ALTER TABLE outfits
                    ADD COLUMN outerwear_id INTEGER
                    """
                )

            if "accessory_id" not in column_names:
                cursor.execute(
                    """
                    ALTER TABLE outfits
                    ADD COLUMN accessory_id INTEGER
                    """
                )

            # -------------------------------------------------
            # Calendar events table
            # -------------------------------------------------
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
            messagebox.showerror(
                "Database Error",
                f"Could not prepare calendar.\n\n{error}"
            )

    # =========================================================
    # GET USER ID
    # =========================================================
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

    # =========================================================
    # UI
    # =========================================================
    def build_ui(self):

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------
        title = tk.Label(
            self.root,
            text="Outfit Calendar",
            font=("Georgia", 27, "bold"),
            fg="#30286F",
            bg="#FFF8F8"
        )
        title.place(
            x=385,
            y=25
        )

        subtitle = tk.Label(
            self.root,
            text="Plan what you want to wear for upcoming days and events",
            font=("Arial", 10),
            fg="#726C85",
            bg="#FFF8F8"
        )
        subtitle.place(
            x=325,
            y=68
        )

        # -----------------------------------------------------
        # BACK
        # -----------------------------------------------------
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

        # =====================================================
        # LEFT FORM CARD
        # =====================================================
        form_frame = tk.Frame(
            self.root,
            bg="white",
            width=410,
            height=455,
            highlightbackground="#E8DDEA",
            highlightthickness=1
        )
        form_frame.place(
            x=50,
            y=120
        )

        form_title = tk.Label(
            form_frame,
            text="Plan an Outfit",
            font=("Arial", 17, "bold"),
            fg="#39356F",
            bg="white"
        )
        form_title.place(
            x=25,
            y=20
        )

        # -----------------------------------------------------
        # DATE
        # -----------------------------------------------------
        date_label = tk.Label(
            form_frame,
            text="Date",
            font=("Arial", 10, "bold"),
            fg="#554C52",
            bg="white"
        )
        date_label.place(
            x=25,
            y=70
        )

        self.date_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            relief="solid",
            borderwidth=1
        )
        self.date_entry.place(
            x=25,
            y=95,
            width=355,
            height=38
        )

        date_hint = tk.Label(
            form_frame,
            text="Example: 2026-09-15",
            font=("Arial", 8),
            fg="#91879B",
            bg="white"
        )
        date_hint.place(
            x=25,
            y=136
        )

        # -----------------------------------------------------
        # OUTFIT
        # -----------------------------------------------------
        outfit_label = tk.Label(
            form_frame,
            text="Select Saved Outfit",
            font=("Arial", 10, "bold"),
            fg="#554C52",
            bg="white"
        )
        outfit_label.place(
            x=25,
            y=165
        )

        self.outfit_var = tk.StringVar()

        self.outfit_menu = tk.OptionMenu(
            form_frame,
            self.outfit_var,
            ""
        )

        self.outfit_menu.config(
            font=("Arial", 9),
            bg="#F7F1FA",
            fg="#39356F",
            activebackground="#E9DDF5",
            relief="flat",
            anchor="w"
        )

        self.outfit_menu["menu"].config(
            font=("Arial", 9)
        )

        self.outfit_menu.place(
            x=25,
            y=190,
            width=355,
            height=40
        )

        # -----------------------------------------------------
        # NOTES
        # -----------------------------------------------------
        notes_label = tk.Label(
            form_frame,
            text="Notes",
            font=("Arial", 10, "bold"),
            fg="#554C52",
            bg="white"
        )
        notes_label.place(
            x=25,
            y=255
        )

        self.notes_text = tk.Text(
            form_frame,
            font=("Arial", 10),
            relief="solid",
            borderwidth=1,
            wrap="word"
        )
        self.notes_text.place(
            x=25,
            y=280,
            width=355,
            height=85
        )

        # -----------------------------------------------------
        # SAVE
        # -----------------------------------------------------
        save_button = tk.Button(
            form_frame,
            text="Save to Calendar",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#A467DF",
            activebackground="#9258CC",
            activeforeground="white",
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            command=self.save_event
        )
        save_button.place(
            x=100,
            y=390,
            width=210,
            height=42
        )

        # =====================================================
        # RIGHT EVENTS CARD
        # =====================================================
        events_frame = tk.Frame(
            self.root,
            bg="white",
            width=470,
            height=455,
            highlightbackground="#E8DDEA",
            highlightthickness=1
        )
        events_frame.place(
            x=490,
            y=120
        )

        events_title = tk.Label(
            events_frame,
            text="Planned Outfits",
            font=("Arial", 17, "bold"),
            fg="#39356F",
            bg="white"
        )
        events_title.place(
            x=25,
            y=20
        )

        # Scrollable area
        container = tk.Frame(
            events_frame,
            bg="white"
        )
        container.place(
            x=20,
            y=65,
            width=430,
            height=365
        )

        self.canvas = tk.Canvas(
            container,
            bg="white",
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.events_container = tk.Frame(
            self.canvas,
            bg="white"
        )

        self.events_container.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.events_container,
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

    # =========================================================
    # LOAD SAVED OUTFITS
    # =========================================================
    def load_outfits(self):
        user_id = self.get_user_id()

        if user_id is None:
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    outfits.id,

                    top_item.name,
                    bottom_item.name,
                    shoes_item.name,

                    dress_item.name,
                    outerwear_item.name,
                    accessory_item.name

                FROM outfits

                LEFT JOIN clothing AS top_item
                    ON outfits.top_id = top_item.id

                LEFT JOIN clothing AS bottom_item
                    ON outfits.bottom_id = bottom_item.id

                LEFT JOIN clothing AS shoes_item
                    ON outfits.shoes_id = shoes_item.id

                LEFT JOIN clothing AS dress_item
                    ON outfits.dress_id = dress_item.id

                LEFT JOIN clothing AS outerwear_item
                    ON outfits.outerwear_id = outerwear_item.id

                LEFT JOIN clothing AS accessory_item
                    ON outfits.accessory_id = accessory_item.id

                WHERE outfits.user_id = ?

                ORDER BY outfits.id DESC
                """,
                (user_id,)
            )

            outfits = cursor.fetchall()

            connection.close()

            # Clear dropdown
            menu = self.outfit_menu["menu"]
            menu.delete(0, "end")

            self.outfit_map = {}

            if not outfits:
                self.outfit_var.set(
                    "No saved outfits"
                )
                return

            for outfit in outfits:

                outfit_id = outfit[0]

                top = outfit[1]
                bottom = outfit[2]
                shoes = outfit[3]

                dress = outfit[4]
                outerwear = outfit[5]
                accessory = outfit[6]

                clothing_names = []

                if dress:
                    clothing_names.append(dress)

                else:
                    if top:
                        clothing_names.append(top)

                    if bottom:
                        clothing_names.append(bottom)

                if shoes:
                    clothing_names.append(shoes)

                if outerwear:
                    clothing_names.append(outerwear)

                if accessory:
                    clothing_names.append(accessory)

                outfit_description = " + ".join(
                    clothing_names
                )

                label = (
                    f"Outfit {outfit_id}: "
                    f"{outfit_description}"
                )

                self.outfit_map[label] = outfit_id

                menu.add_command(
                    label=label,
                    command=lambda value=label:
                    self.outfit_var.set(value)
                )

            first_label = list(
                self.outfit_map.keys()
            )[0]

            self.outfit_var.set(
                first_label
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load saved outfits.\n\n{error}"
            )

    # =========================================================
    # SAVE EVENT
    # =========================================================
    def save_event(self):
        event_date = self.date_entry.get().strip()
        selected_outfit = self.outfit_var.get()
        notes = self.notes_text.get(
            "1.0",
            tk.END
        ).strip()

        # -----------------------------------------------------
        # VALIDATE DATE
        # -----------------------------------------------------
        if event_date == "":
            messagebox.showwarning(
                "Missing Date",
                "Please enter a date."
            )
            return

        # Simple YYYY-MM-DD check
        parts = event_date.split("-")

        if len(parts) != 3:
            messagebox.showwarning(
                "Invalid Date",
                "Please use the date format YYYY-MM-DD."
            )
            return

        if (
            len(parts[0]) != 4
            or len(parts[1]) != 2
            or len(parts[2]) != 2
        ):
            messagebox.showwarning(
                "Invalid Date",
                "Please use the date format YYYY-MM-DD."
            )
            return

        if not all(
            part.isdigit()
            for part in parts
        ):
            messagebox.showwarning(
                "Invalid Date",
                "Please use numbers in the date."
            )
            return

        # -----------------------------------------------------
        # VALIDATE OUTFIT
        # -----------------------------------------------------
        if (
            selected_outfit == ""
            or selected_outfit == "No saved outfits"
        ):
            messagebox.showwarning(
                "No Outfit",
                "Please save an outfit in Outfit Generator first."
            )
            return

        outfit_id = self.outfit_map.get(
            selected_outfit
        )

        if outfit_id is None:
            messagebox.showwarning(
                "Invalid Outfit",
                "Please select a saved outfit."
            )
            return

        user_id = self.get_user_id()

        if user_id is None:
            messagebox.showerror(
                "User Error",
                "Could not find your account."
            )
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO calendar_events (
                    user_id,
                    event_date,
                    outfit_id,
                    notes
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    event_date,
                    outfit_id,
                    notes
                )
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Gola",
                "Outfit added to your calendar! ♡"
            )

            self.date_entry.delete(
                0,
                tk.END
            )

            self.notes_text.delete(
                "1.0",
                tk.END
            )

            self.load_events()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not save calendar event.\n\n{error}"
            )

    # =========================================================
    # LOAD EVENTS
    # =========================================================
    def load_events(self):

        # Clear current event cards
        for widget in self.events_container.winfo_children():
            widget.destroy()

        user_id = self.get_user_id()

        if user_id is None:
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    calendar_events.id,
                    calendar_events.event_date,
                    calendar_events.notes,
                    calendar_events.outfit_id,

                    top_item.name,
                    bottom_item.name,
                    shoes_item.name,

                    dress_item.name,
                    outerwear_item.name,
                    accessory_item.name

                FROM calendar_events

                JOIN outfits
                    ON calendar_events.outfit_id = outfits.id

                LEFT JOIN clothing AS top_item
                    ON outfits.top_id = top_item.id

                LEFT JOIN clothing AS bottom_item
                    ON outfits.bottom_id = bottom_item.id

                LEFT JOIN clothing AS shoes_item
                    ON outfits.shoes_id = shoes_item.id

                LEFT JOIN clothing AS dress_item
                    ON outfits.dress_id = dress_item.id

                LEFT JOIN clothing AS outerwear_item
                    ON outfits.outerwear_id = outerwear_item.id

                LEFT JOIN clothing AS accessory_item
                    ON outfits.accessory_id = accessory_item.id

                WHERE calendar_events.user_id = ?

                ORDER BY calendar_events.event_date ASC
                """,
                (user_id,)
            )

            events = cursor.fetchall()

            connection.close()

            # -------------------------------------------------
            # NO EVENTS
            # -------------------------------------------------
            if not events:

                empty_label = tk.Label(
                    self.events_container,
                    text=(
                        "No planned outfits yet.\n\n"
                        "Save an outfit to your calendar ♡"
                    ),
                    font=("Arial", 11),
                    fg="#91879B",
                    bg="white",
                    justify="center"
                )

                empty_label.pack(
                    padx=80,
                    pady=100
                )

                return

            # -------------------------------------------------
            # CREATE EVENT CARDS
            # -------------------------------------------------
            for event in events:

                event_id = event[0]
                event_date = event[1]
                notes = event[2]
                outfit_id = event[3]

                top = event[4]
                bottom = event[5]
                shoes = event[6]

                dress = event[7]
                outerwear = event[8]
                accessory = event[9]

                self.create_event_card(
                    event_id,
                    event_date,
                    outfit_id,
                    notes,
                    top,
                    bottom,
                    shoes,
                    dress,
                    outerwear,
                    accessory
                )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not load calendar events.\n\n{error}"
            )

    # =========================================================
    # CREATE EVENT CARD
    # =========================================================
    def create_event_card(
        self,
        event_id,
        event_date,
        outfit_id,
        notes,
        top,
        bottom,
        shoes,
        dress,
        outerwear,
        accessory
    ):

        card = tk.Frame(
            self.events_container,
            bg="#FAF6F8",
            width=395,
            height=190,
            highlightbackground="#EEE3EA",
            highlightthickness=1
        )

        card.pack(
            padx=5,
            pady=8
        )

        card.pack_propagate(False)

        # -----------------------------------------------------
        # DATE
        # -----------------------------------------------------
        date_label = tk.Label(
            card,
            text=f"📅  {event_date}",
            font=("Arial", 11, "bold"),
            fg="#342C72",
            bg="#FAF6F8"
        )
        date_label.place(
            x=15,
            y=12
        )

        outfit_number = tk.Label(
            card,
            text=f"Outfit #{outfit_id}",
            font=("Arial", 9),
            fg="#A467DF",
            bg="#FAF6F8"
        )
        outfit_number.place(
            x=300,
            y=15
        )

        # -----------------------------------------------------
        # OUTFIT DETAILS
        # -----------------------------------------------------
        details = []

        if dress:
            details.append(
                f"👗 Dress: {dress}"
            )

        else:
            if top:
                details.append(
                    f"👕 Top: {top}"
                )

            if bottom:
                details.append(
                    f"👖 Bottom: {bottom}"
                )

        if shoes:
            details.append(
                f"👟 Shoes: {shoes}"
            )

        if outerwear:
            details.append(
                f"🧥 Outerwear: {outerwear}"
            )

        if accessory:
            details.append(
                f"👜 Accessory: {accessory}"
            )

        details_text = "\n".join(
            details
        )

        details_label = tk.Label(
            card,
            text=details_text,
            font=("Arial", 9),
            fg="#554C52",
            bg="#FAF6F8",
            justify="left",
            anchor="nw"
        )

        details_label.place(
            x=18,
            y=48,
            width=230,
            height=100
        )

        # -----------------------------------------------------
        # NOTES
        # -----------------------------------------------------
        notes_title = tk.Label(
            card,
            text="Notes",
            font=("Arial", 9, "bold"),
            fg="#39356F",
            bg="#FAF6F8"
        )

        notes_title.place(
            x=260,
            y=50
        )

        if notes:
            notes_display = notes
        else:
            notes_display = "No notes"

        notes_label = tk.Label(
            card,
            text=notes_display,
            font=("Arial", 8),
            fg="#817A96",
            bg="#FAF6F8",
            justify="left",
            anchor="nw",
            wraplength=105
        )

        notes_label.place(
            x=260,
            y=75,
            width=110,
            height=55
        )

        # -----------------------------------------------------
        # DELETE EVENT
        # -----------------------------------------------------
        delete_button = tk.Button(
            card,
            text="Delete",
            font=("Arial", 8, "bold"),
            fg="white",
            bg="#E56B86",
            activebackground="#CF5874",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda:
            self.delete_event(
                event_id
            )
        )

        delete_button.place(
            x=285,
            y=145,
            width=80,
            height=28
        )

    # =========================================================
    # DELETE EVENT
    # =========================================================
    def delete_event(self, event_id):

        answer = messagebox.askyesno(
            "Delete Calendar Event",
            "Do you want to remove this planned outfit?"
        )

        if not answer:
            return

        try:
            connection = sqlite3.connect("gola.db")
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM calendar_events
                WHERE id = ?
                """,
                (event_id,)
            )

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Gola",
                "Calendar event deleted."
            )

            self.load_events()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not delete calendar event.\n\n{error}"
            )

    # =========================================================
    # BACK
    # =========================================================
    def go_back(self):

        from dashboard import DashboardPage

        DashboardPage(
            self.root,
            self.username
        )